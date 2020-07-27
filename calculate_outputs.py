import sys, os
import json
import numpy as np
import math
import glob
import numpy as np
import pandas as pd
from copy import deepcopy
from copy import copy
import re_split_common as rsc
import glob_variables 

scale_value = glob_variables._GLOB().scale_value
filter_value = glob_variables._GLOB().filter_value

def get_all_values(rep, target, target_label, skip=None):
    
    global_dict = {}
    da_dict = {}
    dirs = get_dirs_glob(rep)
    for nd, d in enumerate(dirs):
        idx = int(d.split("/")[-2].strip("split_"))
        global_df = get_test_df(d)
        global_dict[idx] = get_global_summary(rep, target_label, global_df)
        if idx in skip:
            continue
        else:
            tmp_selectors, values, relations = get_selectors_from_subfolder(d)
            selectors = [ rename(s) for s in tmp_selectors ]
            da_dict[idx] = get_subset_summary(d, rep, target, target_label, selectors, values, relations)

    if nd+1 != len(dirs):
        print("Not all files were collected from the relevant subfolders")

    print_summary_complete(da_dict, global_dict)

    return da_dict, global_dict


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

def calc_l1_dispersion(invalues):
    
    return np.mean([ abs(invalues - np.median(invalues)) for i in range(len(invalues)) ])


def calc_l2_dispersion(invalues):
    
    return math.sqrt(np.mean([ (invalues[i] - np.mean(invalues))**2 for i in range(len(invalues)) ]))

def get_global_summary(rep, target_label, tmp_df):
   
    all_targets = copy(scale_value*tmp_df[target_label].values)
    all_preds = copy(scale_value*tmp_df[rep+"_predE"].values)
    all_evals = copy(scale_value*tmp_df["Ef"].values)    
    all_ids = copy(tmp_df["id"].values)    

    assert len(all_preds) == len(all_targets) and len(all_evals) == len(all_targets)

    all_files_dict = { "error": np.mean(all_targets), 
                        "l1": calc_l1(all_evals, all_preds),
                        "l1_disp": calc_l1_dispersion(all_evals),
                        "l2_disp": calc_l2_dispersion(all_evals),
                        "rsquared": calc_r2(all_evals, all_preds),
                        "95per" : np.percentile(all_targets, 95),
                        "all_ids": copy( all_ids ),
                        "all_preds": copy( all_preds ),
                        "all_errors": copy( all_targets ),
                        "all_evals": copy( all_evals ) } 

    return all_files_dict

    
def get_test_df(d):
    return pd.read_csv(os.path.join(d, "test.csv"))

def get_subset_summary(d, rep, target, target_label, selectors, values, relations):

    tmp_dict = {}
    for t in ["test", "train"]:
        in_df = pd.read_csv(os.path.join(d, t+".csv"))
        out_df = selector2df(deepcopy(in_df), selectors, values, relations)
        nsamples = len(out_df[target_label].values)
        DA_preds = copy(scale_value*out_df[out_df["is_reliable"] == 1][rep+"_predE"].values)
        DA_evals = copy(scale_value*out_df[out_df["is_reliable"] == 1]["Ef"].values)
        DA_targets = copy(scale_value*out_df[out_df["is_reliable"] == 1][target_label].values)
        all_targets = copy(scale_value*out_df[target_label].values)
        all_evals = copy(scale_value*out_df["Ef"].values)

        tmp_dict["DA"+"_"+t] = {"DA_error": np.mean(DA_targets), 
                                "DA_cov": float(len(DA_targets))/float(nsamples),
                                "DA_l1": calc_l1(DA_evals, DA_preds),
                                "DA_l1_disp": calc_l1_dispersion(DA_evals),
                                "DA_l2_disp": calc_l2_dispersion(DA_evals),
                                "DA_rsquared": calc_r2(DA_evals, DA_preds),
                                "DA_95per" : np.percentile(DA_targets, 95),
                                "DA_errors": copy(DA_targets),
                                "DA_evals": copy(DA_evals),
                                "DA_ids": copy(out_df[out_df["is_reliable"] == 1]["id"].values),
                                "all_evals": copy(all_evals),
                                "all_errors": copy(all_targets),
                                "global_error": np.mean(all_targets),
                                }
        
        """
        if t == "test":
            print_df = deepcopy(out_df)
            print_df[target_label] = copy(scale_value*print_df[target_label].values)
            print_summary_per_split(print_df, target_label, rep)
        """

    return tmp_dict

def print_summary_per_split(df, target, model):

    print('\n--------------Evaluating SGD on %s for the target %s ---------------' %(model, target))
    print('%i/%i (%.2f) in the reliable region...\nreliable-->MAE = %.3f\nunreliable-->MAE = %.3f \nglobal-->MAE = %.3f' % 
          (df.is_reliable.sum(), len(df), df.is_reliable.mean(), 
           df[target].get((df.is_reliable == 1)).mean(),
           df[target].get((df.is_reliable == 0)).mean(),
           df[target].mean()))
    
    print('Number of points below %s in the rr (global) %s (%s) with an avg. error %s' % 
           (round(filter_value, 2),
           len(df[target].get((df.is_reliable == 1) & (df[target] <= filter_value )))/float(len(df[target].get((df.is_reliable == 1)))),
           len(df[target].get(df[target] <= filter_value))/float(len(df[target])),
           df[target].get((df.is_reliable == 1) & (df[target] <= filter_value )).mean()))
    
    rr_95per = np.percentile(df[target].get(df.is_reliable == 1).tolist(), 95)
    global_95per = np.percentile(df[target].tolist(), 95)
    print('95per. distribution reliable %s ' %rr_95per)
    print('95per. distribution global %s ' %global_95per) 
    tmp_frac = rr_95per/global_95per
    print('relative reductions: %s' %(tmp_frac))
    
    return (df[target].get((df.is_reliable == 1)).mean(), 
            df[target].mean(), df.is_reliable.sum()/float(len(df)), 
            len(df[target].get((df.is_reliable == 1) & (df[target] <= filter_value )))/float(len(df[target].get((df.is_reliable == 1)))),
            len(df[target].get(df[target] <= filter_value))/float(len(df[target])),
            rr_95per,
            global_95per)

def print_global(in_global_dict):
    root_strg = "Global"
    tmp_agg = []

    tmp_agg_errors = [ e for k in list(in_global_dict.keys()) for e in in_global_dict[k]["all_errors"] ] 
    tmp_agg_evals = [ e for k in list(in_global_dict.keys()) for e in in_global_dict[k]["all_evals"] ] 
    tmp_agg_preds = [ e for k in list(in_global_dict.keys()) for e in in_global_dict[k]["all_preds"] ] 
    print("nsamples", len(tmp_agg_errors))
    print("MAE", np.mean(tmp_agg_errors))
    print("95per", np.percentile(tmp_agg_errors, 95))
    print("l1", calc_l1(tmp_agg_evals, tmp_agg_preds))
        
def print_DA(in_DA_dict):
    for t in ["train", "test"]:
        if t == "train":
            root_strg = "DA identification:"
        elif t == "test":
            root_strg = "DA validation:"
        for l, p in zip(["MAE", "l1", "95per", "cov"], ["DA_error", "DA_l1", "DA_95per", "DA_cov"]):
            tmp_list = [ in_DA_dict[i]["DA"+"_"+t][p] for i in in_DA_dict.keys() ]
            print("%s: %s --> avg. (std) DA = %s (%s) " %(root_strg, l, round(np.mean(tmp_list), 3), round(np.std(tmp_list), 3)))
    
def print_summary_complete(final_rep_dict, final_global_dict):
    
    print_global(final_global_dict)
    print_DA(final_rep_dict)
    
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

