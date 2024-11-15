import xarray as xr

from ARMP.io.output import nc_out
from ARMP.lib.preprocessing import data_QAQC, data_QAQC_mf, freq_convert
from ARMP.lib.proc import init_ds


def LFAR_count(
    fn_list, fn_var, region, season, start_date, end_date, mask_lndocn, **kwargs
):
    globals().update(**kwargs)

    mask_reg, da_occur_ts, count_reg_mp, tag_reg_mpts = init_ds(
        fn_list, region, mask_lndocn, fn_var, **kwargs
    )

    with open(fn_list, "r") as f:
        for fn in f:
            # ---------------------------------------------

            tag_reg_lf = data_QAQC(
                fn.strip(),
                mask_reg,
                region,
                season,
                fn_var,
                start_date,
                end_date,
                **kwargs
            )

            if not tag_reg_lf:
                continue

            # ---------------------------------------------

            occur = tag_reg_lf.any(dim=["lat", "lon"])

            # concat counts along time dimension --> if ar_count_ts:
            da_occur_ts = xr.concat([da_occur_ts, occur], dim="time")

            # =============
            # if out_map_ts:
            # tag_reg_lf_occur = tag_reg_lf.where(da_occur_ts).dropna(dim='time')

            tag_reg_lf_occur = tag_reg_lf.where(occur).dropna(dim="time")
            tag_reg_mpts = xr.concat([tag_reg_mpts, tag_reg_lf_occur], dim="time")

            # =============

            # sum 2D total counts --> need to modify after resampling --> if ar_freq_map
            # count_reg_mp +=  tag_reg_lf.sum(dim='time')

        # freq_reg_mp = count_reg_mp / da_occur_ts.time.size

        # ---------------------------------------------
        # resample to target temporal frequency
        # da_occur_ts = freq_convert(da_occur_ts, fn_freq, target_freq, **kwargs)
        # tag_reg_mpts = freq_convert(tag_reg_mpts, fn_freq, target_freq, **kwargs)
        da_occur_ts = freq_convert(da_occur_ts, **kwargs)
        tag_reg_mpts = freq_convert(tag_reg_mpts, **kwargs)

        # ---------------------------------------------

        freq_reg_mp = tag_reg_mpts.astype(int).sum(dim="time") / tag_reg_mpts.time_size

        if tag_out_ts:  # noqa
            nc_out(da_occur_ts, "occur", "ts.nc", case_name, dir_out)  # noqa
            # da_occur_ts.name = 'occur'
            # fn_out =  "_".join([case_name, da_occur_ts.name, 'ts.nc'])
            # da_occur_ts.to_netcdf(os.path.join(dir_out, fn_out))

        if tag_out_map:  # noqa
            nc_out(freq_reg_mp, "freq", "mp.nc", case_name, dir_out)  # noqa
            # freq_reg_mp.name = 'freq'
            # fn_out =  "_".join([case_name, freq_reg_mp.name, 'mp.nc'])
            # freq_reg_mp.to_netcdf(os.path.join(dir_out, fn_out))

        if tag_out_map_ts:  # noqa
            nc_out(
                tag_reg_mpts,
                kwargs["fn_var_out"],
                "mpts.nc",
                case_name,  # noqa
                dir_out,  # noqa
            )
            # tag_reg_mpts.name = 'tag'
            # fn_out =  "_".join([case_name, tag_reg_mpts.name, 'mpts.nc'])
            # tag_reg_mpts.to_netcdf(os.path.join(dir_out, fn_out))
        # else:
        #    del tag_reg_mpts

    return da_occur_ts, freq_reg_mp, tag_reg_mpts


def LFAR_count_mf(
    fn_list, region, season, fn_var, start_date, end_date, mask_lndocn, **kwargs
):
    globals().update(**kwargs)

    # mask_reg, _, _, _ = init_ds(region, tag_list, tag_var=tag_var, **kwargs)

    # ---------------------------------------------

    tag_reg_lf = data_QAQC_mf(
        fn_list, region, season, fn_var, start_date, end_date, mask_lndocn, **kwargs
    )

    da_occur_ts = tag_reg_lf.any(dim=["lat", "lon"])

    # if out_map_ts:
    tag_reg_mpts = tag_reg_lf.where(da_occur_ts).dropna(dim="time")

    # the following two line only works if data freq matches
    # count_reg_mp +=  tag_reg_lf.sum(dim='time')
    # freq_reg_mp = count_reg_mp / da_occur_ts.time.size

    # resample to target temporal frequency
    # da_occur_ts = freq_convert(da_occur_ts, fn_freq, target_freq, **kwargs)
    # tag_reg_mpts = freq_convert(tag_reg_mpts, fn_freq, target_freq, **kwargs)
    da_occur_ts = freq_convert(da_occur_ts, **kwargs)
    tag_reg_mpts = freq_convert(tag_reg_mpts, **kwargs)

    freq_reg_mp = tag_reg_mpts.astype(int).sum(dim="time") / tag_reg_mpts.time_size

    if tag_out_ts:  # noqa
        nc_out(da_occur_ts, "occur", "ts.nc", case_name, dir_out)  # noqa
        # da_occur_ts.name = 'occur'
        # fn_out =  "_".join([case_name, da_occur_ts.name, 'ts.nc'])
        # da_occur_ts.to_netcdf(os.path.join(dir_out, fn_out))

    if tag_out_map:  # noqa
        nc_out(freq_reg_mp, "freq", "mp.nc", case_name, dir_out)  # noqa
        # freq_reg_mp.name = 'freq'
        # fn_out =  "_".join([case_name, freq_reg_mp.name, 'mp.nc'])
        # freq_reg_mp.to_netcdf(os.path.join(dir_out, fn_out))

    if tag_out_map_ts:  # noqa
        nc_out(
            tag_reg_mpts, kwargs["fn_var_out"], "mpts.nc", case_name, dir_out  # noqa
        )
        # tag_reg_mpts.name = 'tag'
        # fn_out =  "_".join([case_name, tag_reg_mpts.name, 'mpts.nc'])
        # tag_reg_mpts.to_netcdf(os.path.join(dir_out, fn_out))

    return da_occur_ts, freq_reg_mp, tag_reg_mpts
