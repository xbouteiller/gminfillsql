# Program for filling a sqllite database for the gmin allometric measures

Version : **0.1**


## How to install?

### Install Python version if needed

[Anaconda](https://www.anaconda.com/products/individual)

[Miniconda](https://docs.conda.io/en/latest/miniconda.html)


### Download full folder from git

1. Direct download

From the green box  named 'clone' in the right corner > download .zip

2. From the terminal

>
> git clone https://github.com/xbouteiller/gminfillsql.git
>


### Program Execution

>
> python setup.py install
>


### Installing updates

>
> git pull origin main
>
> python setup.py install
>

<br> </br>


## How to use?

<img src="img/Screenshot from 2021-10-08 10-42-40.png" width="75%" height="75%">

The program is designed for gathering morphometric measurements of the samples placed in the gmin climatic chambers.

At any time you can't enter **exit** in order to go back to the main menu

### Categorical features are:
- Campaign name
- Site
- Treatment
- Tree number
- Repetion number
<br> </br>

### Numerical features are:
- Length of the leaf or needle
- Width of the leaf or needle 
- Thickness of the leaf or needle
- Fresh weight
- Output weight
- Dry weight
<br> </br>

### Five choices are available:
- Instantiate or complete a data base, features of every individual are asked but you can let empty cells
- Modidy some value
- Create or complete a second table within the db containing informations (campaign, site, X & Y coordinates, temperature, hygro)
- Modify or complete a whole feature, it is possible to do it for a specific site or from a unique key number to the end
- Exit, print a summary and save a csv file
<br> </br>

### Five choices are available:
- Instantiate or complete a data base, features of every individual are asked but you can let empty cells
- Modidy some value
- Create or complete a second table within the db containing informations (campaign, site, X & Y coordinates, temperature, hygro)
- Modify or complete a whole feature, it is possible to do it for a specific site or from a unique key number to the end
- Exit, print a summary and save a csv file



