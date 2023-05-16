from enum import Enum

class myEnums(Enum):
    def __str__(self) -> str:
        return str(self.value)
    def __repr__(self) -> str:
        return self.value
    

class Table_name(myEnums):
    USERS = "users"
    TEST_USERS = "test_users"
    SALES = "sales"

 
class Users_table(myEnums):
    id="id"
    username="username"
    password="password"
    email="email"
    fullname="fullname"
    role="role"
    all_columns: list=['id','username','password','email','fullname','role']

class Query_type(myEnums):
    DELETE="DELETE"
    INSERT="INSERT"
    SELECT="SELECT"
    UPDATE="UPDATE"

class Role(myEnums):
    """
    A class that represents the different roles that a user can have.

    Attributes:
        OWNER (int)      = 3
        ADMIN (int)      = 2
        NORMAL (int)     = 1
        RESTRICTED (int) = 0

    Role.name gives the string representation of the constant
    """
    owner = 3
    admin = 2
    normal = 1
    restricted = 0

class Sort(myEnums):
    """
    A class that represents the different sort orders that can be used for
    Query_Factory.
    
    Attributes:
        ASCENDING (str)   = "ASC"
        DESCENDING (str)  = "DESC"

    Sort.name gives the string representation of the constant
    """
    ASCENDING = "ASC"
    DESCENDING = "DESC"

class CTKbuttonclicks(myEnums):
    LEFT_CLICK = "<Button-1>"
    MIDDLE_CLICK = "<Button-2>"
    RIGHT_CLICK = "<Button-3>"
