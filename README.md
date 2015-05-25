# Socio Spatial Stratification in cities

Python scripts and data necessary to reproduce the results from the paper "Socio-spatial stratification in cities"

If you find this code useful in your research, please let me
know. **If you use a significant part of this code in a publication, please cite**

[citation here]

**Important note:** If you want to apply the methodoly used in the paper rather
than simply reproduce the results, check out
[Marble](https://github.com/scities/marble), a python library to analyse
residential segregation.

## Dependencies

You will need  *GNU Make* and *curl* installed on your machine (this should be
the case if your machine runs linux. Otherwise [Google](http://www.google.com)
is your best friend).  This was tested on Arch Linux and Python 2.7.9. Feel free
to start an issue if you cannot run the code.

To install the python libraries necessary to run the code, go to the cloned folder and type in command line

```bash
pip install -r requirements.txt
```

## Use

Clone the repository, go into the corresponding folder and type 

```bash
make
```

in the console. The programme will prepare the data, perform the analysis and plot the figures in the folder 'figures'.

## Authors and License

Author: Rémi Louf <remi.louf@sciti.es>  
License: BSD
