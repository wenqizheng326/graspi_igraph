# graspi_igraph

Python-Igraph is a graph-based library contender for the library that works with the GraSPI package. 

This repository contains the implementation to test basic algorithm requirements that need to be met for this package to work similarly to GraSPI.
The basic algorithm requirements include:
  -  Construction of graphs
  -  Graph Filtering
  -  Determine the number of connected components
  -  Determine the shortest path from the bottom boundary to all black vertices until the white vertices are met
  -  Graph visualization

## Installation
First, you'd need to clone the repo by running the following command in your command line:
```
git clone git@github.com:wenqizheng326/graspi_igraph.git
```
**Note: You'd need git installed on your system first**
<br />
<br />
  If you do not have git installed or run into issues with git, please visit: https://github.com/git-guides/install-git
<br />
<br />
Next, you'd need to navigate to the cloned repo using terminal. An example would be:
```
cd /path/graspi_igraph
```
Once navigated to the repo, downloads needed can be found in requirements.txt and can be installed by:
```
pip install -r requirements.txt
```
**Note: you must have Python and pip installed onto your system**
<br />
<br />
  If you do not have Python installed, please visit: https://www.python.org/downloads/
<br />
<br />
  If you do not have pip installed or are running into issues with pip, please visit: https://pip.pypa.io/en/stable/installation/
<br />
<br />
  If there are any other issues with installation, please visit: https://python.igraph.org/en/stable/ 

## Running memory tests
First, make sure you're on the memoryFix branch of the repo by running
```
git checkout memoryFix
```
After checking out the branch, you can now run the memory tests
<br />
<br />
To run memory tests, run the following command in terminal:
```
python main.py n dimension function
```
**Make sure of the following:**
  -  Replace "n" with the size of the graph you want. Note: n should be between 1-1000 inclusively 
  -  Replace "dimension" with 2D or 3D to specify if you want a 2D or 3D graph
  -  Replace "function" with either generate, filter, or shortest_path, to choose which function you want to test memory for
 
<br />**An example of a correct command would be:**
```
python main.py 10 2D generate
```
## Outputs
After running this command, you should see
```
Generating results
```
Followed by the results after some time
<br />
<br />
Finally, the following message will be printed out:
```
Completed
```
To know that the tests have been completed
