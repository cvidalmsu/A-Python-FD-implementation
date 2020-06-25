from pysat.solvers import Glucose3
import pickle as pickle
import sys
import os
import tempfile
from pysat.formula import CNF
import time
import itertools
import numpy as np

def getHash(C,l):
    CC = []
    for i in sorted(C):
        if i[0] >= l:
            CC.append(i)

    return str(CC)

def union(A,B):
    res=[]
    for X in A:
        res.extend(X)
    for X in B:
        res.extend(X)
    return res

def is2DList(matrix_list):
  if isinstance(matrix_list[0], list):
    return True
  else:
    return False

def DiffSet(A,B):
    if (is2DList(A)):
        lA = list(itertools.chain.from_iterable(A))
    else:
        lA = A

    if B==[]:
        return lA

    if (is2DList(B)):
        lB = list(itertools.chain.from_iterable(B))
    else:
        lB = B
    
    if lB==[]:
        return lA
    
    li_dif = [item for item in lA if item not in lB]    
    return li_dif
    
def Diff(x, y): 
    li_dif = [item for item in x if item not in y]
    return li_dif

def consistencyCheck(AC,solver,difficulty):
    if solver == "Sat4j":
        f = tempfile.NamedTemporaryFile()
        cnf = CNF()
        for clause in AC: #AC es conjunto de conjuntos
      #      print(clause[1])
            cnf.append(clause[1])#añadimos la constraint
        cnf.to_file(f.name)
        starttime = time.time()
        out=os.popen("java -jar org.sat4j.core.jar "+f.name).read()
        f.close()
        reqtime = time.time() - starttime
        time.sleep(reqtime*difficulty)
        if "UNSATISFIABLE" in out:
#            print("===> AC: " + str(AC) + " - False")
            return False
        else:
 #           print("===> AC: " + str(AC) + " - True")
            return True
        
    elif solver == "Glucose3":
        g = Glucose3()
        for clause in AC: #AC es conjunto de conjuntos
            g.add_clause(clause[1])#añadimos la constraint
        starttime = time.time()
        sol=g.solve()
        reqtime = time.time() - starttime
        time.sleep(reqtime*difficulty)
        return sol
    elif solver == "Choco4":
        f = tempfile.NamedTemporaryFile()
        cnf = CNF()
        for clause in AC: #AC es conjunto de conjuntos
            cnf.append(clause[1])#añadimos la constraint
        cnf.to_file(f.name)
        starttime = time.time()
        out=os.popen("java -jar choco4solver.jar "+f.name).read()
        f.close()
        reqtime = time.time() - starttime
        time.sleep(reqtime*difficulty)
        if "UNSATISFIABLE" in out:
            return False
        else:
            return True
    else :
        raise ValueError("Solver not defined")
    
