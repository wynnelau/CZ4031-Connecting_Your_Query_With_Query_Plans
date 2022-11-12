from tkinter import *
from tkinter import font, messagebox, ttk
import psycopg2
import json
import project

# style=ttk.Style()
# style.theme_use('clam')
# style.configure("Vertical.TScrollbar", background="green", bordercolor="purple", arrowcolor="black")


def get_json(inputValue):
        
        conn = None
        x = None 
        try:
            #connect to postgres 
            conn = psycopg2.connect(
                host="localhost",
                database="postgres",
                user="postgres",
                password="password")
            
            cur = conn.cursor()
            cur.execute("EXPLAIN (ANALYZE, VERBOSE, FORMAT JSON)" + inputValue)
            rows = cur.fetchall()
            x = json.dumps(rows)

            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            messagebox.showerror("Error",error)
         
        finally:
            if conn is not None:
                conn.close()
        print("success")
        return x


def connect():
        conn = None
        try:
            params = conn

            conn = psycopg2.connect(**params)

            cur = conn.cursor()
            cur.execute('SELECT version()')

            db_version = cur.fetchone()

            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
        cur = conn.cursor()

def get_schemas(cur):
  schema_list = []
  cur.execute('SELECT schema_name FROM information_schema.schemata;')
  schemas = cur.fetchall()
  for schema in schemas:
    schema_list.append(schema[0])
  
  return schema_list

def get_schema(schema_name):
    schema_prompt = "You have selected the database: " + schema_name + "."
    messagebox.showinfo(title="Schema selected", message=schema_prompt)

    conn = psycopg2.connect(
                host="localhost",
                database="postgres",
                user="postgres",
                password="password")
            
    cur = conn.cursor()

    schema_path = "SET search_path TO '" + schema_name + "';"
    cur.execute(schema_path)





def format_query(Frame):
    query = ["SELECT l_returnflag,", 
            "       l_linestatus,",
            "       sum(l_quantity) AS sum_qty,",
            "       sum(l_extendedprice) AS sum_base_price,",
            "       sum(l_extendedprice * (1 - l_discount)) AS sum_disc_price,",
            "       sum(l_extendedprice * (1 - l_discount) * (1 + l_tax)) AS sum_charge,",
            "       avg(l_quantity) AS avg_qty,",
            "       avg(l_extendedprice) AS avg_price,",
            "       avg(l_discount) AS avg_disc,",
            "       count(*) AS count_order",
            "FROM lineitem",
            "WHERE l_shipdate <= date '1998-12-01' - interval '90' DAY",
            "GROUP BY l_returnflag,",
            "         l_linestatus",
            "ORDER BY l_returnflag,",
            "         l_linestatus;",
            ]


    for i in range(len(query)):
        colour = [ "Grey", "Pink"]
        x = i%2
        text_font = font.Font(family='Fira Code Retina', size=15)
        text = Text(Frame,height=1, font=text_font, wrap=WORD, highlightbackground= colour[x], highlightthickness = 2)
        text.grid(row=i, column=1)
        text.insert(INSERT, query[i])
        scrollbar = ttk.Scrollbar(Frame, orient='vertical', command=text.yview)
        scrollbar.grid(row=i, column=0, sticky='ns')
        text.configure(yscrollcommand=scrollbar.set)
        text.config(state=DISABLED)
            
        
        
def annotate(Frame):
    annotation = [" ",
                    " ",
                    " ",
                    " ",
                    " ",
                    " ",
                    " ",
                    " ",
                    " ",
                    " ",
                    " ",
                    "This table is read using sequential scan. This is because no index is created on the table. ",
                    " ",
                    " ",
                    " ",
                    " "]

    for i in range(len(annotation)):
        colour = [ "Grey", "Pink"]
        x = i%2
        text_font = font.Font(family='Fira Code Retina', size=15)
        text = Text(Frame,height=1, font=text_font, wrap=WORD, highlightbackground= colour[x], highlightthickness = 2)
        text.grid(row=i, column=1, columnspan = 3)
        text.insert(INSERT, annotation[i])
        scrollbar = ttk.Scrollbar(Frame, orient='vertical', command=text.yview)
        scrollbar.grid(row=i, column=0, sticky='ns')
        text.configure(yscrollcommand=scrollbar.set)
        text.config(state=DISABLED)