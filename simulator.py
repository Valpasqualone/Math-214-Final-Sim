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
transform_matrix = numpy.array([[0,           0,    75/7], 
                           [0.56, (17/18) * 0.82, 0], 
                           [0,   (1/18) * 0.82, 0.9]], float)
#I have a thing in the google doc explaining how I got these changed numbers for the transition matrix
#feel free to mess with the values and see how it changes the pop over time 
start_matrix = numpy.array([0, 0, 0], float)
#Reads the data set into data
data = []
with open(age_file, mode='r') as file:
    reader = csv.reader(file)
    highestyear = 0
    for row in reader:
        data.append(row)
        #print(row[YEAR])
        if(row[YEAR] != "Year"):
            if(int(row[YEAR]) > highestyear):
                highestyear = int(row[YEAR])
        
    CURRENTYEAR = highestyear

for item in data:
    if(item[AGE] != "Age"):
        totalage = int(item[AGE]) + (CURRENTYEAR - int(item[YEAR]))
        if(totalage <= 1):
            start_matrix[HATCHLING] += 1
        elif(totalage > 1 and totalage < 20):
            start_matrix[JUVENILE] += 1
        else:
            start_matrix[ADULT] += 1

past_trans = [start_matrix]
egg = [start_matrix[HATCHLING]]
mid = [start_matrix[JUVENILE]]
grown = [start_matrix[ADULT]]
totalpop = [egg[0] + mid[0] + grown[0]]
year = [CURRENTYEAR]
for i in range(21):

    if(i != 0):
        #Recursively applying the transformation matrix
        year.append( (year[i-1] + 1))
        past_trans.append(numpy.matmul(transform_matrix, past_trans[i-1]))
        result = past_trans[i]
        egg.append(int(result[HATCHLING]))
        mid.append(int(result[JUVENILE]))
        grown.append(int(result[ADULT]))
        totalpop.append(egg[i] + mid[i] + grown[i])
        
    print("{0}: {1} hatchlings, {2} juveniles, and {3} adults.\n".format(year[i], egg[i], mid[i], grown[i]))

#Creating the graphs:
fig = matplotlib.pyplot.figure(figsize = (10, 5))
matplotlib.pyplot.bar(year, grown, color='navy', width=0.4,)
matplotlib.pyplot.xlabel("Year")
matplotlib.pyplot.ylabel("Adult Population")
matplotlib.pyplot.title("Adult Population Over Time")
matplotlib.pyplot.show()    
