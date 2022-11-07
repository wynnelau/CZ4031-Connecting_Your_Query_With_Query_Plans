from utils.plan import get_qep_nodes

if __name__ == '__main__':

    disable = ("hashjoin", "mergejoin", "indexscan", "bitmapscan")
    list_scan, list_operations = get_qep_nodes(5, disable)
    for node in list_scan:
        print(node.node_type)

    print()
    print()
    for node in list_operations:
        print(node.node_type)
