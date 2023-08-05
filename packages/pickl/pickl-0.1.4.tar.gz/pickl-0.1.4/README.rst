======
Pickle
======

Pickle is a simple live Pi calculator that can run on Casio fx-CG50
calculators or any Casio calculator that has MicroPython.

Documentation
-------------

int ``grlpi(int amount, int precision,o=False)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Calculates pi using the Gregory-Leibniz algorithm.
        

int ``nkpi(int amount, int precision,o=False)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Calculates pi using the Nilakantha algorithm.
        

int ``grlpi(int amount, int precision,o=False)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Calculates pi using the Archimedes algorithm. Cannot go higher than 511 iterations.
        

int ``galpi(int amount, int precision,o=False)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Calculates pi using the Gauss-Legendre algorithm.

