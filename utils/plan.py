import queue
import psycopg2
import json
from utils.config import config
import utils.queries as queries


nodeListOperations = []
nodeListScans = {}
rawNodeList = []
nodeListJoins = []
depth = 0


class Node(object):
    def __repr__(self):
        return f"Node({self.node_type}, {self.relation_name}, {self.schema}, {self.alias}, {self.group_key}, {self.sort_key}, {self.join_type}" \
               f", {self.index_name},{self.hash_condition}, {self.table_filter}, {self.index_condition}, {self.merge_condition}" \
               f", {self.recheck_condition}, {self.join_filter},{self.subplan_name}, {self.actual_rows}, {self.actual_time}" \
               f", {self.description},{self.cost},{self.sort_type})"

    def __init__(self, node_type, relation_name, schema, alias, group_key, sort_key, join_type, index_name,
                 hash_condition, table_filter, index_condition, merge_condition, recheck_condition, join_filter,
                 subplan_name, actual_rows, actual_time, description,cost,sort_type):
        self.node_type = node_type.upper()
        self.relation_name = relation_name
        self.schema = schema
        self.alias = alias
        self.group_key = group_key
        self.sort_key = sort_key
        self.join_type = join_type
        self.index_name = index_name
        self.hash_condition = hash_condition
        self.table_filter = table_filter
        self.index_condition = index_condition
        self.merge_condition = merge_condition
        self.recheck_condition = recheck_condition
        self.join_filter = join_filter
        self.subplan_name = subplan_name
        self.actual_rows = actual_rows
        self.actual_time = actual_time
        self.description = description
        self.cost = cost
        self.sort_type =sort_type
        self.children = []





def get_query_plan(query_number, disable_parameters=(), ):
    output_json = {}
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()
        query = queries.getQuery(query_number)
        query = "EXPLAIN (ANALYSE, VERBOSE, FORMAT JSON) " + query
        if query is None:
            print("Please select a valid query number!")
            return

        for param in disable_parameters:
            query = "SET LOCAL enable_" + str(param) + "= off;" + query
        print(query)
        cur.execute(query)
        rows = cur.fetchall()
        output_json = json.dumps(rows)
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

    return output_json


def get_qep_tree(qep_json):
    q_child_plans = queue.Queue()
    q_parent_plans = queue.Queue()
    plan = qep_json[0][0][0]['Plan']

    q_child_plans.put(plan)
    q_parent_plans.put(None)

    while not q_child_plans.empty():
        current_plan = q_child_plans.get()
        parent_node = q_parent_plans.get()

        relation_name = schema = alias = group_key = sort_key = join_type = index_name = hash_condition = table_filter \
            = index_condition = merge_condition = recheck_condition = join_filter = subplan_name = actual_rows = actual_time = description = cost = sort_type=None
        if 'Relation Name' in current_plan:
            relation_name = current_plan['Relation Name']
        if 'Schema' in current_plan:
            schema = current_plan['Schema']
        if 'Alias' in current_plan:
            alias = current_plan['Alias']
        if 'Group Key' in current_plan:
            group_key = current_plan['Group Key']
        if 'Sort Key' in current_plan:
            sort_key = current_plan['Sort Key']
        if 'Join Type' in current_plan:
            join_type = current_plan['Join Type']
        if 'Index Name' in current_plan:
            index_name = current_plan['Index Name']
        if 'Hash Cond' in current_plan:
            hash_condition = current_plan['Hash Cond']
        if 'Filter' in current_plan:
            table_filter = current_plan['Filter']
        if 'Index Cond' in current_plan:
            index_condition = current_plan['Index Cond']
        if 'Merge Cond' in current_plan:
            merge_condition = current_plan['Merge Cond']
        if 'Recheck Cond' in current_plan:
            recheck_condition = current_plan['Recheck Cond']
        if 'Join Filter' in current_plan:
            join_filter = current_plan['Join Filter']
        if 'Actual Rows' in current_plan:
            actual_rows = current_plan['Actual Rows']
        if 'Actual Total Time' in current_plan:
            actual_time = current_plan['Actual Total Time']
        if 'Subplan Name' in current_plan:
            if "returns" in current_plan['Subplan Name']:
                name = current_plan['Subplan Name']
                subplan_name = name[name.index("$"):-1]
            else:
                subplan_name = current_plan['Subplan Name']
        if 'Total Cost' in current_plan:
            cost = current_plan['Total Cost']
        if 'Sort Space Type' in current_plan:
            sort_type = current_plan['Sort Space Type']

        current_node = Node(current_plan['Node Type'], relation_name, schema, alias, group_key, sort_key, join_type,
                            index_name, hash_condition, table_filter, index_condition, merge_condition,
                            recheck_condition, join_filter,
                            subplan_name, actual_rows, actual_time, description,cost,sort_type)

        if parent_node is not None:
            parent_node.children.append(current_node)
        else:
            root_node = current_node

        if 'Plans' in current_plan:
            for item in current_plan['Plans']:
                # push child plans into queue
                q_child_plans.put(item)
                # push parent for each child into queue
                q_parent_plans.put(current_node)

    return root_node


def traverse_tree(node,depth):
    global nodeListOperations
    global nodeListJoins
    global nodeListScans
    global rawNodeList

    for child in node.children:
        traverse_tree(child,depth+1)

    if "SCAN" in str(node.node_type):
        nodeListScans.update({node: depth})

    elif "LOOP" in str(node.node_type) \
            or "JOIN" in str(node.node_type) \
            or str(node.node_type) == "HASH" \
            or (str(node.node_type) == "SORT" and str(node.sort_type) == "Disk"):
        nodeListJoins.append(node)
    else:
        nodeListOperations.append(node)

    rawNodeList.append(node)


def get_qep_nodes_with_depth(query_number, disable=()):
    global nodeListOperations
    global nodeListScans
    global rawNodeList
    global nodeListJoins
    qep_json = json.loads(get_query_plan(query_number,disable))
    nodeListOperations.clear()
    nodeListScans.clear()
    root_node = get_qep_tree(qep_json)
    traverse_tree(root_node,0)


def get_qep_nodes(query_number,disable=()):
    global nodeListOperations
    global nodeListScans
    global rawNodeList
    global nodeListJoins
    nodeListOperations = []
    nodeListScans = {}
    rawNodeList = []
    nodeListJoins = []
    get_qep_nodes_with_depth(query_number,disable)
    sorted_scan = dict(sorted(nodeListScans.items(), key=lambda item: item[1],reverse=True))
    return sorted_scan.keys(), nodeListJoins
