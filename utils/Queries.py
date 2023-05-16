import sys, sqlite3, os

################### initialize directories ######################
this_file_directory=os.path.dirname(os.path.realpath(__file__))
parent_directory=os.path.dirname(this_file_directory)
sys.path.append(parent_directory)
#################################################################

from typing import Optional


from utils.Error_handler import _sanitize
from utils.Enums import Sort,Table_name,Query_type,Users_table

TABLE_NAME_DEFAULT = Table_name.USERS
LIMIT_DEFAULT = 1


DATABASE_LOCATION = f'{parent_directory}\data\db.sqlite3'




class Query_factory:
    """
    --------------------------------
    *****  DO NOT INSTANCIATE  *****
    --------------------------------
    returns a Query_factory object. 

    sample use-case:
        my_query = Query_factory.update(NEW_VALUE="my new email", COLUMN_NAME = 'email', id = 6)

    returned object use-case:
        ...
        cursor.execute(my_query.query, my_query.values)
        ...

    This class has a built-in _sanitize method to sanitize the inputs then
    securely passes the required parameters for an sql execute command

    attributes:
        - query: str
        - values: tuple

    methods available:
        - insert (adds data in a given table)
        - search (searches keyword in a given table)
        - update (updates an existing data in a given table)
        - delete (deletes an existing data in a given table)

    defaults:
        Table_name ="users"
        LIMIT = 1
        username, Sort.ASCENDING -> sorting of data received from database, use Sort.Ascending class from utils.Enums
        UPDATE -> fullname
    """
    query: Optional[str]=None
    values: Optional[tuple]=None
    query_type: Optional[Query_type]=None

    def __repr__(self) -> str:
        return f'{self.query}{self.values}'

    @classmethod
    def insert(self,Table_name: Optional[str] = TABLE_NAME_DEFAULT,**COLUMN_AND_VALUES)->str:
        """
        Inserts a row into a given table.

        Args:
        Table_name: The name of the table to insert the row into.
        **COLUMN_AND_VALUES: A dictionary mapping column names to values.

        Returns:
        A Query_factory object that can be used to execute the query.

        """

        values = list()
        columns = list()
        second_placeholder = list()
        
        for key in COLUMN_AND_VALUES.keys():
            columns.append(key)

        for value in COLUMN_AND_VALUES.values():
            value = _sanitize(value)
            second_placeholder.append("?")
            values.append(value)
            
        query_string=f'{Query_type.INSERT} OR ROLLBACK INTO {Table_name} ({", ".join(columns)}) VALUES ({", ".join(second_placeholder)})'

        values=tuple([item for item in values])


        result = Query_factory()
        result.query = query_string
        result.values = values
        result.query_type=Query_type.INSERT
        return result

    @classmethod
    def search(self,
                Table_name: str = TABLE_NAME_DEFAULT,
                LIMIT: int = LIMIT_DEFAULT,
                ORDER_BY: tuple[Users_table,Sort]=(Users_table.username,Sort.ASCENDING),**WHERE_COLUMN_AND_VALUE):
        
        """
        Searches for rows in a given table that match the specified criteria.

        Args:
        Table_name: The name of the table to search.
        LIMIT: The maximum number of rows to return.
        ORDER_BY: A tuple of column names and directions. 
            The first column name is the column to sort by, 
            and the second column name is the direction to sort in.
            Valid directions Sort.ASCENDING and Sort.Descending

        **WHERE_COLUMN_AND_VALUE: A dictionary mapping column names to values. 
            The rows that match the specified criteria will be returned.

        Returns:
        A Query_factory object that can be used to execute the query.

        """
        conditions = list()
        values = list()
        if not all(ORDER_BY):
            raise TypeError
        
        order_by_column, order_by_direction = ORDER_BY

        self._check_type(order_by_column,Users_table)
        self._check_type(order_by_direction,Sort)
        
        query_string = f"{Query_type.SELECT} * FROM {Table_name} WHERE "

        for key, value in WHERE_COLUMN_AND_VALUE.items():
            values.append(_sanitize(value))
            conditions.append(f" {key} = ? ")

        query_string += " AND ".join(conditions)
        query_string += f' ORDER BY {order_by_column} {order_by_direction}'

        query_string += f" LIMIT {_sanitize(LIMIT)};"

        values=tuple([item for item in values])


        result = Query_factory()
        result.query = query_string
        result.values = values
        result.query_type=Query_type.SELECT
        return result

    
    @classmethod
    def update(self,
                NEW_VALUE: str,
                COLUMN_NAME:Optional[Users_table]=Users_table.fullname,
                Table_name: Optional[Table_name] = TABLE_NAME_DEFAULT,
                **WHERE_COLUMN_AND_VALUE):
        """
        Updates a row in a given table.

        Args:
        NEW_VALUE: The new value for the column.
        COLUMN_NAME: The name of the column to update.
        Table_name: The name of the table to update the row in.
        **WHERE_COLUMN_AND_VALUE: A dictionary mapping column names to values. 
            The rows that match the specified criteria will be updated.

        Returns:
        A Query_factory object that can be used to execute the query.

        """

        conditions = list()
        values = list()
        
        query_string = f"{Query_type.UPDATE} OR IGNORE {Table_name} SET {COLUMN_NAME} = ? "
        values=[_sanitize(NEW_VALUE)]

        conditions = []
        for key, value in WHERE_COLUMN_AND_VALUE.items():
            value = _sanitize(value)

            conditions.append(f" {key} = ? ")

            values.append(value)

        query_string += " WHERE "
        query_string += " AND ".join(conditions)

        values=tuple([item for item in values])


        result = Query_factory()
        result.query = query_string
        result.values = values
        result.query_type=Query_type.UPDATE
        return result


    @classmethod
    def delete(self,
                Table_name: Table_name = TABLE_NAME_DEFAULT,
                **WHERE_COLUMN_AND_VALUE):
        """
        Deletes rows from a given table that match the specified criteria.

        Args:
        Table_name: The name of the table to delete rows from.
        **WHERE_COLUMN_AND_VALUE: A dictionary mapping column names to values. 
            The rows that match the specified criteria will be deleted.

        Returns:
        A Query_factory object that can be used to execute the query.

        """

        conditions = list()
        values = list()

        query_string=f"{Query_type.DELETE} FROM {Table_name} WHERE "

        for key, value in WHERE_COLUMN_AND_VALUE.items():
            value = _sanitize(value)
            conditions.append(f" {key} = ? ")
            values.append(value)

        query_string += " AND ".join(conditions)

        values=tuple([item for item in values])


        result = Query_factory()
        result.query = query_string
        result.values = values
        result.query_type=Query_type.DELETE
        return result



    @classmethod
    def _check_type(self,input: any, data_type: any) -> None:
        """
        Raises an error if input has incorrect data type

        Error:
            TypeError: input is not data_type
        """
        if isinstance(input,data_type):
            return
        raise TypeError(f"{input} is not {data_type}")

class Execute_connection:
    """
    --------------------------------
    *****  DO NOT INSTANCIATE  *****
    --------------------------------
    returns Execute_connection object.

    Use-case:
    - Execute_connection.ROWS to get results from the query
    - Execute_connection._SUCCESSFUL for boolean expressions
    - Execute_connection.STATUS to get status / any error messages


    Attributes: DO NOT CHANGE ANY ATTRIBUTES

        STATUS: The status of the last query executed.
        _SUCCESSFUL: A boolean value indicating whether the last query was successful.
        ROWS: A list of rows returned by the last query executed. (dict-like)

    Methods:
    perform: runs the query
    """
    STATUS = ""
    _SUCCESSFUL: bool = False
    ROWS: Optional[sqlite3.Cursor] = None

    @classmethod
    def perform(self,query: Query_factory, database: str = DATABASE_LOCATION):
        """Connect to the database and execute the query.

        Args:
            query: The query to execute. use Query_factory at utils.Queries.py
            database: The path to the database file.

        Returns:
            A list of rows if the query was successful, or None if the query failed.
        """
        with sqlite3.connect(database) as db:
            db.row_factory = sqlite3.Row
            cursor=db.cursor()
            
            result = Execute_connection()

            try:
                cursor.execute(query.query,query.values)
                
                result._SUCCESSFUL = True
                result.STATUS = "Query successful"

            except Exception as e:
                print(str(e))
                result._SUCCESSFUL = False
                result.STATUS = str(e)

            result.ROWS=self.row_manager(query,cursor)
            db.commit()
            cursor.close()
            return result

    @classmethod
    def row_manager(self,query: Query_factory,cursor: sqlite3.Cursor):
        if query.query_type==Query_type.SELECT:
            rows = cursor.fetchone() 
            if rows is None:
                return None
            if len(rows) == 0:
                return None
            return rows 
        return None
        
        

    

def tests():
    NOT_USER="notuser"
    JOHN_DOE="John doe"
    JOHN_DOE_EMAIL="johndoe@example.com"
    JANE_DOE="Jane Doe"
    JANE_DOE_EMAIL = "janedoe@example.com"
    JANE_DOENUT="Janedoenut"
    JANE_DOENUT_EMAIL="janedoenut@example.com"
    SQL_INJECT="' OR 1=1 --"
    actual_insert_query1 = Query_factory.insert(username=JOHN_DOE,email=JOHN_DOE_EMAIL, password="password123")
    expected_insert_query1="INSERT OR ROLLBACK INTO users (username, email, password) VALUES (?, ?, ?)('John doe', 'johndoe@example.com', 'password123')"

    actual_insert_query2 = Query_factory.insert(username=JOHN_DOE, email=JOHN_DOE_EMAIL)
    expected_insert_query2 = "INSERT OR ROLLBACK INTO users (username, email) VALUES (?, ?)('John doe', 'johndoe@example.com')"
    actual_insert_query3 =  Query_factory.insert(Table_name=NOT_USER, id=5)
    expected_insert_query3 = "INSERT OR ROLLBACK INTO notuser (id) VALUES (?)('5',)"


    actual_search_query1 = Query_factory.search(username=JOHN_DOE)
    expected_search_query1 = "SELECT * FROM users WHERE  username = ?  ORDER BY username ASC LIMIT = 1('username', ASC)"
    actual_search_query2 = Query_factory.search(email=JANE_DOE_EMAIL,fullname=JANE_DOE)
    expected_search_query2 = "SELECT * FROM users WHERE  email = ?  AND  fullname = ?  ORDER BY username ASC LIMIT = 1('username', ASC)"
    actual_search_query3 = Query_factory.search(NOT_USER, 10, email=JANE_DOE_EMAIL)
    expected_search_query3 = "SELECT * FROM notuser WHERE  email = ?  ORDER BY username ASC LIMIT = 10('username', ASC)"


    actual_update_query1 = Query_factory.update("newpassword123","password",id=1)
    expected_update_query1 = "UPDATE OR IGNORE users SET password = ?  WHERE  id = ? ('newpassword123', '1')"
    actual_update_query2 = Query_factory.update(JANE_DOENUT,"username",id=2,username=JANE_DOE,email=JANE_DOE_EMAIL)
    expected_update_query2 = "UPDATE OR IGNORE users SET username = ?  WHERE  id = ?  AND  username = ?  AND  email = ? ('Janedoenut', '2', 'Jane Doe', 'janedoe@example.com')"
    actual_update_query3 = Query_factory.update(JANE_DOENUT_EMAIL,COLUMN_NAME="email", Table_name=NOT_USER,id=5,email=JANE_DOE_EMAIL)
    expected_update_query3 = "UPDATE OR IGNORE notuser SET email = ?  WHERE  id = ?  AND  email = ? ('janedoenut@example.com', '5', 'janedoe@example.com')"

    actual_delete_query1 = Query_factory.delete(id=1)
    expected_delete_query1 = "DELETE FROM users WHERE  id = ? ('1',)"
    actual_delete_query2 = Query_factory.delete(username=JOHN_DOE,role = "admin")
    expected_delete_query2 = "DELETE FROM users WHERE  username = ?  AND  role = ? ('John doe', 'admin')"
    actual_delete_query3 = Query_factory.delete(Table_name=NOT_USER,email=JANE_DOE_EMAIL)
    expected_delete_query3 = "DELETE FROM notuser WHERE  email = ? ('janedoe@example.com',)"


    SQL_insert_injection = Query_factory.insert(Table_name=NOT_USER, id=5, fullname = SQL_INJECT)
    SQL_search_injection = Query_factory.search(Table_name="users",username=SQL_INJECT)
    SQL_update_injection = Query_factory.update("newpassword123","password",id=SQL_INJECT)
    SQL_delete_injection = Query_factory.delete(id=1,role=SQL_INJECT)

if __name__ == "__main__":
    tests()
