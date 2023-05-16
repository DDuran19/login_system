if __name__ == "__main__":
    import os,sys

    this_file_directory=os.path.dirname(os.path.realpath(__file__))
    parent_directory = os.path.dirname(this_file_directory)
    sys.path.append(parent_directory)

from ast import literal_eval
from dataclasses import dataclass,field
from typing import Optional

from Login_system.User import Logged_in_user
from utils.Enums import Table_name, Users_table
from utils.Queries import Query_factory, Execute_connection
from utils.Error_handler import User_not_found,Password_did_not_matched
from utils.Encryption import Encryption

@dataclass
class Login:
    username: str
    password_attempt: str
    _real_password: Optional[bytes]  = None
    _user_details: dict =  field(default_factory=dict)
    _table: Table_name=Table_name.USERS
    _query: Optional[Query_factory] = None

    def login(self):
        
        self._get_password_from_username()
        self._verify_password()
        return self._successful_login()

    def _get_password_from_username(self):

        self._prepare_username_query()
        self._perform_query()
        
                 
    def _verify_password(self):
        
        password_matched = Encryption.decrypt(self._real_password,self.password_attempt)
        
        if password_matched:
            return self._successful_login
        
        raise Password_did_not_matched(details = f'Username: "{self.username}" Password attempted: "{self.password_attempt}"') 

    def _successful_login(self):

        return Logged_in_user(**self._user_details)
    
    def _prepare_username_query(self):
        self._query = Query_factory.search(username=self.username)
    
    def _perform_query(self):
        found = Execute_connection.perform(self._query)
        

        if not found.ROWS is None:
            self._get_details(found)
            return
        raise User_not_found(details = f'Username: "{self.username}" Password attempted: "{self.password_attempt}"')
    
    def _get_details(self, found: Execute_connection):
        details={}
        for column in Users_table.all_columns.value:
            if column == "id":
                details["_id"] = found.ROWS[column]
                continue
            if column == Users_table.password.value:
                self._real_password=literal_eval(found.ROWS[column])
                continue
            details [column] = found.ROWS[column]
        
        self._user_details=details

            
if __name__ == "__main__":        
    pw=b'$2b$12$rhqAk4.BjC.3MK2Xe6epH.w7VzSBigsaJodnAP5LQH3RriniMCz5y'
    pwt="adminpassword"
    un = "Admin"

    user=Login(un,pwt)
    result=user.login()

    print(result)
