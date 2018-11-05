# -*- coding: utf-8 -*-
"""
The script calculates top ten statistics for H1B data.
Created on Fri Nov  2 11:46:31 2018
@author: Huifang Wang
"""

# importing csv, operator module
import csv
import operator

# H1B data file name
filename = "./input/h1b_input.csv"
#filename = "./input/H1B_FY_2016.csv"

# function that calculates the top ten statistics
def H1BStat(topfield,Fields,CERList,NShift):
    # Calculating the location of the interested field
    FIELD_Num = Fields.index(topfield) - NShift
    
    # extracting all the records for the interested field
    FLD_List = []
    i = 0
    for i in range(len(CERList)):
        FLD_List.append(CERList[i][FIELD_Num])
    FLD_Set = list(set(FLD_List))
    
    # Calculate number of certified applications for each classification
    FLD_Count = []
    FLD_Pct = []
    i = 0
    for i in range(len(FLD_Set)):
        FLD_Count.append(FLD_List.count(FLD_Set[i]))
        FLD_Pct.append(str(round(FLD_Count[i]*100/len(FLD_List),1))+'%')
        
    # Creating the statistics list
    FLD_Tup = list(zip(FLD_Set,FLD_Count,FLD_Pct))
    FLD_Tup.sort(key = operator.itemgetter(0))
    FLD_Tup.sort(key = operator.itemgetter(1),reverse = True)
    StatTup = FLD_Tup[0:10]        
    return StatTup;


# function that writes to files
def WriteFiles(FileName,Fieldr,FileData):
    with open(FileName,'w') as Statfile:
        FileWr = csv.writer(Statfile,delimiter=";")
        FileWr.writerow(Fieldr)
        FileWr.writerows(FileData)
        return;


# reading H1B data file

# initializing the fields and data lists
fields = []
wholelist = []
cerlist = []
with open(filename,'r', encoding="utf-8") as H1B_file:
    H1B_reader = csv.reader(H1B_file, delimiter=';')
    
    # extracting field names
    fields = next(H1B_reader) 

    # extracting whole list  
    for row in H1B_reader: 
        wholelist.append(row) 
        
# generating list for certified visa applications
if 'CASE_STATUS' in fields :
    CER_Num = fields.index('CASE_STATUS')    
else :
    CER_Num = fields.index('STATUS')  
    
for i in range(len(wholelist)):
    if wholelist[i][CER_Num] == 'CERTIFIED':
        cerlist.append(wholelist[i])
    
# Calculating statistics for top 10 occupations 
if 'FULL_TIME_POSITION' in fields :
    Top_10_Occu = H1BStat('JOB_TITLE',fields,cerlist,-2)
else:
    Top_10_Occu = H1BStat('FULL_TIME_POS',fields,cerlist,5)
    
# Calculating statistics for top 10 states 
if 'WORKSITE_STATE' in fields :
    Top_10_States = H1BStat('WORKSITE_STATE',fields,cerlist,0)
else:
    Top_10_States = H1BStat('LCA_CASE_WORKLOC1_STATE',fields,cerlist,0)
    
# Writing statistics to files
# Field names
fields1 = ['TOP_OCCUPATIONS', 'NUMBER_CERTIFIED_APPLICATIONS', 'PERCENTAGE']
fields2 = ['TOP_STATES', 'NUMBER_CERTIFIED_APPLICATIONS', 'PERCENTAGE']

filename1 = "./output/top_10_occupations.txt"
filename2 = "./output/top_10_states.txt"
        
WriteFiles(filename1,fields1,Top_10_Occu)
WriteFiles(filename2,fields2,Top_10_States)