import matplotlib

matplotlib.use("Agg")  # noqa

import os  # noqa
from itertools import product  # noqa

import numpy as np  # noqa
from matplotlib import pyplot as plt  # noqa

from ARMP.io.input import read_json_file  # noqa
from ARMP.io.output import update_dict_ref  # noqa
from ARMP.io.printting import str_fn, str_print  # noqa
from ARMP.lib.control import iter_list, iter_list_ref, make_case  # noqa
from ARMP.lib.convention import Case  # noqa


def histogram_peak_day(
    dic, dict_in, model, ARDT, region, season, ref=False, model_ref=None
):
    results = dict_in["RESULTS"][model][ARDT][region][season]
    count_mean = results["count_mean"]
    count_std = results["count_std"]
    count_ens = results["count_ens"]

    xt = np.arange(1, 13, 1)
    yr = count_mean

    plt.figure()

    plt.xlabel("month", fontsize=19)
    plt.ylabel("AR counts", fontsize=19)
    plt.title(model + "  " + str_print(region) + "  " + ARDT, fontsize=19)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.ylim(0, 80)  # custom axis limit when needed

    plt.bar(xt, yr, yerr=count_std)

    nyear = len(count_ens)
    for j in range(nyear):
        plt.plot(xt, count_ens[j], "o", markersize=2, color="k")

    if ref:
        results_ref = dict_in["REF"][model_ref][ARDT][region][season]
        count_ref = results_ref["count_mean"]

        # add reference data as bar mark
        for k in range(1, 13):
            plt.hlines(count_ref[k - 1], xmin=k - 0.3, xmax=k + 0.3, colors="red")

    plt.tight_layout()

    fig_filename = (
        "histogram_AR_count_" + model + "_" + str_fn(region) + "_" + ARDT + "_" + season
    )
    plt.savefig(os.path.join(dic["dir_fig"], fig_filename, ".png"), dpi=300)

    plt.close()


def plot_histogram_peak_day(dic, metric, ref=False):
    if not ref:
        layout_pool = iter_list(dic)

    else:
        layout_pool, model_ref = iter_list_ref(dic)

        for combi in product(*layout_pool):
            case = make_case(Case, combi, dic)

            model = case.model
            ARDT = case.ARDT
            region = case.region
            season = case.season

            dict_in = read_json_file(dic, metric)

            if not ref:
                histogram_peak_day(dic, dict_in, model, ARDT, region, season)

            else:
                dict_in = update_dict_ref(dic, dict_in)
                histogram_peak_day(
                    dic,
                    dict_in,
                    model,
                    ARDT,
                    region,
                    season,
                    ref=ref,
                    model_ref=model_ref,
                )


# if __name__ == "__main__":
#    metric = "metric_peak_day"
#
#    if not dic["diag_peak_day_histogram"]:
#        # raise FileNotFoundError(f"The file '{file_path}' does not exist.")
#        raise NameError("diag_peak_day_histogram not True")
