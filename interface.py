from tkinter import *
from tkinter import font, messagebox, ttk
import psycopg2
import json
import annotation
from utils.config import config

import project

# style=ttk.Style()
# style.theme_use('clam')
# style.configure("Vertical.TScrollbar", background="green", bordercolor="purple", arrowcolor="black")


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
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    schema_path = "SET search_path TO '" + schema_name + "';"
    cur.execute(schema_path)


def format_query(Frame,query):

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
            
        
        
def annotate(Frame,annotation):

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