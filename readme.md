### <p align="center">Work in progress</p>

## About
Source code for a research project which forecasts the viability of a single parameter cosmological model in F(Q) geometry that mimics a ΛCDM background using gravitational waves.


## Table of contents
- [Repository outline](#repository-outline)
- [Virtual environment](#virtual-environment)
  - [Dependencies](#dependencies)
  - [Replicate virtual environment](#replicate-virtual-environment)
- [Reproducing the results](#reproducing-the-results)
- [Credits](#credits)
- [License](#license)


## Repository outline
(...)


## Virtual environment
This virtual environment was created using [micromamba](https://mamba.readthedocs.io/en/latest/), a C++ package manager which is fully compatible with the well known [conda](https://docs.conda.io/) package manager.

### Dependencies
The packages that were (explicitly) used are the following:
- [cosmocatalog](https://github.com/jpmvferreira/cosmocatalog)
- [ezmc](https://github.com/jpmvferreira/ezmc)

If you don't want to fully replicate the virtual environment, then installing these two packages is enough.

### Replicate virtual environment
To replicate the virtual environment start by cloning this repository locally:
```console
$ git clone https://github.com/jpmvferreira/forecasting-viable-FQ-cosmology-with-GW fqgw
```

Then, assuming that you are using `conda`, create a new environment from `venv/environment.yml`:
```console
$ conda env create -f fqgw/venv/environment.yml
```

Activate on this newly created environment:
```console
$ conda activate fqgw
```

And finally, install all packages managed by `pip`:
```console
$ pip install -r fqgw/venv/requirements.txt
```


## Reproducing the results
(...)


## Credits
The contents on this repository are being developed by myself. You can contact me in the following ways:
- Institutional email: [joseferreira@alunos.fc.ul.pt](mailto:joseferreira@alunos.fc.ul.pt) - [[PGP key](https://pastebin.com/rfBpi8jc)]
- Personal email: [jose@jpferreira.me](mailto:jose@jpferreira.me) - [[PGP key](https://pastebin.com/REkhQKg2)]

This work is being carried out for an on-going research project, which is being supervised by:
- José Mimoso
- Nelson Nunes
- Tiago Barreiro


## License
[MIT](./license.md)
