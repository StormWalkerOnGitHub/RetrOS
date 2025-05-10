print("Retros.home")

from tkinter import *

def perc2float(percentage:int|float,max_value:float|int=100)-> float:
    """Returns a given percentage of a number as a decimal value"""

    if not isinstance(percentage,(int,float,)):
        raise TypeError(f"Please ensure percentage is of type int OR float, not {type(percentage)}")
    elif not isinstance(max_value,(int,float,)):
        raise TypeError(f"Please ensure max_value is of type int OR float, not {type(max_value)}")

    return (percentage/100)*max_value
def theme(mode:str="light",attr:str="fg")-> str:
    """Returns the value based on the provided mode (theme) and attribute

    ---

    Valid inputs for each argument includes the following:

    MODE: Light/Dark\n
    ATTR: FG, BG, Primary, Secondary, Accent
    """

    dark_theme:dict={
        "fg":"#FAF7EB", # Floral White
        "bg":"#28300D", # Drab Dark Brown
        "primary":"#BC9C29", # Satin Sheen Gold
        "secondary":"#820DA5", # Mauveine
        "accent":"#A2B74E" # Apple Green
        }
    light_theme:dict={
        "fg":"#141105", # Smokey Black
        "bg":"#EAF2CF", # Light Yellow
        "primary":"#D6B643", # Old Gold
        "secondary":"#CE5AF2", # HelioTrope
        "accent":"#9CB148" # Apple Green
        }

    attr_err_msg:str= f"ATTR: \"{attr}\" could not be found. Please try a valid entry"
    mode_err_msg:str= f"MODE: \"{mode}\" could not be found. Try \"light\"/\"dark\""

    # Attempts to find the value using mode and attr inputs
    # Will return ValueError if value could not be found for either
    match mode.lower().strip():
        case "light":
            return light_theme.get(
                attr.lower().strip(),
                ValueError(attr_err_msg)
                )
        case "dark":
            return dark_theme.get(
                attr.lower().strip(),
                ValueError(attr_err_msg)
                )
        case _: raise ValueError(mode_err_msg)

class RetrosHome:

    def __init__(self):
        self.theme="dark"   # light/dark mode
        border_width:int|float= 0.003# local value to provide as default
        self.bulk_widgets:dict= {# widget configurations reference chart}
            # All scales are percentages from 0-1
            "gamelist_frame":{
                "width":0.15,
                "left_offset":0,
                "height":0.9,
                "top_offset":0,
                "fg":"Black",
                "bg":"Blue",
                "border":{
                    "top":border_width,
                    "bottom":border_width/2,
                    "left":border_width,
                    "right":border_width/2,
                    },
                },
            "gamebanner_frame":{
                "width":0.85,
                "left_offset":0.15,
                "height":0.2,
                "top_offset":0,
                "fg":"Black",
                "bg":"LimeGreen",
                "border":{
                    "top":border_width,
                    "bottom":border_width/2,
                    "left":border_width/2,
                    "right":border_width,
                    },
                },
            "gameinfo_frame":{
                "width":0.6,
                "left_offset":0.15,
                "height":0.7,
                "top_offset":0.2,
                "fg":"Black",
                "bg":"Yellow",
                "border":{
                    "top":border_width/2,
                    "bottom":border_width/2,
                    "left":border_width/2,
                    "right":border_width/2,
                    },
                },
            "gamemngr_frame":{
                "width":0.25,
                "left_offset":0.75,
                "height":0.7,
                "top_offset":0.2,
                "fg":"Black",
                "bg":"Red",
                "border":{
                    "top":border_width/2,
                    "bottom":border_width/2,
                    "left":border_width/2,
                    "right":border_width,
                    },
                },
            "appmngr_frame":{
                "width":1.0,
                "left_offset":0,
                "height":0.1,
                "top_offset":0.9,
                "fg":"Black",
                "bg":"Purple",
                "border":{
                    "top":border_width/2,
                    "bottom":border_width,
                    "left":border_width,
                    "right":border_width,
                    },
                },
        }
        self.games_dir:str="./Games"

        # Initialize window and configure display settings
        self.tk = Tk()
        self.tk.title("RetrOS")
        self.tk.config(bg=theme(self.theme,"bg"))
        self.tk.attributes('-zoomed', True)  # This just maximizes it so we can see the window. It's nothing to do with fullscreen.

        # Fullscreen handler
        self.state = False # Assumes window defaulted to maximized mode
        self.tk.bind("<F11>", self.toggle_fullscreen)
        self.tk.bind("<Escape>", self.end_fullscreen)

        # Add Elements to the window
        #region Initiate Frame
        self.frame = Frame( # Placement manager
            self.tk, # Parent frame belongs to
            name="frame",
            width=self.tk.winfo_screenwidth(), # Sets width of the frame
            height=self.tk.winfo_screenheight() # Sets height of the frame
            )
        self.frame.pack() # Add changes to the window
        self.tk.update_idletasks() # Ensure information is updated after scaling window

        self.bg = Label( # Background override
            self.frame, # Parent label belongs to
            name="bg",
            text="",
            width=0, # Offset from left to right
            height=0, # Offset from top to bottom
            fg=theme(self.theme,"fg"),
            bg=theme(self.theme,"bg"))
        self.gamelist_frame= Frame(# Stores list of owned games)
            self.frame,
            name="gamelist_frame",
            bg=self.bulk_widgets["gamelist_frame"]["bg"],
            )
        self.gamebanner_frame= Frame(# Stores imagery for selected game)
            self.frame,
            name="gamebanner_frame",
            bg=self.bulk_widgets["gamebanner_frame"]["bg"],
            )
        self.gameinfo_frame= Frame(# Stores information for selected game)
            self.frame,
            name="gameinfo_frame",
            bg=self.bulk_widgets["gameinfo_frame"]["bg"],
            )
        self.gamemngr_frame= Frame(# Stores game options for selected game)
            self.frame,
            name="gamemngr_frame",
            bg=self.bulk_widgets["gamemngr_frame"]["bg"],
            )
        self.appmngr_frame= Frame(# Stores options relating to the game library and the app
            self.frame,
            name="appmngr_frame",
            bg=self.bulk_widgets["appmngr_frame"]["bg"],
            )

        self.games_listbox= Listbox(
            self.gamelist_frame,
            selectmode="single",
            bg= "blue",
            fg= "black",
            relief="solid",
            bd=0, # disables the relief border
            highlightthickness=0, # disables the listbox border
            )

        self.bg.place(# Cover entire window)
            relwidth= 1.0,
            relheight=1.0,
            relx=0,
            rely=0
            )
        self.place_frame(self.gamelist_frame, self.bulk_widgets)
        self.place_frame(self.gamebanner_frame, self.bulk_widgets)
        self.place_frame(self.gameinfo_frame, self.bulk_widgets)
        self.place_frame(self.gamemngr_frame, self.bulk_widgets)
        self.place_frame(self.appmngr_frame, self.bulk_widgets)

        self.games_listbox.place(
            relwidth=0.95,
            relheight=1,
            relx=0.025,
            rely=0,
            )
        for i in range(100):
            self.games_listbox.insert(0, i)

        self.toggle_fullscreen() # Open into fullscreen mode

    def toggle_fullscreen(self, event=None):
        self.state = not self.state  # Just toggling the boolean
        self.tk.attributes("-fullscreen", self.state)
        self.tk.update()
        self.tk.update_idletasks()
        return "break"
    def end_fullscreen(self, event=None):
        self.state = False
        self.tk.attributes("-fullscreen", False)
        self.tk.update()
        self.tk.update_idletasks()
        return "break"

    def place_frame(self, widget, reference_chart:dict)-> list[tuple[int]]:
        """Ensures borders are properly calculated for a given frame when placed"""
        widget_name= widget.winfo_name()

        widget_width= reference_chart[widget_name]["width"]
        widget_height= reference_chart[widget_name]["height"]
        widget_offsetx= reference_chart[widget_name]["left_offset"]
        widget_offsety= reference_chart[widget_name]["top_offset"]

        widget_border= reference_chart[widget_name]["border"]

        widget.place(
            relwidth= widget_width-(widget_border["left"]+widget_border["right"]),
            relheight= widget_height-(widget_border["top"]+widget_border["bottom"]),
            relx= widget_offsetx+widget_border["left"],
            rely= widget_offsety+widget_border["top"],
        )

if __name__ == '__main__':
    w = RetrosHome()
    w.tk.mainloop()
