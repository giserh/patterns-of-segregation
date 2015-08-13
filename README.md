# Patterns of residential segregation

Python scripts and data necessary to reproduce the results of the article
"Patterns of residential segregation" by R. Louf and M. Barthelemy.

If you find this code useful in your research, please let me
know! **If you use a significant part of this code in a publication, please cite**

[citation here]

**Important note:** If you want to apply the methodoly used in the paper rather
than simply reproduce the results, check out
[Marble](https://github.com/scities/marble), a python library to analyse
residential segregation.


## Use

You will need  *GNU Make*, *curl*, *git* and Python 2.7 installed on your machine (this should be
the case if your machine runs linux. Otherwise [Google](http://www.google.com)
is your best friend).  This was tested on Arch Linux and Python 2.7.9. Feel free
to [start an issue](https://github.com/rlouf/socio-spatial-stratification/issues/new) if you cannot run the code.

### Clone the repository

In command line, type

```bash
git clone https://github.com/rlouf/socio-spatial-stratification *your_folder_name*
```

This should download all the files and data necessary to *your_folder_name*.

### Dependencies


To install the python libraries necessary to run the code, go to the cloned folder and type in command line

```bash
pip install -r requirements.txt
```

### Run the analysis

Go into the corresponding folder and type 

```bash
make
```
The programme will prepare the data, perform the analysis and plot the figures in the folder 'figures'.

## Authors and License

Author: Rémi Louf <remi.louf@sciti.es>  
License: BSD
