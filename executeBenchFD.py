#!/bin/python3
import os
import time

starttime = time.time()
cc=["16","8","4","2","1"]

for i in cc:
    modelPath="./cnf/bench/model_"+i+".cnf"
    for j in range(3):
        productPath="./cnf/bench/prod-"+i+"-"+str(j)+".prod"
        for solver in ["Sat4j"]:    
            for lmax in ["3","2","1","0"]:
                for difficulty in ["0","50","100"]:
                    if lmax == "0":
                        print("    python3 ./fmdiag.py " + modelPath + " "+productPath+" "+lmax+" "+solver+" "+difficulty)
                        os.system("python3 ./fmdiag.py " + modelPath + " "+productPath+" "+lmax+" "+solver+" "+difficulty+" >>"+ " resultFD.csv")
                    else:
                        print("    python3 ./fd_parallel_mp.py " + modelPath + " "+productPath+" "+lmax+" "+solver+" "+difficulty)
                        os.system("python3 ./fd_parallel_mp.py " + modelPath + " "+productPath+" "+lmax+" "+solver+" "+difficulty+" >>"+ " resultFD.csv")

reqtime = time.time() - starttime
print("GlucoseSat4j time: "+str(reqtime))

for i in cc:
    modelPath="./cnf/bench/model_"+i+".cnf"
    for j in range(3):
        productPath="./cnf/bench/prod-"+i+"-"+str(j)+".prod"
        for solver in ["Choco4"]:    
            for lmax in ["3","2","1","0"]:
                for difficulty in ["0","50","100"]:
                    os.system("python ./fmdiag.py " + modelPath + " "+productPath+" "+lmax+" "+solver+" "+difficulty+" >>"+ " resultFD_choco4.csv")
                    if not lmax == "0":
                        os.system("python ./fd_parallel_mp.py " + modelPath + " "+productPath+" "+lmax+" "+solver+" "+difficulty+" >>"+ " resultFD_choco4.csv")

reqtime = time.time() - starttime
print("Choco4 time: "+(reqtime))
