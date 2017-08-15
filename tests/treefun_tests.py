from nose.tools import *
from treefun.treefun import *

tree = DirectedTree()
tree.add_Vertex('vert_1',0,2)
tree.del_Vertex('vert_1')

for i in range(0,10):
	tree.add_Vertex('vert_'+str(i),i,1)
	
tree.move_Levels(0,5)
for i in range(5,15):
	assert_equal(tree.get_Vertex('vert_'+str(i-5)).level,i)
	assert_equal(tree.get_Level(i).vertices,['vert_'+str(i-5)])
	assert_equal(tree.get_Level(0).vertices,[])
for i in range(0,10):
	for j in range(0,10):
		if i < j:
			tree.add_Edge('vert_' + str(i),'vert_' + str(j),1)
			tree.add_Edge('vert_' + str(i),'vert_' + str(j),2)
			assert_equal(tree.get_Edge(('vert_' + str(i),'vert_' + str(j))).weight,2)
			assert_equal(tree.add_Edge('vert_' + str(i),'vert_' + str(j),'w'), 'weight is not a number')
		if i < j:
			assert_equal(tree.add_Edge('vert_' + str(j),'vert_' + str(i)), 'this edge goes from a higher level vertex to a lower level vertex')
	assert_equal(tree.add_Edge('ver_'+str(i),'ver_' +str(j)), 'this edge is not between two vertices')

			
for i in range(0,15):
	tree.del_Level(i)
	
for i in range(0,10):
	tree.add_Vertex('vert_'+str(i),i,1)
for i in range(0,10):
	for j in range(0,10):
		if i < j:
			tree.add_Edge('vert_' + str(i),'vert_' + str(j),1)
assert_equal(max_first([(0,[2]),(2,[2])])[1],[2])			
#optimal_weighted_path_edges(tree)