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

def checkFullSequence(checkSeq, knownSeq):
    seqLength = len(knownSeq)
    differences = 0
    for letterIdx in range(seqLength):
        knownLetter = knownSeq[letterIdx]
        testLetter = checkSeq[letterIdx]

        if knownLetter != testLetter:
            differences += 1
    return differences


for file in os.listdir('eColiSeqs'):
    print(file)
    seqName = file.split('.')[0]

    seqDict = SeqIO.index(os.path.join('eColiSeqs',file), "fasta")
    for seqKey in seqDict:
        key = seqKey

    seqResultDict = json.load(open(os.path.join('results', seqName +".json"), 'r'))

    for geneName in seqResultDict:
        print(geneName)
        if seqResultDict[geneName]['matches'] == []:
            continue
        startIndex = seqResultDict[geneName]['matches'][0]
        path = os.path.join('geneRefSeqs', geneName +".txt")
        geneRefSeq = getRefSeq(path)
        lengthOfGene = len(geneRefSeq)
        
        sampleSeq = seqDict[key].seq[startIndex: startIndex + lengthOfGene]
        differences = checkFullSequence(sampleSeq, geneRefSeq)
        seqResultDict[geneName]['sequence'] = str(sampleSeq)
        seqResultDict[geneName]['differences'] = differences
        seqResultDict[geneName]['diffPercent'] = differences/lengthOfGene * 100

    json.dump(seqResultDict, open(os.path.join('results', seqName +".json"), 'w'), indent=4)

