import os, sqlite3

if __name__ == "__main__":
    import sys

    this_file_directory=os.path.dirname(os.path.realpath(__file__))
    parent_directory = os.path.dirname(this_file_directory)
    sys.path.append(parent_directory)
    print(parent_directory)

import unittest
from Login_system.User import User, Logged_in_user, Role
from Login_system.User_manager import New_user,DATABASE_LOCATION
from utils.Enums import Table_name

USER_PY="Login_system\\User.py"

class UserTests(unittest.TestCase):
    def setUp(self):
        self.first_user = Logged_in_user(1,"Juan_1","Juan Felipe", Role.normal,"Juan@gmail.com")
        self.second_user = Logged_in_user(2, "Michael_2","Michael Faraday",Role.normal, "Michael@gmail.com")
    def test_logged_in_user_as_singleton(self):
        message = f"test created a new instance, check out {USER_PY}"
        self.assertIs(self.first_user,self.second_user,message)
    def tearDown(self) -> None:
        return super().tearDown()

class New_userTests(unittest.TestCase):
    def setUp(self):
        self.actual_new_user1=New_user("Admin","adminpassword","Admin admin",Role.admin.name,"Admin@admin.com",_tablename=Table_name.TEST_USERS)
        self.expected_user1_info = "New_user(_id=None, username='Admin', fullname='Admin admin', role='admin', email='Admin@admin.com', _tablename=test_users)"
        self.actual_user1_info={'username': 'Admin', 'password': b'$2b$12$rhqAk4.BjC.3MK2Xe6epH.w7VzSBigsaJodnAP5LQH3RriniMCz5y', 'fullname': 'Admin admin', 'role': 'admin', 'email': 'Admin@admin.com','_tablename':Table_name.TEST_USERS}

        self.actual_new_user2=New_user("Sample12","password","Sample Only",Role.normal.name,"sample@sample.com",_tablename=Table_name.TEST_USERS)
        self.expected_user2_info = "New_user(_id=None, username='Sample12', fullname='Sample Only', role='normal', email='sample@sample.com', _tablename=test_users)"
        self.actual_user2_info={'username': 'Sample12', 'password': b'$2b$12$rhqAk4.BjC.3MK2Xe6epH.CokS.YTGkTMgQ7YPMnW/NtopGiHVBu2', 'fullname': 'Sample Only', 'role': 'normal', 'email': 'sample@sample.com','_tablename':Table_name.TEST_USERS}


    def test_str_representation(self):
        self.assertEqual(str(self.actual_new_user1), self.expected_user1_info)
        self.assertEqual(str(self.actual_new_user2), self.expected_user2_info)

    def test_repr_representation(self):
        self.assertEqual(repr(self.actual_new_user1), self.expected_user1_info)
        self.assertEqual(repr(self.actual_new_user2), self.expected_user2_info)

    def test_attributes(self):
        self.assertEqual(self.actual_new_user1.username, "Admin")
        self.assertEqual(self.actual_new_user1.fullname, "Admin admin")
        self.assertEqual(self.actual_new_user1.role, Role.admin.name)
        self.assertEqual(self.actual_new_user1.email, "Admin@admin.com")
        self.assertEqual(self.actual_new_user1.password, self.actual_new_user1.encrypt_password("adminpassword"))
        self.assertEqual(self.actual_new_user2.username, "Sample12")
        self.assertEqual(self.actual_new_user2.fullname, "Sample Only")
        self.assertEqual(self.actual_new_user2.role, Role.normal.name)
        self.assertEqual(self.actual_new_user2.email, "sample@sample.com")
        self.assertEqual(self.actual_new_user2.password, self.actual_new_user2.encrypt_password("password"))

    def test_dict_representation(self):
        self.assertEqual(self.actual_new_user1.__dict__, self.actual_user1_info)
        self.assertEqual(self.actual_new_user2.__dict__, self.actual_user2_info)

    def test_save_method(self):
        self.actual_new_user1.save()
        with sqlite3.connect(DATABASE_LOCATION) as db:
            db.row_factory = sqlite3.Row
            cursor=db.cursor()
            row = cursor.execute(f"SELECT * FROM test_users WHERE username = 'Admin'")
            row = cursor.fetchone()

            if row:
                username = row['username']
                db.commit()
                
                message = "save method did not save the new_user"
                self.assertEqual(username, "Admin", message)    
            else:
                self.fail("No row found for username 'Admin'")
                  
        with self.assertRaises(ValueError,msg="Duplicate not recognized"):
            New_user("Admin","adminpassword","Admin admin",Role.admin.name,"Admin@admin.com",_tablename=Table_name.TEST_USERS)

    def tearDown(self) -> None:
        with sqlite3.connect(DATABASE_LOCATION) as db:
            cursor=db.cursor()
            cursor.execute('DELETE FROM test_users')
            db.commit()

if __name__ == "__main__":
    unittest.main(verbosity= 2)