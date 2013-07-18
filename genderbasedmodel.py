#code from http://www.kaggle.com/c/titanic-gettingStarted/details/getting-started-with-python

import csv as csv 
import numpy as np

#Open up the csv file in to a Python object
csv_file_object = csv.reader(open('train.csv', 'rb')) 

header = csv_file_object.next()  #The next() command just skips the 
                                 #first line which is a header

data=[]                          #Create a variable called 'data'

for row in csv_file_object:      #Run through each row in the csv file
    data.append(row)             #adding each row to the data variable
data = np.array(data) 	         #Then convert from a list to an array
								#Be aware that each item is currently
                                 #a string in this format

#print data

#number_passengers = np.size(data[0::,0].astype(np.float))
#number_survived = np.sum(data[0::,0].astype(np.float))
#proportion_survivors = number_survived / number_passengers

#print number_passengers 
#print number_survived
#print proportion_survivors

women_only_stats = data[0::,4] == "female"
men_only_stats = data[0::,4] != "female"

#print women_only_stats

women_onboard = data[women_only_stats,0].astype(np.float)     
men_onboard = data[men_only_stats,0].astype(np.float)

#proportion_women_survived = np.sum(women_onboard) / np.size(women_onboard)  
#proportion_men_survived = np.sum(men_onboard) / np.size(men_onboard) 

#print 'Proportion of women who survived is %s' % proportion_women_survived
#print 'Proportion of men who survived is %s' % proportion_men_survived

#read in the test file by opening a Python object to read and another to write
test_file_obect = csv.reader(open('test.csv', 'rb'))
header = test_file_obect.next()

open_file_object = csv.writer(open("genderbasedmodelpy.csv", "wb"))

for row in test_file_obect:
    if row[2] == 'female':
        row.insert(0,'1') 
        open_file_object.writerow(row)
    else:
        row.insert(0,'0')
        open_file_object.writerow(row)