key_lookup="frame.help.me"
test_dict= {
    "frame": {
        "help": {"me":"PLEASE"},
        "bitch":{"ass":"hoe"},
    },
    "test":[],
}

def depth_first_search(data:dict, target:list|str, sep:str=",", new_value=None, default=None):
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
    #endregion verify data input
    #region Clean target input
    if isinstance(target, str):# convert to list
        target:list=target.split(sep)
    if not isinstance(target,list):
        raise TypeError("Please ensure target search is a list")
    cleaned_target:list= []
    for node in target:# remove unwanted inputs
        if node.strip()=="":
            continue
        cleaned_target.append(node)
    del target
    if cleaned_target==[]:# raise issue if unable to retain a value
        raise ValueError("Please ensure target is a valid search entry")
    #endregion Clean target input
    print(cleaned_target)




print(depth_first_search(test_dict,key_lookup,sep="."))
