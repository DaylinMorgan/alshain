import collections.abc
import json
import os
import pkgutil

import altair as alt

def load_schema(theme):

    base_schema = json.loads(pkgutil.get_data(__name__,os.path.join('theme_jsons',"{}.json".format(theme))).decode('utf-8'))
    
    return base_schema

def theme_update(d, u):

    for k, v in u.items():
        if isinstance(v, collections.abc.Mapping):
            d[k] = theme_update(d.get(k, {}), v)
        else:
            d[k] = v
    
    return d

def get_schemas():

    schema_repo = {}

    for f in os.listdir(os.path.join(os.path.dirname(__file__),'theme_jsons')):
        name, ext = filename, file_extension = os.path.splitext(f)
        schema_repo[name]=load_schema(f)
    
    return schema_repo

def get_themes():
    
    themes=[]
    
    for f in os.listdir(os.path.join(os.path.dirname(__file__),'theme_jsons')):
        name, ext = filename, file_extension = os.path.splitext(f)
        themes.append(name)

    print("Alshain is shipped with the following themes: " ,', '.join(themes))
    
    return themes
    
def bulk_theme_registration(themes):
    print('registering the following custom themes: {}'.format(", ".join(themes)))
    
    for theme in themes:
        use_theme(theme)

    #reset to my default altair theme
    alt.themes.enable('my_default')

def use_theme(theme):
    """
    Make a termporary theme by modifying one of the alshain themes. 

    Parameters
    -----------
    chart : altair chart object 
        object defining altair chart schema
    theme : string
        name of theme to test on chart 
    """

    try:
        load_schema(theme)    
    except:
        print('Unable to register this theme...')
        print('Is this a supported theme?')
    else:
        alt.themes.register(theme, lambda: load_schema(theme))
        alt.themes.enable(theme)

def use_theme_custom(theme,json_file):
    """
    Create a custom theme using a json_file

    Parameters
    -----------
    theme : string
        name of theme to create
    json_file : string
        path to json defining theme
    """

    try:
        with open(json_file) as f:
            schema = json.load(f)
        alt.themes.register(theme,lambda: schema)
    except:
        print('there was a problem registering your theme')
    
def theme_mod(theme, theme_mods, new_theme=None):
    """
    Make a modification to one of the alshain themes. 

    Parameters
    -----------
    theme : string 
        name of alshain theme to modify 
    theme_mods : dict
        dictionary with theme modifications 
    new_theme : string
        name for the new theme if none specified "_mod" will be appended to original theme name
    """

    if new_theme == None:
        new_theme = "{}_mod".format(theme)
    
    base_schema = load_schema(theme)
    
    #add theme_mods sanity checks?
    # check for 'config' key

    updated_schema = theme_update(base_schema,theme_mods)

    alt.themes.register(new_theme,lambda: updated_schema)
    alt.themes.enable(new_theme)

def theme_test(chart, theme):
    """
    Make a modification to one of the alshain themes. 

    Parameters
    -----------
    chart : altair chart object 
        object defining altair chart schema
    theme : string
        name of theme to test on chart 
    """

    chart_dict = chart.to_dict()
    theme_schema = load_schema(theme)
    chart_dict['config'] = theme_schema['config']
    chart = alt.Chart().from_dict(chart_dict)
    return chart

def view_theme_json(theme):
    print("See below for the json for theme: {}".format(theme))
    print("-----------------------------------------------")
    print(json.dumps(load_schema(theme), indent=4))