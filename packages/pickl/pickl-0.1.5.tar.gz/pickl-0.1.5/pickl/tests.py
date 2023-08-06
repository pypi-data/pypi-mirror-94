from methods import *
def do_tests(iters):
    print("Nilakantha: "+str(nkpi(iters, 1000)))
    if(iters < 511):
        print("Archimedes: "+str(ampi(iters, 1000)))
    else:
        print("Resorting to iterations=511 for Archimedes due to a ValueError occuring if the value is higher.")
        print("Archimedes: "+str(ampi(511, 1000)))
    print("Gauss-Legendre: "+str(galpi(iters, 1000)))
    print("Gregory-Leibniz: "+str(grlpi(iters, 1000)))
    
do_tests(1000)
