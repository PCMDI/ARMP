# Atmospheric River Metrics Package (ARMP)



[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.14188790.svg)](https://doi.org/10.5281/zenodo.14188790)



## Reference 

Dong, B., Ullrich, P., Lee, J., Gleckler, P., Chang, K., and O'Brien, T. A.: A new metrics framework for quantifying and intercomparing atmospheric rivers in observations, reanalyses, and climate models, Geosci. Model Dev., 18, 961–976, https://doi.org/10.5194/gmd-18-961-2025, 2025.

## Documentation

Please see the [Wiki](https://github.com/PCMDI/ARMP/wiki) tab of this GitHub repository, which include the following pages.

* [Installation](https://github.com/PCMDI/ARMP/wiki/Installation)
* [User manual](https://github.com/PCMDI/ARMP/wiki/User-Instructions)
* [Demo Notebook](https://nbviewer.org/github/PCMDI/ARMP/blob/main/ARMP/doc/demo_AR_peak_day_metrics.ipynb)
* [Known issue](https://github.com/PCMDI/ARMP/wiki/Known-issues)


## Key Dependencies

- xarray
- xcdat
- eofs
- numpy
- regionmask
- matplotlib

(See [`environment.yml`](installation/environment.yml) for details.)

## Acknowledgement

Content in this repository is developed by climate and computer scientists from the Program for Climate Model Diagnosis and Intercomparison ([PCMDI][PCMDI]) at Lawrence Livermore National Laboratory ([LLNL][LLNL]). This work is sponsored by the Regional and Global Model Analysis ([RGMA][RGMA]) program, of the Earth and Environmental Systems Sciences Division ([EESSD][EESSD]) in the Office of Biological and Environmental Research ([BER][BER]) within the [Department of Energy][DOE]'s [Office of Science][OS]. The work is performed under the auspices of the U.S. Department of Energy by Lawrence Livermore National Laboratory under Contract DE-AC52-07NA27344.

<p>
    <img src="https://pcmdi.github.io/assets/PCMDI/100px-PCMDI-Logo-NoText-square-png8.png"
         width="65"
         style="margin-right: 30px"
         title="Program for Climate Model Diagnosis and Intercomparison"
         alt="Program for Climate Model Diagnosis and Intercomparison"
    >&nbsp;
    <img src="https://github.com/PCMDI/assets/blob/main/DOE/480px-DOE_Seal_Color.png?raw=true"
         width="65"
         style="margin-right: 30px"
         title="United States Department of Energy"
         alt="United States Department of Energy"
    >&nbsp;
    <img src="https://github.com/PCMDI/assets/blob/main/LLNL/212px-LLNLiconPMS286-WHITEBACKGROUND.png?raw=true"
         width="65"
         title="Lawrence Livermore National Laboratory"
         alt="Lawrence Livermore National Laboratory"
    >
</p>


[PCMDI]: https://pcmdi.llnl.gov/
[LLNL]: https://www.llnl.gov/
[RGMA]: https://climatemodeling.science.energy.gov/program/regional-global-model-analysis
[EESSD]: https://science.osti.gov/ber/Research/eessd
[BER]: https://science.osti.gov/ber
[DOE]: https://www.energy.gov/
[OS]: https://science.osti.gov/
