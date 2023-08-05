def _fit_method_exception_msg(passed):
    print(
        f"Only 'advi', 'low_rank', and 'nf_block_ar' are supported, but you passed {passed}"
    )
