from pysat.formula import CNF
from pysat.solvers import Glucose3
import utils
import sys
import time
count=0

def callConsistencyCheck(D, AC):
	global count,solver,difficulty
	count=count+1
	for _ in range(lmax):
		utils.getHash(AC,len(modelCNF.clauses))
	sol=utils.consistencyCheck(AC,solver,difficulty)
#	print("Consistency: " + str(D) + ": " + str(sol))
	return sol

def fastDiag(S, AC):
	if len(S)==0 or not callConsistencyCheck([], Diff(AC,S)):
		return []
	else:
		return diag([],S,AC)
	
def diag(D, S, AC):
	if len(D)!=0 and callConsistencyCheck(D, AC):
		return []
		
	if len(S)==1:
		return S
		
	k=int(len(S)/2)
	S1=S[0:k]
	S2=S[k:len(S)]
	A1=diag(S2,S1,Diff(AC,S2))
	A2=diag(A1,S2,Diff(AC,A1))
	return A1 + A2

def Diff(li1, li2): 
    li_dif = [i for i in li1 + li2 if i not in li1 or i not in li2] 
    return li_dif 

if __name__ == '__main__':

	if len(sys.argv) > 1:
		model=sys.argv[1]
		requirements=sys.argv[2]
		lmax=int(sys.argv[3])
		solver=sys.argv[4]
		difficulty=int(sys.argv[5])

	else : #Default values
		lmax=int(2)
		requirements="./cnf/paperA/p1.prod"
		model="./cnf/paperA/fm.cnf"
		solver="Sat4j"
		difficulty=int(0)

modelCNF = CNF(from_file=model)
requirementsCNF = CNF(from_file=requirements)
#print(str(len(modelCNF.clauses)))
M_C=sorted(enumerate(modelCNF.clauses), key=lambda x: x[0])
RQ_C=sorted(enumerate(requirementsCNF.clauses,len(modelCNF.clauses)), key=lambda x: x[0])

starttime = time.time()
result= fastDiag(RQ_C, M_C + RQ_C)
reqtime = time.time() - starttime
print(model+"|"+requirements+"|"+str(reqtime)+"|"+str(count)+"|"+str(count)+"|"+str(lmax)+"|FMDiag|"+solver+"|"+str(difficulty)+"|"+str(result))