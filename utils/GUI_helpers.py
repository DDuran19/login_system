if __name__ == "__main__":
    import os,sys

    this_file_directory=os.path.dirname(os.path.realpath(__file__))
    sys.path.append(os.path.dirname(this_file_directory))

import customtkinter as CTk


from typing import Optional


def classmethods(cls):
    for name, value in vars(cls).items():
        if callable(value):
            setattr(cls, name, classmethod(value))
    return cls

"""
@dataclass
class get_center_of_screen:
    window: CTk.CTk | CTk.CTkToplevel
    WIDTH: int | float
    HEIGHT: int | float
    @classmethod
    def geometry_string(self,window = None, width = None,height = None,X_OFFSET=0,Y_OFFSET=-100) -> str:

        if window is None: 
            window = self.window
        
        if width is None:
            width = self.WIDTH

        if height is None:
            height=self.HEIGHT

        self.screen_width = self.window.winfo_screenwidth()//2
        self.screen_height = self.window.winfo_screenheight()//2
        x = (self.screen_width - (self.WIDTH // 2)) + X_OFFSET
        y = (self.screen_height - (self.HEIGHT // 2)) + Y_OFFSET

        return f'{width}x{height}+{x}+{y}'
    """

def extract_geometry(window: Optional[CTk.CTk] = None, width: int = 450,height: int = 120,X_OFFSET=0,Y_OFFSET=-100) -> str:
    
    screen_width = window.winfo_screenwidth()//2
    screen_height = window.winfo_screenheight()//2

    x = (screen_width - (width // 2)) + X_OFFSET
    y = (screen_height - (height // 2)) + Y_OFFSET

    return f'{width}x{height}+{x}+{y}'
