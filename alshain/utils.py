import os
import sys

global base_url
base_url = None

def splitall(path):
    allparts = []
    while True:
        parts = os.path.split(path)
        if parts[0] == path:  # sentinel for absolute paths
            allparts.insert(0, parts[0])
            break
        elif parts[1] == path: # sentinel for relative paths
            allparts.insert(0, parts[1])
            break
        else:
            path = parts[0]
            allparts.insert(0, parts[1])
    return allparts
    
##### old find path would fail at first directory 
# #what to do where next level needs to be searched
# def find_path(directory,list_o_dir):
#     if len(list_o_dir) == 1: 
#         return directory
#     else:
#         with os.scandir(directory) as it:
#             for entry in it:
#                 if not entry.name.startswith('.') and entry.is_dir():
#                     if entry.name in list_o_dir:
#                         i = list_o_dir.index(entry.name)
#                         return find_path(entry.path,list_o_dir[i:])          
                    
def filename_gen(df):
    """ Return a file name  
   
    """
    columns = list(df.columns)
    if len(columns) > 5:
        columns = [col[:3].lower() for col in columns]
        
    filename = "_".join(columns) + "__" + str(df.shape[0])+"rows_" + str(df.shape[1])+"cols" +".json"
    
    return filename

def find_path(directory,list_o_dir):
    if len(list_o_dir) == 1: 
        return os.path.join(directory,list_o_dir[0])
    else:
        with os.scandir(directory) as it:
            for entry in it:
                if not entry.name.startswith('.') and entry.is_dir():
                    #make a new list of objects and a list of entry.names to check against list_o_dir    
                    if entry.name in list_o_dir:
                        i = list_o_dir.index(entry.name)
                        return find_path(entry.path,list_o_dir[i+1:])
                    else: 
                        with os.scandir(entry.path) as it:
                            for entry in it:
                                if not entry.name.startswith('.') and entry.is_dir():
                                    if entry.name in list_o_dir:
                                        i = list_o_dir.index(entry.name)
                                        return find_path(entry.path,list_o_dir[i+1:])
    
                    
                    
def getURL(df, filename=None,return_df=False):
    """
    Generate json objects and return a url to inline display altair charts with large dataframes.

    Parameters
    -----------
    df : pandas dataframe
        dataframe used to generate altair chart   
    filename : string
        name for json to be referenced in json's directory 
    return_df : boolean
        return the dataframe that is passed instead of url

    """
    global base_url
    #change the way filename is defined to be semi-random
    if return_df==True:
        return df
    
    if not os.path.exists('./alshain_jsons'):
        os.mkdir('alshain_jsons')

    if filename == None:
        filename = filename_gen(df)
        
    if base_url == None:
        tmp_path = find_path(os.getenv('HOME'),splitall(os.getcwd()))
        
        base_url = 'http://localhost:8888/tree' + tmp_path.split(os.getenv('HOME'))[1]
        
        print("Setting base_url as: {}".format(base_url))

    name, ext = os.path.splitext(filename)
    if ext == '':
        filename = name + '.json'
    elif ext != '.json':  
        raise ValueError('filenames must use extension .json')
    
    
    df.to_json('alshain_jsons/' + filename, orient='records')

        
    url = base_url + '/alshain_jsons/' + filename
    
    return url 