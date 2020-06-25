from pysat.formula import CNF
import utils
import random
import sys
import time
import os
import time
count=0

#---------------------------------------------------------
def read_text_file (fname):
    with open(fname) as f:
        content = f.readlines()
    return [x.strip() for x in content] 

def read_DIMACS (fname):
    content=read_text_file(fname)
    variables_total, clauses_total = 0, 0
    clauses=[]
    for c in content[0:]:
        l = c.split(" ")
        if l[0]=="c":
            continue
        elif l[0]=="p" and l[1].lower()=="cnf":
            variables_total, clauses_total = int(l[2]), int(l[3])
        elif l[0] != "":
            clause=[]
            for var_s in l:
                var=int(var_s)
                if var!=0:
                    clause.append(var)
            clauses.append(clause)

    if clauses_total != len(clauses):
        print("warning: header says ", clauses_total, " but read ", len(clauses))
    return variables_total, clauses

def callConsistencyCheck(AC):
	global count,solver,difficulty
	count=count+1
	for _ in range(lmax):
		utils.getHash(AC,len(modelCNF.clauses))
	sol=utils.consistencyCheck(AC,solver,difficulty)
	return sol


def quickXplain(C, B):
	if callConsistencyCheck(B + C):
		return "No Conflict"
	elif len(C)==0:
		return []
	else :
		return QX(C,B,[])
		
	
def QX(C,B,Bo):
	if len(Bo)!=0 and not callConsistencyCheck(B):
		return []
	
	if len(C) == 1:
		return C 
		
	k=int(len(C)/2) 
	Ca=C[0:k]
	Cb=C[k:len(C)]
	A2=QX(Ca,(B+Cb),Cb)
	A1=QX(Cb,(B+A2),A2)
	return (A1 + A2)

if __name__ == '__main__':

	if len(sys.argv) > 1:
		model=sys.argv[1]
		requirements=sys.argv[2]
		lmax=int(sys.argv[3])
		solver=sys.argv[4]
		difficulty=int(sys.argv[5])

	else : #Default values
		lmax=int(1)
		requirements="./cnf/paper0/p1.prod"
		model="./cnf/paper0/fm.cnf"
		solver="Sat4j"
		difficulty=int(0)

	modelCNF = CNF(from_file=model)
	requirementsCNF = CNF(from_file=requirements)
	
	M_C=sorted(enumerate(modelCNF.clauses), key=lambda x: x[0])
	RQ_C=sorted(enumerate(requirementsCNF.clauses,len(modelCNF.clauses)), key=lambda x: x[0])
	
	starttime = time.time()
	result= quickXplain(RQ_C,M_C)
	reqtime = time.time() - starttime
	print(model+"|"+requirements+"|"+str(reqtime)+"|"+str(count)+"|"+str(count)+"|"+str(lmax)+"|qx|"+solver+"|"+str(difficulty)+"|"+str(result))
