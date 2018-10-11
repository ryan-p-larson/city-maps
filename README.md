# City-Maps

## Introduction

*To be filled.*

## Step 0: Setup

*Checkout git branch `00-setup` to follow along*.

1. Create a repository on Github.
2. Download repo and change directories into it:
    `git clone xxx@github.com/yyy/repos/zzz && cd zzz`
3. Create directories using the `mkdir` command for the notebook/scripts, data, and final outputs: 
    `mkdir src data output`.
4. Create a README file using `echo` to write text to a Markdown file: 
    `echo '# City-Maps' >> README.md`
5. Create a `Makefile` using the `touch` command:
    `touch Makefile`
6. Create a new Python environment using `conda`
    - Add the 'Conda Forge' channel to `.condarc` to fix Geopandas issue with mixing channels: `conda config --add channels conda-forge`
    - Create a new conda environment, installing Geopandas and Jupyter packages: `conda create -n city-maps -c conda-forge python=3.6 geopandas jupyter`
    - Export Conda environment: `conda env export > environment.yml`
7. Add base files to git:
    `git add Makefile README.md environment.yml`


