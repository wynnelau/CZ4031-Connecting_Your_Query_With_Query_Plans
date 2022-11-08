from utils.plan import get_qep_nodes

if __name__ == '__main__':

    disable = tuple(["hashjoin"])
    list_scan, list_operations = get_qep_nodes()
    for node in list_scan:
        print(node.__repr__())
        # print(node.node_type)

    print()
    print()
    for node in list_operations:
        print(node)
