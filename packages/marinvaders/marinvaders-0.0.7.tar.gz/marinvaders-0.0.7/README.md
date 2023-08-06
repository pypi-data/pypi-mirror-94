# Marinvaders

The marinvaders [Marine Invaders] tool is an interactive
tool that process data on marine invasive species from 
existing databases. 

It enables the user to query, visualize and analyse information per 
[marine ecoregion](https://academic.oup.com/bioscience/article/57/7/573/238419),
and create maps that distinguish alien and natives distributions 
of a species. 

Marine Invaders aims to facilitate the development 
of large-scale impact assessments of marine invasive species. 

The Marine Invaders is developed and maintained by the 
[Industrial Ecology Digital Lab](https://iedl.no) 
and *Francesca Research Group???* at the 
[Norwegian University of Science and Technology](https://www.ntnu.edu) 
in Trondheim, Norway. 


## Getting Started

These instructions will get you a copy of the project up and running on
your local machine.

### Installation from PyPI

`pip install marinvaders --upgrade`


## Usage

The marinvaders.ipynb jupyter notebook provides documentation and interactive tutorial on how to use this package.

The notebook is located either at:
https://gitlab.com/dlab-indecol/marinvaders/-/blob/master/marinvaders.ipynb

or ar mybinder:
TODO

## Citations
TODO

## Data sources
* [Marine Ecoregions of the World—MEOW](https://en.wikipedia.org/wiki/Marine_ecoregions)

    Marine ecoregions are ecoregions (ecological regions) of the oceans and seas identified
    and defined based on biogeographic characteristics.

* [OBIS](https://obis.org/)

    OBIS is a global open-access data and information clearing-house on marine biodiversity
    for science, conservation and sustainable development

* [WoRMS](http://www.marinespecies.org/index.php)

    World register of marine species.

* [GISD](http://www.iucngisd.org/gisd/)

    The Global Invasive Species Database is a free, online searchable source of
    information about alien and invasive species that negatively impact biodiversity.

* [Molnar](https://www.conservationgateway.org/ConservationPractices/Marine/Pages/marineinvasives.aspx)

    The global database contains information on over 330 marine invasive species,
    including non-native distributions by marine ecoregion, invasion pathways,
     and ecological impact and other threat scores.
     
## Data wrangling
The Marine Invaders tool currently integrates data on marine 
(invasive) species from four existing databases OBIS, WoRMS, GISD 
and a database by Molnar et al. After selecting an ecoregion,
the [OBIS API v3](https://api.obis.org/) is used to query all 
species for which there is occurrence data within that ecoregion 
in the OBIS database. Each species is then searched for in the 
latter three databases to potentially identify as alien. 
The [WoRMS REST webservice](http://www.marinespecies.org/rest/)
is used to find the establishmentMeans –whether the species is 
flagged as alien or not-, whereas all species included in 
the GISD and Molnar databases as per definition alien. 
These databases provide geographical distributions on different 
scales. The Molnar distributions are on a marine ecoregion level. 
Most of the WoRMS distributions are either IHO Sea Areas, 
Exclusive Economic Zones (EEZ), or an intersect of these, 
and have a Marine Regions Geographic Identifier (MRGID) is easily 
matched to a marine ecoregion by the use of shapefiles. 
GISD does not provide such MRGID’s but instead gives only 
quantitative distributions, such as country names. Most of these 
could still be matched to existing shapefiles by comparing names, 
and subsequently be matched to marine ecoregions. 
All the distributions that could not automatically be matched 
were searched for manually and matched to one or more marine 
ecoregions. 


## Communication, issues, bugs and enhancements

Please use the issue tracker for documenting bugs, proposing enhancements and all other communication related to marinvaders.

## Installation from source code

Alternatively the the software can be installed from source code.
This is good in case of contributing or developing changes.

The project needs Python 3.7 and higher. For this project
we recommend to use 
[Anaconda Python Distribution](https://www.anaconda.com/distribution/).

#### Get copy of source code 
The project is located at https://gitlab.com/dlab-indecol/marine-invaders

Either use Git to clone project or download the source code and unzip.


#### Install packages

Using terminal navigate to marine-invaders directory. 

To install necessary packages use either [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)
the Anaconda package and environment management or 
Python [virtual environment](https://docs.python.org/3/library/venv.html) which is
included in standard library since Python3.
 

Here are steps to create virtual environments for both options.

- conda

    In terminal create new virtual environment inside the marine-invaders directory:

    `conda create --name venv`

    This will create new directory **venv** 
    
    Install required packages:

    `conda install -f -y -q -n venv --file requirements.txt`

   Activate the virtual environment:

    `conda activate venv`

- Python3.7

    In terminal create new virtual environment inside the marine-invaders directory:

    `python3 -m venv env`

    This will create new directory **venv** 

    Activate the virtual environment:

    `source env/bin/activate`

    Install required packages:

    `pip install -r requirements.txt`
    
After installing and activating new environment (Note that the order is different 
in conda and Python) open IPython notebook

`jupyter notebook MarineInvaders.ipynb`

Jupyter is part of Anaconda distribution. If the Python3.7 is used
then Jupyter must be installed in addition. For more information please refer to
[Jupyter project](https://jupyter.readthedocs.io/en/latest/install.html).


## Authors
TODO

## License
This project is licensed under The [3-Clause BSD License](LICENSE.md)



