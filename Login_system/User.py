import os

if __name__ == "__main__":
    import sys

    this_file_directory=os.path.dirname(os.path.realpath(__file__))
    sys.path.append(os.path.dirname(this_file_directory))


from dataclasses import dataclass
from typing import Optional
from utils.Enums import Role,Users_table, Table_name


@dataclass
class User:
    """
    Parent class, has attributes based on database columns
    id, username, fullname, role, email

    `password` is NOT included as it will not be saved in memory

    """
    _id: Optional[int] = None
    username: Optional[str] = None
    fullname: Optional[str] = None
    role: Optional[Role] = None
    email: Optional[str] = None
    _tablename: Table_name=Table_name.USERS

    def get_all_info(self) -> dict:
        user_info = {}
        for attribute_name, attribute_value in vars(self).items():
            if not attribute_name in Users_table.all_columns.value or attribute_name.startswith("_"):
                continue
            user_info[attribute_name] = attribute_value
        return user_info

class Logged_in_user(User):
    """
    Currently logged in user
    """

    _instance=None

    def __new__(cls,*args,**kwargs):
        if cls._instance is None:
            cls._instance=super().__new__(cls)
        return cls._instance

