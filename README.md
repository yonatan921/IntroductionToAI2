# Project Assignment Two - Introduction to AI

## Cooperating and adversarial agents in the MAPD problem using Python 3.8

### Overview

This project aim's to solve the MAPD problem with two agents playing together in the same world. The project deals with 3 different types of relations between the agents: Adversarial, Cooperative and Semi-Cooperative ,  using various algorithms implemented in Python 3.8. 

### Getting Started

To run the program, follow the steps below:

1. Ensure you have Python 3.8 installed on your system.


## How to run

run main with the example text you want as input and type of agents you want: "cooperative, semi, adversarial".

for example:

```bash
python3 main.py --file "example.txt" --utility "adversarial"
```

## Explanation for the heuristic evaluation function
The heuristic function we used is:

IS = 1 point for delivered package + 0.5 point for carry package + 0.25 for unpicked package.

this heuristic function was suggested by the teacher in class, and also good enough for our project, because it encourages the agents to pick and deliver packages for themselves, and help/avoid other agents to pick/deliver packages according to the part of agent it is. 
## Running examples
Running examples in output_adversarial, coperative, semi.txt files.

we can see that for the same input all three agents act differently.
