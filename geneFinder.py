from Bio import SeqIO
from collections import defaultdict
import time
import os
import json

def getRefSeq(path):
    seq = ""
    with open(path, 'r') as f:
        for line in f.readlines()[1:]:
            seq += line.strip().upper()
    return seq
    

def checkSequence(checkSeq, knownSeq):
        differences = 0
        if len(checkSeq)< len(knownSeq):
            return False
        for letterIdx in range(len(checkSeq)):
            if checkSeq[letterIdx] != knownSeq[letterIdx]:
                differences +=1
            if differences > 2:
                return False
        
        return True

for file in os.listdir('eColiSeqs'):
    print(file)
    seqName = file.split('.')[0]

    seqDict = SeqIO.index(os.path.join('eColiSeqs',file), "fasta")
    for seqKey in seqDict:
        key = seqKey

    if os.path.exists(os.path.join('results', seqName +".json")):
        seqResultDict = json.load(open(os.path.join('results', seqName +".json"), 'r'))
    else:
        seqResultDict = {}


    for geneRefFile in os.listdir('geneRefSeqs'):
        geneName = geneRefFile.split('.')[0]
        path = os.path.join('geneRefSeqs', geneRefFile)

   
        startSequence = getRefSeq(path)[:30]
        matchesFound = []
        startTime = time.time()
        for letterIdx in range(len(seqDict[key].seq)):
            checkSeq = seqDict[key].seq[letterIdx: letterIdx +30]
            if checkSequence(checkSeq, startSequence):
                matchesFound.append(letterIdx)

        print(matchesFound)
        print("Time taken: ", time.time() - startTime)

        
        
        seqResultDict[geneName] = {'matches': matchesFound}
    json.dump(seqResultDict, open(os.path.join('results', seqName +".json"), 'w'), indent=4)




