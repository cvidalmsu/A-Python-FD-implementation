# A-Python-QX-implementation

This repository is hosting the source code and scripts implementing QuickExplain and Parallel QuickExplain, the scripts allows the following paramenter:

* model: A CNF file depicting the constraints representing the background knowledge for the algorithm (e.g. the constraints in a feature model)
* product: A CNF file representing the product selection or user requirements to look for the confict set. 
* lmax: The number of look aheads to perform per step in the algorithm
* solver: The backend solver to use, we support at this time, Glucose3, Sat4j and Choco. 
* difficulty: A parameter to inject more difficult consistency checks, any integer representing secods can be used (dafaullt to zero)

Also, the following scripts are provided:
* fastdiag.py: The implementation of the traditional FastDiag algorithm.
* fastdiag_parallel_mp.py: An implementation o the Parallel FastDiag relying on the multiprocessing python package. 

Finally, also provide:
 * A set of models with a fixed set of conflict sets. 
 * The results shown in the associated paper. 
