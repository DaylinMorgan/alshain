import os
import json

def theme_json_maker(theme, schema):
    json_path = os.path.join('../theme_jsons',"{}.json".format(theme))
    with open(json_path, "w") as outfile:  
        json.dump(schema, outfile, indent=4)
    print('created json for theme: {}'.format(theme))