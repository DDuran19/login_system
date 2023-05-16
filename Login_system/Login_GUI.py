if __name__ == "__main__":
    import os,sys

    this_file_directory=os.path.dirname(os.path.realpath(__file__))
    parent_directory = os.path.dirname(this_file_directory)
    sys.path.append(parent_directory)

import customtkinter as CTk


from dataclasses import dataclass
from typing import Optional

from utils.Error_handler import Empty_fields
from Login_system.Login_handler import Login

@dataclass
class Login_screen:
    Login_window = CTk.CTk()

    # App Details
    TITLE = "Brewing in a Bike - Login"
    WIDTH = 300
    HEIGHT= 400
    APPEARANCE_MODE = "dark"
    SHOW_PASSWORD = False


    # Helper global variables
    LEFT_CLICK = "<Button-1>"
    MIDDLE_CLICK = "<Button-2>"
    RIGHT_CLICK = "<Button-3>"
    LOGIN_IS_SUCCESSFUL = False

    _logged_user: Optional[Login] = None

    def __repr__(self):
        return self._logged_user

    def __str__(self):
        return self._logged_user.__str__()


    def setup(self):
        self.Login_window.title(self.TITLE)
        self.Login_window.geometry(self.get_center_of_screen())
        self.Login_window.minsize(self.WIDTH,self.HEIGHT)
        self.Login_window.maxsize(self.WIDTH,self.HEIGHT)
        CTk.set_appearance_mode(self.APPEARANCE_MODE)
        
        self.Login_window.grid_columnconfigure(0,weight=1)
    
        self.add_widgets()

    def add_widgets(self):
        # Creating widgets
        self.username_field = CTk.CTkEntry(
            self.Login_window,
            height=25,
            corner_radius=10,
            placeholder_text="username",
            justify=CTk.CENTER)
        
        self.password_field = CTk.CTkEntry(
            self.Login_window,
            height=25,
            corner_radius=10,
            placeholder_text="password",
            show="*",
            justify=CTk.CENTER)
        
        self.show_hide_password = CTk.CTkSwitch(
            self.Login_window, 
            corner_radius=15,
            text="Show password",
            text_color="Gray",
            command=self.toggle_password)
        
        self.login_button = CTk.CTkButton(
            self.Login_window, 
            corner_radius=15,
            text = "Login"
            )

        self.forgot_password_label = CTk.CTkLabel(
            self.Login_window,
            text="Forgot Password?",)
        
        # Binding widget to backend functions
        self.login_button.bind(self.LEFT_CLICK, command=self.login)
        self.forgot_password_label.bind(self.LEFT_CLICK,command=self.forgot_password)


        # Positions in GRID
        self.username_field.grid(row=0,column=0,padx = 40, pady=(80,5),sticky="we")
        self.password_field.grid(row=1,column=0,padx = 40, pady=(0,5),sticky="we")
        self.show_hide_password.grid(row=2,column=0,padx = 80, pady=(0,10),sticky="we")
        self.login_button.grid(row=3,column=0,padx = 40, pady=(120,5),sticky="we")
        self.forgot_password_label.grid(row=4,column=0,padx = 20, pady=(0,10),sticky="we")

    # Helper functions

    def toggle_password(self):
        if self.SHOW_PASSWORD:
            self.password_field.configure(show="*")
            self.show_hide_password.configure(text="Show password")
            self.SHOW_PASSWORD = False
        else:
            self.password_field.configure(show="")
            self.show_hide_password.configure(text="Hide password")
            self.SHOW_PASSWORD = True
          
    def get_center_of_screen(self,window = None, width = None,height = None,X_OFFSET=0,Y_OFFSET=-100) -> str:

        if window is None: 
            window = self.Login_window
        
        if width is None:
            width = self.WIDTH

        if height is None:
            height=self.HEIGHT

        self.screen_width = window.winfo_screenwidth()//2
        self.screen_height = window.winfo_screenheight()//2
        x = (self.screen_width - (self.WIDTH // 2)) + X_OFFSET
        y = (self.screen_height - (self.HEIGHT // 2)) + Y_OFFSET

        return f'{width}x{height}+{x}+{y}'

    def start_login(self):
        self.setup()
        self.Login_window.mainloop()
        

    # Functions that connects to Backend

    def login(self, event=None):
        self.username = self.username_field.get()
        password = self.password_field.get()

        self._input_validator(self.username,password)
        self._logged_user=Login(username=self.username,password_attempt=password).login()
        self.LOGIN_IS_SUCCESSFUL = True
        self.Login_window.destroy()
        
    def _input_validator(self, *args):
        if any([arg == '' for arg in args]): raise Empty_fields(self.Login_window)

    def forgot_password(self,event=None):
        
        print('I forgotten my password')


if __name__ == "__main__":
    Login_screen().start_login()