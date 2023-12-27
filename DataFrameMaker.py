import pandas as pd
import os
import json
import dataframe_image as dfi
import matplotlib.pyplot as plt


def genDFforGene(gene):

    seqDict = {}
    lengthOfGene = 0
    for i in range(1,11):
        path = os.path.join('results', f'sequence{i}.json')
        with open(path) as json_data:
            result = json.load(json_data)
            if len(result[gene]["matches"]) > 0:
                seqDict[i] = result[gene]["sequence"]
                lengthOfGene = len(result[gene]["sequence"])

    df = pd.DataFrame(columns=seqDict.keys(), index=seqDict.keys())
    for key in seqDict:
        for key2 in seqDict:
            df[key][key2] = returnDifferences(seqDict[key],seqDict[key2])
    df = df.apply(pd.to_numeric)
    # df = df.style.background_gradient(cmap= 'YlGnBu').set_caption(f"{gene} - {lengthOfGene} nucleotides")  
    
    return df
        



def returnDifferences(seq1,seq2):
    differences = 0
    for i in range(len(seq1)):
        if seq1[i] != seq2[i]:
            differences += 1
    return differences




path = os.path.join('results', f'sequence1.json')
with open(path) as json_data:
    result = json.load(json_data)
genes = list(result.keys())
print(genes)
group1 = ['nhaR', 'nhaA', 'thrA', 'thrC', 'thrB', 'dnaJ', 'ribF', 'mog']
group2 = ['yaaA', 'satP']

group1len = 0
group2len = 0
for gene in group1:
    group1len += len(result[gene]["sequence"])

path = os.path.join('results', f'sequence2.json')
with open(path) as json_data:
    result = json.load(json_data)
    
for gene in group2:
    group2len += len(result[gene]["sequence"])

print(group1len)
print(group2len)
# for gene in genes:
#     df = genDFforGene(gene)
#     dfi.export(df, f"dataframes/{gene}.png")

# group1DF = genDFforGene(group1[0])
# for gene in group1[1:]:
#     group1DF = group1DF.add(genDFforGene(gene), fill_value=0)

# group1DF = group1DF.style.background_gradient(cmap= 'YlGnBu').set_caption(f"Group 1 - {group1len} nucleotides") 
# dfi.export(group1DF, f"dataframes/group1.png")

group2DF = genDFforGene(group2[0]).add(genDFforGene(group2[1]), fill_value=0)
group2DF = group2DF.style.background_gradient(cmap= 'YlGnBu').set_caption(f"Group 2 - {group2len} nucleotides")
dfi.export(group2DF, f"dataframes/group2.png")
