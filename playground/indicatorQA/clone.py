#!/usr/bin/env python

"""This script gets the pregnancy and child visit exports and computes the values
 for the indicator for the given month and year  """
from numpy.core.test_rational import numerator, denominator

__author__ = "Josiah Njuki <jnjuki@cgcafrica.org>"
__copyright__ = "Copyright 2014, Modi Labs"

###############################################################################3
# imports section
#
###############################################################################
import sys
import os
import csv
import datetime



###############################################################################3
# configs section
#
###############################################################################
site_id = sys.argv[3]
if (site_id == "sauri"): 
    pregnancy_timeend_col = 130
    pregnancy_referral_col = 145
    pregnancy_case_id_col = 20
    child_timeend_col = 154
    child_referral_col = 242
    child_medication_type_col = 191
    child_case_id_col = 20
    
    
elif (site_id == "mwandama"):
    pregnancy_timeend_col = 83
    pregnancy_referral_col = 96
    pregnancy_case_id_col = 20
    child_timeend_col = 96
    child_referral_col = 156
    child_medication_type_col = 117
    child_case_id_col = 21
    
elif (site_id == "bonsaaso"):
    pregnancy_timeend_col = 84
    pregnancy_referral_col = 109
    pregnancy_case_id_col = 19
    child_timeend_col = 69
    child_referral_col = 109
    child_medication_type_col = 81
    child_case_id_col = 20

elif (site_id == "tiby"):
    pregnancy_timeend_col = 76
    pregnancy_referral_col = 101
    child_timeend_col = 69
    child_referral_col = 109
    child_medication_type_col = 81
    
elif (site_id == "mbola"):
    pregnancy_timeend_col = 82
    pregnancy_referral_col = 71
    child_timeend_col = 79
    child_referral_col = 129
    child_medication_type_col = 89
    
valid_referral_types = ["emergency", "take_to_clinic", "immediate", "basic"]
valid_medication_types = ["coartem", "anti_malarial", "ors", "zinc"]




# order of arguments pregnancy_visits_file.csv child_visits_file.csv SITE_ID MONTH YEAR  
# pregnancy_visits = os.path.

current_dir = os.getcwd()

pregnancy_visits_file = sys.argv[1]
child_visits_file = sys.argv[2]
mnth = sys.argv[4]
yr = sys.argv[5]

pregnancy_timeend_col = pregnancy_timeend_col - 1
pregnancy_referral_col = pregnancy_referral_col - 1
pregnancy_case_id_col = pregnancy_case_id_col - 1

child_timeend_col = child_timeend_col - 1
child_referral_col = child_referral_col - 1
child_medication_type_col = child_medication_type_col - 1
child_case_id_col = child_case_id_col - 1


###############################################################################3
# process pregnancy visits file and get the valid counts
#
###############################################################################

pregnancy_visits = csv.reader(open(pregnancy_visits_file, 'rb'))                           
pregnancy_count = len(list(pregnancy_visits))
#print pregnancy_count
#print yr
#print mnth
pregancy_csv_reader = csv.reader(pregnancy_visits)
pregnancy_visits_iterator = csv.reader(open(pregnancy_visits_file, 'r+')) 
thisRow = pregnancy_visits_iterator.next()
p_counts = 0
c1_counts = 0
c2_counts = 0
p_numerator1 = 0
p_numerator2 = 0
c1_numerator1 = 0
c1_numerator2 = 0
c2_numerator = 0
details_container = []
valid_counts_details = []
for i in range(pregnancy_count - 1): 
    thisRow = pregnancy_visits_iterator.next()   
    my_time_end = datetime.datetime.strptime(str.strip(thisRow[pregnancy_timeend_col][:-1]), "%Y-%m-%dT%H:%M:%S")
    #print int(yr)
    if(my_time_end.year == int(yr) and my_time_end.month >= int(mnth)): 
       #save the case details
       case_id = thisRow[pregnancy_case_id_col]
       referral = str.strip(thisRow[pregnancy_referral_col])
       details_container.append([case_id,referral,my_time_end])
       if(my_time_end.year == int(yr) and my_time_end.month == int(mnth)):
           if(str.strip(thisRow[pregnancy_referral_col]) in valid_referral_types):
               p_counts += 1
               valid_counts_details.append([thisRow[pregnancy_case_id_col], str.strip(thisRow[pregnancy_referral_col]), my_time_end]);
                #print str(my_time_end.year) + " " + str(my_time_end.month) + "--" + str(thisRow[pregnancy_referral_col])
print '-----Pregnancy----denon the nume'
print p_counts
#print len(valid_counts_details)
#get the numerator value in 3 steps:
# 1. foreach valid_counts element, check in the detailed array date diff <= without counting the referral date in question for subsequent
# 2. 
for c in range(len(valid_counts_details) - 1): 
   for c_det in range(len(details_container) - 1):  
       if(valid_counts_details[c][0] == details_container[c_det][0]) and valid_counts_details[c][2] < details_container[c_det][2]:
           if(str.strip(details_container[c_det][1]) not in valid_referral_types):
               diff = details_container[c_det][2] - valid_counts_details[c][2]
               if(diff.days <= 2 and diff.days > 0):
                   p_numerator1 += 1
#                    print valid_counts_details[c][2]
#                    print details_container[c_det][2]
#                    print '------------------'
#    
   diff2 = valid_counts_details[c][2] - valid_counts_details[c-1][2]                             
   if(diff2.days <= 2 and diff2.days > 0):
       p_numerator2 += 1
#        print valid_counts_details[c-1][2]
#        print valid_counts_details[c][2]               
#print p_numerator1
#print p_numerator2                 
print p_numerator1 +  p_numerator2             
###############################################################################3
# process child visits file and get the valid counts for the month/year and with valid referral
#
###############################################################################
child_handler = open(child_visits_file, 'rb')
child_visits = csv.reader(child_handler)                           
child_count = len(list(child_visits))
child_csv_reader = csv.reader(child_visits)
child_visits_iterator = csv.reader(open(child_visits_file, 'r+')) 
thisRow = child_visits_iterator.next()
valid_counts_details = []
details_container = []
for i in range(child_count - 1):#
    thisRow = child_visits_iterator.next()
    #print str.strip(thisRow[child_timeend_col][:-1])
    my_time_end = datetime.datetime.strptime(str.strip(thisRow[child_timeend_col][:-1]), "%Y-%m-%dT%H:%M:%S")
    if(my_time_end.year == int(yr) and my_time_end.month >= int(mnth)):  
        details_container.append([thisRow[child_case_id_col], str.strip(thisRow[child_referral_col]), my_time_end]);      
        if(my_time_end.year == int(yr) and my_time_end.month == int(mnth)):
            if(str.strip(thisRow[child_referral_col]) in valid_referral_types):
                c1_counts += 1
                valid_counts_details.append([thisRow[child_case_id_col], str.strip(thisRow[child_referral_col]), my_time_end]);
             #print 'id=>' + str(thisRow[0]) + ' ' + str(my_time_end.year) + " " + str(my_time_end.month) + "--" + str(thisRow[child_referral_col])
#
for c in range(len(valid_counts_details) - 1): 
   for c_det in range(len(details_container) - 1):  
       if(valid_counts_details[c][0] == details_container[c_det][0]) and valid_counts_details[c][2] < details_container[c_det][2]:
           if(str.strip(details_container[c_det][1]) not in valid_referral_types):
               diff = details_container[c_det][2] - valid_counts_details[c][2]
               if(diff.days <= 2 and diff.days > 0):
                   c1_numerator1 += 1
                   print valid_counts_details[c][2]
                   print details_container[c_det][2]
#                    
#    
   diff2 = valid_counts_details[c][2] - valid_counts_details[c-1][2]                             
   if(diff2.days <= 2 and diff2.days > 0):
       c1_numerator2 += 1  
       print '--teren--'
       print valid_counts_details[c-1][2]
       print valid_counts_details[c][2]
       

print '-----child ref----denon the nume'                  
print c1_counts
print c1_numerator1 + c1_numerator2
child_handler.close()
 
 
# ###############################################################################3
# # process child visits file second time and get the valid counts for the month/year and with valid medication type
# #
# ###############################################################################
# 
# 
valid_counts_details = []
details_container = []
child_handler2 = open(child_visits_file, 'rb')
child_visits = csv.reader(child_handler2)                           
child_count = len(list(child_visits))
child_csv_reader = csv.reader(child_visits)
child_visits_iterator = csv.reader(open(child_visits_file, 'r+')) 
thisRow = child_visits_iterator.next()
for i in range(child_count - 1):
    thisRow = child_visits_iterator.next()
    my_time_end = datetime.datetime.strptime(str.strip(thisRow[child_timeend_col][:-1]), "%Y-%m-%dT%H:%M:%S")
    if(my_time_end.year == int(yr) and my_time_end.month >= int(mnth)):  
        details_container.append([thisRow[child_case_id_col], str.strip(thisRow[child_medication_type_col]), my_time_end]);      
        if(my_time_end.year == int(yr) and my_time_end.month == int(mnth)):
            valid = 0
            for med_type in valid_medication_types:            
                if(thisRow[child_medication_type_col].find(med_type) != -1):
                    valid = 1   
            if(valid == 1):             
                c2_counts += 1
                valid_counts_details.append([thisRow[child_case_id_col], str.strip(thisRow[child_medication_type_col]), my_time_end]);
                #print 'id=>' + str(thisRow[0]) + ' ' + str(my_time_end.year) + " " + str(my_time_end.month) + "--" + str(thisRow[child_referral_col]) + "--" + str(thisRow[child_medication_type_col])
            

for c in range(len(valid_counts_details) - 1): 
   for c_det in range(len(details_container) - 1):  
       if(valid_counts_details[c][0] == details_container[c_det][0]) and valid_counts_details[c][2] < details_container[c_det][2]:
           valid = 0
           for med_type in valid_medication_types:           
                if(valid_counts_details[c][1].find(med_type) != -1):
                    valid = 1   
           if(valid == 0):             
               diff = details_container[c_det][2] - valid_counts_details[c][2]
               if(diff.days <= 2 and diff.days > 0):
                   c2_numerator += 1


print '-----child med----denon the nume'                           
print c2_counts
print c2_numerator

print '------Finally-----------'
print p_numerator1
print p_numerator2
print c1_numerator1
print c1_numerator2
print c2_numerator
numerator = (p_numerator1 + p_numerator2 + c1_numerator1 + c1_numerator2 + c2_numerator)
demoninator = (p_counts + c1_counts + c2_counts)
val = float(numerator)/float(demoninator)*100
# 
print 'Indicator value is:\n ' + str(numerator) + '/' + str(demoninator)  + '=' + str(val)+"%"
#           
