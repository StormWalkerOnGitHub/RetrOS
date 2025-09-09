class Frame:
    """ . """
    class Test:
        """ . """
        class Help:
            """ . """
obj= Frame
dic:str|dict= ".Frame.Test"
seperator:str= "."
nest_ref:str="children"
default_values= {
    #"obj":all_widgets[index],
    "obj":obj,
    #"tree":f"{_widget_heritage}".rsplit(".",1)[0],
    "tree":"Frame",
    "children":{},
    }
final_default_values= dict(default_values)
blacklisted_str:str="«¦·§·¦»"

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


def genMasterDict(root:str|dict, nested_ref:str|list, sep:str=None, default={})-> dict:
    """Makes &/ Returns a master dictionary"""
    def nest_values(starting_dict:dict, levels:list, nested_ref:str|list, defaults)-> dict:
        """Uses keys and defaults to assign depth"""

        default_values= dict(defaults)
        
        temp_dict:dict= starting_dict
        top_level= [key for key in temp_dict.keys()][0]
        if levels==[]:
            return temp_dict
        temp_dict=temp_dict[top_level][nested_ref]
        for i, level in enumerate(levels):
            i+=1
            
            if temp_dict.get(level,{})=={}:
                temp_dict[level]= default_values
            temp_dict=temp_dict[level]

            if len(levels)<=i:
                temp_dict= temp_dict[nested_ref][level]= final_default_values
                temp_dict[nested_ref]={}
                break
            temp_dict= temp_dict[nested_ref]


        return starting_dict

    match f"{type(root)}":
        case "<class 'dict'>":
            return root
        case "<class 'str'>":
            if isinstance(sep,type(None)):
                raise ValueError("Please include a seperator value and try again")
            elif not isinstance(sep,str):
                raise TypeError("Please ensure seperator value is of type string")
            elif sep=="":
                raise ValueError("Please ensure seperator is not empty")
            root=root.strip()
        case _:
            print(f"{type(root)}")
            raise ValueError("Please ensure you pass a valid datatype as the root")
    
    cleaned_root:list= [entry for entry in root.split(seperator) if f"{entry}"!=""]
    root:str= sep.join(cleaned_root)

    root_dict= nest_values(
        starting_dict= {cleaned_root[0]: dict(default_values)},
        levels= cleaned_root[1:],
        nested_ref= nested_ref,
        defaults= dict(default_values)
        )

    print(f"{root= }")                 # Visible on "normal" output
    print(f"{sep= }")                  # NOT Visible on "normal" output
    print(f"{cleaned_root= }")         # NOT Visible on "normal" output
    print(f"{nested_ref= }")           # Visible on "normal" output
    print(f"{default= }")              # NOT Visible on "normal" output
    print()
    print(f'{root_dict= }')            # NOT Visible on "normal" output
    

print(genMasterDict(dic,nest_ref,seperator,default_values))