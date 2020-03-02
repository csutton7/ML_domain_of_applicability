import sys, os
import math
import random
import glob
import numpy as np
import pandas as pd
from copy import deepcopy
import re_split_common as rsc
import calculate_outputs as co

class _GLOB:
    root_path_dir = "."
    exchange_value = 1.0 #exchange_value = 100.0
    random_state_dict = {"mbtr": 4, "soap": 4, "ngram": 14}
    random_state = None
    skip_dict = {"mbtr": {"norm_abs_error":[1, 4]},
                "soap": {"norm_abs_error":[1, 5]},
                "ngram":{"norm_abs_error":[4]},
                "atomic": {"norm_abs_error":[1, 6]}}
    n_splits = 6

def main():
    target = "norm_abs_error"
    target_label = "abs_error"
    model = "soap" # other options: "ngram", "mbtr", "atomic"
    #rsc.main(target, model=model, random_state=random_state_dict[model])
    co.get_all_values(model, target, target_label, skip=True)

if __name__ == "__main__":
    main()

