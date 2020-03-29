import pandas as pd
import altair as alt
import json
from jinja2 import Template, Environment, PackageLoader
#import jinja2

def chart_to_user_dict(chart_dict):
    with alt.data_transformers.disable_max_rows():
        user_dict = {}
        for num, chart in enumerate(chart_dict.keys(),1):
            chart_id = 'vis' + str(num)
            spec = json.dumps(chart_dict[chart].to_dict())
            user_dict[chart_id] = {chart : spec}

        return user_dict


    
def make_report(chart_dict,filename, title):
    """
    Make a master report in the form of html of all altair chart objects. 
    
    Parameters
    -----------
    chart_dict : dictionary of altair chart objects
        the charts to save 
    filename : string filename of file-like object
        file in which to save all the chart objects
    title : string
        title for overall master report
 
    """
    

    if filename is None:
        filename = 'master_report.html'

    if title is None:
        title = ''

    #make jinja evnironment
    env = Environment(
        loader = PackageLoader('altair_addon','templates')
        )

    #get child template for populating with chart objects

    t = env.get_template('chart_child.html')

    #generate a user dict for use in html generation
    user_dict = chart_to_user_dict(chart_dict)

    master = t.render(user_dict = user_dict, title = title)

    #make actual master html doc
    with open(filename, 'w') as f:
        f.write(master)
        

