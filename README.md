# ML_domain_of_applicability
These files allow for an analysis of the domain of applicability (DA) to be performed once some ML model predictions have been generated.
Both the model predictions and the descriptive language required to perform the DA analysis are contained in the data.csv file. 

The main script is make_run_print.py, which calls two additional scripts: re_split_common.py and calculate_outputs.py. 

The DA analysis is performed by partitioning the data.csv file into six non-overlapping folds using scripts contained in re_split_common.py. The output of re_split_common.py is a sixe xarf files, which is used to run sgd using a wrapper to the java source code (and the parameters sets in the neg_mean_shift_abs_norm_error.json file).

The output of SGD is a json file that is analyzed using calculate_outputs.py. 

Several global variables that set using the class _GLOB to reproduce the numbers from the manuscript.  For example,  the number of splits is hard coded in this file with n_splits = 6.






