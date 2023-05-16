from Login_system.Login_GUI import Login_screen
from Login_system.Identification_card_gui import IdentificationCardGUI



if __name__ == "__main__":

    LOGGED_USER = Login_screen()
    LOGGED_USER.start_login()
    IdentificationCardGUI(LOGGED_USER._logged_user)
