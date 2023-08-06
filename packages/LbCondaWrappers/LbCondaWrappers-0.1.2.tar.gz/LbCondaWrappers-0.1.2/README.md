# LHCb Conda Wrappers

Wrapper scripts for providing access to conda environments which are installed on CVMFS.

## Standard Usage

The main environment provided is named `default` and aims to provide most software tools that will be needed for analaysis that is performed outside of the standard LHCb software stack.
This includes a recent version of Python 3, ROOT, Snakemake, jupyterlab, matplotlib, scikit-learn, tensorflow and many more.

### Basic usage

Environments can be activated using the `lb-conda` command which works similarly to `lb-run`.
To launch a `bash` shell inside the default environment run:

```bash
$ lb-conda default bash
[bash-5.0]$ python --version
Python 3.7.6
[bash-5.0]$ root --version
ROOT Version: 6.20/04
Built for linuxx8664gcc on Apr 20 2020, 15:03:00
From @
```

Alternative commands can be ran directly using:

```bash
$ lb-conda default python -c 'import math; print(math.sqrt(2))'
1.4142135623730951
```

### Including texlive

A fully featured texlive installation is not included in any of the environments due to it's large size however one can be added by passing the `--texlive` argument.

```bash
$ lb-conda --texlive default latex --version
pdfTeX 3.14159265-2.6-1.40.21 (TeX Live 2020)
kpathsea version 6.3.2
Copyright 2020 Han The Thanh (pdfTeX) et al.
There is NO warranty.  Redistribution of this software is
covered by the terms of both the pdfTeX copyright and
the Lesser GNU General Public License.
For more information about these matters, see the file
named COPYING and the pdfTeX source.
Primary author of pdfTeX: Han The Thanh (pdfTeX) et al.
Compiled with libpng 1.6.37; using libpng 1.6.37
Compiled with zlib 1.2.11; using zlib 1.2.11
Compiled with xpdf version 4.02
```

### Versioning

Occasionally new versions of the `default` environment will be made to add new packages and generally keep it up-to-date.
If you wish to use an older version you can list the available versions using:

```bash
$ lb-conda --list default
2019-12-26
2020-05-14
```

The `2020-05-14` version can explicitly chosen using:

```bash
$ lb-conda default/2020-05-14 bash
```

### Customising

As the conda environment used is installed on the read-only CVMFS filesystem the usual `pip install` and `conda install` commands will not work.
Two options are provided to allow environments to be customised.

### Installing additional python packages

This is the preferred option as most data will be kept on CVMFS and works by creating a virtual environment on top of the CVMFS installed environment.
It is however limited to only allowing `pip` installed Python packages and locally built software.

To create the virtual environment in a local directory ("my-local-directory") run

```bash
$ lb-conda-dev virtual-env default my-local-directory
```

The environment can now be used similarly to `lb-conda default` using the `run` script:

```bash
$ my-local-directory/run bash
```

To upgrade the `uproot` Python package run:

```bash
$ my-local-directory/run bahs
[bash-5.0]$ python -c 'import uproot; print(uproot.__version__)'
3.11.6  # <- Original version
[bash-5.0]$ pip install --upgrade uproot
Collecting uproot
# Truncated output
Successfully installed uproot-3.11.7
[bash-5.0]$ python -c 'import uproot; print(uproot.__version__)'
3.11.7  # <- New version
```

To install a locally compiled application in the virtual environment you should set the install prefix to be the absolute path to your local directory.
How this is done will depend on the build system used by the specific application.

### Fully customising an environment

This option is discouraged, especially when running on AFS/EOS as it will result in a large amount of data and many small files being copied to your local directory.
It does however allow you to completely clone the environment and then make any modifications.

TODO: This is not currently documented...

## Advanced usage

### Using non-default environments

To see the full list of available environments run:

```bash
$ lb-conda --list
B2OC/b2dstdspi-gpu
B2OC/b2dstdspi
Charm/D02KsHH
Semilep/rdst
default
DPA/analysis-productions-certification
DPA/analysis-productions
```

A custom environment can then be chosen using it's name:

```bash
$ lb-conda Charm/D02KsHH python --version
Python 3.6.5 :: Anaconda, Inc.
```

### Suggesting new or upgraded packages in the default environment

Please open an issue [here](https://gitlab.cern.ch/lhcb-core/conda-environments/-/issues) explaining what should be added/upgraded and why.

### Adding new environments to CVMFS

This is not yet widely available available.
If you have a strong reason to add an environment please open an issue [here](https://gitlab.cern.ch/lhcb-core/conda-environments/-/issues) to explaing what your requirements are.
