import cPickle as cp


def do_the_job(city_list,time,your_city,price=['2500','17']):
	global route_dict
	for c in city_list:
		for i in range(len(time)):
			k = {'name':str(c),'rupee':price[0],'time':str(time[i]),'usd':price[1]}
			if k not in route_dict[your_city]:
				route_dict[your_city].append(k)


def process():
	global route_dict
	route_dict['trincomalee'] = route_dict['trincomalee'] + route_dict['trinco'] #SAME		
	del route_dict['nuwara']
		
	time = ['03:40','17:00','10:30']
	city = ['baticloa','pasikudah','galle','polonaruwa','trincomalee','nilaveli']
	do_the_job(city,time,'bia')

	time = ['20:30','04:00','14:30']
	city = ['bia']
	do_the_job(city,time,'galle')

	time = ['08:00','12:00','22:00']
	city = ['hatton','nuwaraeliya']
	do_the_job(city,time,'galle')

	time = ['07:30','23:30']
	city = ['arugam','baticloa','pasikudah','trinco','nilaveli']
	do_the_job(city,time,'hambantota',price=['3500','23'])

	time = ['08:00','12:00','00:00']
	city = ['hatton','nuwaraeliya']
	do_the_job(city,time,'hambantota')

	time = ['15:15','07:30']
	city = ['udawalawe']
	do_the_job(city,time,'arugam',price=['3500','23'])

	time = ['13:15','05:15']
	city = ['baticloa','pasikudah','trinco','nilaveli']
	do_the_job(city,time,'arugam',price=['3500','23'])

	time = ['08:00','14:45','21:15']
	city = ['polonaruwa','trincomalee','nilaveli','polonaruwa','baticloa','pasikudah']
	do_the_job(city,time,'dambula')

	time = ['11:30','14:30','01:30']
	city = ['kandy','nuwara','hatton']
	do_the_job(city,time,'dambula')

	time = ['17:45','20:45','07:45']
	city = ['polonaruwa']
	do_the_job(city,time,'dambula')

	time = ['16:00','23:30','10:00']
	city = ['polonaruwa','dambula','bia']
	do_the_job(city,time,'baticloa')

	time = ['12:00','04:15']
	city = ['arugam','udawalawe','hambantota']
	do_the_job(city,time,'baticloa',price=['3500','23'])

	time = ['16:30','08:30']
	city = ['pasikudah','trinco','nilaveli']
	do_the_job(city,time,'baticloa',price=['3500','23'])

	time = ['10:00','13:00','00:00']
	city = ['nuwaraeliya','kandy','dambula']
	do_the_job(city,time,'hatton')

	time = ['09:40','13:45','01:45']
	city = ['udawalawe','hambantota']
	do_the_job(city,time,'hatton')

	time = ['14:15','18:15','06:15','16:15','20:15','06:15']
	city = ['nuwaraeliya']
	do_the_job(city,time,'hatton')

	time = ['09:45','13:45','23:45']
	city = ['mirissa','galle']
	do_the_job(city,time,'hatton')


	time = ['15:00','22:30','09:00']
	city = ['baticloa','polonoruwa','dambula']
	do_the_job(city,time,'pasikudah')


	time = ['11:00','03:15']
	city = ['baticloa','arugam','udawalawe','hambantota']
	do_the_job(city,time,'pasikudah',price=['3500','23'])

	time = ['17:30','09:30']
	city = ['trinco','nilaveli']
	do_the_job(city,time,'pasikudah',price=['3500','23'])

	time = ['14:30','17:30','04:30']
	city = ['nuwara','hatton']
	do_the_job(city,time,'kandy')

	time = ['14:45','17:45','04:45']
	city = ['dambula','polonaruwa']
	do_the_job(city,time,'kandy')



	time = "09:30	13:30	23:30".split()
	city = ['hatton','nuwaraeliya']
	do_the_job(city,time,'mirissa')

	time = "09:45	13:45	23:45".split()
	city = ['galle']
	do_the_job(city,time,'mirissa')


	time = "17:30	20:30	07:30".split()
	city = ['hatton']
	do_the_job(city,time,'nuwaraeliya')

	time = "11:45	14:45	01:45".split()
	city = "Kandy Dambula Polonaruwa".lower().split()
	do_the_job(city,time,'nuwaraeliya')

	time = "08:00	12:00	00:00".split()
	city = "Hatton Udawalawa Hambantota".lower().split()
	do_the_job(city,time,'nuwaraeliya')

	time = "08:00	12:00	22:00".split()
	city = "Hatton Mirissa Galle".lower().split()
	do_the_job(city,time,'nuwaraeliya')

	time = "15:00	22:30	09:00".split()
	city = """Trincomalee Polonoruwa Dambulla BIA""".lower().split()
	do_the_job(city,time,'nilaveli')


	time = "07:30	23:30".split()
	city = """Trinco
	Pasikudah
	Baticloa
	Arugam
	Udawalawe
	Hambantota
	""".lower().split()
	do_the_job(city,time,'nilaveli',price=['3500','23'])


	time = "16:00	23:30	10:00".split()
	city = "Polonoruwa Dambulla BIA".lower().split()
	do_the_job(city,time,'trincomalee')

	time = "08:30	00:45".split()
	city = """Pasikudah
	Baticloa
	Arugam
	Udawalawe
	Hambantota
	""".lower().split()
	do_the_job(city,time,'trincomalee',price=['3500','23'])


	time = "09:45	16:30	23:00".split()
	city = """Trincomalee Nilaveli baticloa pasikudah""".lower().split()
	do_the_job(city,time,'polonaruwa')

	time = "18:45	02:15	12:45 18:15 01:45".split()
	city = "Dambulla BIA".lower().split()
	do_the_job(city,time,'polonaruwa')

	time = "10:00	13:00	00:00".split()
	city = """Dambula
	Kandy
	Nuwara
	Hatton""".lower().split()
	do_the_job(city,time,'polonaruwa')


	time = '09:15	01:15'.split()
	city = """Arugam
	Baticloa
	Pasikudah
	Trinco
	Nilaveli
	""".lower().split()
	do_the_job(city,time,'udawalawa',price=['3500','23'])

	time = '09:45	13:45	01:45'.split()
	city = "Hatton Nuwaraeliya".split()
	do_the_job(city,time,'udawalawa')


def create_route():
	with open('routes_final.pkl','rb') as f: #routes_final is updated version
		route_dict = cp.load(f)
	global route_dict
	process()
	return route_dict
	

