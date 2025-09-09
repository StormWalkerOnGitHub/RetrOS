"""Displays the home page of the application"""

print("Retros.home")

from typing import Literal
from tkinter import *
from tkinter.font import Font

# Used to as a default value for current game selection
# Not intended for appearance on UI
blacklisted_str:str="«¦·§·¦»"
blacklisted_game:dict={
    "Emulator": "",
    "Enabled": False,
    "Alias": blacklisted_str,
    "Description": "",
    "Icon_Location": "",
    "Banner_Location": "",
    "Game_Location": "",
    "Save_location": "",
    "Game_Type": "",
    "Save_Type": "",
    "Args": [],
    "Manual_Start_Cmd": "",
    "Release_Dates": {"USA":"January 1st, 2000",},
    "Popularity": "10/10",
    "Genres": [],
    "Languages": ["English",],
    "Developer": [],
    "Publishers": [],
    "Players": "1",
    "Connectivity": "",
    "Series": "",
    "Rating": {"ESRB":"E",},
    "Ext_Link": "",
    }

def perc2float(percentage:int|float,max_value:float|int=100)-> float:
    """Returns a given percentage of a number as a decimal value"""

    if not isinstance(percentage,(int,float,)):
        raise TypeError(f"Please ensure percentage is of type int OR float, not {type(percentage)}")
    elif not isinstance(max_value,(int,float,)):
        raise TypeError(f"Please ensure max_value is of type int OR float, not {type(max_value)}")

    return (percentage/100)*max_value
def minMax_values(
    current:int|float,
    minimum:int|float=0,
    maximum:int|float=1
    )-> int|float:
    """
    ### Returns a validated value within the provided range

    This function is for data validation only,
    it does not serve as an alternative to the builtin "range(start, stop[, step])" function

    ---

    Will return TypeError if any of the inputs are not the correct type

    Will return ValueError if minimum value is greater than the maximum value

    Will default to False if overflow input could not be understood
    """
    #region sterilize inputs and place guard clauses
    if any({# inputs are incorrect type}):
        not isinstance(current,(int,float)),
        not isinstance(minimum,(int,float)),
        not isinstance(maximum,(int,float)),
        }):
        return TypeError("Please ensure all inputs are of the correct type before parsing")
    if maximum < minimum:
        return ValueError("Please make sure your minimum value is SMALLER than your maximum value")

    if isinstance(minimum, int):# convert to float
        minimum= float(minimum)
    if isinstance(maximum, int):# convert to float
        maximum= float(maximum)
    if isinstance(current, int):# convert to float
        current= float(current)
    #endregion sterilize inputs and place guard clauses
    clean_to_float= lambda value: int(value) if str(value).endswith(".0") else value
    #region quick return if valid entry
    if minimum<current<maximum:
        return clean_to_float(current)
    elif current<=minimum:
        return clean_to_float(minimum)
    elif maximum<=current:
        return clean_to_float(maximum)
    #endregion quick return if valid entry
def clean_simple_dict_to_str(table:dict,sep:str="\n",start="",end="")-> str:
    """Takes a shallow dictionary and converts it to a string"""
    _temp:str=start
    for key,value in table.items():
        if key=="":
            key='""'
        if value=="":
            value='""'
        _temp+= f"{key}: {value}{sep}"
    return f"{_temp.removesuffix(sep)}{end}"
def clean_list_to_str(values:list|str,sep:str=", ",start="",end="")-> str:
    """Takes a shallow dictionary and converts it to a string"""
    if isinstance(values,str):
        return values
    _temp:str=start
    values:set= set(values)
    for index in values:
        if index=="" and not '""' in values:
            index='""'
        _temp+= f"{index}{sep}"
    return f"{_temp.removesuffix(sep)}{end}"
def depth_first_search(data:dict, target:list|str, sep:str=",", new_value=None, default={}):
    """
    Performs a depth-first search on a nested dictionary/list structure to find a target value.

    Args:\n
        data: The dictionary or list to search.\n
        target: The values to search for at varying depth.\n
        sep: The value used to split the target is parsed as a string.\n
        new_value: The value to write to data.\n
        default: The return value if nothing was found in the data using the provided target.\n

    ---

    ## Returns:

    Value if found, else returns default.
    """

    #region verify data input
    if len(data)==0:# no data passed
        raise ValueError("Please ensure your data entry is not empty")
    elif not isinstance(data, dict):
        raise TypeError("Please ensure your data is passed as a dictionary type")
    #endregion verify data input
    #region check arg types
    if not isinstance(sep,str) and isinstance(target,str):
        raise TypeError("Please ensure your seperator is a string format")
    if not new_value is None:
        match fr"{new_value}".strip():
            case r""|r"()"|r"{}"|r"[]"|r"<>":
                new_value=None
    #endregion check arg types
    #region Clean target input
    if isinstance(target, str):# convert to list
        target:list=target.split(sep)
    if not isinstance(target,list):
        raise TypeError("Please ensure target search is a list")
    cleaned_target:list= []
    for node in target:# remove unwanted inputs
        if f"{node}".strip()=="":
            continue
        cleaned_target.append(node)
    del target
    if cleaned_target==[]:# raise issue if unable to retain a value
        raise ValueError("Please ensure target is a valid search entry")
    #endregion Clean target input
    
    #print(data)
    #print(cleaned_target)

    for key in cleaned_target[:-1]:
        data = data.setdefault(key, default)
    if new_value is not None and f"{new_value}".strip()!="":
        data[cleaned_target[-1]] = new_value
    
    return data[cleaned_target[-1]]

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
        """Localized Game Hub"""

        #region "Global" variables
        self.app_name:str= "RetrOS"
        self.theme="dark"   # light/dark mode
        self.opp_theme= lambda: "light" if self.theme=="dark" else "dark"
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
        self.owned_games:dict= {}
        self.__selected_game:dict=blacklisted_game
        self.tk = Tk(className=self.app_name)
        self.selected_font = Font(family="Arial", size=12)
        self.tk.minsize(width=770,height=460)
        #endregion "Global" variables

        #region Prep window
        window_geometry:str= f"WINDOW:\t{self.tk.winfo_screenwidth()}x{self.tk.winfo_screenheight()}"
        # Initialize window and configure display settings
        self.tk.title(self.app_name)
        self.tk.config(bg=theme(self.theme,"bg"))
        self.tk.attributes('-zoomed', True)  # This just maximizes it so we can see the window. It's nothing to do with fullscreen.

        # Fullscreen handler
        self.state = False # Assumes window defaulted to maximized mode
        self.tk.bind("<F11>", self.toggle_fullscreen)
        self.tk.bind("<Escape>", self.end_fullscreen)
        #endregion Prep window

        #region Add objects to window
        # Add Elements to the window
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
            bg=theme(self.theme,"bg"),
            )
        self.games_listbox= Listbox(
            self.gamelist_frame,
            name="games_listbox",
            selectmode="single",
            activestyle="none",
            fg=theme(self.theme,"fg"),
            bg=theme(self.theme,"bg"),
            relief="solid",
            bd=0, # disables the relief border
            highlightthickness=0, # disables the listbox border
            font=self.selected_font,
            )

        self.gamebanner_frame= Frame(# Stores imagery for selected game)
            self.frame,
            name="gamebanner_frame",
            bg=theme(self.theme,"Accent"),
            )

        self.gameinfo_frame= Frame(# Stores information for selected game)
            self.frame,
            name="gameinfo_frame",
            bg=theme(self.theme,"Primary"),
            )
        self.gameinfo_noticeLabel= Label(
            self.gameinfo_frame,
            name="gameinfo_noticeLabel",
            text= "No Games Detected",
            bg= theme(self.theme,"Primary"),
            fg= theme(self.opp_theme(),"fg"),
            justify= "center",
            font=self.selected_font,
        )
        self.gameinfo_Description= Label(
            self.gameinfo_frame,
            name="gameinfo_Description",
            text= "",
            bg= theme(self.theme,"Primary"),
            fg= theme(self.opp_theme(),"fg"),
            justify= "left",
            font=self.selected_font,
        )
        self.gameinfo_Series= Label(
            self.gameinfo_frame,
            name="gameinfo_Series",
            text= "",
            bg= theme(self.theme,"Primary"),
            fg= theme(self.opp_theme(),"fg"),
            justify= "left",
            font=self.selected_font,
        )
        self.gameinfo_Genres= Label(
            self.gameinfo_frame,
            name="gameinfo_Genres",
            text= "",
            bg= theme(self.theme,"Primary"),
            fg= theme(self.opp_theme(),"fg"),
            justify= "left",
            font=self.selected_font,
        )
        self.gameinfo_Languages= Label(
            self.gameinfo_frame,
            name="gameinfo_Languages",
            text= "",
            bg= theme(self.theme,"Primary"),
            fg= theme(self.opp_theme(),"fg"),
            justify= "left",
            font=self.selected_font,
        )
        self.gameinfo_Players= Label(
            self.gameinfo_frame,
            name="gameinfo_Players",
            text= "",
            bg= theme(self.theme,"Primary"),
            fg= theme(self.opp_theme(),"fg"),
            justify= "left",
            font=self.selected_font,
        )
        self.gameinfo_Popularity= Label(
            self.gameinfo_frame,
            name="gameinfo_Popularity",
            text= "",
            bg= theme(self.theme,"Primary"),
            fg= theme(self.opp_theme(),"fg"),
            justify= "left",
            font=self.selected_font,
        )
        self.gameinfo_Rating= Label(
            self.gameinfo_frame,
            name="gameinfo_Rating",
            text= "",
            bg= theme(self.theme,"Primary"),
            fg= theme(self.opp_theme(),"fg"),
            justify= "left",
            font=self.selected_font,
        )
        self.gameinfo_Connectivity= Label(
            self.gameinfo_frame,
            name="gameinfo_Connectivity",
            text= "",
            bg= theme(self.theme,"Primary"),
            fg= theme(self.opp_theme(),"fg"),
            justify= "left",
            font=self.selected_font,
        )
        self.gameinfo_Release_Dates= Label(
            self.gameinfo_frame,
            name="gameinfo_Release_Dates",
            text= "",
            bg= theme(self.theme,"Primary"),
            fg= theme(self.opp_theme(),"fg"),
            justify= "left",
            font=self.selected_font,
        )
        self.gameinfo_Developer= Label(
            self.gameinfo_frame,
            name="gameinfo_Developer",
            text= "",
            bg= theme(self.theme,"Primary"),
            fg= theme(self.opp_theme(),"fg"),
            justify= "left",
            font=self.selected_font,
        )
        self.gameinfo_Publishers= Label(
            self.gameinfo_frame,
            name="gameinfo_Publishers",
            text= "",
            bg= theme(self.theme,"Primary"),
            fg= theme(self.opp_theme(),"fg"),
            justify= "left",
            font=self.selected_font,
        )
        self.gameinfo_Ext_Link= Label(
            self.gameinfo_frame,
            name="gameinfo_Ext_Link",
            text= "",
            bg= theme(self.theme,"Primary"),
            fg= theme(self.opp_theme(),"fg"),
            justify= "left",
            font=self.selected_font,
        )

        self.gamemngr_frame= Frame(# Stores game options for selected game)
            self.frame,
            name="gamemngr_frame",
            bg=self.bulk_widgets["gamemngr_frame"]["bg"],
            )
        self.start_game_btn = Button(
            self.gamemngr_frame,
            name="start_game_btn",
            text="Select A Game First",
            font=self.selected_font,
            command=self.start_game_onClick,
            state="disabled"
            )
        self.gamemngr_selgame_gamepath= Label(
            self.gamemngr_frame,
            name="gamemngr_selgame_path",
            text= f"Game Location: ",
            bg= "red",
            fg= "Black",
            justify= "left",
            font=self.selected_font,
            )
        self.gamemngr_selgame_savepath= Label(
            self.gamemngr_frame,
            name="gamemngr_selgame_savepath",
            text= f"Save Location: ",
            bg= "red",
            fg= "Black",
            justify= "left",
            font=self.selected_font,
            )
        self.gamemngr_selgame_gametype= Label(
            self.gamemngr_frame,
            name="gamemngr_selgame_gametype",
            text= f"Game Type: ",
            bg= "red",
            fg= "Black",
            justify= "left",
            font=self.selected_font,
            )
        self.gamemngr_selgame_savetype= Label(
            self.gamemngr_frame,
            name="gamemngr_selgame_savetype",
            text= f"Save Type: ",
            bg= "red",
            fg= "Black",
            justify= "left",
            font=self.selected_font,
            )
        self.gamemngr_selgame_args= Label(
            self.gamemngr_frame,
            name="gamemngr_selgame_args",
            text= f"Args: ",
            bg= "red",
            fg= "Black",
            justify= "left",
            font=self.selected_font,
            )
        self.gamemngr_selgame_cmd= Label(
            self.gamemngr_frame,
            name="gamemngr_selgame_cmd",
            text= f"Manual Command: ",
            bg= "red",
            fg= "Black",
            justify= "left",
            font=self.selected_font,
            )
        self.gamemngr_divider= Label(
            self.gamemngr_frame,
            name="gamemngr_divider",
            text= "",
            bg= "black",
            fg= "Black",
            )
        self.gamemngr_selgame_cursave= Label(
            self.gamemngr_frame,
            name="gamemngr_selgame_cursave",
            text= f"Current Save: ",
            bg= "red",
            fg= "Black",
            justify= "left",
            font=self.selected_font,
            )
        self.gamemngr_selgame_bckpsave1= Label(
            self.gamemngr_frame,
            name="gamemngr_selgame_bckpsave1",
            text= f"Backup Save (1): ",
            bg= "red",
            fg= "Black",
            justify= "left",
            font=self.selected_font,
            )
        self.gamemngr_selgame_bckpsave2= Label(
            self.gamemngr_frame,
            name="gamemngr_selgame_bckpsave2",
            text= f"Backup Save (2): ",
            bg= "red",
            fg= "Black",
            justify= "left",
            font=self.selected_font,
            )
        self.gamemngr_selgame_bckpsave3= Label(
            self.gamemngr_frame,
            name="gamemngr_selgame_bckpsave3",
            text= f"Backup Save (3): ",
            bg= "red",
            fg= "Black",
            justify= "left",
            font=self.selected_font,
            )
        self.gamemngr_selgame_bckpsave4= Label(
            self.gamemngr_frame,
            name="gamemngr_selgame_bckpsave4",
            text= f"Backup Save (4): ",
            bg= "red",
            fg= "Black",
            justify= "left",
            font=self.selected_font,
            )
        self.gamemngr_selgame_bckpsave5= Label(
            self.gamemngr_frame,
            name="gamemngr_selgame_bckpsave5",
            text= f"Backup Save (5): ",
            bg= "red",
            fg= "Black",
            justify= "left",
            font=self.selected_font,
            )
        self.gamemngr_selgame_bckpsave6= Label(
            self.gamemngr_frame,
            name="gamemngr_selgame_bckpsave6",
            text= f"Backup Save (6): ",
            bg= "red",
            fg= "Black",
            justify= "left",
            font=self.selected_font,
            )
        self.gamemngr_selgame_bckpsave7= Label(
            self.gamemngr_frame,
            name="gamemngr_selgame_bckpsave7",
            text= f"Backup Save (7): ",
            bg= "red",
            fg= "Black",
            justify= "left",
            font=self.selected_font,
            )

        self.appmngr_frame= Frame(# Stores options relating to the game library and the app
            self.frame,
            name="appmngr_frame",
            bg=self.bulk_widgets["appmngr_frame"]["bg"],
            )
        self.appmngr_settings= Label(
            self.appmngr_frame,
            name="appmngr_settings",
            text= f"Settings: ",
            bg="grey",
            fg= "Black",
            justify= "left",
            font=self.selected_font,
            )
        self.appmngr_theme_btn = Button(
            self.appmngr_frame,
            name="appmngr_theme_btn",
            text=self.theme.capitalize(),
            font=self.selected_font,
            command=self.toggle_theme,
            state="normal"
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

        # Owned Games (Left)
        self.games_listbox.place(
            relwidth=0.975,
            relheight=1,
            relx=0.025,
            rely=0,
            )
        self.populate_gameList()
        # Selected Game Banner (Top)
        # Selected Game Information (Middle)
        self.gameinfo_noticeLabel.place(
            relwidth=1,
            relheight=1,
            relx=0,
            rely=0,
            )
        # Selected Game Management (Right)
        self.start_game_btn.place(
            relwidth= 0.95,
            relheight= 0.1,
            relx= 0.025,
            rely= 0.025,
            )
        # Selected App Management (Bottom)
        self.appmngr_settings.place(
            relwidth= 0.1,
            relheight= 0.5,
            relx= 0.01875,
            rely= 0.25,
            )
        self.appmngr_theme_btn.place(
            relwidth= 0.1,
            relheight= 0.5,
            relx= 0.88125,
            rely= 0.25,
            )
        #endregion Add objects to window

        print(self.get_all_widgets(self.frame, self.frame))
        self.toggle_fullscreen() # Open into fullscreen mode

    def get_all_widgets(self, parent, master):
        """
        Returns a list of all child widgets within the given parent widget.
        """
        def genMasterDict(root:str|dict, sep:str=None)-> dict:
            """Makes &/ Returns a master dictionary"""
            
            match type(root):
                case dict:
                    return root
            new_dict:dict={}
        print(genMasterDict({"help":"me"}))

        print(master)
        print(parent)
        root= f"{master}" if master==parent else f"{parent}"
        print(root)



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

    def toggle_theme(self)-> None:
        """
        Toggles the currently selected theme to the opposite

        Default is Dark mode
        """
        print(self.theme)
        match self.theme.lower().strip():
            case "light":
                self.theme="dark"
            case "dark":
                self.theme="light"
            case _:
                self.theme="dark"
        self.appmngr_theme_btn.configure(
            text=self.theme.capitalize(),
            bg="black" if self.theme=="light" else "white",
            fg="white" if self.theme=="light" else "black",
            )

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
    def populate_gameList(self)-> list:
        """Populates the list with games installed on the computer"""
        # Read through Games.conf
            # Check if added game has all required variables
            # Check if added game has "Enabled" to "True"
            # If Game is correctly setup,
                # Add to game library
            #
            # If Any portion of the check fails, return empty dict
        for i in range(100):
            self.games_listbox.insert(i,f"{i}")
            self.owned_games[f"{i}"]= {
                "Emulator": "PC",
                "Enabled": True,
                "Alias": f"{i}",
                "Description": f"This is the number {i}",
                "Icon_Location": "./Games",
                "Banner_Location": "./Games",
                "Game_Location": "./Games",
                "Save_location": "./Games",
                "Game_Type": ".nds",
                "Save_Type": ".sav",
                "Args": [],
                "Manual_Start_Cmd": "",
                "Release_Dates": {"USA":"January 1st, 2000",},
                "Popularity": "10/10",
                "Genres": ["Tools","Game Hub", "Alternative"],
                "Languages": ["English",],
                "Developer": "St0rmWalker",
                "Publishers": "N/A",
                "Players": "1",
                "Connectivity": "N/A",
                "Series": "St0rmLabs",
                "Rating": {"ESRB":"E",},
                "Ext_Link": "https://github.com/StormWalkerOnGitHub/RetrOS",
            }
        if self.owned_games!={}:
            self.gameinfo_noticeLabel.configure(
                text="Please Select A Game"
                )
        self.games_listbox.bind("<<ListboxSelect>>",self.selected_game)
    def selected_game(self, event)-> Literal[False]|dict:
        selected_value:str= self.games_listbox.get(self.games_listbox.curselection())

        if self.__selected_game["Alias"]!=selected_value \
            and selected_value!=blacklisted_game["Alias"]:
            game_selected:dict= self.owned_games[selected_value]

            # # Game Manager Content
            self.selected_gameFile:str= f"{selected_value}{self.owned_games[selected_value]["Game_Type"]}"
            self.selected_gameEmulator= self.owned_games[selected_value]["Emulator"]
            self.selected_gameGame_Location= self.owned_games[selected_value]["Game_Location"]
            self.selected_gameSave_location= self.owned_games[selected_value]["Save_location"]
            self.selected_gameGame_Type= self.owned_games[selected_value]["Game_Type"]
            self.selected_gameSave_Type= self.owned_games[selected_value]["Save_Type"]
            self.selected_gameArgs= self.owned_games[selected_value]["Args"]
            self.selected_gameManual_Start_Cmd= self.owned_games[selected_value]["Manual_Start_Cmd"]

            # # Banner Content
            self.selected_gameAlias= self.owned_games[selected_value]["Alias"]
            self.selected_gameIcon_Location= self.owned_games[selected_value]["Icon_Location"]
            self.selected_gameBanner_Location= self.owned_games[selected_value]["Banner_Location"]

            # # Game Info Content
            self.selected_gameDescription= self.owned_games[selected_value]["Description"]
            self.selected_gameSeries= self.owned_games[selected_value]["Series"]
            self.selected_gameGenres= self.owned_games[selected_value]["Genres"]
            self.selected_gameLanguages= self.owned_games[selected_value]["Languages"]
            self.selected_gamePlayers= self.owned_games[selected_value]["Players"]
            self.selected_gamePopularity= self.owned_games[selected_value]["Popularity"]
            self.selected_gameRating= self.owned_games[selected_value]["Rating"]
            self.selected_gameConnectivity= self.owned_games[selected_value]["Connectivity"]
            self.selected_gameRelease_Dates= self.owned_games[selected_value]["Release_Dates"]
            self.selected_gameDeveloper= self.owned_games[selected_value]["Developer"]
            self.selected_gamePublishers= self.owned_games[selected_value]["Publishers"]
            self.selected_gameExt_Link= self.owned_games[selected_value]["Ext_Link"]

            self.start_game_btn.configure(
                text= "Start",
                state= "active"
                )

            self.gameinfo_noticeLabel.place_forget()

            self.gameinfo_Description.configure(
                text=f"Description:\n{self.selected_gameDescription}",
                )
            self.gameinfo_Description.pack(
                fill="both",
                side="top",
                expand=True,
            )
            # Update information based on window
            self.gameinfo_Description.bind("<Configure>", self.update_descr_wraplength)

            self.gameinfo_Series.configure(text=f"Series: {self.selected_gameSeries}")
            self.gameinfo_Series.pack(
                fill="both",
                side="top",
                expand=True,
            )
            self.gameinfo_Genres.configure(text=f"Genres: {clean_list_to_str(self.selected_gameGenres)}")
            self.gameinfo_Genres.pack(
                fill="both",
                side="top",
                expand=True,
            )
            self.gameinfo_Languages.configure(text=f"Languages: {clean_list_to_str(self.selected_gameLanguages)}")
            self.gameinfo_Languages.pack(
                fill="both",
                side="top",
                expand=True,
            )
            self.gameinfo_Players.configure(text=f"Players: {self.selected_gamePlayers}")
            self.gameinfo_Players.pack(
                fill="both",
                side="top",
                expand=True,
            )
            self.gameinfo_Popularity.configure(text=f"Popularity: {self.selected_gamePopularity}")
            self.gameinfo_Popularity.pack(
                fill="both",
                side="top",
                expand=True,
            )
            self.gameinfo_Rating.configure(
                text=f"Rating:{clean_simple_dict_to_str(self.selected_gameRating,
                    sep="\n- ",
                    start="\n- ",
                    )}")
            self.gameinfo_Rating.pack(
                fill="both",
                side="top",
                expand=True,
            )
            self.gameinfo_Connectivity.configure(text=f"Connectivity: {self.selected_gameConnectivity}")
            self.gameinfo_Connectivity.pack(
                fill="both",
                side="top",
                expand=True,
            )
            self.gameinfo_Release_Dates.configure(
                text=f"Release Dates:\n{clean_simple_dict_to_str(
                    self.selected_gameRelease_Dates,
                    sep="\n- ",
                    start="\n- ",
                    )}")
            self.gameinfo_Release_Dates.pack(
                fill="both",
                side="top",
                expand=True,
            )
            self.gameinfo_Developer.configure(text=f"Developer: {clean_list_to_str(self.selected_gameDeveloper)}")
            self.gameinfo_Developer.pack(
                fill="both",
                side="top",
                expand=True,
            )
            self.gameinfo_Publishers.configure(text=f"Publishers: {clean_list_to_str(self.selected_gamePublishers)}")
            self.gameinfo_Publishers.pack(
                fill="both",
                side="top",
                expand=True,
            )
            self.gameinfo_Ext_Link.configure(text=f"External Link(s): {(clean_list_to_str(self.selected_gameExt_Link))}")
            self.gameinfo_Ext_Link.pack(
                fill="both",
                side="top",
                expand=True,
            )

            self.gamemngr_selgame_gamepath.place(
                relwidth= 0.95,
                relx= 0.025,
                rely= 0.15,
                )
            self.gamemngr_selgame_savepath.place(
                relwidth= 0.95,
                relx= 0.025,
                rely= 0.2,
                )
            self.gamemngr_selgame_gametype.place(
                relwidth= 0.95,
                relx= 0.025,
                rely= 0.25,
                )
            self.gamemngr_selgame_savetype.place(
                relwidth= 0.95,
                relx= 0.025,
                rely= 0.3,
                )
            self.gamemngr_selgame_args.place(
                relwidth= 0.95,
                relx= 0.025,
                rely= 0.35,
                )
            self.gamemngr_selgame_cmd.place(
                relwidth= 0.95,
                relx= 0.025,
                rely= 0.4,
                )
            self.gamemngr_divider.place(
                relwidth= 0.95,
                relheight=0.006,
                relx= 0.025,
                rely= 0.497,
                )
            self.gamemngr_selgame_cursave.place(
                relwidth= 0.95,
                relx= 0.025,
                rely= 0.55,
                )
            self.gamemngr_selgame_bckpsave1.place(
                relwidth= 0.95,
                relx= 0.025,
                rely= 0.6,
                )
            self.gamemngr_selgame_bckpsave2.place(
                relwidth= 0.95,
                relx= 0.025,
                rely= 0.65,
                )
            self.gamemngr_selgame_bckpsave3.place(
                relwidth= 0.95,
                relx= 0.025,
                rely= 0.7,
                )
            self.gamemngr_selgame_bckpsave4.place(
                relwidth= 0.95,
                relx= 0.025,
                rely= 0.75,
                )
            self.gamemngr_selgame_bckpsave5.place(
                relwidth= 0.95,
                relx= 0.025,
                rely= 0.8,
                )
            self.gamemngr_selgame_bckpsave6.place(
                relwidth= 0.95,
                relx= 0.025,
                rely= 0.85,
                )
            self.gamemngr_selgame_bckpsave7.place(
                relwidth= 0.95,
                relx= 0.025,
                rely= 0.9,
                )

            self.__selected_game= game_selected; return game_selected
        return False
    def update_descr_wraplength(self, event)-> None:
        self.gameinfo_Description.configure(wraplength=event.width)
    def start_game_onClick(self)-> None:
        game_file= [key for key in self.__selected_game.keys()][0]
        print(f"Starting {game_file}")
        self.start_game_btn.configure(
            text="Loading...",
            state="disabled"
            )

        # Emulator= "PC"
        # Alias= ""
        # Game_Location= "./Games"
        # Save_location= "./Games"
        # Game_Type= ".game"
        # Save_Type= ".sav"
        # Args= []
        # Manual_Start_Cmd= ""

if __name__ == '__main__':
    w = RetrosHome()
    w.tk.mainloop()
