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
print("nodes")
client.create_node("test1", "name1")
client.create_node("test2", "name2")
for node in Node.select():
	print(str(node.item_id) + ', ' + node.source_key + ', ' + node.name)

print("edges")
client.create_edge("edge1", "edge1", 0, 1)
edge = client.get_edge("edge1")
# print(edge.item_id)
# print(edge.source_key)
# print(edge.name)
# print(edge.from_node_id)
# print(edge.to_node_id)
# for edge in e:
# 	print(str(edge.item_id) + ', ' + edge.source_key + ', ' + edge.name)
# 	print(edge.from_node_id)
# 	print(edge.to_node_id)

print("graph")
