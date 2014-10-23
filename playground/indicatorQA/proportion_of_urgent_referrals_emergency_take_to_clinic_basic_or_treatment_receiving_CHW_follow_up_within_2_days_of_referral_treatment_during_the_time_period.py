#!/usr/bin/env python

"""This script gets the pregnancy and child visit exports and computes the values
 for the indicator for the given month and year  """

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
site_id = "tiby"
if (site_id == "sauri"): 
    pregnancy_timeend_col = 130
    pregnancy_referral_col = 145
    child_timeend_col = 154
    child_referral_col = 242
    child_medication_type_col = 191
    
elif (site_id == "mwandama"):
    pregnancy_timeend_col = 83
    pregnancy_referral_col = 96
    child_timeend_col = 96
    child_referral_col = 156
    child_medication_type_col = 117
    
elif (site_id == "bonsaaso"):
    pregnancy_timeend_col = 84
    pregnancy_referral_col = 109
    child_timeend_col = 69
    child_referral_col = 109
    child_medication_type_col = 81

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




# order of arguments YEAR MONTH pregnancy_visits_file.csv child_visits_file.csv
# pregnancy_visits = os.path.

current_dir = os.getcwd()

pregnancy_visits_file = sys.argv[1]
child_visits_file = sys.argv[2]
yr = sys.argv[3]
mnth = sys.argv[4]

pregnancy_timeend_col = pregnancy_timeend_col - 1
pregnancy_referral_col = pregnancy_referral_col - 1

child_timeend_col = child_timeend_col - 1
child_referral_col = child_referral_col - 1
child_medication_type_col = child_medication_type_col - 1


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
for i in range(pregnancy_count - 1):
    thisRow = pregnancy_visits_iterator.next()
    my_time_end = datetime.datetime.strptime(str.strip(thisRow[pregnancy_timeend_col][:-1]), "%Y-%m-%dT%H:%M:%S")
    if(my_time_end.year == int(yr) and my_time_end.month == int(mnth)):
        if(str.strip(thisRow[pregnancy_referral_col]) in valid_referral_types):
            p_counts += 1
            print str(my_time_end.year) + " " + str(my_time_end.month) + "--" + str(thisRow[pregnancy_referral_col])

print p_counts


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
c1_counts = 0
for i in range(child_count - 1):#
    thisRow = child_visits_iterator.next()
    #print str.strip(thisRow[child_timeend_col][:-1])
    my_time_end = datetime.datetime.strptime(str.strip(thisRow[child_timeend_col][:-1]), "%Y-%m-%dT%H:%M:%S")
    if(my_time_end.year == int(yr) and my_time_end.month == int(mnth)):
         if(str.strip(thisRow[child_referral_col]) in valid_referral_types):
             c1_counts += 1
             print 'id=>' + str(thisRow[0]) + ' ' + str(my_time_end.year) + " " + str(my_time_end.month) + "--" + str(thisRow[child_referral_col])
#               
print c1_counts
child_handler.close()


###############################################################################3
# process child visits file second time and get the valid counts for the month/year and with valid medication type
#
###############################################################################


child_handler2 = open(child_visits_file, 'rb')
child_visits = csv.reader(child_handler2)                           
child_count = len(list(child_visits))
child_csv_reader = csv.reader(child_visits)
child_visits_iterator = csv.reader(open(child_visits_file, 'r+')) 
thisRow = child_visits_iterator.next()
c2_counts = 0
for i in range(child_count - 1):
    thisRow = child_visits_iterator.next()
    my_time_end = datetime.datetime.strptime(str.strip(thisRow[child_timeend_col][:-1]), "%Y-%m-%dT%H:%M:%S")
    if(my_time_end.year == int(yr) and my_time_end.month == int(mnth)):
        valid = 0
        for med_type in valid_medication_types:            
            if(thisRow[child_medication_type_col].find(med_type) != -1):
                valid = 1   
        if(valid == 1):             
            c2_counts += 1
            print 'id=>' + str(thisRow[0]) + ' ' + str(my_time_end.year) + " " + str(my_time_end.month) + "--" + str(thisRow[child_referral_col]) + "--" + str(thisRow[child_medication_type_col])
           
              
print c2_counts

demoninator = p_counts + c1_counts + c2_counts

print 'Denominator value is ' + str(demoninator)




        
                
