import numpy
import matplotlib.pyplot 
import csv


population_file = "green_sea_turtle_population_characteristics.csv"
age_file = "Green_sea_turtle_age_growth.csv"
#Stranding_ID_Number,Sex,Straightline_Carapace_Length,Growth_Rate,Age,Year
# 0                   1                   2                 3      4    5
AGE = 4 
YEAR = 5
#STAGES:
HATCHLING = 0
JUVENILE = 1
ADULT = 2
#
CURRENTYEAR = 2024
transformer = numpy.array([[0,           0,    75/20], 
                           [0.56, 0.94737 * 0.82, 0], 
                           [0,   0.0526 * 0.82, 0.9]], float)
#I have a thing in the google doc explaining how I got these changed numbers for the transition matrix
#feel free to mess with the values and see how it changes the pop over time 
start_matrix = numpy.array([0, 0, 0], float)
#Reads the data set into data
with open(age_file, mode='r') as file:
    reader = csv.reader(file)
    for row in reader:
        #data.append(row)
        if(row[AGE] != "Age"):
            totalage = int(row[AGE]) + (2024 - int(row[YEAR]))
            if(totalage <= 1):
                start_matrix[HATCHLING] += 1
            elif(totalage > 1 and totalage < 20):
                start_matrix[JUVENILE] += 1
            else:
                start_matrix[ADULT] += 1

past_trans = [start_matrix]
for i in range(21):
    year = CURRENTYEAR + i

    if(i != 0):
        #Recursively applying the transformation matrix
        past_trans.append(numpy.matmul(transformer, past_trans[i-1]))
    result = past_trans[i]
    egg = int(result[HATCHLING])
    hatch = int(result[JUVENILE])
    grown = int(result[ADULT])
    print("{0}: {1} hatchlings, {2} juveniles, and {3} adults.\n".format(year, egg, hatch, grown))

