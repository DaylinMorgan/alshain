from gen_utils import theme_json_maker

#developed based on dark theme at https://github.com/vega/vega-themes/

def dark2_gen():
    
    lightColor = '#fff';
    medColor = '#888';

    schema = { 
        'config':{
            'background': '#333',
        
            'title': {'color': lightColor},

            'style': {
                'guide-label': {
                'fill': lightColor,
                },
            'guide-title': {
                'fill': lightColor,
                },
            },

            'axis': {
                'grid':False,
                'domainColor': lightColor,
                'gridColor': medColor,
                'tickColor': lightColor,
            }
        }
    }

    theme_name = 'dark2'

    theme_json_maker(theme_name, schema)

if __name__ == '__main__':
    dark2_gen()