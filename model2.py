dataPath = "data/"
outPath = "alpharesults/"

import pandas as pd

import datetime

#scikit Machine learning kit in Python

from sklearn import preprocessing

from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.neighbors import KNeighborsRegressor

def loadData(datafile):
	return pd.read_csv(datafile)

#extract more usable information from "datetime" field
def splitDatetime(data):
	#first split the field into seperate date and time fields
	sub = pd.DataFrame(data.datetime.str.split(' ').tolist(), columns = "date time".split())
	
	#split into day and time info
	date = pd.DataFrame(sub.date.str.split('-').tolist(), columns="year month day".split())
	
	#extract hour information, minute and second info is not used
	time = pd.DataFrame(sub.time.str.split(':').tolist(), columns = "hour minute second".split())
	
	#make custom data array to hold all the relevant extracted information
	data['year'] = date['year']
	data['month'] = date['month']
	data['day'] = date['day']
	data['hour'] = time['hour'].astype(int)
	count = 0;
	
	#the following is done to further make a field that virtually divides a week into weekends(Sat, Sun), midweek (Tue, Wed, Thu), and others(Mon, Fri).
	#this was expected to yield some better pattern since days in the middle of the week are slightly different from mondays and fridays.
	#not to mention this also marks a field for weekends and further enphises the weekend data field.
	weekend = set([5, 6])
	
	week = []
	
	#daypart is used to further classify the hours of the day together. 
	#There is a similar pattern observed in hours of the day. 
	#So, classifying the day into morning, noon, and evening hours etc helps the learning algorithm to better group together morning and afternoon hours.
	daypart = []
	weekpart = []
	
	for x in range(0,len(date['year'])):
		y = data['year'][x];
		m = data['month'][x];
		d = data['day'][x];
		time = datetime.date(int(y), int(m), int(d))
		
        	h = data['hour'][x]
		if(h>=6 and h <=9):
			daypart.append(0);
		elif(h>=10 and h<=15):
			daypart.append(1);
		elif(h>=16 and h<=19):
			daypart.append(2);
		elif(h>=20 and h<=23 or h==0):
			daypart.append(3);
		else:
			daypart.append(4);
		week.append(time.weekday());

		x = time.weekday()
		if (x==0 or x==4):
			weekpart.append(0)
		elif (x==1 or x==2 or x==3):
			weekpart.append(1)
		else:
			weekpart.append(2)
	data['weekday'] = week;
	data['daypart'] = daypart;
	data['weekpart'] = weekpart;
	#print len(week)
	#for x in data:
	#	print x
	return data
	
#these are the initializer functions to generate the learned pattern. 
def createExtraTree():
    est = ExtraTreesRegressor(n_estimators=100,verbose=1)
    return est

def createRandomForest():
    est = RandomForestRegressor(n_estimators=100)
    return est

def createGradientBoostingRegressor():
    est = GradientBoostingRegressor()
    return est

# fit(x,y) fits the model given to it as a parameter 
def predict(est, train, test, features, target):
	est.fit(train[features], train[target])
	return est

def main():

	train = loadData(dataPath + "train.csv")
	test = loadData(dataPath + "test.csv")

	#split and make appropriate format of usable data.
	train = splitDatetime(train)
	test = splitDatetime(test)
	
	target1 = 'casual'
	#some useless features ignored form the data. rest are read into features1 to be fed into scikit function
	features1 = [col for col in train.columns if col not in ['datetime', 'casual', 'registered', 'count']]
	
	# object of Random Forest
	casual = createRandomForest()
	
	# Fit the model
	casual = predict(casual, train, test, features1, target1)
	
	target2 = 'registered'
	
	#for registered users, an entirely seperate learning model is generated using ExtraTree instead of RandomForest
	features2 = [col for col in train.columns if col not in ['datetime', 'casual', 'registered', 'count']]
	
	# Object of Extremely Randomized Tree	
	regis = createExtraTree()
	
	# Fit the model
	regis = predict(regis, train, test, features2, target2)

	with open(outPath + "output2.csv", 'wb') as f:
		f.write("datetime,count\n")
		
		#predict(X) method of the regressor that, given unlabeled observations test[features], returns the predicted label.
		l1 = list(casual.predict(test[features1]))
		l2 = list(regis.predict(test[features2]))
		l3 = []
		
		#Combining the 'casual' and 'registered' users into 'count' 
		for x in range(0,len(l1)):
			l3.append(int(l1[x])+int(l2[x]))
		
		#Writing final output to File
		for index, value in enumerate(l3):
			f.write("%s,%s\n" % (test['datetime'].loc[index], int(value)))


if __name__ == "__main__":
    main()
