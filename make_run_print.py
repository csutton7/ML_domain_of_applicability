import sys, os
import random
import re_split_common as rsc
import calculate_outputs as co
import glob_variables 

def main():

	target = "norm_abs_error"
	target_label = "abs_error"
	# other options: "ngram", "mbtr", "atomic" "soap" 
	#model = "mbtr" 
	#model = "soap"
	#model = "ngram" 
	#model = "atomic"
	#rsc.gen_sgd_inputs(target, model=model, random_state=glob_variables._GLOB.random_state_dict[model])
	
	for model in ["mbtr", "soap",  "ngram", "atomic"]
		res = co.get_all_values(model, target, target_label, skip=glob_variables._GLOB.skip_dict[model][target])

if __name__ == "__main__":
    main()
