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
		db.create_tables([Edge, EdgeVersion])

		# if not os.path.exists(self.path + 'next_id.txt'):
		# 	with open(self.path + 'next_id.txt', 'w') as f:
		# 		f.write('0')
		if not os.path.exists('next_id.txt'):
			with open('next_id.txt', 'w') as f:
				f.write('0')
        # if not os.path.exists(self.path + 'index/' + 'index.json'):
        #     with open(self.path + 'index/' + 'index.json', 'w') as f:
        #         json.dump({}, f)
        # if not os.path.exists(self.path + 'index/index_version.json'):
        #     with open(self.path + 'index/index_version.json', 'w') as f:
        #         json.dump({}, f)

	def _gen_id(self):
		#borrowed from Grit
		with open('next_id.txt', 'r') as f:
			newid = int(f.read())
		nxtid = str(newid + 1)
		with open('next_id.txt', 'w') as f:
			f.write(nxtid)
		return int(newid)

	### EDGES ###
	def create_edge(self,_source_key, _name, _from_node_id, _to_node_id, tags=None):
		Edge.create(item_id=self._gen_id(), source_key=_source_key, from_node_id=_from_node_id, 
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
		item = EdgeVersion.create(id=self._gen_id(), edge_id=edge_id, 
					from_node_version_start_id=from_node_version_start_id,
					to_node_version_start_id=to_node_version_start_id,
					to_node_version_end_id=0,
					from_node_version_end_id=0,
					reference=reference,
					reference_parameters=reference_parameters,
					tags=tags,
					structure_version_id=structure_version_id,
					parent_ids=parent_ids
					)
		if to_node_version_end_id > 0:
			item.to_node_version_end_id = to_node_version_end_id
		if from_node_version_end_id > 0:
			item.from_node_version_end_id = from_node_version_end_id
		item.save() #check on this syntax

	def get_edge(self, s_key):
		item = Edge.select(Edge.source_key == s_key) #correct because source_key is unique
		return item #check whether this needs to return a different object

	def get_edge_latest_versions(self, source_key):
		'''This is a naive implementation'''
		#need to find a better way of checking this out...
		# item = None
		# for each in Edge.select(source_key == source_key)


		# return item
		pass

	def get_edge_history(self, source_key):
		pass

	def get_edge_version(self, id):
		item = EdgeVersion.select(id=id) #this is problematic because you got rid of id...
		return id

	### Graph Methods ###
	def create_graph(self, source_key, name, tags=None):
		Graph.create(source_key=source_key, name=name)

	def create_graph_version(self, graph_id, edge_version_ids, reference=None,
							reference_parameters=None, tags=None,
							structure_version_id=-1, parent_ids=None):
		pass

	def get_graph(self, source_key):
		item = Graph.select(Graph.source_key==source_key)

	def get_graph_latest_versions(self, source_key):
		pass

	def get_graph_history(self, source_key):
		pass

	def get_graph_version(self, id):
		pass

	### Node Methods ###
	def create_node(self, source_key, name, tags=None):
		Node.create(source_key=source_key, name=name)

	def create_node_version(self, node_id,
	                            reference=None,
	                            reference_parameters=None,
	                            tags=None,
	                            structure_version_id=-1,
	                            parent_ids=None):
		NodeVersion.create(node_id=node_id) #check on this because of all the additional information

	def get_node(self, source_key):
		item = Node.select(Node.source_key == source_key)
		return item #check on this pls

	def get_node_latest_versions(self, source_key):
		pass

	def get_node_history(self, source_key):
		pass

	def get_node_version(self, id):
		pass

	def get_node_version_adjacent_lineage(self, id):
		pass

	### Structure Methods ###
	def create_structure(self, source_key, name, tags=None): #pls double check on this
		Structure.create(source_key=source_key, name=name)

	def create_structure_version(self, structure_id, attributes, parent_id=None):
		StructureVersion.create(structure_id=structure_id)

	def get_structure(self, source_key):
		pass

	def get_structure_latest_versions(self, source_key):
		pass

	def get_structure_history(self, source_key):
		pass

	def get_structure_version(self, id):
		pass

	### Lineage Edge Methods ###
	def create_lineage_edge(self, source_key, name, tags=None):
		pass

	def create_lineage_edge_version(self, edge_id,
	                                    to_rich_version_id,
	                                    from_rich_version_id,
	                                    reference=None,
	                                    reference_parameters=None,
	                                    tags=None,
	                                    structure_version_id=-1,
	                                    parent_ids=None):
		pass

	def get_lineage_edge(self, source_key):
		pass

	def get_lineage_edge_latest_versions(self, source_key):
		pass

	def get_lineage_edge_latest_versions(self, source_key):
		pass

	def get_lineage_edge_Version(self, id):
		pass

	### Lineage Graph Methods ###
	def create_lineage_graph(self, source_key, name, tags=None):
		pass

	def create_lineage_graph_version(self, lineage_graph_id,
	                                     lineage_edge_version_ids,
	                                     reference=None,
	                                     reference_parameters=None,
	                                     tags=None,
	                                     structure_version_id=-1,
	                                     parent_ids=None):
		pass

	def get_lineage_graph(self, source_key):
		pass

	def get_lineage_graph_latest_versions(self, source_key):
		pass

	def get_lineage_graph_history(self, source_key):
		pass

	def get_lineage_graph_version(self, id):
		pass