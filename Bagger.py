import csv
import sys
import operator
import pandas as pd

ip1 = "alpharesults/output1.csv"
ip2 = "alpharesults/output2.csv"

def loadData(datafile):
	return pd.read_csv(datafile)

x1 = loadData(ip1)
x2 = loadData(ip2)
z = loadData(ip1)

print len(x1['count'])

for index in range(0,len(x1['count'])):
	a = x1['count'][index]
	b = x2['count'][index]
	#c = x3['count'][index]
	#d = x4['count'][index]
	#e = x5['count'][index]
	z['count'][index] = int((a+b+1)/2)


with open("alpharesults/final.csv", 'wb') as f:
	f.write("datetime,count\n")
	for index in range(0,len(x1['count'])):
		f.write("%s,%s\n" % (z['datetime'][index], z['count'][index]))



