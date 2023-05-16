if __name__ == "__main__":
    import os,sys

    this_file_directory=os.path.dirname(os.path.realpath(__file__))
    sys.path.append(os.path.dirname(this_file_directory))

import customtkinter as CTk
import logging


from dataclasses import dataclass
from typing import Optional
from utils.GUI_helpers import extract_geometry

def setup_logging():
    logger = logging.getLogger("app_errors")
    logger.setLevel(logging.ERROR)
    
    file_handler = logging.FileHandler("errors.log")
    file_handler.setLevel(logging.ERROR)
    
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    
    return logger

logger = setup_logging()


class CustomException(Exception):
    details=''
    def __init__(self, details,*args: object,**kwargs) -> None:
        super().__init__(*args)
        self.details = details
        
    def _show(self):
        logger.exception(f"{self.__class__.__name__} Details: {self.details}. Message sent to user: {self.message}." )
        ErrorDialogueBox(Error=self).show_window()

class Invalid_characters(CustomException):
    """
    Indicates that there are some possible malicious strings that has been entered on Query_factory
    """
   
    def __init__(self, *args: object,**kwargs) -> None:
        super().__init__(*args,**kwargs)
        self.message = 'Please avoid using the following characters in your input: ";" "--" "null" "drop" "=" "*" "delete" "where" "join" "from" "update" "insert" "select". These characters are prohibited for security reasons.'
        self._show()

class User_not_found(CustomException):
    """
    Indicates that given username was not found on database
    """
    def __init__(self, *args: object,**kwargs) -> None:
        super().__init__(*args,**kwargs)
        self.message = "Username not found."
        self._show()

class Empty_fields(CustomException):
    """
    Indicates that the fields are blank
    """
    def __init__(self, *args: object,**kwargs) -> None:
        super().__init__(*args,**kwargs)
        self.message = "Username and Password are required."
        self._show()

class Password_did_not_matched(CustomException):
    """
    Indicates that given password did not match password on database
    """
    def __init__(self, *args: object,**kwargs) -> None:
        super().__init__(*args,**kwargs)
        self.message = "Passwords do not match!"
        self._show()

def _sanitize(input: any) -> str:
    """
    Sanitizes an input value to prevent SQL injection attacks.

    Args:
    input: The input value to sanitize.

    Returns:
    The sanitized string.

    Raises:
    ValueError: If the input string contains any prohibited characters.

    """
    prohibited_characters={
        ";",
        "--",
        "null",
        "drop",
        "=",
        "*",
        "delete",
        "where",
        "join",
        "from",
        "update",
        "insert",
        "select",
        }
    for character in prohibited_characters:
        if character in str(input).lower():
            raise Invalid_characters (details=f'Invalid Character found: "{character}" in "{input}"')
    return str(input)


class ErrorDialogueBox:
    Error: Exception
    parent_widget: Optional[any] = None
    WIDTH: int = 450
    HEIGHT: int = 200
    Window: CTk.CTk | None = None
    _default_geometry: str = f'{WIDTH}x{HEIGHT}'
    def __init__(self,Error: Exception,*args,**kwargs):
        self.Error = Error
        self.Window= None
        self.Window = CTk.CTk()
    def show_window(self):
              
        self._default_geometry=extract_geometry(self.Window,self.WIDTH, self.HEIGHT)    
        self.Window.title(self.Error.__class__.__name__)
        self.Window.geometry(self._default_geometry)
        self.Window.grid_columnconfigure(0,weight=1)
        self.Window.wm_attributes("-topmost", True)
        

        message = f"{str(self.Error.message)}"
        error_name_label = CTk.CTkLabel(self.Window, text=f"{self.Error.__class__.__name__}", font=("Helvetica-Bold", 20), wraplength= 200)
        error_name_label.grid(row=0, column = 0, padx=10, pady = (25,0), sticky="we")
        
        error_message = CTk.CTkLabel(self.Window,text=message, font=("Helvetica", 14),wraplength= 400)
        error_message.grid(row=1, column = 0, padx=10, pady = (10,25), sticky="we")

        OK_button = CTk.CTkButton(self.Window,text="OK", command= lambda: self.close(self.Window))
        OK_button.grid(row=2,column=0,padx=70,pady=(10,10),sticky="we")

        self.Window.mainloop()
    def close(self, window_to_close:CTk.CTk):
        window_to_close.destroy()
        

if __name__ == "__main__":
    _sanitize('--')