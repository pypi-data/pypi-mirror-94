"""Epm table module."""

from .record import Record
from .queryset import Queryset
from ..exceptions import FieldValidationError, RecordDoesNotExistError


# TODO [GL] [ZB] see how we deal with this dynamically generated docstring for our documentation... We could make a
#  dummy add function (only for documentation) and monkey-patch the new one.
def _get_documented_add(self, record_descriptors):
    # This hack is used to document add function.
    # a methods __doc__ attribute is read-only (or must use metaclasses, what I certainly don't want to do...)
    # we therefore create a function (who's __doc__ attribute is read/write), and will bind it to Table in __init__
    def add(data=None, **or_data):
        """
        Add a record to this table.

        A lowercase name is the lowercase EnergyPlus name, for which all non alpha-numeric characters have been replaced
        by underscores. All multiple consecutive underscores are then replaced by one unique underscore.

        The two syntaxes are not meant to cohabit. The kwargs syntax is nicer, but does not enable to use indexes
        instead of names.

        Parameters
        ----------
        data: dictionary containing field lowercase names or index as keys, and field values as values (dict syntax)
        or_data: keyword arguments containing field names as keys (kwargs syntax)

        Examples
        --------
        for Schedule:Compact table:

        schedule = table.add(  # kwarg syntax
            name="Heating Setpoint Schedule - new[1]",
            schedule_type_limits_name="Any Number",
            field_1="Through: 12/31",
            field_2="For: AllDays",
            field_3="Until: 24:00,20.0"
        )

        schedule = table.add({  # dict syntax, mixing names and index keys
            name="Heating Setpoint Schedule - new[1]",
            schedule_type_limits_name="Any Number",
            2="Through: 12/31",
            3="For: AllDays",
            4="Until: 24:00,20.0"
        })

        Returns
        -------
        Created Record instance
        """
        return self.batch_add([or_data if data is None else data]).one()

    add.__doc__ = "\n".join([fd.ref.lower() for fd in record_descriptors if fd.ref is not None])

    return add


class Table:
    """
    Table class, each table contains a specific kind of EnergyPlus object.

    Parameters
    ----------
    table_descriptor: opyplus.idd.table_descriptor.TableDescriptor
    epm: opyplus.Epm
    """

    def __init__(self, table_descriptor, epm):
        self._dev_descriptor = table_descriptor
        self._epm = epm
        self._records = dict()

        # no pk if first field is not a required reference
        self._dev_no_pk = not (
                (table_descriptor.field_descriptors[0].detailed_type == "reference") and
                ("required-field" in table_descriptor.field_descriptors[0].tags)
        )

        # monkey-patch add
        self.add = _get_documented_add(self, self._dev_descriptor.field_descriptors)

        # register table hooks
        table_hooks_references = self._dev_descriptor.field_descriptors[0].tags.get("reference-class-name")
        if table_hooks_references is not None:
            self._epm._dev_relations_manager.register_table_hook(table_hooks_references, self)

    def _dev_record_id_was_updated(self, old_id):
        # remove old id
        record = self._records.pop(old_id)

        # check uniqueness
        new_id = record.id
        if new_id in self._records:
            field_descriptor = record.get_field_descriptor(0)
            raise FieldValidationError(
                f"Primary key already exists, can't create. {field_descriptor.get_error_location_message(new_id)}")

        # store with new id
        self._records[new_id] = record

    def _dev_add_inert(self, records_data):
        # Inert: hooks and links are not activated.
        added_records = []
        for r_data in records_data:
            # create record
            record = Record(
                self,
                data=r_data
            )

            # store
            # we don't check uniqueness here => will be done while checking hooks
            self._records[record.id] = record

            # remember record
            added_records.append(record)

        return added_records

    def _dev_remove_record_without_unregistering(self, record):
        del self._records[record.id]

    # --------------------------------------------- public api ---------------------------------------------------------
    def __repr__(self):
        """
        Repr of table, including its name.

        Returns
        -------
        str
        """
        return f"<Table {self.get_name()}>"

    def __str__(self):
        """
        Get str, including list of records.

        Returns
        -------
        str
        """
        header = f"Table {self.get_name()} ({self.get_ref()})"
        if self._dev_no_pk:
            return header.strip()
        return (header + "\n" + "\n".join(f"  {record.id}" for record in sorted(self._records.values()))).strip()

    def __getitem__(self, item):
        """
        Get record by index.

        Parameters
        ----------
        item: int or slice
            record(s) position(s) (records are ordered by their content, not by creation order)

        Returns
        -------
        Record or typing.List[Record]
        """
        return self.select()[item]

    def __iter__(self):
        """
        Iterate through table records.

        Returns
        -------
        typing.Iterator[Record]
        """
        # !! we create a list before transforming to an iterator. If we don't do this, user may modify self._record key
        # (by changing the pk field key if any), which will not raise an error (surprisingly, it only raises if dict
        # changes size), but will continue iteration in values of new key (although already itered) !!
        return iter(tuple(self._records.values()))

    def __len__(self):
        """
        Get number of records in the Table.

        Returns
        -------
        int
        """
        return len(self._records)

    # get context
    def get_ref(self):
        """
        Get table ref.

        The table ref is the converted name, in order to be compatible with Python variable rules (so we can access
        table from Epm using __getattr__).
        Conversion rule: all non alphanumeric characters are transformed to underscores.
        Example: 'Schedule_Compact'

        Returns
        -------
        str
        """
        return self._dev_descriptor.table_ref

    def get_name(self):
        """
        Get table name.

        The table name is the name given by EnergyPlus.
        Example: 'Schedule:Compact'
        """
        return self._dev_descriptor.table_name

    def get_epm(self):
        """
        Get epm to which this table belongs.

        Returns
        -------
        opyplus.Epm
        """
        return self._epm

    # explore
    def select(self, filter_by=None):
        """
        Select records from Table by applying a filter.

        Parameters
        ----------
        filter_by: typing.Callable or None
            Callable must take one argument (a record of table), and return True to keep record, or False to skip it.
            Example : .select(lambda x: x.name == "my_name").
            If None (default), records are not filtered.

        Returns
        -------
        Queryset
        """
        records = self._records.values() if filter_by is None else filter(filter_by, self._records.values())
        return Queryset(self, records=records)

    def one(self, filter_by=None):
        """
        Get a single record from the Table by applying a filter. If we get more than one record, raise.

        Parameters
        ----------
        filter_by: typing.Callable or str
            if str: record id
            if callable: a callable must take one argument (a record of table), and return True to keep record,
            or False to skip it. Example : .one(lambda x: x.name == "my_name").
            if None (default): records are not filtered.

        Returns
        -------
        Record

        Raises
        ------
        TypeError
            if id search on a table that does not have a pk
        RecordDoesNotExistError
            if no record is found
        MultipleRecordsReturnedError
            if multiple records are found
        """
        if isinstance(filter_by, str):
            if self._dev_no_pk:
                raise TypeError(f"table {self.get_ref()} does not have a primary key, can't use string syntax")
            try:
                return self._records[filter_by]
            except KeyError:
                raise RecordDoesNotExistError(
                    f"table {self.get_ref()} does not contain a record who's id is '{filter_by}'")
        return Queryset(self, records=self._records.values()).one(filter_by=filter_by)

    # construct
    # def add(self, data=None, **or_data):
    #     return self.batch_add([or_data if data is None else data])[0]
    # monkey-patched

    def batch_add(self, records_data):
        """
        Add records as batch.

        Parameters
        ----------
        records_data: typing.List[typing.Dict[typing.Union[str, int], dict]]
            list of dictionaries containing records data. Keys of dictionary may be field names and/or field
            indexes

        Returns
        -------
        Queryset
            added records
        """
        # workflow
        # --------
        # (methods belonging to create/update/delete framework:
        #     epm._dev_populate_from_json_data, table.batch_add, record.update, queryset.delete, record.delete)
        # 1. add inert
        #     * data is checked
        #     * old links are unregistered
        #     * record is stored in table (=> id uniqueness is checked)
        # 2. activate: hooks, links, external files

        # add inert
        added_records = self._dev_add_inert(records_data)

        # activate hooks
        for r in added_records:
            r._dev_activate_hooks()

        # activate links and external files
        for r in added_records:
            r._dev_activate_links()
            r._dev_activate_external_files()

        return Queryset(self, records=added_records)

    # delete
    def delete(self):
        """Delete all records of table."""
        self.select().delete()

    # get idd info
    def get_info(self):
        """
        Get table info.

        Returns
        -------
        str
        """
        return self._dev_descriptor.get_info()

    # ------------------------------------------- export ---------------------------------------------------------------
    def to_json_data(self):
        """
        Get Table as a json-serializable dict.

        Returns
        -------
        A dictionary of serialized data.
        """
        return self.select().to_json_data()
