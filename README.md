## Simplex Algorithm
This is an implementation of the Simplex method, used for large linear optimization problems with several variables. Given $f: \mathbb{R}^n \longrightarrow \mathbb{R}$ a linear function, $A \in \mathbb{R}^{m \times n}$ a matrix and $b \in \mathbb{R}^n$, considering $x \in \mathbb{R}^n$ the variables to optimize and $A \cdot x = b$ the constraints that must hold, the problem that this program solves is the following:

$$
(P_x) = \left \{ \begin{array}{l}
        \hspace{3mm} \text{min} \hspace{12mm} T_n(y) = \displaystyle\sum_{i = 1}^{n} \frac{\sqrt{(y_i - y_{i - 1})^2 + (x_i - x_{i - 1})^2}}{\sqrt{2gy_{i-1}}} \hspace{33mm} (1) \\ 
        \hspace{1mm} y_i \in \mathbb{R} \\
        %x_{kij} \in \mathbb{R}^3 \\
        \hspace{4mm} s.a. \hspace{27mm} y_i - y_{i - 1} > 0, \hspace{3mm} \forall i \in \{1, ..., n\} \hspace{38mm} (2) \\
        \hspace{37mm} x_i = \displaystyle\frac{i}{n} \hspace{2mm} \forall i \in \{0, ..., n\} \hspace{4mm} (3), \hspace{2mm} y_0 = 0 \hspace{4mm} (4), \hspace{2mm} y_{n} = 1 \hspace{4mm} (5)
    \end{array} \right.
$$ \\

## Use
The optimization problems are written in the ```pm21_pràctica_ASP1_dades.txt``` file. The problem selected is determined in the ```llegeix_dades.py``` file, where a student number (between 1 and 64) and a problem number (between 1 and 4) have to be chosen. These two values are defined by the variables ```numero_estudiant``` and ```numero_problema```, respectively.

## Authors
Alessandro Valls Pau and Martí Batista Obiols
