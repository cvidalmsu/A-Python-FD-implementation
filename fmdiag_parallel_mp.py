from pysat.formula import CNF
import multiprocessing as mp
import utils
import sys
import time
import os

#-------------------------------------------------------
#------------Auxiliary functions definition-------------
#-------------------------------------------------------
# Function to create a hash. 
def LookUpCC(hash):
	global cache,count
	result=cache.get(hash)
	if result.ready():
		count=count+1
	return result.get()

def existConsistencyCheck(hash):
	return (hash in cache)

#-------------------------------------------------------
#------------Auxiliary Parallel functions definition-------------
#-------------------------------------------------------

def callConsistencyCheck(AC):
	global solver, difficulty
	sol=utils.consistencyCheck(AC,solver,difficulty)
	return sol


def f(AC):
	res=0
	for C in AC:
		res=res+len(C)
	return res
#-------------------------------------------------------
#-----------------QX functions definition---------------
#-------------------------------------------------------
def FDGen(D, S, AC, d, l):
    global genhash, contar
    if l< lmax :
        if f(d)>0 :
 #           print("antes")
            u=utils.DiffSet(AC,D,0)
            if(genhash == ""):
                hash=utils.getHash(u,len(modelCNF.clauses))                
            else:
                hash=genhash
                genhash=""
#            print("despues")
      
            if (not (hash in cache)):#evito crear multiples hilos si ya esta en ejecución
                future=pool.apply_async(callConsistencyCheck,args=([u]))
                cache.update({hash:future})
        
        if f(S)==1 and f(D)>0:
            FDGen([], D, utils.DiffSet(AC,[S[0]], 0),[S[0]],l+1)
        elif f(S)>1 :
            if(len(S)>1):
                k=int(len(S)/2) 
                Sa=S[0:k]
                Sb=S[k:len(S)]
            else :
                k=int(len(S[0])/2) 
                Sa=[S[0][0:k]]
                Sb=[S[0][k:len(S[0])]]
            FDGen(Sb + D, Sa, AC, Sb, l+1)
        if f(D)>0 and f(d)>0  :
#            print("1a - D: " + str(D))
#            print("D[0]: " + str([D[0]]))
#            contar=contar+1
#            print("aqui")
#            if contar==5:
#                print("Acaaaaaaaa " + str(D))
            FDGen(Difff(D,[D[0]]), [D[0]], AC,[],l+1)
            #print("2")

def Difff(x, y): 
#    print("x: " + str(x))
#    print("y: " + str(y))
    
    li_dif = [item for item in x if item not in y]
#    print("diff: " + str(li_dif))
    
    return li_dif

def consistent(D, S, AC):
    global genhash
    genhash=hashAC=utils.getHash(AC,len(modelCNF.clauses))
    if not existConsistencyCheck(hashAC):
        FDGen([D], [S], [AC+D],[D],0)

    return (LookUpCC(hashAC)) #check the shared table	

def fastDiag(S, AC):
	if len(S)==0 or not callConsistencyCheck(Diff(AC,S)):
		return []
	else:
		return diag([],S,AC)
	
def diag(D, S, AC):
    if len(D)!=0 and consistent(D, S, AC):
        return []
    if len(S)==1:
        return S
        
    k=int(len(S)/2)
    S1=S[0:k]
    S2=S[k:len(S)]
    A1=diag(S2,S1,Diff(AC,S2))
    A2=diag(A1,S2,Diff(AC,A1))
    return A1 + A2


def Diff(x, y): 
    li_dif = [item for item in x if item not in y]
    return li_dif

#-------------------------------------------------------
#--------------Gloval variable definition---------------
#-------------------------------------------------------
if __name__ == '__main__':
    lmax=2
    cache={}
    count=0
    contar=1
    genhash=""
    if len(sys.argv) > 1:
        model=sys.argv[1]
        requirements=sys.argv[2]
        lmax=int(sys.argv[3])
        solver=sys.argv[4]
        difficulty=sys.argv[5]
        difficulty=int(sys.argv[5])
    else:
        lmax=int(5)
#        requirements="./cnf/paperB/p1.prod"
#        model="./cnf/paperB/fm.cnf"
        solver="Sat4j"
        difficulty=int(0)
        requirements="./cnf/bench/prod-16-0.prod"
        model="./cnf/bench/model_16.cnf"
    
    modelCNF = CNF(from_file=model)
    requirementsCNF = CNF(from_file=requirements)
    #Vamos a almacenar el id con la C
    AC=sorted(enumerate(modelCNF.clauses,0), key=lambda x: x[0])
    S=sorted(enumerate(requirementsCNF.clauses,len(modelCNF.clauses)), key=lambda x: x[0])
    pool = mp.Pool(mp.cpu_count())
    starttime = time.time()
    result= fastDiag(S,AC+S)
    reqtime = time.time() - starttime
    print(model+"|"+requirements+"|"+str(reqtime)+"|"+str(count+1)+"|"+str(len(cache))+"|"+str(lmax)+"|pFMDiag|"+solver+"|"+str(difficulty)+"|"+str(result))
    pool.close()
    pool.terminate()