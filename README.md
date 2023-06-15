## About
Source code for the article "Forecasting F(Q) cosmology with ΛCDM background using standard sirens".

Available under an APS subscription at [PhysRevD.105.123531](https://journals.aps.org/prd/abstract/10.1103/PhysRevD.105.123531) and for free at [arXiv:2203.13788](https://arxiv.org/abs/2203.13788) (both include the same version of the document)


## Table of contents
- [Repository outline](#repository-outline)
- [Virtual environment](#virtual-environment)
  - [Dependencies](#dependencies)
  - [Replicate virtual environment](#replicating-the-virtual-environment)
- [Reproducing the results](#reproducing-the-results)
- [Citation](#citation)
- [Feedback](#feedback)
- [License](#license)


## Repository outline
`/analyzed`: Includes catalog and corner plots, which are analyzed by `simplemc`.
`/aux`: A set of auxiliary scripts to aid in analysis or automation, which can be easily ignored by an external user.
`/config`: The configuration files location used by the `simplemc` samplers.
`/cosmology`: Custom cosmological models to be used by `gwcatalog` when generating standard sirens mock catalogs. Can be ignored by an external user.
`/data`: All of the datasets used throughout our analysis, either real or generated.
`/model`: The cosmological models to be constrained using `simplemc`.
`/output`: The output of the MCMC performed by `simplemc`.
`/venv`: Files related to the virtual environment used to develop our analysis.

The corresponding file to each of the catalogs used are:
- ET: `data/ET-4.csv`
- LISA (best): `data/LISA-9`
- LISA (median): `data/LISA-10`
- LISA (worst): `data/LISA-12`
- LIGO (best): `data/LIGO-13`
- LIGO (median): `data/LIGO-1`
- LIGO (worst): `data/LIGO-2`


## Virtual environment

### Dependencies
Besides a working Python environment, the packages explicitly being used are:
- [gwcatalog](https://github.com/jpmvferreira/gwcatalog) (v1): Generate catalogs of standard siren events.
- [simplemc](https://github.com/jpmvferreira/simplemc) (v1): A CLI that simplifies the usage of MCMC methods.

Although developed in the context of this work, these packages are completely independent.

If you don't wish to fully replicate the virtual environment, then installing the dependencies listed before will suffice.

### Replicating the virtual environment
Start by cloning this repository locally using `git` to a folder named "fqgw":
```console
$ git clone https://github.com/jpmvferreira/forecasting-FQ-cosmology-with-SS fqgw
```

Use `conda` (or any other compatible package manager) to create a new virtual environment from the file `fqgw/venv/environment.yml`, which we will call "fqgw":
```console
$ conda env create -f fqgw/venv/environment.yml
```

Activate the newly created environment:
```console
$ conda activate fqgw
```

Use `pip` to install all Python packages listed in `fqgw/venv/environment.yml`:
```console
$ pip install -r fqgw/venv/requirements.txt
```


## Citation
If you used any of the contents available in this repository, or found it useful in any way, you can cite it using the following BibTeX entry:
```
@article{PhysRevD.105.123531,
  title = {Forecasting $F(Q)$ cosmology with $\mathrm{\ensuremath{\Lambda}}\mathrm{CDM}$ background using standard sirens},
  author = {Ferreira, Jos\'e and Barreiro, Tiago and Mimoso, Jos\'e and Nunes, Nelson J.},
  journal = {Phys. Rev. D},
  volume = {105},
  issue = {12},
  pages = {123531},
  numpages = {10},
  year = {2022},
  month = {Jun},
  publisher = {American Physical Society},
  doi = {10.1103/PhysRevD.105.123531},
  url = {https://link.aps.org/doi/10.1103/PhysRevD.105.123531}
}
```


## Feedback
Any discussion, suggestions or bug reports are always welcome. To do so, feel free to use this issue section in this repository, or even send me an email at:
- Personal email: [jose@jpferreira.me](mailto:jose@jpferreira.me) - [[PGP key](https://pastebin.com/raw/REkhQKg2)]
- Institutional email: [jpmferreira@fc.ul.pt](mailto:jpmferreira@fc.ul.pt) - [[PGP key](https://pastebin.com/raw/AK2trPBw)]


## License
All of the contents provided in this repository are available under the MIT license.

For further information, refer to the file [LICENSE.md](./LICENSE.md) provided in this repository.
