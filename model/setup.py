from peewee import * 

db = SqliteDatabase('database.db') #find a better way to do this?

class Version(Model):
	id = BigIntegerField(primary_key=True) #primary key

class VersionSuccessor(Model):
	id = BigIntegerField(primary_key=True)
	from_version_id = BigIntegerField() #references version(id)
	to_version_id = BigIntegerField() #references version(id)
	#constraint: version_successor_unique_endpoints = Unique (from_version_id, to_version_id)

class Item(Model):
	id = BigIntegerField(primary_key=True)

class ItemTag(Model):
	item_id = BigIntegerField() #references Item(id)
	key = CharField()
	value = CharField(null=True)
	data_type1 = BigIntegerField()
	data_type2 = CharField()
	data_type3 = BooleanField()
	#constraint item_tag_pkey Primary key (item_id, key)

class VersionHistoryDag(Model):
	item_id = BigIntegerField() #references item(id)
	version_successor_id = BigIntegerField() #references version_successor(id)
    # CONSTRAINT version_history_dag_pkey PRIMARY KEY (item_id, version_successor_id)


class Edge(Model):
	item_id = BigIntegerField(null=True)
	#we are omitting item_id until I figure out what is happening
	source_key = CharField(unique=True)
	from_node_id = BigIntegerField()
	to_node_id = BigIntegerField()
	name = CharField()
	
	class Meta:
		database = db

class EdgeVersion(Model):
	id = BigIntegerField()
	edge_id = BigIntegerField()
	from_node_version_start_id = BigIntegerField()
	from_node_version_end_id = BigIntegerField()
	to_node_version_start_id = BigIntegerField()
	to_node_version_end_id = BigIntegerField()
	#not in actual ground model
	reference = CharField(null=True)
	reference_parameters = CharField(null=True)
	tags = CharField(null=True)
	structure_version_id = BigIntegerField()
	parent_ids = BigIntegerField(null=True)

	class Meta:
		database = db

class Graph(Model):
	item_id = BigIntegerField()
	source_key = CharField()
	name = CharField()

	class Meta:
		database = db

class GraphVersion(Model):
	id = BigIntegerField()
	graph_id = BigIntegerField() #question about the implementation of this model

	class Meta:
		database = db

class Node(Model):
	#item_id = BigIntegerField()
	source_key = CharField()
	name = CharField()

	class Meta:
		database = db

class NodeVersion(Model):
	#id = BigIntegerField()
	node_id = BigIntegerField()

	class Meta:
		database = db

class RichVersion(Model):
	#id = BigIntegerField()
	structure_version_id = BigIntegerField()
	reference = CharField()

	class Meta:
		database = db

class Structure(Model):
	#item_id = BigIntegerField()
	source_key = CharField()
	name = CharField()

	class Meta:
		database = db

class StructureVersion(Model):
	# id = BigIntegerField()
	structure_id = BigIntegerField()

	class Meta:
		database = db

#These may be unnecessary? In ground spec but not in grit
class StructureVersionAttribute(Model):
	structure_version_id = BigIntegerField()
	key = CharField()
	type = CharField()
	#constraint: structure_version_attribute_pkey = structure_version_id + key

	class Meta:
		database = db

class RichVersionExternalParameter(Model):
	rich_version_id = BigIntegerField()
	key = CharField()
	value = CharField()
	#constraint: rich_version_external_parameter_pkey = rich_version_id + key

	class Meta:
		database = db

class RichVersionTag(Model):
	rich_version_id = BigIntegerField()
	key = CharField()
	value = CharField()
	type = CharField() #is actually data_type

	class Meta:
		database = db

class GraphVersionEdge(Model):
	graph_version_id = BigIntegerField()
	edge_version_id = BigIntegerField()
	#constraint: graph_version_edge_pkey = graph_version_id + edge_version_id

	class Meta:
		database = db

#----Usage----
class LineageEdge(Model):
	#item_id = BigIntegerField()
	source_key = CharField()
	name = CharField()

	class Meta:
		database = db

class LineageEdgeVersion(Model):
	# id = BigIntegerField()
	lineage_edge_id = BigIntegerField()
	from_rich_version_id = BigIntegerField()
	to_rich_version_id = BigIntegerField()
	principal_id = BigIntegerField()

	class Meta:
		database = db

class LineageGraph(Model):
	#item_id = BigIntegerField()
	source_key = CharField()
	name = CharField()

	class Meta:
		database = db

class LineageGraphVersion(Model):
	# id = BigIntegerField()
	lineage_graph_id = BigIntegerField()

	class Meta:
		database = db

#Possibly unnessary
class LineageGraphVersionEdge(Model):
	lineage_graph_version_id = BigIntegerField()
	lineage_edge_version_id = BigIntegerField()
	#constraint: lineage_graph_version_edge_pkey = lineage_graph_version_id + lineage_edge_version_id

	class Meta:
		database = db

class Principal(Model):
	node_id = BigIntegerField()
	source_key = CharField()
	name = CharField()

	class Meta:
		database = db

#----Versions----
class Item(Model):
	# id = BigIntegerField()

	class Meta:
		database = db

class Tag(Model):
	#item_id = BigIntegerField()
	key = CharField()
	value = CharField()
	type = CharField() # is actually data_type
	#constraint: item_tag_pkey = item_id + key

class Version(Model):
	# id = BigIntegerField()

	class Meta:
		database = db

class VersionHistoryDag(Model):
	#item_id = BigIntegerField()
	version_successor_id = BigIntegerField()
	#constraint version_history_dag_pkey = item_id + version_successor_id

class VersionSuccessor(Model):
	# id = BigIntegerField()
	from_version_id = BigIntegerField()
	to_version_id = BigIntegerField()
	#constraint version_successor_unique_endpoints is unique from (from_version_id, to_version_id)
