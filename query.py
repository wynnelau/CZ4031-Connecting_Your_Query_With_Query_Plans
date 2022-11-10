from utils.plan import get_qep_nodes, get_query_plan

if __name__ == '__main__':

    disable = tuple(["hashjoin"])
    list_scan, list_join = get_qep_nodes(19, disable)



    for node in list_scan:
        print(node.__repr__())
        print(node.node_type, node.relation_name)

    print()
    print()
    for node in list_join:
        print(node)
        # print(node.node_type)
        if node.node_type == "HASH JOIN":
            print(node.node_type, node.hash_condition)
        elif node.node_type == "MERGE JOIN":
            print(node.node_type, node.merge_condition)
        elif node.node_type == "NESTED LOOP":
                print(node.node_type, node.join_filter)
        else: print(node.node_type)

    splitted_query = get_query_plan(19, disable, True)
    print()
    for each_row in splitted_query:
        if ("WHERE" in each_row) or ("AND" in each_row) or ("OR" in each_row):
            each_word = each_row.split(" ")
            if ("WHERE" in each_word):
                del each_word[0:1]
            elif ("AND" in each_word) or ("OR" in each_row):
                del each_word[0:3]

            for node in list_join:
                # print(node)
                # print(node.node_type)
                
                for z in each_word:
                    if z in str(node.hash_condition) and "HASH JOIN" in node.node_type:
                        hash_join = True
                    else: 
                        hash_join = False
                    # print(hash_join, z, node.hash_condition)
                    if z in str(node.merge_condition) and "MERGE JOIN" in node.node_type:
                        merge_join = True
                    else: 
                        merge_join = False
                    # print(merge_join, z, node.merge_condition)
                    if z in str(node.join_filter) and "NESTED LOOP" in node.node_type:
                        nested_loop = True
                    else: 
                        nested_loop = False
                    # print(nested_loop, z, node.join_filter)
                if hash_join == True:
                    print(each_row, "       ", "HASH JOIN")
                elif merge_join == True:
                    print(each_row, "       ", "MERGE JOIN")
                elif nested_loop == True:
                    print(each_row, "       ", "NESTED LOOP")
                else:
                    print(each_row)
            

            # print(splitted_query.index(x))
            
    
            
