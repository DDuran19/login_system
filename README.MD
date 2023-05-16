# Software Overview

This software is a small Python project created by Denver James Duran. It uses the following libraries:

- <strong style="color:green">Database</strong>: SQLite3
- <strong style="color:green">GUI</strong>: customtkinter
- <strong style="color:green">Error Checking</strong>: unittest, importlib, Logging
- <strong style="color:green">Encryption</strong>: bcrypt
- <strong style="color:green">Others</strong>: os, sys

The software has the following features:

- <strong style="color:green">Data cleaning</strong>: User inputs are sanitized to prevent common SQL injection attacks. Inputs are also parameterized before execution, which improves security.
- <strong style="color:green">Factory Design</strong>: Codes are separated as much as possible and objects are given unique names.
- <strong style="color:green">Error handling</strong>: Customized Exceptions with their own GUI dialogue and descriptive message allow end users to understand what is happening.
- <strong style="color:green">Logging</strong>: All customized errors are saved in an `errors.log` file within the project directory for backtracking of events.
- <strong style="color:green">Encryption</strong>: The bcrypt module is used to encrypt and decrypt passwords saved in the SQL database.

## Possible Future Improvements

The following are possible future improvements for the software:

- <strong style="color:green">Add more features</strong>: The current software is very basic. It would be more useful if it had more features, such as the ability to add and delete users based on permission/role, and the ability to change passwords.
- <strong style="color:green">Implement the Forgot Password link</strong>: A Forgot Password link could be implemented, which would allow users to reset their passwords by entering their email address. ()
- <strong style="color:green">Integrate with a separate software</strong>: It would be more useful if this software could be linked to a bigger software, such as Sales Tracking.


## Conclusion

This software is a small but powerful Python project that can be used for a variety of purposes related to logging on a database. It is well-designed and secure, and it has the potential to be even more useful with future improvements.

## Additional Information

The following additional information is provided for developers who are interested in learning more about the software:

- The software is open source and can be found on [GitHub](https://github.com/DDuran19/login_system).
- The software is licensed under the MIT License.
- The software is currently in development and is not yet complete.

## Notes from creator
* as of writing, User class has 2 subclass.
    - New user - Not yet implemented. Will be used in passing the details to queries.py to be saved on database
    - Logged in User - Implemented. Used as a Singleton will be referenced all throughout the app
* Docstrings are added to easily understand each function/class, although it might need some tweaking to standardize the format
* there are errors showing on the terminal upon using the OK button which has the command of closing the current window using CTk.CTk.destroy() method. 
    - <strong>ERROR SAMPLE:</strong> 
    ```invalid command name "2586856708096update"
    while executing
    "2586856708096update"
    ("after" script)
    invalid command name "2586807241920check_dpi_scaling"
    while executing
    "2586807241920check_dpi_scaling"
    ("after" script)
    invalid command name "2586871033600_click_animation"
    while executing
    "2586871033600_click_animation"
    ("after" script)
    ```
* There is a code found at the top of all modules. The purpose this is to automatically append the absolute dparent directory to resolve import issues when  not running on main.py. I found this useful specially on the coding stage where I need to test and tweak codes


    This is removable (since the main.py will be the primary module that will be used to run the software). 
    ```
    if __name__ == "__main__":
        import os,sys

        this_file_directory=os.path.dirname(os.path.realpath(__file__))
        parent_directory = os.path.dirname(this_file_directory)
        sys.path.append(parent_directory)
    ```
* I used [BARD](https://bard.google.com/) to generate some base doc strings which I later edited to match the actual description of classes.

* For testing purposes, these are all the users saved on the database:

    | Username   | Password      | Email                       | Fullname        |
    |------------|---------------|-----------------------------|-----------------|
    | Admin      | adminpassword |Admin@admin.com              |Admin admin      |
    | JSmith1    | password1     | johnsmith1@example.com      | John Smith      |
    | SSmith1    | password1     | sarahsmith1@example.com     | Sarah Smith     |
    | MBrown1    | password1     | michaelbrown1@example.com   | Michael Brown   |
    | ODavis1    | password1     | oliviadavis1@example.com    | Olivia Davis    |
    | AAnderson1 | password2     | danielanderson1@example.com | Daniel Anderson |
    | OMartinez1 | password2     | oliviamartinez1@example.com | Olivia Martinez |
    | MTaylor1   | password2     | matthewtaylor1@example.com  | Matthew Taylor  |
    | SThomas1   | password2     | sophiathomas1@example.com   | Sophia Thomas   |
    | NAdams1    | password3     | NULL                        | NULL            |
    | RClark1    | password3     | NULL                        | NULL            |

