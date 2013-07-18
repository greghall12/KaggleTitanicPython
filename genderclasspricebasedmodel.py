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

fare_ceiling = 40
data[data[0::,9].astype(np.float) >= fare_ceiling, 9] = fare_ceiling-1.0
fare_bracket_size = 10
number_of_price_brackets = fare_ceiling / fare_bracket_size
number_of_classes = 3 #There were 1st, 2nd and 3rd classes on board 
# Define the survival table
survival_table = np.zeros((2, number_of_classes, number_of_price_brackets))

for i in range(number_of_classes): #search through each class
	for j in range(int(number_of_price_brackets)):   #search through each price

		women_only_stats = np.array(data[ (data[0::,4] == "female") \
			#& (data[0::,1].astype(np.float) == i+1) \
			& (data[0:,9].astype(np.float) >= j*fare_bracket_size) \
            & (data[0:,9].astype(np.float) < (j+1)*fare_bracket_size), 0])

		men_only_stats = np.array(data[ (data[0::,4] != "female") \
			#& (data[0::,1].astype(np.float) == i+1) \
			& (data[0:,9].astype(np.float) >= j*fare_bracket_size) \
            & (data[0:,9].astype(np.float) < (j+1)*fare_bracket_size), 0])		
        
survival_table[0,i,j] = np.mean(women_only_stats.astype(np.float)) #Women stats
survival_table[1,i,j] = np.mean(men_only_stats.astype(np.float)) #Men stats

survival_table[ survival_table != survival_table ] = 0
survival_table[ survival_table < 0.5 ] = 0
survival_table[ survival_table >= 0.5 ] = 1 

test_file_object = csv.reader(open('test.csv', 'rb'))
fname = "genderclasspricebasedmodelpy.csv"
open_file_object = csv.writer(open(fname, "wb"))
header = test_file_object.next() 

for row in test_file_object:
	for j in range(int(number_of_price_brackets)): 
		try: 
			row[7] = float(row[7])
		except:
			bin_fare = 3-float(row[0])
			break
		if row[7] > fare_ceiling:
			bin_fare = number_of_price_brackets-1 
			break
		if row[7] >= j*fare_bracket_size and row[7] < (j+1)*fare_bracket_size: 
			bin_fare = j
			break
	if row[2] == 'female': 
		row.insert(0, int(survival_table[0,float(row[0])-1, bin_fare]))
		open_file_object.writerow(row) 
	else:
		row.insert(0, int(survival_table[1,float(row[0])-1,bin_fare]))
		open_file_object.writerow(row)