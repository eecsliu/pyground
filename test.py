from peewee import * 
from model.setup import *
from client import *
import os

class Test(object):
	def __init__(self):
		self.z =0

# origin = os.getcwd()
# os.chdir(os.path.expanduser("~"))
client = PygroundClient()
print(Edge.table_exists())
client.create_edge("test1", "name1", 2, 3)
# print(Edge.select(Edge.name == 'name1'))
print()
print()
for edge in Edge.select():
	print(str(edge.item_id) + ', ' + edge.source_key + ', ' + edge.name + ', ' + 
		str(edge.from_node_id) + ', ' + str(edge.to_node_id))

client.create_edge_version(edge.item_id, 1, 2)

for edge in EdgeVersion.select():
	print(str(edge.id) + ', ' + str(edge.edge_id) + ', ' + str(edge.structure_version_id) + ', ' + 
		str(edge.from_node_version_start_id) + ', ' + str(edge.to_node_version_end_id))