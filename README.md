# ML_domain_of_applicability
These files allow for an analysis of the domain of applicability (DA) to be performed once some ML model predictions have been generated.
Both the model predictions and the descriptive language required to perform the DA analysis are contained in the data.csv file. 

The main script is make_run_print.py, which calls two main scripts: re_split_common.py and calculate_outputs.py. 

In make_run_print, the global variables that are used in these scripts are set using the class _GLOB. 

For example, the DA analysis is performed by partitioning the data.csv file into six non-overlapping folds using scripts contained in re_split_common.py. The number of splits is hard coded in this file with n_splits = 6.

The output of re_split_common.py. is to produce a xarf file (the formatted file that can be used to run subgroup discovery). 

This file can then be ran with sgd using a wrapper to the java source code. 

The output of this is a json file that must be analyzed, which is done 




