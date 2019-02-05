from peewee import * 

db = SqliteDatabase('database.db') #find a better way to do this?

### Versions ###
class Version(Model):
	id = BigIntegerField(primary_key=True) #primary key

	class Meta:
		database = db

class VersionSuccessor(Model):
	id = BigIntegerField(primary_key=True)
	from_version_id = ForeignKeyField(Version) #references version(id)
	to_version_id = ForeignKeyField(Version) #references version(id)

	class Meta:
		database = db
		indexes = (
			(('from_version_id', 'to_version_id'), True), #version_successor_unique_endpoints
			)

class Item(Model):
	id = BigIntegerField(primary_key=True)

	class Meta:
		database = db

class ItemTag(Model):
	item_id = ForeignKeyField(Item) #BigIntegerField() #references Item(id)
	key = CharField()
	value = CharField(null=True)
	data_type1 = BigIntegerField(null=True)
	data_type2 = CharField(null=True)
	data_type3 = BooleanField(null=True)

	class Meta:
		primary_key = CompositeKey('item_id', 'key') #item_tag_pkey
		database = db

class VersionHistoryDag(Model):
	item_id = ForeignKeyField(Item) #BigIntegerField() #references item(id)
	version_successor_id = ForeignKeyField(VersionSuccessor, to_field='id') #references version_successor(id)

	class Meta:
		primary_key = CompositeKey('item_id', 'version_successor_id') #version_history_dag_pkey
		database = db

### Models ###
class Structure(Model):
	item_id = ForeignKeyField(Item) #BigIntegerField(primary_key=True) #references item(id)
	source_key = CharField(unique=True)
	name = CharField(null=True)

	class Meta:
		database = db

class StructureVersion(Model):
	id = ForeignKeyField(Version) #references version(id)
	structure_id = ForeignKeyField(Structure, to_field='id') #references structure(item_id)
	#structure must exist 

	class Meta:
		database = db

#These may be unnecessary? In ground spec but not in grit
class StructureVersionAttribute(Model):
	structure_version_id = ForeignKeyField(StructureVersion, to_field='id') #ref structure_version(id)
	key = CharField()
	type = CharField()

	class Meta:
		primary_key = CompositeKey('structure_version_id', 'key') #structure_version_attribute_pkey
		database = db

class RichVersion(Model):
	id = ForeignKeyField(Version) #primary key!
	structure_version_id = ForeignKeyField(StructureVersion, to_field='id', null=True) #references structure_version(id)
	#the structure version must exist first
	reference = CharField(null=True)

	class Meta:
		database = db

#In Ground but not grit
class RichVersionExternalParameter(Model):
	rich_version_id = ForeignKeyField(RichVersion, to_field='id') #references rich_version(id)
	key = CharField()
	value = CharField()

	class Meta:
		primary_key = CompositeKey('rich_version_id', 'key') #rich_version_external_parameter_pkey
		database = db

#in ground but not grit
class RichVersionTag(Model):
	rich_version_id = ForeignKeyField(RichVersion, to_field='id')
	key = CharField()
	value = CharField(null=True)
	data_type1 = BigIntegerField(null=True)
	data_type2 = CharField(null=True)
	data_type3 = BooleanField(null=True)

	class Meta:
		primary_key = CompositeKey('rich_version_id', 'key') #rich_version_tag_pkey = (rich_version_id, key)
		database = db

class Node(Model):
	item_id = ForeignKeyField(Item) #references item(id)
	source_key = CharField(unique=True)
	name = CharField(null=True)

	class Meta:
		database = db

class Edge(Model):
	item_id = ForeignKeyField(Item) #references item(id)
	source_key = CharField(unique=True, null=True)
	from_node_id = ForeignKeyField(Node, to_field='item_id')
	to_node_id = ForeignKeyField(Node, to_field='item_id')
	#nodes must first exist
	name = CharField(null=True)
	
	class Meta:
		database = db

class Graph(Model):
	item_id = ForeignKeyField(Item) #references item(id)
	source_key = CharField(unique=True, null=True)
	name = CharField(null=True)

	class Meta:
		database = db

class NodeVersion(Model):
	id = ForeignKeyField(RichVersion, to_field='id') #references rich_version(id)
	node_id = ForeignKeyField(Node, to_field='item_id') #references node(item_id)
	#node must previously exist

	class Meta:
		database = db

class EdgeVersion(Model):
	id = ForeignKeyField(RichVersion, to_field='id') #references rich_version(id)
	edge_id = ForeignKeyField(Edge, to_field='item_id') #references edge(item_id)
	from_node_version_start_id = ForeignKeyField(NodeVersion, to_field='id')
	from_node_version_end_id = ForeignKeyField(NodeVersion, to_field='id', null=True)
	to_node_version_start_id = ForeignKeyField(NodeVersion, to_field='id')
	to_node_version_end_id = ForeignKeyField(NodeVersion, to_field='id', null=True) #all reference node_version(id)

	class Meta:
		database = db

class GraphVersion(Model):
	id = ForeignKeyField(RichVersion, to_field='id') #references rich_version(id)
	graph_id = ForeignKeyField(Graph, to_field='item_id') #references graph(item_id)

	class Meta:
		database = db

#in ground but not in grit
class GraphVersionEdge(Model):
	graph_version_id = ForeignKeyField(GraphVersion, to_field='id') #references graph_version(id)
	edge_version_id = ForeignKeyField(EdgeVersion, to_field='id') #references edge_version(id)

	class Meta:
		primary_key = CompositeKey('graph_version_id', 'edge_version_id') #graph_version_edge_pkey
		database = db

### Usage ###
#This is in ground but not in grit
class Principal(Model):
	node_id = ForeignKeyField(Node, to_field='id') #ref node(item_id)
	source_key = CharField(null=True, unique=True)
	name = CharField(null=True)

	class Meta:
		database = db

class LineageEdge(Model):
	item_id = ForeignKeyField(Item) #ref item(id)
	source_key = CharField(null=True, unique=True)
	name = CharField(null=True)

	class Meta:
		database = db

class LineageEdgeVersion(Model):
	id = ForeignKeyField(RichVersion, to_field='id') #ref rich_version(id)
	lineage_edge_id = ForeignKeyField(LineageEdge, to_field='item_id') #ref lineage_edge(id)
	from_rich_version_id = ForeignKeyField(RichVersion, to_field='id') #ref rich_version(id)
	to_rich_version_id = ForeignKeyField(RichVersion, to_field='id') #ref rich_version(id)
	#not sure if principal is necessary
	# principal_id = ForeignKeyField(NodeVersion, to_field='id') #ref node_version(id)

	class Meta:
		database = db

class LineageGraph(Model):
	item_id = ForeignKeyField(Item) #ref item(id)
	source_key = CharField(null=True, unique=True)
	name = CharField(null=True)

	class Meta:
		database = db

class LineageGraphVersion(Model):
	id = ForeignKeyField(RichVersion, to_field='id') #ref rich_version(id)
	lineage_graph_id = ForeignKeyField(LineageGraph, to_field='id') #ref lineage_graph(item_id)

	class Meta:
		database = db

#In ground but not in grit
class LineageGraphVersionEdge(Model):
	lineage_graph_version_id = ForeignKeyField(LineageGraphVersion, to_field='id') #ref lineage_graph_version(id),
	lineage_edge_version_id = ForeignKeyField(LineageEdgeVersion, to_field='id') #ref lineage_edge_version(id),

	class Meta:
		primary_key = CompositeKey('lineage_graph_version_id', 'lineage_edge_version_id')
		database = db

