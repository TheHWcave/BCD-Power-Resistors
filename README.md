# BCD-Power-Resistors
Combinations of BCD (1,2,4,8  and 10,20,40,80) power resistors

Python 3.x program to print out:

1: all unique combinations of 1,2 4, and 8 Ohm power resistors and their overloading capability (assuming that all 4 resistors have the same watt rating)

2: same as 1 but for 10,20,40, and 80 Ohm 

3: a table with targets from 0.1 Ohm to 165 Ohm in 0.1 Ohm steps were each line shows:
- the target 
- the error in % of a combination of 1,2,4,8 and 10,20,40,80 Ohm resistors that comes closest to the target
- the required combination for the 1,2,4,8 set
- the required combination for the 10,20,40,80 set
Note, the output of a line is suppressed if no combination comes within 5% of the target.

The program is called: resist-comb.py

a sample output is: BCD_Resistors.txt
