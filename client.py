import os

from model.setup import *
import globals

class PygroundClient(object):
	def __init__(self):
		self.path = globals.PYGROUND_D

		# if not os.path.isdir(self.path):
		# 	os.mkdir(self.path)
		db = SqliteDatabase('database.db') #find a better way to do this?
		db.connect()
		db.create_tables([Item, ItemTag, Version, VersionSuccessor, VersionHistoryDag, Structure,
			StructureVersion, RichVersion, Node, NodeVersion, Edge, EdgeVersion, Graph, 
			GraphVersion, LineageEdge, LineageEdgeVersion, LineageGraph, LineageGraphVersion])

		if not os.path.exists('next_id.txt'):
			with open('next_id.txt', 'w') as f:
				f.write('0')

		self.edge_dag = self._gen_id()
		self.graph_dag = self._gen_id()
		self.node_dag = self._gen_id()
		self.struct_dag = self._gen_id()
		self.lin_edge_dag = self._gen_id()
		self.lin_graph_dag = self._gen_id()

	def _gen_id(self):
		#borrowed from Grit
		with open('next_id.txt', 'r') as f:
			newid = int(f.read())
		nxtid = str(newid + 1)
		with open('next_id.txt', 'w') as f:
			f.write(nxtid)
		return int(newid)

	def _gen_item(self):
		id = self._gen_id()
		Item.create(id=id)
		return id

	def _gen_version(self):
		id = self._gen_id()
		Version.create(id=id)
		return id

	def _gen_rich_version(self):
		id = self._gen_version()
		RichVersion.create(id=id)
		return id

	def _get_latest_versions(self, current):
		latest_versions = []
		while current != []:
			id = current.pop()
			query = VersionSuccessor.select().where(VersionSuccessor.from_version_id == id)
			if not query.exists():
				latest_versions.append(id)
			else:
				for v in query:
					if v.to_version_id not in current:
						current.append(v.to_version_id)
		return latest_versions

	### EDGES ###
	def create_edge(self,_source_key, _name, _from_node_id, _to_node_id, tags=None):
		Edge.create(item_id=self._gen_item(), source_key=_source_key, from_node_id=_from_node_id, 
			to_node_id=_to_node_id, name=_name)
		#ignoring tags for now

	def create_edge_version(self, edge_id,
	                            from_node_version_start_id,
	                            to_node_version_start_id,
	                            from_node_version_end_id=-1,
	                            to_node_version_end_id=-1,
	                            reference=None,
	                            reference_parameters=None,
	                            tags=None,
	                            structure_version_id=-1,
	                            parent_ids=None):
		to_id = self._gen_rich_version()

		item = EdgeVersion.create(id=id, edge_id=edge_id, 
					from_node_version_start_id=from_node_version_start_id,
					to_node_version_start_id=to_node_version_start_id,
					to_node_version_end_id=0,
					from_node_version_end_id=0,
					)
		if to_node_version_end_id > 0:
			item.to_node_version_end_id = to_node_version_end_id
		if from_node_version_end_id > 0:
			item.from_node_version_end_id = from_node_version_end_id
		item.save() #check on this syntax

		if parent_ids:
			for parent in parent_ids:
				v_id = self._gen_id()
				test = VersionSuccessor.create(id=v_id, from_version_id=parent, to_version_id=to_id)
				VersionHistoryDag.create(id=self.edge_dag, version_successor_id=v_id)


	def get_edge(self, s_key):
		return Edge.get(Edge.source_key == s_key) #correct because source_key is unique

	def get_edge_latest_versions(self, source_key):
		current = []
		identity = (Edge.get(Edge.source_key == source_key)).id
		query = EdgeVersion.select().where(EdgeVersion.node_id == identity)
		if not query.exists():
			return current
		for g in query:
			current.append(g)

		return self._get_latest_versions()


	def get_edge_history(self, source_key):
		pairs = []
		identity = (Edge.get(Edge.source_key == source_key)).id
		query = VersionSuccessor.select().where((VersionSuccessor.from_version_id == identity) | 
			(VersionSuccessor.to_version_id == identity))
		for v in query:
			pairs.append(v.id)
		return pairs


	def get_edge_version(self, id):
		return EdgeVersion.get(EdgeVersion.id == id)

	### Graph Methods ###
	def create_graph(self, source_key, name="null", tags=None):
		Graph.create(item_id=self._gen_item(), source_key=source_key, name=name)

	def create_graph_version(self, graph_id, edge_version_ids, reference=None,
							reference_parameters=None, tags=None,
							structure_version_id=-1, parent_ids=None):
		to_id = self._gen_rich_version()
		GraphVersion.create(id=id, graph_id=graph_id)

		if parent_ids:
			for parent in parent_ids:
				v_id = self._gen_id()
				test = VersionSuccessor.create(id=v_id, from_version_id=parent, to_version_id=to_id)
				VersionHistoryDag.create(id=self.graph_dag, version_successor_id=v_id)

	def get_graph(self, source_key):
		return Graph.get(Graph.source_key==source_key)

	def get_graph_latest_versions(self, source_key):
		current = []
		identity = (Graph.get(Graph.source_key == source_key)).id
		query = GraphVersion.select().where(GraphVersion.node_id == identity)
		if not query.exists():
			return current
		for g in query:
			current.append(g)

		return self._get_latest_versions(current)

	def get_graph_history(self, source_key):
		pairs = []
		identity = (Graph.get(Graph.source_key == source_key)).id
		query = VersionSuccessor.select().where((VersionSuccessor.from_version_id == identity) | 
			(VersionSuccessor.to_version_id == identity))
		for v in query:
			pairs.append(v.id)
		return pairs

	def get_graph_version(self, id):
		return GraphVersion.get(GraphVersion.id == id)

	### Node Methods ###
	def create_node(self, source_key, name='null', tags=None):
		Node.create(item_id=self._gen_item(), source_key=source_key, name=name)

	def create_node_version(self, node_id,
	                            reference=None,
	                            reference_parameters=None,
	                            tags=None,
	                            structure_version_id=-1,
	                            parent_ids=None):
		to_id = self._gen_rich_version()
		NodeVersion.create(id=to_id, node_id=node_id) 

		if parent_ids:
			for parent in parent_ids:
				v_id = self._gen_id()
				test = VersionSuccessor.create(id=v_id, from_version_id=parent, to_version_id=to_id)
				VersionHistoryDag.create(id=self.node_dag, version_successor_id=v_id)

	def get_node(self, source_key):
		return Node.get(Node.source_key == source_key)

	def get_node_latest_versions(self, source_key):
		current = []
		identity = (Node.get(Node.source_key == source_key)).id
		query = NodeVersion.select().where(NodeVersion.node_id == identity)
		if not query.exists():
			return current
		for node in query:
			current.append(node.id)

		return self._get_latest_versions(current)

	def get_node_history(self, source_key):
		pairs = []
		identity = (Node.get(Node.source_key == source_key)).id
		query = VersionSuccessor.select().where((VersionSuccessor.from_version_id == identity) | 
			(VersionSuccessor.to_version_id == identity))
		for v in query:
			pairs.append(v.id)
		return pairs

	def get_node_version(self, id):
		return NodeVersion.get(NodeVersion.id == id)

	def get_node_version_adjacent_lineage(self, id):
		pass

	### Structure Methods ###
	def create_structure(self, source_key, name="null", tags=None): #pls double check on this
		Structure.create(item_id=self._gen_item(), source_key=source_key, name=name)

	def create_structure_version(self, structure_id, attributes, parent_id=None):
		to_id = self._gen_version()
		StructureVersion.create(id = to_id, structure_id = structure_id)

		if parent_id:
			v_id = self._gen_id()
			test = VersionSuccessor.create(id=v_id, from_version_id=parent_id, to_version_id=to_id)
			VersionHistoryDag.create(id=self.struct_dag, version_successor_id=v_id)

	def get_structure(self, source_key):
		return Structure.get(Structure.source_key==source_key)

	def get_structure_latest_versions(self, source_key):
		latest_versions = []
		identity = (Structure.get(Structure.source_key == source_key)).id
		for g in StructureVersion.select().where(StructureVersion.node_id == identity).order_by(
			StructureVersion.id.desc()):
			latest_versions.append(g)
		return latest_versions

	def get_structure_history(self, source_key):
		pairs = []
		identity = (Structure.get(Structure.source_key == source_key)).id
		query = VersionSuccessor.select().where((VersionSuccessor.from_version_id == identity) | 
			(VersionSuccessor.to_version_id == identity))
		for v in query:
			pairs.append(v.id)
		return pairs

	def get_structure_version(self, id):
		return StructureVersion.get(StructureVersion.id == id)

	### Lineage Edge Methods ###
	def create_lineage_edge(self, source_key, name="null", tags=None):
		LineageEdge.create(item_id=self._gen_item(), source_key=source_key, name=name)

	def create_lineage_edge_version(self, edge_id,
	                                    to_rich_version_id,
	                                    from_rich_version_id,
	                                    reference=None,
	                                    reference_parameters=None,
	                                    tags=None,
	                                    structure_version_id=-1,
	                                    parent_ids=None):
		to_id = self._gen_rich_version()
		LineageEdgeVersion.create(id = id, lineage_edge_id = edge_id, 
			from_rich_version_id = from_rich_version_id,
			to_rich_version_id=to_rich_version_id)

		if parent_ids:
			v_id = self._gen_id()
			test = VersionSuccessor.create(id=v_id, from_version_id=parent_ids, to_version_id=to_id)
			VersionHistoryDag.create(id=self.lin_edge_dag, version_successor_id=v_id)

	def get_lineage_edge(self, source_key):
		return LineageEdge.get(LineageEdge.source_key==source_key)

	def get_lineage_edge_latest_versions(self, source_key):
		current = []
		identity = (LineageEdge.get(LineageEdge.source_key == source_key)).id
		query = LineageEdgeVersion.select().where(LineageEdgeVersion.node_id == identity)
		if not query.exists():
			return current
		for g in query:
			current.append(g)
		return self._get_latest_versions()

	def get_lineage_edge_history(self, source_key):
		pairs = []
		identity = (LineageEdge.get(LineageEdge.source_key == source_key)).id
		query = VersionSuccessor.select().where((VersionSuccessor.from_version_id == identity) | 
			(VersionSuccessor.to_version_id == identity))
		for v in query:
			pairs.append(v.id)
		return pairs

	def get_lineage_edge_Version(self, id):
		return LineageEdgeVersion.get(LineageEdgeVersion.id == id)

	### Lineage Graph Methods ###
	def create_lineage_graph(self, source_key, name="null", tags=None):
		LineageGraph.create(item_id=self._gen_item(), source_key=source_key, name=name)

	def create_lineage_graph_version(self, lineage_graph_id,
	                                     lineage_edge_version_ids,
	                                     reference=None,
	                                     reference_parameters=None,
	                                     tags=None,
	                                     structure_version_id=-1,
	                                     parent_ids=None):
		to_id = self._gen_rich_version()
		LineageGraphVersion.create(id = id, lineage_graph_id = lineage_graph_id)

		if parent_ids:
			v_id = self._gen_id()
			test = VersionSuccessor.create(id=v_id, from_version_id=parent_ids, to_version_id=to_id)
			VersionHistoryDag.create(id=self.lin_graph_dag, version_successor_id=v_id)

	def get_lineage_graph(self, source_key):
		return LineageGraph.get(LineageGraph.source_key==source_key)

	def get_lineage_graph_latest_versions(self, source_key):
		current = []
		identity = (LineageGraph.get(LineageGraph.source_key == source_key)).id
		query = LineageGraphVersion.select().where(LineageGraphVersion.node_id == identity)
		if not query.exists():
			return current
		for g in query:
			current.append(g)
		return self._get_latest_versions()

	def get_lineage_graph_history(self, source_key):
		pairs = []
		identity = (LineageGraph.get(LineageGraph.source_key == source_key)).id
		query = VersionSuccessor.select().where((VersionSuccessor.from_version_id == identity) | 
			(VersionSuccessor.to_version_id == identity))
		for v in query:
			pairs.append(v.id)
		return pairs

	def get_lineage_graph_version(self, id):
		return LineageGraphVersion.get(LineageGraphVersion.id == id)