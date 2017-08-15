#finding the lowest weight path through a weighted directed tree with a start point
#note: levels are numbers cannot be negetive

class DirectedTree(object):
	def __init__(self):
		self.vertex_dict = {}
		self.edge_dict = {}
		self.level_dict = {}
		
	def get_Vertex(self, name):
		return self.vertex_dict[name]
		
	def get_Edge(self, name):
		return self.edge_dict[name]
		
	def get_Level(self, name):
		return self.level_dict[name]
	
	class Edge(object):
		def __init__(self, start, end, weight):
			self.start = start 
			self.end = end
			self.weight = weight
			
	class Vertex(object):
		def __init__(self, name, level, weight):
			self.name = name
			#all children of a vertex in lower levels all parents in higher levels
			self.level = level
			self.weight = weight
			self.children = []
			self.parents = []
			#smallest level of child of a vertex
			self.minlevel = -1

	class Level(object):
		def __init__(self, name):
			self.name = name
			self.vertices = []
	
	def add_Level(self, name):
		self.level_dict[name] = self.Level(name)
	
	def del_Level(self, name):
		for vertex in self.get_Level(name).vertices:
			self.del_Vertex(vertex)
		del self.level_dict[name]
		
	def add_Vertex(self, name, level, weight=0):
		if level in self.level_dict.keys():
			self.get_Level(level).vertices.append(name)
		else:
			self.add_Level(level)
			self.get_Level(level).vertices.append(name)
		self.vertex_dict[name]= self.Vertex(name, level, weight)
	
	def del_Vertex(self, name):
		for vertex in self.get_Vertex(name).children:
			self.del_Edge(name,vertex)
		for vertex in self.get_Vertex(name).parents:
			self.del_Edge(vertex,name)
		self.get_Level(self.get_Vertex(name).level).vertices.remove(name)
		del self.vertex_dict[name]
		
	def add_Edge(self, start, end, weight=0):
		try: int(weight)
		except ValueError:
			return 'weight is not a number'
		if start not in self.vertex_dict.keys() or end not in self.vertex_dict.keys():
			return'this edge is not between two vertices'
		#assumes levels are numbers
		if self.get_Vertex(start).level > self.get_Vertex(end).level:
			return 'this edge goes from a higher level vertex to a lower level vertex'
		# to keep only edges with smallest or largest weights because the other edge is always wasted
		elif (start, end) in self.edge_dict.keys():
			#if get_Edge((start, end)).weight > weight:
			 if self.get_Edge((start, end)).weight < weight:
				self.get_Edge((start, end)).weight = weight
		else:
			self.edge_dict[(start,end)] = self.Edge(start,end,weight)
			self.get_Vertex(start).children.append(end)
			self.get_Vertex(end).parents.append(start)
			if self.get_Vertex(end).level < self.get_Vertex(start).minlevel or self.get_Vertex(start).minlevel==-1:
				self.get_Vertex(start).minlevel = self.get_Vertex(end).level
				
	def del_Edge(self, start, end):
		del self.edge_dict[(start,end)]
		try:
			self.get_Vertex(start).children.remove(end)
			self.get_Vertex(end).parents.remove(start)
		except KeyError:
			pass
	
	def move_Vertex(self, name, level):
		if level not in self.level_dict.keys():
			self.add_Level(level)
		start_Level = self.get_Vertex(name).level
		self.get_Level(start_Level).vertices.remove(name)
		self.get_Vertex(name).level = level
		self.get_Level(level).vertices.append(name)
		
	def move_Level(self,start, new):
		#moves all vertices from start level to new level
		list=self.get_Level(start).vertices[:]
		for vertex in list:
			self.move_Vertex(vertex, new)		
	
	def move_Levels(self,start, delta):
		#move all vertices from start level and higher up delta levels down
		#assumes levels are numbers
		sorted_keys = self.level_dict.keys()
		sorted_keys.sort()
		sorted_keys.reverse()
		for level in sorted_keys:
			try:
				if level >= start:
					next = level+delta
					self.move_Level(level, next)
			except ValueError:
				return 'cannot move levels if they are not numbers'

def list_of_tuples(list,number):
	#turns a list of tuples into a list of a number element in the tuple
	out= []
	for element in list:
		sub_tuple=element[number]
		out.append(sub_tuple)
	return out

def max_first(list):
	#takes a list of 2-tuples returns tuple with highest first element
	weights = list_of_tuples(list,0)
	max_weight = max(weights)
	max_weight_index = weights.index(max_weight)
	tuple = list[max_weight_index]
	return tuple
			
def optimal_weighted_path_edges(tree):
#takes a directed tree with weighted edges and returns a path with maximum weight by working backwards
	dict={}
	for vertex in tree.vertex_dict.keys():
		dict[vertex]=[(0,['>'])]
	tree.level_dict.keys().sort
	sorted_levels=tree.level_dict.keys()
	
	def sub_function(sorted_levels,dict):
		bottom_level=tree.get_Level(sorted_levels.pop()).vertices
		list=[]	
		for vertex in bottom_level:
			weights_list = dict[vertex][:]
			max_weight_info = max_first(weights_list)
			tree.get_Vertex(vertex).weight = max_weight_info[0]
			prev = max_weight_info[1]
			prev.append(vertex)
			for parent in tree.get_Vertex(vertex).parents:
				weight=tree.get_Edge((parent,vertex)).weight+tree.get_Vertex(vertex).weight
				dict[parent].append((weight,prev))
		
			if len(sorted_levels)==0:
				list.append((max_weight_info[0], prev))
		if len(sorted_levels)==0:
			max_weight = max_first(list)
			max_weight[1].reverse()
			prev=max_weight[1]
			history=''
			for part in prev:
				history += str(part) + ' > '
			return max_weight[0], history[:-7], prev
		return sub_function(sorted_levels,dict)	
	return sub_function(sorted_levels,dict)
	
def optimal_weighted_path_vertices(tree):
	#takes a directed tree with weighted vertices and returns a path with maximum weight if it also has weighted edges replace = with += in  the for loop 
	for edge in tree.edge_dict.keys(): 
		tree.get_Edge(edge).weight=tree.get_Vertex(tree.get_Edge(edge).end).weight
	for top in tree.get_Level(0).vertices:
		for child in tree.get_Vertex(top).children:
			tree.get_Edge((top,child)).weight+=tree.get_Vertex(top).weight
	return optimal_weighted_path_edges(tree)

def optimal_weighted_path_vertices_level(tree):
	#assumes levels are numbers
	#takes a directed tree with weighted vertices whose children are all vertices of a certain level and below and returns a path with maximum weight
	#this was created as a solution for creating a maximum weight set of nonoverlapping requests from a set of requests with weights
	newtree = DirectedTree()
	sorted_levels = sorted(tree.level_dict.keys())
	bottom_level = sorted_levels[-1] + 1
	for level in tree.level_dict.keys():
		newtree.add_Vertex(level,level,1)
	newtree.add_Vertex(bottom_level,bottom_level,1)
	for vertex in tree.vertex_dict.keys():
		if tree.get_Vertex(vertex).children:
			for level in sorted_levels:
				if level >= tree.get_Vertex(vertex).minlevel: 
					newtree.add_Edge(tree.get_Vertex(vertex).level, level,tree.get_Vertex(vertex).weight) 
		else:
			newtree.add_Edge(tree.get_Vertex(vertex).level, bottom_level, tree.get_Vertex(vertex).weight)
	soln = optimal_weighted_path_edges(newtree)
	
	soln_list=soln[2]
	soln_list.pop()
	out = []
	parents = []
	soln_list.reverse()
	
	for vertex in tree.get_Level(soln_list[1]).vertices:
		if not tree.get_Vertex(vertex).children:
			parents.append((tree.get_Vertex(vertex).weight,vertex))
	max_element = max_first(parents)
	out.append(max_element[1])
	i=2
	while i < len(soln_list):
		parents=[]
		for vertex in tree.get_Level(soln_list[i]).vertices:
			if tree.get_Vertex(vertex).minlevel<=soln_list[i-1]:
				parents.append((tree.get_Vertex(vertex).weight,vertex))
		max_element = max_first(parents)
		out.append(max_element[1])
		i += 1
	out.reverse()
	history = ''
	for part in out:
		history += str(part) + ' > '
	
	return soln[0], history[:-3], out 
	
tree = DirectedTree()
for i in range(0,10):
	tree.add_Vertex('vert_'+str(i),i,1)
for i in range(0,10):
	for j in range(0,10):
		if i < j:
			tree.add_Edge('vert_' + str(i),'vert_' + str(j),1)	
print optimal_weighted_path_edges(tree)