import matplotlib.pyplot as plt
import csv

x = []
y = []

with open('exoskeleton_data.csv') as csvfile:
	lines = csv.reader(csvfile, delimiter=',')
	for row in lines:
		x.append(row[2])
		y.append(float(row[1]))


plt.plot(y, color='r', label= 'Motor current')
plt.xticks(rotation = 90)
plt.ylabel('Current in amps')
plt.grid()
plt.show()