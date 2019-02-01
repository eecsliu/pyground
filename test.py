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
	print(str(node.id) + ', ' + node.source_key + ', ' + node.name)

for item in Item.select():
	print(item.id)

print(RichVersion.select().exists())

print("node versions")
# client.create_node_version(0)
# client.create_node_version(2)
# identity = (Node.get(Node.source_key == "test1")).id
# print(identity)
# for node in NodeVersion.select().where(NodeVersion.node_id == identity).order_by(NodeVersion.id.desc()):
# 	print(str(node.id) + ', ' + str(node.node_id))

# print("checking version successor")
# for node in VersionSuccessor.select():
# 	print(str(node.id) + ', ' + str(node.from_version_id))# + ', ' + str(node.to_version_id))

# print("checking DAG")
# for node in VersionHistoryDag.select():
# 	print(str(node.id) + ', ' + str(node.version_successor_id))

# print("test get")
# test = NodeVersion.select().where(NodeVersion.node_id == identity).order_by(NodeVersion.id.desc()).get()
# print(test.id)

print("edges")
# client.create_edge("edge1", "edge1", 0, 1)
# edge = client.get_edge("edge1")
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

