import os
import re
import sys
import json
import pandas as pd
import altair as alt
from jinja2 import Template, Environment, PackageLoader

#from bigdatautils import *

class Report(object):
    
    def __init__(self):
        #self.filename = filename #should these be defined here? or in the save itself?? 
        #self.title = title
        self.charts = {}
        
    def add_chart(self, chart, title=None, skip_df_check=False):
        """
        Make a master report in the form of an html of all altair chart objects. 

        Parameters
        -----------
        chart : altair chart object
            the chart to add to master report  
        title : string
            title for individual chart
        """
        
        if len(self.charts) == 0:
            num = '1' 
            chart_id = 'vis' + num
        else:
            #get number from last defined chart object 
            num = str(int(list(self.charts)[-1][-1]) + 1)
            chart_id = 'vis' + num
        
        if title==None:
            title = 'Chart ' + num
        
        if not skip_df_check:
        #check if chart is defined by dataframe -> will this work if it is big? 
            if not isinstance(chart.data, pd.DataFrame):
                raise ValueError('Data in this chart object is not a pandas DataFrame, if using als.getURL() set return_df=True')
        
        #altair defaults to keeping datasets below 5000 rows for good reason but let's ignore for making reports
        with alt.data_transformers.disable_max_rows():
            spec = json.dumps(chart.to_dict())
        
        self.charts[chart_id] = { title : spec }
         
    def chart_list(self):
        """
        Make a pretty looking table of the defined chart objects 

        Parameters
        -----------
        None
        
        """

        chart_info={}
        for key, value in  self.charts.items():
            for k,v in self.charts[key].items():
                chart_title,spec_str = list(self.charts[key].items())[0]
                m = re.findall(r'"mark": "(.*?)"', spec_str)
                #may need to prevent an error here if it can't find a mark
                marks = ', '.join(m)
                chart_info[chart_title] = marks
        
        df_info = pd.DataFrame(chart_info.items())       
        
        #get necessary info to build table
        title_max = df_info[0].str.len().max()
        if title_max > 30:
            title_max = 30
        mark_max = df_info[1].str.len().max()
        tbl_len = title_max + mark_max + 3

        header = 'Chart' + ' '*(tbl_len-9) + 'Mark'
        line = '='* tbl_len
        print(header)
        print(line)
        #add a line for each chart 
        for chart_title,marks in chart_info.items():
            if len(chart_title) > 30:
                chart_title = chart_title[:27] + '...'  
                
            space1 = (title_max-len(chart_title)) * ' '
            space2 = (mark_max-len(marks)) * ' '
            row = chart_title + space1 + ' | ' + space2 + marks
            print(row)
        
  
    def save(self, filename = 'master_report.html', title = 'Master Report'):
        """
        Make a master report in the form of an html of all altair chart objects. 

        Parameters
        -----------
        chart_dict : dictionary of altair chart objects
            the charts to save 
        filename : string filename of file-like object
            file in which to save all the chart objects
        title : string
            title for overall master report

        """

        # TODO: add a comment under title or at the bottom of page with compile date using datetime 
        # use a seperate block for this?

        #make jinja evnironment
        env = Environment(
            loader = PackageLoader('alshain','templates')
            )

        #get child template for populating with chart objects

        t = env.get_template('chart_child.html')

        #generate a user dict for use in html generation

        master = t.render(chart_dict = self.charts, title = title)

        #make actual master html doc
        with open(filename, 'w') as f:
            f.write(master)
        
        
        
        
        
        