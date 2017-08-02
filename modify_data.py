import csv
from collections import defaultdict

def read_data():
	data = []
	with open('data_2.csv','rb') as f:
		reader = csv.reader(f)
		for i in reader:
			data.append(i)

	routes = []
	k = 0
	for i in range(len(data)):
		if ['']*len(data[i]) == data[i]: #completely empy row signifies end of a route.
			routes.append(data[k:i+1])
			k = i

	routes.append(data[100:len(data)])

	#d = defaultdict(list)
	#for r in range(1,len(routes)-1):
	#	for j in range(3,len(routes[r]-1):
	#		d[

	return routes

"""
take routes.pkl and transform
: for k in keys:
    ...:     for j in range(len(d[k])):
    ...:         rr = []
    ...:         kk = d[k][j].keys()
    ...:         kk.remove('rupee')
    ...:         kk.remove('usd')
    ...:         rr.append({'name':kk[0]})
    ...:         rr.append({'rupee':d[k][j]['rupee']})
    ...:         rr.append({'usd':d[k][j]['usd']})
    ...:         rr.append({'time':d[k][j][kk[0]]})
    ...:         ss[k].append(rr)
    ...:         
"""


if __name__ == '__main__':
	read_data()
