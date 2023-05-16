if __name__ == "__main__":
    import os,sys

    this_file_directory=os.path.dirname(os.path.realpath(__file__))
    parent_directory = os.path.dirname(this_file_directory)
    sys.path.append(parent_directory)

import customtkinter as CTk

class IdentificationCardGUI:
    """
    This class creates a GUI for displaying a user's identification card.

    Takes one argument, logged_in_user a Logged_in_user Object (Login_system\User.py)
    
    """
    def __init__(self, logged_in_user):
        self.logged_in_user = logged_in_user

        self.create_window()
        self.setup_title()
        self.use_dark_theme()
        self.position_in_center_of_screen()
        self.place_user_initials_on_top()
        self.place_fullname()
        self.place_role()
        self.place_username()
        self.place_email()

        self.root.mainloop()

    def create_window(self):
        self.root = CTk.CTk()
        self.window_width = 300
        self.window_height = 400

    def setup_title(self):
        self.root.title("User Identification Card")

    def use_dark_theme(self):
        CTk.set_appearance_mode("dark")

    def position_in_center_of_screen(self):
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        x = (self.screen_width - self.window_width) // 2
        y = (self.screen_height - self.window_height) // 2
        self.root.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")

    def place_user_initials_on_top(self):
        lastname = self.logged_in_user.fullname.split()[-1]
        initials = self.logged_in_user.fullname[0].upper()+lastname[0].upper()

        self.logo_label = CTk.CTkLabel(self.root, text=initials, font=('Arial', 50),fg_color="black")
        self.logo_label.place(relx=0.5, rely=0.15, anchor=CTk.CENTER)
        self.logo_label.configure( bg_color = "white",width=200)
    
    def place_fullname(self):
        fullname_label = CTk.CTkLabel(self.root, text=self.logged_in_user.fullname.upper(), font=('Arial', 18, 'bold'))
        fullname_label.place(relx=0.5, rely=0.45, anchor=CTk.CENTER)

    def place_role(self):
        role_label = CTk.CTkLabel(self.root, text=self.logged_in_user.role, font=('Arial', 12))
        role_label.place(relx=0.5, rely=0.5, anchor=CTk.CENTER)
    
    def place_username(self):
        username_label = CTk.CTkLabel(self.root, text="Username: " + self.logged_in_user.username, font=('Arial', 12))
        username_label.place(relx=0.5, rely=0.55, anchor=CTk.CENTER)
    
    def place_email(self):
        email_label = CTk.CTkLabel(self.root, text="Email: " + self.logged_in_user.email, font=('Arial', 12))
        email_label.place(relx=0.5, rely=0.65, anchor=CTk.CENTER)