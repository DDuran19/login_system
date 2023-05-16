import unittest
if __name__ == "__main__":
    import os,sys

    this_file_directory=os.path.dirname(os.path.realpath(__file__))
    sys.path.append(os.path.dirname(this_file_directory))

from utils.Queries import Query_factory
from utils.Error_handler import Invalid_characters
QUERIES_PY="utils\\Queries.py"

class Query_factory_Tests(unittest.TestCase):
    def setUp(self) -> None:
        NOT_USER="notuser"
        JOHN_DOE="John doe"
        JOHN_DOE_EMAIL="johndoe@example.com"
        JANE_DOE="Jane Doe"
        JANE_DOE_EMAIL = "janedoe@example.com"
        JANE_DOENUT="Janedoenut"
        JANE_DOENUT_EMAIL="janedoenut@example.com"
        
        self.actual_insert_query1 = Query_factory.insert(username=JOHN_DOE,email=JOHN_DOE_EMAIL, password="password123")
        self.expected_insert_query1="INSERT OR ROLLBACK INTO users (username, email, password) VALUES (?, ?, ?)('John doe', 'johndoe@example.com', 'password123')"
        self.actual_insert_query2 = Query_factory.insert(username=JOHN_DOE, email=JOHN_DOE_EMAIL)
        self.expected_insert_query2 = "INSERT OR ROLLBACK INTO users (username, email) VALUES (?, ?)('John doe', 'johndoe@example.com')"
        self.actual_insert_query3 =  Query_factory.insert(Table_name=NOT_USER, id=5)
        self.expected_insert_query3 = "INSERT OR ROLLBACK INTO notuser (id) VALUES (?)('5',)"

        self.actual_search_query1 = Query_factory.search(username=JOHN_DOE)
        self.expected_search_query1 = "SELECT * FROM users WHERE  username = ?  ORDER BY username ASC LIMIT 1;('John doe',)"
        self.actual_search_query2 = Query_factory.search(email=JANE_DOE_EMAIL,fullname=JANE_DOE)
        self.expected_search_query2 = "SELECT * FROM users WHERE  email = ?  AND  fullname = ?  ORDER BY username ASC LIMIT 1;('janedoe@example.com', 'Jane Doe')"
        self.actual_search_query3 = Query_factory.search(NOT_USER, 10, email=JANE_DOE_EMAIL)
        self.expected_search_query3 = "SELECT * FROM notuser WHERE  email = ?  ORDER BY username ASC LIMIT 10;('janedoe@example.com',)"

        self.actual_update_query1 = Query_factory.update("newpassword123","password",id=1)
        self.expected_update_query1 = "UPDATE OR IGNORE users SET password = ?  WHERE  id = ? ('newpassword123', '1')"
        self.actual_update_query2 = Query_factory.update(JANE_DOENUT,"username",id=2,username=JANE_DOE,email=JANE_DOE_EMAIL)
        self.expected_update_query2 = "UPDATE OR IGNORE users SET username = ?  WHERE  id = ?  AND  username = ?  AND  email = ? ('Janedoenut', '2', 'Jane Doe', 'janedoe@example.com')"
        self.actual_update_query3 = Query_factory.update(JANE_DOENUT_EMAIL,COLUMN_NAME="email", Table_name=NOT_USER,id=5,email=JANE_DOE_EMAIL)
        self.expected_update_query3 = "UPDATE OR IGNORE notuser SET email = ?  WHERE  id = ?  AND  email = ? ('janedoenut@example.com', '5', 'janedoe@example.com')"

        self.actual_delete_query1 = Query_factory.delete(id=1)
        self.expected_delete_query1 = "DELETE FROM users WHERE  id = ? ('1',)"
        self.actual_delete_query2 = Query_factory.delete(username=JOHN_DOE,role = "admin")
        self.expected_delete_query2 = "DELETE FROM users WHERE  username = ?  AND  role = ? ('John doe', 'admin')"
        self.actual_delete_query3 = Query_factory.delete(Table_name=NOT_USER,email=JANE_DOE_EMAIL)
        self.expected_delete_query3 = "DELETE FROM notuser WHERE  email = ? ('janedoe@example.com',)"

    def test_insert_query1(self):
        result = str(self.actual_insert_query1)
        expected = self.expected_insert_query1
        self.assertEqual(result, expected, msg=f"A problem occurred in insert_query1. Please check out insert method in {QUERIES_PY}")

    def test_insert_query2(self):
        result = str(self.actual_insert_query2)
        expected = self.expected_insert_query2
        self.assertEqual(result, expected, msg=f"A problem occurred in insert_query2. Please check out insert method in {QUERIES_PY}")

    def test_insert_query3(self):
        result = str(self.actual_insert_query3)
        expected = self.expected_insert_query3
        self.assertEqual(result, expected, msg=f"A problem occurred in insert_query3. Please check out insert method in {QUERIES_PY}")

    def test_search_query1(self):
        result = str(self.actual_search_query1)
        expected = self.expected_search_query1
        self.assertEqual(result, expected, msg=f"A problem occurred in search_query1. Please check out search method in {QUERIES_PY}")

    def test_search_query2(self):
        result = str(self.actual_search_query2)
        expected = self.expected_search_query2
        self.assertEqual(result, expected, msg=f"A problem occurred in search_query2. Please check out search method in {QUERIES_PY}")

    def test_search_query3(self):
        result = str(self.actual_search_query3)
        expected = self.expected_search_query3
        self.assertEqual(result, expected, msg=f"A problem occurred in search_query3. Please check out search method in {QUERIES_PY}")

    def test_update_query1(self):
        result = str(self.actual_update_query1)
        expected = self.expected_update_query1
        self.assertEqual(result, expected, msg=f"A problem occurred in update_query1. Please check out update method in {QUERIES_PY}")

    def test_update_query2(self):
        result = str(self.actual_update_query2)
        expected = self.expected_update_query2
        self.assertEqual(result, expected, msg=f"A problem occurred in update_query2. Please check out update method in {QUERIES_PY}")

    def test_update_query3(self):
        result = str(self.actual_update_query3)
        expected = self.expected_update_query3
        self.assertEqual(result, expected, msg=f"A problem occurred in update_query3. Please check out update method in {QUERIES_PY}")

    def test_delete_query1(self):
        result = str(self.actual_delete_query1)
        expected = self.expected_delete_query1
        self.assertEqual(result, expected, msg=f"A problem occurred in delete_query1. Please check out delete method in {QUERIES_PY}")

    def test_delete_query2(self):
        result = str(self.actual_delete_query2)
        expected = self.expected_delete_query2
        self.assertEqual(result, expected, msg=f"A problem occurred in delete_query2. Please check out delete method in {QUERIES_PY}")

    def test_delete_query3(self):
        result = str(self.actual_delete_query3)
        expected = self.expected_delete_query3
        self.assertEqual(result, expected, msg=f"A problem occurred in delete_query3. Please check out delete method in {QUERIES_PY}")            

class Query_factory_SQL_Injection(unittest.TestCase):
    def setUp(self) -> None:
        self.SQL_INJECT = "' OR 1=1 --"
        
    def test_SQL_insert_injection(self):
        message = f"a problem occurred in insert method. Please check the insert method in {QUERIES_PY}. Possible SQL Injection, Input will be logged for security purposes"
        with self.assertRaises(Invalid_characters, msg=message):
            Query_factory.insert(Table_name="notuser", id=5, fullname=self.SQL_INJECT)

    def test_SQL_search_injection(self):
        message = f"a problem occurred in search method. Please check the search method in {QUERIES_PY}. Possible SQL Injection, Input will be logged for security purposes"
        with self.assertRaises(Invalid_characters, msg=message):
            Query_factory.search(Table_name="users", username=self.SQL_INJECT)

    def test_SQL_update_injection(self):
        message = f"a problem occurred in update method. Please check the update method in {QUERIES_PY}. Possible SQL Injection, Input will be logged for security purposes"
        with self.assertRaises(Invalid_characters, msg=message):
            Query_factory.update("newpassword123", "password", id=self.SQL_INJECT)

    def test_SQL_delete_injection(self):
        message = f"a problem occurred in delete method. Please check the delete method in {QUERIES_PY}. Possible SQL Injection, Input will be logged for security purposes"
        with self.assertRaises(Invalid_characters, msg=message):
            Query_factory.delete(id=1, role=self.SQL_INJECT)


if __name__ == "__main__":
    unittest.main()