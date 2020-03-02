import os, sys
import pandas as pd
import random
import numpy as np
import glob_variables 

root_path_dir = glob_variables._GLOB.root_path_dir
n_splits = glob_variables._GLOB.n_splits 

def gen_sgd_inputs(target, model=None, dataset=None, random_state=None):
    
    random.seed(random_state)
    final_df = get_df(model)
    split_total_df_and_write(target, model, n_splits, final_df, random_state)
    
def split_total_df_and_write(target, model, n_splits, final_df, random_state):

    initial_list = final_df.id.tolist()
    master_list = {i:[] for i in range(0, n_splits) }
    for n_split in range(0, n_splits): 
        idxs = random.sample(initial_list, 100)
        master_list[n_split] = idxs
        for i in idxs:
            del initial_list[initial_list.index(i)]
        
    for n_split in master_list:
        if not os.path.exists(model):
            os.mkdir(model)
        
        tmp_dir = os.path.join(model,"random_state_"+str(random_state))
        if not os.path.exists(tmp_dir):
            os.mkdir(tmp_dir)
        dirname = os.path.join(model,"random_state_"+str(random_state), "split"+"_"+str(n_split+1))
        if not os.path.exists(dirname):
            os.mkdir(dirname)
        
        idxs = master_list[n_split]

        test_df = final_df[final_df.id.isin(idxs)]
        train_df = final_df[~final_df.id.isin(idxs)]
        train_df.to_csv(os.path.join(dirname, "train.csv"), index=False)
        test_df.to_csv(os.path.join(dirname, "test.csv"), index=False)
        
        xarf_write_name = os.path.join(dirname, "xarf.txt") 
        write_xarf_file(train_df, target, xarf_write_name, write_dir = ".")

def get_df(model):
    end_label = "_predE"
    test_infile = os.path.join(root_path_dir,'data.csv')
    df = pd.read_csv(test_infile)
    label = model+end_label

    keep_cols = [ i for i in df.columns.tolist() if end_label not in i and i != "Ef" ] 
    
    df = calc_sum_predE_abs_error(df, label)

    #keep_cols = get_keep_ids()
    keep_cols.extend( ["Ef", label, "abs_error", "error", "sq_error", "norm_abs_error", "sum_Ef_and_normalized_error", "sum_pred_Ef_and_abs_error"] )
    final_df = df[keep_cols]

    return final_df 

def calc_sum_predE_abs_error(df, label):

    df["error"] = df[label].values - df["Ef"].values
    df["abs_error"] = abs(df[label].values - df["Ef"].values)
    df["sq_error"] = (df[label].values - df["Ef"].values)**2
    df["norm_abs_error"] = [ abs(i-j)/i if round(i - 0.00, 3) != 0.000 else 0.000  for i, j in zip(df["Ef"].tolist(),df[label].tolist()) ]
    df["sum_pred_Ef_and_abs_error"] = df[label] + df["abs_error"]
    if "sum_Ef_and_normalized_error" not in df.columns.tolist():
        df["sum_Ef_and_normalized_error"] = df[label] + df["norm_abs_error"]

    return df

def write_xarf_file(write_df, target, write_name, write_dir="."):
    print("writing to dir", write_dir)
    feature_list = get_feature_txt(write_df.columns.tolist(), write_name.strip('_xarf_file.txt'))

    outFile2=write_name+'.tmp'
    if os.path.isfile(outFile2):
         os.remove(outFile2) 

    write_df.to_csv(outFile2, header=None, sep=',', mode='a', index=False)

    with open(outFile2) as f:
        lines = f.readlines()
    
    content = [ line.strip() for line in lines ] 

    feature_list.extend(content)
    outFile3=os.path.join(write_dir, write_name)

    with open(outFile3, 'w') as f:
        f.write('\n'.join(feature_list))

    os.remove(outFile2)


def get_feature_txt(features, header_name):
    
    feature_list = []
    header = ('@relation wpo_1_0_0 caption="WPO 1.0.0" description="generated from %s.csv"' %header_name)
    feature_list.append( "%s" %header )

    for i in features:
        if i == "label":
            name_type = "categoric"
        else:
            name_type = "numeric"
        c = " ".join(["@attribute", i, name_type])
        feature_list.append( "%s" %c )

    feature_list.append( "%s" %"@data" )

    return feature_list

if __name__ == '__main__':
    main()
