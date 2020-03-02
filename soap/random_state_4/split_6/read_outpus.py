import glob
import os
import json

def read_json(fjson):
    with open(fjson) as f:
        return json.load(f)


for root, dirs, files in os.walk('.'):
    for f in files:
        if ".json" in f:
            res = read_json(os.path.join(root, f))
            for r in res:
                try: 
                    r.keys()
                except AttributeError:
                    continue
                res_dict = r["descriptor"]['selector']
                selectors = res_dict["attributes"]
                values = [ i["value"] for i in res_dict["constraints"] ]
                relations = [ i["type"] for i in res_dict["constraints"] ]
              
print(selectors, values, relations)

