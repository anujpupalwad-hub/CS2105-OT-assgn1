# CS2105-OT-assgn1
# Big-M Simplex Method

## Problem

Maximize:

Z = 40x1 + 30x2

Subject to:

2x1 + 3x2 <= 12
2x1 + x2 <= 8
x1 >= 1
x2 >= 1

x1, x2 >= 0

## Method

The problem is solved using the Big-M Simplex Method.

The program handles:

- <= constraints using slack variables
- >= constraints using surplus and artificial variables
- = constraints using artificial variables

## Programming Language

Python

## Libraries

- NumPy

## Result

Optimal solution:

x1 = 3
x2 = 2

Maximum Profit = 180
