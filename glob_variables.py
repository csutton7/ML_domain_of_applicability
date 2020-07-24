
class _GLOB:
    root_path_dir = "."
    
    scale_value = 1000.0 # could also be 1.0
    filter_value = 0.024915234375000001*scale_value
    
    random_state_dict = {"mbtr": 4, "soap": 4, "ngram": 14, "atomic":2}
    random_state = None
    
    skip_dict = {"mbtr": {"norm_abs_error":[1, 4]},
                "soap": {"norm_abs_error":[5, 1]},
                "ngram":{"norm_abs_error":[4]},
                "atomic": {"norm_abs_error":[1, 6]}}

    n_splits = 6
