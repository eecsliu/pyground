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
for node in Node.select().where((Node.name == "name1") | (Node.name == "name2")):
	print(str(node.id) + ', ' + node.source_key + ', ' + node.name)

for item in Item.select():
	print(item.id)

# print(RichVersion.select().exists())

print("node versions")
client.create_node_version(0)
client.create_node_version(2)
identity = (Node.get(Node.source_key == "test1")).id
print(identity)
for node in NodeVersion.select().where(NodeVersion.node_id == identity).order_by(NodeVersion.id.desc()):
	print(str(node.id) + ', ' + str(node.node_id))

print("checking version successor")
#there shouldn't be a version successor yet
for node in VersionSuccessor.select():
	print(str(node.id) + ', ' + str(node.from_version_id))# + ', ' + str(node.to_version_id))

print("checking DAG")
#there shouldn't be a dag yet
for node in VersionHistoryDag.select():
	print(str(node.id) + ', ' + str(node.version_successor_id))

print("edges")
#bug in edges
# client.create_edge("edge1", "edge1", 0, 1)
# edge = client.get_edge("edge1")
# print(edge.from_node_id)
# print(edge.to_node_id)
# for edge in Edge.select():
# 	print(str(edge.item_id) + ', ' + edge.source_key + ', ' + edge.name)
# 	print(edge.from_node_id)
# 	print(edge.to_node_id)

print("graph")

