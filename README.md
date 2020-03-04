## Code and Data Repository for
# Identifying Domains of Applicability of Machine Learning Models for Materials Science
by Christopher Sutton, Mario Boley, Luca M Ghiringhelli, Matthias Rupp, Jilles Vreeken, Matthias Scheffler

These files allow for an analysis of the domain of applicability (DA) to be performed once ML model predictions have been generated.
Both the descriptive language required to perform the DA analysis and the ML model predictions are contained in the provided data.csv file. 

The main script is make_run_print.py, which calls two additional scripts: re_split_common.py (for partitioning the initial total dataset into non-overlapping folds) and calculate_outputs.py (for analyszing the outcome of the DA analysis).

The DA analysis is performed by partitioning the data.csv file into six non-overlapping folds using the line in make_run_print.py:
    rsc.gen_sgd_inputs(target, model=model, random_state=glob_variables._GLOB.random_state_dict[model])

This line calls re_split_common.py  The output of re_split_common.py are six xarf files created from splitting data.csv. Once the xarf file have been created, the DA analysis can be performed, which utalizing subgroup discovery (SGD). The java excutable and source code for SGD is in "software/realkd-0.7.2". The parameters sets in the neg_mean_shift_abs_norm_error.json file.

In each subfolder, run SGD using the line:

java software/realkd-0.7.2/bin/realkd-0.7.2-jar-with-dependencies.jar ../../neg_mean_shift_abs_norm_error.json

SGD creates a subfolder called "outputs", which is time stamped for each run. After SGD has been performed in each subfolder (i.e., for each non-overlapping fold), run calculate_outputs.py from the make_run_print.py using the line:

co.get_all_values(model, target, target_label, skip=glob_variables._GLOB.skip_dict[model][target])

Several global variables that set using the class _GLOB to reproduce the numbers from our manuscript. In terms of using this python script beyond the data.csv file we provided, the global varibles "skip_dict" and random_state need not be set in make_run_print.py for the code to work. Additionally, the number of splits is hard coded in glob_variables.py with n_splits = 6, which should be adjusted to the specific dataset. 

