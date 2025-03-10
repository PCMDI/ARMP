from itertools import product

from ARMP.io.input import read_json_file
from ARMP.io.output import update_dict_ref, update_json_file
from ARMP.lib.control import iter_list_ref, make_case
from ARMP.lib.convention import Case_clim


def Clim_metrics_bias(dic, metric, var_stats):
    """
    add bias result to metrics json file
    e.g., metric_freq, metric_peak_day
    """
    print(f"\ncalculating bias metrics for {dic['clim_var_out']} {var_stats}")

    layout_pool, model_ref = iter_list_ref(dic)

    for combi in product(*layout_pool):
        case = make_case(Case_clim, combi, dic)

        model = case.model
        ARDT = case.ARDT
        region = case.region
        season = case.season

        dict_in = read_json_file(dic, metric)

        dict_in = update_dict_ref(dic, dict_in)

        results = dict_in["RESULTS"][model][ARDT][region][season][case.fn_var_out][
            var_stats
        ]
        results_ref = dict_in["REF"][model_ref][ARDT][region][season][case.fn_var_out][
            var_stats
        ]
        bias = results - results_ref

        var_bias = var_stats + "_bias"
        var_bias_dict = {var_bias: bias}

        dict_in["RESULTS"][model][ARDT][region][season][case.fn_var_out].update(
            var_bias_dict
        )
        update_json_file(dic, metric + "_bias", dict_in)
