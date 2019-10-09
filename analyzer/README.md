# Analyzer

This folder contains two scripts: **federated_visualize.py** permits to analyze tests carried out on a Federated Learning Architecture, while **gossip_visualize.py** to analyze tests executed on the Gossip Learning Architecture.

## Federated Visualize
This permits to calculate 4 indices passing as argument the directory path containing a Federated Learning Architecture that has been put in execution for some time: 
- **Value of max accuracy reached**
- **Value of min accuracy reached**
- **Iteration of max accuracy reached**
- **Iteration of min accuracy reached**

It also prints a plot showing how accuracy have changed during the test.

## Gossip Visualize
This permits to calculate 7 indices passing as argument the directory path containing a Gossip Learning Architecture that has been put in execution for some time: 
- **Mean number of unique peers contacted by a node**
- **Mean number of unique peers suggested by a node**
- **Mean number of unique peers loaded by a node**
- **Mean value of max accuracy reached**
- **Mean value of min accuracy reached**
- **Mean iteration of max accuracy reached**
- **Mean iteration of min accuracy reached**

It also prints a plot showing how accuracy have changed during the test.
