# importing the required modules
import os
import argparse
import math
import random
import matplotlib.pyplot as plt
  
  
parser=argparse.ArgumentParser(description = "Calculating test statistic to classify cis interaction of UMLILO with nominal p-value as test of signifcance")

parser.add_argument("-g",nargs = 1,metavar = "GENCODE",type = str, help = "The location of Gencode File containing positions of genes - which is used to calculate the distance of each gene on chr. 4 to UMLILO")
parser.add_argument("-c",nargs = 1,metavar = "Control-data",type = str, help = "The location of control data file")
parser.add_argument("-ko",nargs = 1,metavar = "KO-data",type = str, help = "The location of UMLILO Knock-Out file")
parser.add_argument("-exponent",nargs = 1,metavar="Exponent",type = float, help = "The exponent a, in the test statistic 1/d^a - where d is distance of gene from UMLILO")


args = parser.parse_args()



with open(args.ko[0],'r') as f:
    KO_gene_tpm_dict={}
    next(f)
    for line in f:
        line=line.split()
        #line[1] = gene symbol
        #line[3] = TPM
        
        if line[3] == '0':
            KO_gene_tpm_dict.update({line[1]:'0.1'})
        else:
            KO_gene_tpm_dict.update({line[1]:line[3]})
            
#print(KO_gene_tpm_dict)

with open(args.c[0],'r') as f:
    CON_gene_tpm_dict={}
    next(f)
    for line in f:
        line=line.split()
        #line[1] = gene symbol
        #line[3] = TPM
        
        if line[3] == '0':
            CON_gene_tpm_dict.update({line[1]:'0.1'})
        else:
            CON_gene_tpm_dict.update({line[1]:line[3]})


log_exp_dict_TARGETS={}
log_exp_dict_ALL={}
for gene in CON_gene_tpm_dict.keys():
    if float(KO_gene_tpm_dict[gene])!=float(CON_gene_tpm_dict[gene]): #THIS ENSURES ONLY DFG ARE CONSIDERED FROM HERE ON
        log_exp_dict_TARGETS.update({gene: float(math.log(float(KO_gene_tpm_dict[gene])/float(CON_gene_tpm_dict[gene]),2))})
        
for gene in CON_gene_tpm_dict.keys():
    #if float(KO_gene_tpm_dict[gene])!=float(CON_gene_tpm_dict[gene]): #THIS ENSURES ALL GENES ARE CONSIDERED FROM HERE ON
    log_exp_dict_ALL.update({gene: float(math.log(float(KO_gene_tpm_dict[gene])/float(CON_gene_tpm_dict[gene]),2))})

#print(len(log_exp_dict_TARGETS))

with open(args.g[0],'r') as f:
    p=args.exponent[0]
    distance_dict={}
    distance_dict_ALL={}
    targets_filtered=[]
    targets_filtered_exp=[]
    next(f)
    for line in f:
        UMLILO_start=73710302
        line=line.split()
    
        #line[1] = chr. no.
        #line[2] = start pos
        #line[3] = end pos
        #line[11] = gene symbol
        if line[11] in log_exp_dict_TARGETS.keys() and line[1]=='chr4':
            distance_dict.update({line[11]:1/(abs(int(line[2]) - UMLILO_start)**p)})  #DFG Genes common to GENCODE file and Gene Exp file and which are on chromosome 4
        
        if line[11] in log_exp_dict_ALL.keys() and line[1]=='chr4':
            distance_dict_ALL.update({line[11]:1/(abs(int(line[2]) - UMLILO_start)**p)}) #All Genes common to GENCODE file and Gene Exp file and which are on chromosome 4
#print(len(distance_dict_ALL))

for gene in distance_dict.keys():
    if abs(log_exp_dict_TARGETS[gene]) >1:
        targets_filtered+=[gene]
        targets_filtered_exp.append(distance_dict[gene])
    #print(log_exp_dict_ALL[gene])
#print(len(targets_filtered_exp))
avg=sum(targets_filtered_exp)/len(targets_filtered_exp)
#print(avg)
#Unchanged Gene exp values
unchanged_genes=set(distance_dict_ALL.keys())-set(distance_dict.keys())


#NOW WE CHOOSE GENES WHICH HAVE AN EXP OUTSIDE (-0.5,0.5)

filtered=[]

for gene in distance_dict_ALL.keys():
    if abs(log_exp_dict_ALL[gene]) >1:
        filtered+=[gene]
    #print(log_exp_dict_ALL[gene])


#print(len(filtered))

#Retrieve simulations by calling fn simulations and store statistic values in a new list called 'statistic'
#GENERATE SIMULATIONS


newl=filtered
other_half=list(unchanged_genes)  #Unchanged_genes contains all genes NOT differentially expressed (DE)
p_val={}
def simulation():
    #random.seed(3)
    #number=0#random.randint(1,196)  #Since 196 genes pass the filters. Filters- i) Gene is DE ii) Gene is on chr. 4 iii) Expression is >abs(1)
    #random.shuffle(newl)
    random.shuffle(other_half)
    sim=other_half[:196]
    #sim=newl[:196-number] + other_half[:number]  #sim partly contains genes which passed all three filters and partly genes which were not DE
    #print(len(sim))
    return sim#,number#len(sim)

#Populates a list with test statistic values for the genes now chosen

iter=5000 #Number of iterations for a particular statistic
def test_stat(inp):
   
    statistic=[]
    for gene in inp:
        statistic.append(distance_dict_ALL[gene])
    #print(len(statistic))
    return sum(statistic)/len(statistic)  #Returns mean value of 1/d^0.2
    
test_stat_val=[]
for _ in range(iter):
    test_stat_val.append(test_stat(simulation()))
    



n=plt.hist(test_stat_val,bins=65)
plt.xlabel('Test Statistic')
plt.ylabel('Number of simulations')
#plt.legend()
print('Statistic of orginal dataset:',avg)
plt.axvline(x=avg,color='red')

def index_hist_val():
    for val in range(len(n[1])):
        if avg<n[1][val]:
            #print(val)
            break

    sum=0
    for i in range(val,len(n[1])-1):
        #print(sum,n[0][i])
        sum=+sum+n[0][i]
    print('Nom. p-value',sum/iter)
    return sum/iter

p_val.update({simulation()[1]:index_hist_val()})
