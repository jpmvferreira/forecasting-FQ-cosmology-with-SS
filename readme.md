## About
Source code for a research project which forecasts the viability of a single parameter cosmological model in F(Q) geometry that mimics a ΛCDM background using gravitational waves.


## Table of contents
- [Repository outline](#repository-outline)
- [Virtual environment](#virtual-environment)
  - [Dependencies](#dependencies)
  - [Automated install with conda/pip](#automated-install-with-conda/pip)
- [Reproducing the results](#reproducing-the-results)
- [Release cycle](#release-cycle)
- [Credits](#credits)
- [License](#license)


## Repository outline
(...)


## Virtual environment
This virtual environment was created using [micromamba](https://mamba.readthedocs.io/en/latest/), a drop-in C++ replacement which is fully compatible with the well known [conda](https://docs.conda.io/) package manager, with a more minimal footprint.

### Dependencies
The packages that were (explicitly) used were the following:
- [cosmocatalog](https://github.com/jpmvferreira/cosmocatalog)
- [ezmc](https://github.com/jpmvferreira/ezmc)

### Automated install with conda/pip
To replicate the virtual environment start by cloning and cd in this repository:
```console
$ git clone https://github.com/jpmvferreira/forecasting-viable-FQ-cosmology-with-GW fqgw
```

Then, assuming that you are using `conda`, create a new environment from `env/environment.yml`:
```console
$ conda env create -f fqgw/env/environment.yml
```

You can now activate on this newly created environment:
```console
$ conda activate fqgw
```

And finally get all of the packages managed by `pip`:
```console
$ pip install -r fqgw/env/requirements.txt
```


## Reproducing the results
(...)


## Release cycle
If a paper were to be release as the outcome of this project then this repository would freeze the branch corresponding to that paper version. So branch v1 will be the v1 of the paper, which will be frozen as soon as that version is to come out, if a revision is required then a different branch, in this case v2, would be created and work would be carried out there.

As such you can always be assured that the source code for a given paper version will always remain the same.


## Credits
The contents on this repository was developed by myself. You can contact me in the following ways:
- Institutional email: [joseferreira@alunos.fc.ul.pt](mailto:joseferreira@alunos.fc.ul.pt) - [[PGP key](https://pastebin.com/rfBpi8jc)]
- Personal email: [jose@jpferreira.me](mailto:jose@jpferreira.me) - [[PGP key](https://pastebin.com/REkhQKg2)]

This work is being carried out for an on-going research project, supervised by:
- José Mimoso
- Nelson Nunes
- Tiago Barreiro


## License
[MIT](./license.md)
