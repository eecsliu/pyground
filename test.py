from peewee import * 
from model.setup import *
from client import *
import os

origin = os.getcwd()
os.chdir(os.path.expanduser("~"))
db = SqliteDatabase('database.db') #find a better way to do this?
db.connect()
print(Edge.table_exists())
db.create_tables([Edge])
print(Edge.table_exists())
create_edge("test1", "name1", 2, 3)
print(Edge.select(Edge.name == 'name1').from_node_id)
print()
print()
for edge in Edge.select(Edge.name == 'name1'):
	print(edge.name + '. ' + str(edge.from_node_id) + ', ' + str(edge.to_node_id))
db.close()