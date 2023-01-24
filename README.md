## Simplex Algorithm
This is an implementation of the Simplex method, used for large linear optimization problems with several variables. Given $f: \mathbb{R}^n \longrightarrow \mathbb{R}$ a linear function, $A \in \mathbb{R}^{m \times n}$ a matrix and $b \in \mathbb{R}^n$, considering $x \in \mathbb{R}^n$ the variables to optimize and $Ax = b$ the constraints that must hold, the problem that this program solves is the minimization of $f(x)$.

## Use
The optimization problems are written in the ```pm21_pràctica_ASP1_dades.txt``` file. The problem selected is determined in the ```llegeix_dades.py``` file, where a student number (between 1 and 64) and a problem number (between 1 and 4) have to be chosen. These two values are defined by the variables ```numero_estudiant``` and ```numero_problema```, respectively.

## Authors
Alessandro Valls Pau and Martí Batista Obiols
