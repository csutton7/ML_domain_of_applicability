
class _GLOB:
    root_path_dir = "."
    #exchange_value = 1.0 
    exchange_value = 1000.0
    random_state_dict = {"mbtr": 4, "soap": 4, "ngram": 14, "atomic":2}
    random_state = None
    
    skip_dict = {"mbtr": {"norm_abs_error":[1, 4]},
                "soap": {"norm_abs_error":[5, 1]},
                "ngram":{"norm_abs_error":[4]},
                "atomic": {"norm_abs_error":[1, 6]}}

    n_splits = 6
