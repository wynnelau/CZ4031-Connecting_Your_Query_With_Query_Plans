import psycopg2
import json
from config import config
import queries


def getQueryPlan(query_number, disable_parameters=(), ):
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
        query = "EXPLAIN (ANALYZE, FORMAT JSON) " + query
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


if __name__ == '__main__':
    x = getQueryPlan(19)
    print(x)
    disable1 = ("hashjoin", "mergejoin", "indexscan", "bitmapscan")
    y = getQueryPlan(19, disable1)
    print(y)

