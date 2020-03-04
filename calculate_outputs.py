import os
import json
import numpy as np
import math
import glob
import numpy as np
import pandas as pd
from copy import deepcopy
import re_split_common as rsc
import glob_variables 

exchange_value = glob_variables._GLOB().exchange_value

def get_all_values(rep, target, target_label, skip=None):

    global_dict = {}
    da_dict = {}
    dirs = get_dirs_glob(rep)
    for d in dirs:
        try: 
            tmp_selectors, values, relations = get_selectors_from_subfolder(d)
            selectors = [ rename(s) for s in tmp_selectors ]
        except UnboundLocalError:
            # throws an error if there are no sgd outputs in the subfolder
            continue
    
        idx = int(d.split("/")[-2].strip("split_"))
        if idx in skip:
            continue
        else:
            global_df = rsc.get_df(rep)
            global_dict[idx] = get_global_summary(global_df, rep, target, target_label, selectors, values, relations)
            da_dict[idx] = get_subset_summary(d, rep, target, target_label, selectors, values, relations)

    print_summary(da_dict, global_dict)


def calc_r2(values1, values2):
 
    avg_e = np.mean(values1)
    sum_of_square_error = [ ((values2[i] - values1[i])**2) for i in range(len(values1)) ]
    var = [ (values1[i] - avg_e)**2 for i in range(len(values1)) ]
     
    return 1-np.sum(sum_of_square_error)/np.sum(var)
 
def calc_l1(values1, values2):
 
    median_e = np.median(values1)
    sum_of_abs_error = [ abs(values2[i] - values1[i]) for i in range(len(values1)) ]
    var = [ abs(values1[i] - median_e) for i in range(len(values1)) ]
     
    return 1-np.sum(sum_of_abs_error)/np.sum(var)

def partition_and_print(bigdf, target):
    rr_df = bigdf[bigdf["is_reliable"] == 1]
    other_df = bigdf[bigdf["is_reliable"] == 0]
    print("avg. rr --> %s, cov = %s, vs. glob --> %s" %(np.mean(rr_df[target].values), len(rr_df)/float(len(bigdf)), np.mean(bigdf[target].values)))
 
    return rr_df, other_df
 
def selector2df(tmp_df, in_selectors, in_values, in_relations):
 
    tmp_df["is_reliable"] = [ 1 for i in range(0, len(tmp_df)) ]
    for s, v, r in zip(in_selectors, in_values, in_relations):
        if r == "greaterOrEquals":
            tmp_df["is_reliable"] = [ 1*tmp_df["is_reliable"].values[i] if tmp_df[s].values[i] >= v  else 0  for i in range(0, len(tmp_df)) ]
        elif r == "greaterThan":
            tmp_df["is_reliable"] = [ 1*tmp_df["is_reliable"].values[i] if tmp_df[s].values[i] > v  else 0  for i in range(0, len(tmp_df)) ]
        elif r == "lessThan":
            tmp_df["is_reliable"] = [ 1*tmp_df["is_reliable"].values[i] if tmp_df[s].values[i] < v else 0  for i in range(0, len(tmp_df)) ]
        elif r == "lessOrEquals":
            tmp_df["is_reliable"] = [ 1*tmp_df["is_reliable"].values[i] if tmp_df[s].values[i] <= v  else 0  for i in range(0, len(tmp_df)) ]
         
    return tmp_df

def get_dirs_glob(rep):
    subfolders = glob.glob(rep+"/*/split_*/")
    
    return subfolders

def get_global_summary(global_df, rep, target, target_label, selectors, values, relations):
     
    global_df[target] = global_df[target].values
    
    if target != target_label:
        global_df[target_label] = exchange_value*global_df[target_label].values
     
    global_df[rep+"_predE"] = exchange_value*global_df[rep+"_predE"].values
    global_df["Ef"] = exchange_value*global_df["Ef"].values    
    
    for s, v, r in zip(selectors, values, relations):
        print(s, v, r)
    
    out_global_df = selector2df(deepcopy(global_df), selectors, values, relations)
    
    global_dict = { "error": np.mean(out_global_df[target_label].values), 
                    "l1": calc_l1(out_global_df["Ef"].values, out_global_df[rep+"_predE"].values),
                    "l1_disp": np.mean([ abs(out_global_df["Ef"].values[i] - np.median(out_global_df["Ef"].values)) for i in range(len(out_global_df["Ef"].values)) ]),
                    "l2_disp": math.sqrt(np.mean([ (out_global_df["Ef"].values[i] - np.mean(out_global_df["Ef"].values))**2 for i in range(len(out_global_df["Ef"].values)) ])),
                    "rsquared": calc_r2(out_global_df["Ef"].values, out_global_df[rep+"_predE"].values),
                    "95per" : np.percentile(out_global_df[target_label].values, 95),
                    "DA_rsquared": calc_r2(out_global_df[out_global_df["is_reliable"] == 1]["Ef"].values, out_global_df[out_global_df["is_reliable"] == 1][rep+"_predE"].values),
                    "DA_error": np.mean(out_global_df[out_global_df["is_reliable"] == 1][target_label].values),
                    "samples": deepcopy( out_global_df[target_label].values ),
                    "Ef": deepcopy( out_global_df["Ef"].values ) }
 
    return global_dict

def get_subset_summary(d, rep, target, target_label, selectors, values, relations):

    tmp_dict = {}
    for t in ["test", "train"]:
        in_df = pd.read_csv(os.path.join(d, t+".csv"))
        out_df = selector2df(deepcopy(in_df), selectors, values, relations)
        pred_e_value = deepcopy(exchange_value*out_df[out_df["is_reliable"] == 1][rep+"_predE"].values)
        e_value = deepcopy(exchange_value*out_df[out_df["is_reliable"] == 1]["Ef"].values)
        target_e_value = deepcopy(exchange_value*out_df[out_df["is_reliable"] == 1][target_label].values)
        all_target_e_value = deepcopy(exchange_value*out_df[target_label].values)

        #print("for model %s split %s, avg. rr vs. glob error --> %s vs. %s" %(rep, split, target, t, np.mean(df[target].values), np.mean(df[df["is_reliable"] == 1][target].values)))
        tmp_dict["DA"+"_"+t] = {"error": np.mean(target_e_value), 
                                "cov": len(out_df[out_df["is_reliable"] == 1])/float(len(out_df)),
                                "l1": calc_l1(e_value, pred_e_value),
                                "l1_disp": np.mean([ abs(e_value[i] - np.median(e_value)) for i in range(len(e_value)) ]),
                                "l2_disp": math.sqrt(np.mean([ (e_value[i] - np.mean(e_value))**2 for i in range(len(e_value)) ])),
                                "rsquared": calc_r2(e_value, pred_e_value),
                                "95per" : np.percentile(target_e_value, 95),
                                "samples": deepcopy(target_e_value), #abs(e_value - pred_e_value),
                                "all_error": np.mean(all_target_e_value),
                                "ids": deepcopy(out_df[out_df["is_reliable"] == 1]["id"].values),
                                }
    return tmp_dict


def print_summary(final_rep_dict, final_global_dict):
    
    root_strg = "Global"
    for l, p in zip(["MAE", "r^2", "l1", "95per" ], ["error", "rsquared", "l1", "95per"]):
        tmp_list = [ final_global_dict[i][p] for i in final_global_dict.keys() ]
        print("%s: %s --> avg. = %s" %(root_strg, l, np.mean(tmp_list)))

    root_strg = "DA of Global"
    for l, p in zip(["MAE","r^2", "l1", "95per"], ["DA_error", "DA_rsquared", "l1", "95per"]):
        tmp_list = [ final_global_dict[i][p] for i in final_global_dict.keys() ]
        print("%s: %s --> avg. = %s" %(root_strg, l, np.mean(tmp_list)))

    for t in ["train", "test"]:
        if t == "train":
            root_strg = "DA identification:"
        elif t == "test":
            root_strg = "DA validation:"
        for l, p in zip(["MAE", "l1", "95per", "cov"], ["error", "l1", "95per", "cov"]):
            tmp_list = [ final_rep_dict[i]["DA"+"_"+t][p] for i in final_rep_dict.keys() ]
            print("%s: %s --> avg. (std) DA = %s (%s) " %(root_strg, l, np.mean(tmp_list), np.std(tmp_list)))

def rename(in_key):
    rename_dict = {'ecn_bond_dist_Al_O': 'ecn_bond_dist_Al-O',
                    'ecn_bond_dist_Ga_O': 'ecn_bond_dist_Ga-O',
                    'ecn_bond_dist_In_O': 'ecn_bond_dist_In-O'
                    }
    try:
        return rename_dict[in_key]
    except KeyError: 
        return in_key

def read_json(fjson):
    with open(fjson) as f:
        return json.load(f)

def get_selectors_from_subfolder(in_dir):
    # need to set folder to perform the walk and need to check based on the string
    for root, dirs, files in os.walk(in_dir):
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
                  
    return selectors, values, relations

