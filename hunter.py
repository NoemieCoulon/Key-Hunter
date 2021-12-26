# -*- coding: utf-8 -*-
"""
Created on Fri Dec 24 18:23:49 2021

@author: coulon noémie
"""
import numpy as np
import matplotlib.pyplot as pl

#nb_bits: how many bits are used to write an int 
#ex: nb_bits=8; 00000101 or nb_bits=4; 0101

#nb_max: (decimal) maximal value of the input; input goes from 0 to nb_max

#key: (decimal) secret value that we ar looking for
#bit_tested: bit that is being analysed and tested; from 0 to 7 where 0 is LSB



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
    
    return l_out 
        
def function_add(nb_max,nb_bits,nb_sum):
    #nb_sum is whatever the key or the hypothetical key
    l_sum=[]
    
    for i in range (nb_max+1): 
        l_sum.append(bin(i+nb_sum)) #add to the list the number made of the sum of the input and the nb_sum
    
    return l_sum

def leakage(nb_max,nb_bits,key):
    
    data_out=bin_on_nb_bits(nb_bits,function_add(nb_max,nb_bits,key))
    
    ref=data_out[0] #the leakage is calculated from the reference which is the output when the input is zero
    
    leakage=[]
    
    for i in range (len(data_out)):
        l=0
               
        for j in range (len(data_out[i])):
            
            if int(ref[-j])!=int(data_out[i][-j]):
                l+=1 # 
            # if int(ref[-j])-int(data_out[i][-j])==1: # 1 to 0 leakage is 1
        
            #     p+=1
            # if int(ref[-j])-int(data_out[i][-j])==-1: # 0 to 1 leakage is 2
            #     p+=2
        leakage.append(l)
    
    return (leakage) #return leakage for each input, the first number coresponds to the leakage of 0

def function_add_class(nb_max,nb_bits,hypo,bit_tested,key):
    
    data_out=bin_on_nb_bits(nb_bits,function_add(nb_max,nb_bits,hypo))
    leakage_out=leakage(nb_max,nb_bits,key)
    
    listclass=[[[],[],[]],[[],[],[]]]
    
        
    for i in range (len(data_out)):
        
        if data_out[i][-(bit_tested+1)]=="1":
            listclass[1][0].append(i)
            listclass[1][1].append(data_out[i])
            listclass[1][2].append(leakage_out[i])
            
            
        else: #if data_out[i][bit_tested]=="0":
            listclass[0][0].append(i)
            listclass[0][1].append(data_out[i])
            listclass[0][2].append(leakage_out[i])
            
                    
    
    return listclass

def average(l): #l is a list of integer
    s=sum(l)
    
    if len(l)==0:
        return False #return False if the list as no len
    
    return s/len(l) # return average of a list of integer

def average_class(nb_max,nb_bits,hypo,bit_tested,key): #bit tested; 0=bit poids faible
    listclass=function_add_class(nb_max,nb_bits,hypo,bit_tested,key)
    
    average0=average(listclass[0][2])#leakage class 0
    
    average1=average(listclass[1][2])#leakage class 1
    
    if average0==False or average1==False:
        return 0
    return (abs(average0-average1))
    
       
def courbe(nb_max,nb_bits,bit_tested,key):
    #print ("nb_max=%d nb_bits=%d bit_tested=%d key=%d" % (nb_max,nb_bits,bit_tested,key))
    #x=np.linspace(0,nb_max,nb_max+1)
    
    y=[]
    
    for i in range (nb_max+1):
        y.append(average_class(nb_max,nb_bits,i,bit_tested,key))
    
    #pl.plot(x,y,"+")
    
    return y
        
def average_courbe(nb_max,nb_bits,key):
    if key>nb_max:
        return "Error: key cannot be found, please choose a higher nb_max"
    
    x=np.linspace(0,nb_max,nb_max+1)
    
    y=[]
    average=[]
    
    for i in range (nb_bits):
        y.append(courbe(nb_max,nb_bits,i,key))
    
    for i in range (len(y[0])):
        
        a=0
        for j in range (len (y)):
            a=a+y[j][i]
        average.append(a/len(y))
        
    pl.plot(x,average,"+")
    
    if average.index(max(average))==key:
        print ("key:",key, " Found !")
        return 1 # the right key has been found
    else:
        print ("key:",key," Found key:",average.index(max(average)))
        return 0 # the key hasn't been found
    
    
def loop(nb_max,nb_bits):
        ind=0
        j=nb_max
    # for j in range (nb_max+1):
    #     ind=0
        for i in range (j+1):
            ind+=average_courbe(nb_max,nb_bits,i)
        if j!=0:
            print ("number of success:",ind,"over",j, "| achievement:",int(ind/j*100),"%")
        
def looploop(nb_max,nb_bits):
    for i in range (nb_max):
        loop(i,nb_bits)
