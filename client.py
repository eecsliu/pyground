from model.setup import *
### EDGES ###
def create_edge(source_key, name, from_node_id, to_node_id, tags=None):
	Edge.create(source_key=source_key, from_node_id=from_node_id, 
		to_node_id=to_node_id, name=name)
	#ignoring tags for now

def create_edge_version(edge_id,
                            from_node_version_start_id,
                            to_node_version_start_id,
                            from_node_version_end_id=-1,
                            to_node_version_end_id=-1,
                            reference=None,
                            reference_parameters=None,
                            tags=None,
                            structure_version_id=-1,
                            parent_ids=None):
	item = Edge.create(edge_id=edge_id, 
				from_node_version_start_id=from_node_version_start_id,
				to_node_version_start_id=to_node_version_start_id,
				to_node_version_end_id=0,
				from_node_version_end_id=0)
	if to_node_version_end_id > 0:
		item.to_node_version_end_id = to_node_version_end_id
	if from_node_version_end_id > 0:
		item.from_node_version_end_id = from_node_version_end_id
	item.save() #check on this syntax

def get_edge(s_key):
	item = Edge.select(source_key == s_key)
	return item

def get_edge_latest_versions(source_key):
	'''This is a naive implementation'''
	# item = None
	# for each in Edge.select(source_key == source_key)


	# return item
	pass

def get_edge_history(source_key):
	pass

def get_edge_version(id):
	pass

### Graph Methods ###
def create_graph(source_key, name, tags=None):
	pass

def create_graph_version(graph_id, edge_version_ids, reference=None,
						reference_parameters=None, tags=None,
						structure_version_id=-1, parent_ids=None):
	pass

def get_graph(source_key):
	pass

def get_graph_latest_versions(source_key):
	pass

def get_graph_history(source_key):
	pass

def get_graph_version(id):
	pass

### Node Methods ###
def create_node(source_key, name, tags=None):
	pass

def create_node_version(node_id,
                            reference=None,
                            reference_parameters=None,
                            tags=None,
                            structure_version_id=-1,
                            parent_ids=None):
	pass

def get_node(source_key):
	pass

def get_node_latest_versions(source_key):
	pass

def get_node_history(source_key):
	pass

def get_node_version(id):
	pass

def get_node_version_adjacent_lineage(id):
	pass

### Structure Methods ###
def create_structure(source_key, name, tags=None):
	pass

def create_structure_version(structure_id, attributes, parent_id=None):
	pass

def get_structure(source_key):
	pass

def get_structure_latest_versions(source_key):
	pass

def get_structure_history(source_key):
	pass

def get_structure_version(id):
	pass

### Lineage Edge Methods ###
def create_lineage_edge(source_key, name, tags=None):
	pass

def create_lineage_edge_version(edge_id,
                                    to_rich_version_id,
                                    from_rich_version_id,
                                    reference=None,
                                    reference_parameters=None,
                                    tags=None,
                                    structure_version_id=-1,
                                    parent_ids=None):
	pass

def get_lineage_edge(source_key):
	pass

def get_lineage_edge_latest_versions(source_key):
	pass

def get_lineage_edge_latest_versions(source_key):
	pass

def get_lineage_edge_Version(id):
	pass

### Lineage Graph Methods ###
def create_lineage_graph(source_key, name, tags=None):
	pass

def create_lineage_graph_version(lineage_graph_id,
                                     lineage_edge_version_ids,
                                     reference=None,
                                     reference_parameters=None,
                                     tags=None,
                                     structure_version_id=-1,
                                     parent_ids=None):
	pass

def get_lineage_graph(source_key):
	pass

def get_lineage_graph_latest_versions(source_key):
	pass

def get_lineage_graph_history(source_key):
	pass

def get_lineage_graph_version(id):
	pass