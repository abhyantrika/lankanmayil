from collections import defaultdict
import cPickle as cp


class Graph():
	def __init__(self,vertices):
		self.V= vertices
		self.graph = defaultdict(list)
		self.results = []

	def addEdge(self,u,v):
		self.graph[u].append(v)

	def util(self,start,goal):
		stack = [(start, [start])]
		while stack:
			(vertex, path) = stack.pop()
			for next in (set(self.graph[vertex]) - set(path)):
				if next == goal:
					yield path + [next]
				else:
					stack.append((next, path + [next]))

	def get_all_paths(self,start,goal):
		visited =[False]*(self.V)
		return self.util(start,goal)


def spell_correction(dest,keys):
	dest = dest[:3].lower()
	for k in keys:
		if dest == k[:3].lower():
			return k
	return None

def create_graph(route):
	#with open('routes_final.pkl','rb') as ff:
	#	route = cp.load(ff)
	keys = route.keys()
	mapping = defaultdict()
	g = Graph(18)

	for i in range(len(keys)):
		mapping[keys[i]] = i
	e = 0
	for k in keys:
		dest = []
		for r in route[k]:
			dest.append(r['name'])
		dest = list(set(dest))
		src = mapping[k]
		for d in dest:
			try:
				nearest_spelling = spell_correction(d,keys)
				g.addEdge(src,mapping[nearest_spelling])
				print 'edge ',e,' added'
				e+=1
			except:
				print k
				continue
	print 'graph created!'
	return g,mapping

