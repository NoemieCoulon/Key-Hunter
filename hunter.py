#
import numpy as np
import matplotlib.pyplot as plt
import time

from sklearn import preprocessing
#nb_bits: how many bits are used to write an int 
#ex: nb_bits=8; 00000101 or nb_bits=4; 0101

#nb_max: (decimal) maximal value of the input; input goes from 0 to nb_max

#key: (decimal) secret value that we ar looking for
#bit_tested: bit that is being analysed and tested; from 0 to 7 where 0 is LSB

L=[64, 38, 51, 51, 64, 51, 64, 63, 76, 39, 51, 51, 64, 51, 64, 63, 76, 51, 64, 63, 76,
   63, 76, 74, 86, 38, 51, 51, 65, 51, 64, 63, 76, 52, 64, 63, 76, 63, 76, 74, 86, 51,
   64, 63, 76, 63, 76, 74, 85, 63, 76, 76, 86, 73, 86, 83, 96, 38, 51, 50, 64, 50, 64,
   62, 75, 50, 64, 62, 75, 62, 75, 73, 86, 51, 64, 62, 75, 62, 73, 73, 86, 68, 75, 72,
   86, 73, 86, 84, 95, 50, 63, 62, 74, 66, 74, 72, 85, 62, 74, 72, 85, 72, 79, 82, 95,
   61, 75, 72, 85, 72, 85, 82, 95, 72, 85, 82, 95, 82, 94, 91, 103, 39, 52, 52, 64, 51,
   64, 63, 76, 51, 64, 63, 76, 63, 76, 74, 86, 51, 65, 63, 76, 63, 76, 76, 86, 63, 76,
   74, 86, 74, 86, 83, 96, 50, 63, 62, 75, 62, 75, 73, 86, 62, 75, 73, 86, 73, 85, 83,
   95, 62, 75, 73, 85, 73, 86, 83, 95, 73, 85, 82, 95, 82, 95, 91, 103, 50, 63, 62, 75,
   62, 74, 73, 85, 64, 75, 73, 85, 72, 85, 83, 95, 62, 73, 73, 85, 74, 85, 82, 93, 72,
   85, 82, 94, 82, 94, 91, 103, 60, 73, 71, 84, 71, 84, 81, 93, 71, 83, 81, 93, 84, 93,
   90, 102, 71, 83, 81, 93, 81, 88, 93, 102, 80, 93, 90, 102, 90, 102, 98, 100, 24, 38,
   39, 52, 47, 51, 51, 64]

def bin_on_nb_bits(nb_bits,l_in): 
    #l is a list of str which represents a binary int ex: "0b101"
    
    l_out=[]
    
    for e in l_in: 
        e=e[2:] #remove "0b" at the beginning of the int, ex: 0b101 ==> 101
        if nb_bits>len(e):   
                e=(nb_bits-len(e))*"0"+e #put the right number of zeros to have nb_bits bits
                                         # ex: nb_bits=8, "101" ==> "00000101"
        if len(e)>nb_bits: #the int is already written on more than nb_bits
            e=e[-nb_bits:] # keep only the first nb_bits; ex: "100000101" ==> "00000101"
        l_out.append(e)
    
    return l_out #l_out is a list of str which represents a binary int on nb_bits ex: "00000101"
        
def function_add(nb_max,nb_bits,nb_sum):
    #nb_sum is whatever the key or the hypothetical key
    l_sum=[]
    
    for i in range (nb_max+1): 
        l_sum.append(bin(i+nb_sum)) #add to the list the number made of the sum of the input and the nb_sum
    
    return l_sum

def function_xor(nb_max,nb_bits,xor_key):
    #nb_xor is whatever the key or the hypothetical key
    l_xor=[]
    
    for i in range (nb_max+1): 
        l_xor.append(bin(i^xor_key)) #add to the list the number made of the xor of the input and the nb_xor
    
    return l_xor

def leakage_simu(nb_max,nb_bits,key):
    data_out=bin_on_nb_bits(nb_bits,function_add(nb_max,nb_bits,key))  #choose if function used is add

    leakage_simu=[]
    
    for i in range (len(data_out)):
        l=0
               
        for j in range (len(data_out[i])):
            l=l+ int(data_out[i][-j])#add 1 if bit is equal to 1
          
        leakage_simu.append(l)# l correponds to hamming weight of data_out[i]
    return (leakage_simu) #return leakage_simu for each input, the first number coresponds to the leakage_simu of 0

def function_class(nb_max,nb_bits,hypo,bit_tested,key,function):
    
    data_out=bin_on_nb_bits(nb_bits,function_add(nb_max,nb_bits,hypo))
    #data_out=bin_on_nb_bits(nb_bits,function_xor(nb_max,nb_bits,hypo))
    
    if function=="simu":
        leakage_out=leakage_simu(nb_max,nb_bits,key)
        
    else:
        leakage_out=L
    
    listclass=[[[],[],[]],[[],[],[]]]
    
        
    for i in range (len(data_out)):
        
        if data_out[i][-(bit_tested+1)]=="1":
            listclass[1][0].append(i)# put in listclass[1][0] input i in class 1
            listclass[1][1].append(data_out[i]) # put in listclass[1][1] output when input egal i in class 1
            listclass[1][2].append(leakage_out[i]) # put in listclass[1][2] real leakage when input egal i in class 1
            
            
        else: #if data_out[i][bit_tested]=="0":
            listclass[0][0].append(i)
            listclass[0][1].append(data_out[i])
            listclass[0][2].append(leakage_out[i])
    
    return listclass #listclass big list organising both classes with input,output and leakage

def average(l): #l is a list of integer
    s=sum(l)
    
    if len(l)==0:
        return False #return False if the list as no len
    
    return s/len(l) # return average of a list of integer

def average_class(nb_max,nb_bits,hypo,bit_tested,key,function): 
# generate difference between two classes, for one hyp and one bit tested; 0=bit poids faible
    listclass=function_class(nb_max,nb_bits,hypo,bit_tested,key,function)
    
    average0=average(listclass[0][2])#leakage_simu class 0
    average1=average(listclass[1][2])#leakage_simu class 1
    
    if average0==False or average1==False:
        return 0
    
    return (abs(average0-average1)) #return difference between the average fo the bit_tested and hypo of the two classes

def coef_cor(nb_max,nb_bits,key,function): 
    y=[]
    
    for j in range (nb_max+1):
        a=[]
        for i in range (nb_bits):
            a.append(average_class(nb_max,nb_bits,j,i,key,function))
        y.append(average(a))
   
    return y # return list of coef_cor for each hypo
        
def test_key(nb_max,nb_bits,key):
    t1=time.time() #count inital time
    if key>nb_max:
        return "Error: key cannot be found, pltease choose a higher nb_max"
    
    x=np.linspace(0,nb_max,nb_max+1) #list of all the hypothesis

    average_simu=coef_cor(nb_max,nb_bits,key,"simu")
    average_exp=coef_cor(nb_max,nb_bits,key,"exp")
       
    average_simu = np.array(average_simu).reshape(-1,1)# normalise la liste average_simu
    scaler = preprocessing.MinMaxScaler()
    average_simu=list(scaler.fit_transform(average_simu))

    average_exp = np.array(average_exp).reshape(-1,1) # normalise la liste average_exp
    scaler = preprocessing.MinMaxScaler()
    average_exp=list(scaler.fit_transform(average_exp))
   
    max_average=np.where(np.array(average_simu) == max(average_simu))[0] 
    #return all hypo with the higher coef_cor
    
    plt.plot(x,average_simu,"r-")#show graph for simu leakage
    plt.plot(x,average_exp,"b-") # show graph for exp leakage
    
    plt.title("Fonction addition, clef trouvée: "+ str(max_average[0]))
    plt.legend(["simu", "exp"], loc ="lower right") 
    plt.xlabel("Hypothèses")
    plt.ylabel("Facteur de corrélation normalisé")

    
    if average_exp.index(max(average_exp))==key:
        print ("key:",key, " Found !")
        print("equi proba:",max_average)
        print ("calculation time: ", time.time()-t1, "s")
        return 1 # the right key has been found
    else:
        print("key:",average_exp[key],"found:",max(average_exp))
        print("equi proba:",max_average)
        print ("key:",key," Found key:",average_exp.index(max(average_exp)))
        print ("calculation time: ", time.time()-t1, "s")
        return 0 # the key hasn't been found
