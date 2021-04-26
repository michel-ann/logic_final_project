# logic_final_project

Hello! This is the final project for Logic and Computation Spring 2021.

The file within this repository is the implementation of a Z3 SMT solver using Python. 
Here is a download page for Z3 python: https://github.com/Z3Prover/z3
  To use it, simply open a python file and include the header "from z3 import *"

It is used to solve the Thinkominos puzzle: http://www.virtualtoychest.com/p/puzzles/thinkominos/thinkominos.html

Our first attempt at this solver is shown in attempt1.py but it was later scrapped 

Next, we tried another implementation but it turned out to be ooverly complicated, and is shown in attempt2.py

The current / final version of the solver is in finalAttempt.py
Note: This does not actually work - it never returns the final solution because there is an error in the 
        rotations constraint. However, the implementation itself is correct and the general layout of the 
        program would have worked 
