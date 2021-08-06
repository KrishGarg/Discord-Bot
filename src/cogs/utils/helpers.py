import aiosqlite
from typing import List, Union, Dict
from .custom_errors import CacheError
import textwrap


class Caching:
    """
    A basic class to handle the caching of data and cleanly and professionally handle the data.

    Attributes
    ----------
    conn : aiosqlite.Connection
        The sqlite connection to the database.
    table_name : str
        The sqlite table to link the object with.
    default_datatype : str, optional
        The datatype in which the data will be returned in the object, by default 'dict'.
        Choose between 'tuple' and 'dict'. 'tuple' is just shorthand for List[tuple].
    data : Union[List[tuple], Dict[int, list]]
        The cache/data stored. You can access the local cache from this attribute or use
        the methods update_local_cache and get_local_cache.
    """
    async def __init__(self, *, connection: aiosqlite.Connection, table_name: str, datatype: str = 'dict') -> None:
        self.conn: aiosqlite.Connection = connection

        cur = await self.conn.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name=?", (table_name, ))
        if_table_exists_check = await cur.fetchall()
        if if_table_exists_check == 0:
            raise CacheError("Invalid Table.")
        self.table_name: str = table_name

        if not datatype in ('tuple', 'dict'):
            raise CacheError("Invalid Datatype.")
        self.default_datatype: str = datatype

        self.data = None

    async def get_fresh_data(self) -> Union[List[tuple], Dict[int, list]:]:
        """
        get_fresh_data Method to get new and fresh data from the database for the table. 
        This method sets the `self.data` with the current data from the database and also
        returns the data.

        Returns
        -------
        Union[List[tuple], Dict[int, list]]
            Depends on you chose in the initializing. Default is dict with guild_id as the key.
        """

        ''' 
        Below isn't recommended but in this case, self.table_name 
        is only defined by the coder, and I don't know why but placeholder
        (?) doesn't work with table name. -- (1)
        '''

        cur = await self.conn.execute(f"SELECT * FROM {self.table_name}")
        all_data = await cur.fetchall()

        if not all_data:
            self.data = None
            return None

        if self.default_datatype == 'tuple':
            self.data = all_data
            return all_data

        else:
            '''
            (1) ↓
            '''
            cur = await self.conn.execute(f"PRAGMA table_info({self.table_name})")
            table_schema = await cur.fetchall()
            guild_id_index = next(
                (column[0] for column in table_schema if column[1] == "guild_id"), [])

            if not guild_id_index:
                raise CacheError(textwrap.dedent(f"""There is no column found named 'guild id' 
                in the table '{self.table_name}'. Please edit the table to have the specified 
                column or switch the default datatype to 'tuple'. Do keep in mind tuples are 
                harder to manage."""))

            self.table_schema = table_schema

            if guild_id_index == 0:
                self.data = {data_packet[guild_id_index]: [
                    [*datap[1:]] for datap in all_data if datap[guild_id_index] == data_packet[guild_id_index]] for data_packet in all_data}
            elif guild_id_index == len(table_schema) - 1:
                self.data = {data_packet[guild_id_index]: [
                    [*datap[:-1]] for datap in all_data if datap[guild_id_index] == data_packet[guild_id_index]] for data_packet in all_data}
            else:
                self.data = {data_packet[guild_id_index]: [[*datap[:guild_id_index], *datap[guild_id_index+1:]]
                                                           for datap in all_data if datap[guild_id_index] == data_packet[guild_id_index]] for data_packet in all_data}