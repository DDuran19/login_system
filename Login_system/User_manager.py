
if __name__ == "__main__":
    import os,sys

    this_file_directory=os.path.dirname(os.path.realpath(__file__))
    parent_directory=os.path.dirname(this_file_directory)
    sys.path.append(parent_directory)

from typing import Union,Optional


from Login_system.User import User
from utils.Queries import Query_factory, Execute_connection,DATABASE_LOCATION
from utils.Enums import Role, Table_name
from utils.Encryption import Encryption


class New_user (User):
    """
    A class representing a new user.

    Attributes:
    username: The user's username.
    password: The user's password, encrypted.
    fullname: The user's full name.
    role: The user's role.
    email: The user's email address.

    Methods:
    __init__(self, username: str, password: str | bytes, fullname: str, role: Role, email: str)
        Create a new New_user object.

    check_username_duplicate(self, username_to_check: str, _tablename: Table_name=Table_name.USERS, _database: Optional[str]=DATABASE_LOCATION) -> None:
        Check if the given username already exists in the database.

    encrypt_password(self, password: str) -> str:
        Encrypt the given password.

    save(self, _tablename: Table_name=Table_name.USERS, _database: Optional[str]=DATABASE_LOCATION) -> bool:
        Save the user to the database.
    """

    password: Union[str,bytes]
    def __init__(self, 
                 username: str, 
                 password: str | bytes,
                 fullname: str, 
                 role: Role, 
                 email: str, 
                 _tablename: Table_name=Table_name.USERS) -> None:
        self.username = self.check_username_duplicate(username,_tablename)
        self.password=self.encrypt_password(password)
        self.fullname=fullname
        self.role=role
        self.email=email 
        self._tablename=_tablename

    def check_username_duplicate(self, username_to_check,_tablename: Table_name=Table_name.USERS,_database: Optional[str]=DATABASE_LOCATION):
        """
        Check if the given username already exists in the database.

        Args:
            username_to_check: The username to check.
            _tablename: The name of the table to check.
            _database: The name of the database to check.

        Raises:
            ValueError: If the username already exists.
        """
        existing_username = Query_factory.search(_tablename,username=username_to_check)
        
        query = Execute_connection.perform(existing_username, _database)

        if query.ROWS is None: 
            return username_to_check
        
        if len(query.ROWS) > 0:

            raise ValueError (f'{username_to_check} already exists in {_tablename}') 
        return username_to_check

    def encrypt_password(self, password):
        """
        Encrypt the given password if it is a string.

        Args:
            password: The password to encrypt.

        Returns:
            The encrypted password.
        """

        if isinstance(password,str):
            return Encryption.encrypt(password)
        return password
        
    def save (self,_database: Optional[str]=DATABASE_LOCATION):
        """
        Save the user to the database.

        Args:
            _tablename: The name of the table to save the user to.
            _database: The name of the database to save the user to.

        Returns:
            True if the user was saved successfully, False otherwise.
        """

        details = self.get_all_info()

        new_user = Query_factory.insert(self._tablename, **details)
        query = Execute_connection.perform(new_user,_database)

        return query._SUCCESSFUL







def tests():
    actual_new_user1=New_user("Admin","adminpassword","Admin admin",Role.admin.name,"Admin@admin.com",_tablename=Table_name.TEST_USERS)
    expected_user1_info = "New_user(_id=None, username='Admin', fullname='Admin admin', role='admin', email='Admin@admin.com', _tablename=test_users)"
    actual_user1_info={'username': 'Admin', 'password': b'$2b$12$rhqAk4.BjC.3MK2Xe6epH.w7VzSBigsaJodnAP5LQH3RriniMCz5y', 'fullname': 'Admin admin', 'role': 'admin', 'email': 'Admin@admin.com'}

    actual_new_user2=New_user("Sample12","password","Sample Only",Role.normal.name,"sample@sample.com",_tablename=Table_name.TEST_USERS)
    expected_user2_info = "New_user(_id=None, username='Sample12', fullname='Sample Only', role='normal', email='sample@sample.com', _tablename=test_users)"
    actual_user2_info={'username': 'Sample12', 'password': b'$2b$12$rhqAk4.BjC.3MK2Xe6epH.CokS.YTGkTMgQ7YPMnW/NtopGiHVBu2', 'fullname': 'Sample Only', 'role': 'normal', 'email': 'sample@sample.com'}

    actual_new_user1.save(_database=DATABASE_LOCATION)
    actual_new_user2.save(_database=DATABASE_LOCATION)


if __name__ == "__main__":
    tests()