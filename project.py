from tkinter import *
from tkinter import font, ttk, messagebox
import annotation
from PIL import ImageTk, Image
import interface
import psycopg2
from utils.config import config

formatted_query = ["",""]
annotation_list = ["",""]


def retrieveInput():
    inputValue = query_text.get('1.0', 'end-1c')
    return inputValue


def multiple_yview(*args):
    mycanvas.yview(*args)
    mycanvas2.yview(*args)


def get_json(input_query):
    print("REACHED GET_JSON")
    global formatted_query
    global annotation_list
    formatted_query, annotation_list = annotation.get_annotations(input_query)
    print(formatted_query)
    interface.format_query(myframe,formatted_query)
    print("REACHED GET_JSON")
    print(annotation_list)
    interface.annotate(myframe2,annotation_list)
    mycanvas.pack(side=LEFT, fill=BOTH, expand=1)
    mycanvas.bind('<Configure>', lambda e: mycanvas.configure(scrollregion=mycanvas.bbox('all')))
    mycanvas2.pack(side=LEFT, fill=BOTH, expand=1)
    mycanvas2.bind('<Configure>', lambda e: mycanvas2.configure(scrollregion=mycanvas2.bbox('all')))
    mycanvas.configure(yscrollcommand=mscrollbar.set)
    mycanvas2.configure(yscrollcommand=mscrollbar2.set)

    # frame2 = Frame(root, highlightbackground="black", highlightthickness=3, height=1500)
    # frame2.grid(row=6, column=0, columnspan=2, sticky='new', padx=5)

    # mycanvas = Canvas(frame2)
    # mycanvas.pack(side=LEFT, fill=BOTH, expand=1)
    # mycanvas.bind('<Configure>', lambda e: mycanvas.configure(scrollregion=mycanvas.bbox('all')))
    # myframe = Frame(mycanvas)
    # mycanvas.create_window((0, 0), window=myframe, anchor="nw")
    # interface.format_query(myframe,formatted_query)
    # frame3 = Frame(root, highlightbackground="black", highlightthickness=3, height=1500)
    # frame3.grid(row=6, column=2, columnspan=2, sticky="new", padx=5)
   

    # mycanvas2 = Canvas(frame3)
    # mycanvas2.pack(side=LEFT, fill=BOTH, expand=1)
    # mycanvas2.bind('<Configure>', lambda e: mycanvas2.configure(scrollregion=mycanvas2.bbox('all')))
    # myframe2 = Frame(mycanvas2)
    # mycanvas2.create_window((0, 0), window=myframe2, anchor="nw")
    # interface.annotate(myframe2,annotation_list)

    # mscrollbar = ttk.Scrollbar(frame2, orient="vertical", command=multiple_yview)
    # mscrollbar.pack(side=RIGHT, fill=Y)
    # mycanvas.configure(yscrollcommand=mscrollbar.set)




if __name__ == '__main__':
    # global annotations
    # global formatted_query

    root = Tk()
    root.title('Query Panel Annotator')
    root.iconphoto(False, PhotoImage(file='utils/bob.png'))
    root.geometry('1500x600')

    database = Menu(root)
    root.config(menu=database)

    schemamenu = Menu(database, tearoff=5)
    schemamenu.add_command(label="Exit", command=root.quit)
    params = config()
    conn = psycopg2.connect(**params)

    cur = conn.cursor()
    schema_list = interface.get_schemas(cur)

    for i in range(len(schema_list)):
        print(schema_list[i])
        schemamenu.add_command(label=schema_list[i], command=lambda i=i: interface.get_schema(schema_list[i]))

    database.add_cascade(label="Select Schema", menu=schemamenu)

    style = ttk.Style()
    style.theme_use('clam')
    style.configure("Vertical.TScrollbar", background="green", bordercolor="purple", arrowcolor="black")

    frame1 = LabelFrame(root, highlightbackground="black", highlightthickness=3)
    frame1.grid(row=1, rowspan=3, column = 0, columnspan=3)

    query_label = Label(root, text="ENTER QUERY HERE")
    query_label.grid(row=0, column=0, columnspan=3)

    query_text = Text(frame1, height=15, width=90)
    query_text.grid(row=0, column=1)

    query_scrollbar = ttk.Scrollbar(frame1, orient='vertical', command=query_text.yview)
    query_text.configure(yscrollcommand=query_scrollbar.set)
    query_scrollbar.grid(row=0, rowspan=3, column=0, sticky='ns')


    frame4 = Frame(root)
    frame4.grid(row=1, rowspan=2, column=3, columnspan=3)

    img = ImageTk.PhotoImage(Image.open("utils/sponge.png").resize((600, 200)))
    my_img = Label(frame4, image=img)
    my_img.grid(row=0, columnspan=2, padx=40)

    img2 = ImageTk.PhotoImage(Image.open("utils/bob.png").resize((100, 100)))
    my_img2 = Label(root, image=img2)
    my_img2.grid(row=1, column = 6, columnspan=3, padx=40)


    frame2 = Frame(root, highlightbackground="black", highlightthickness=3, height=1500)
    frame2.grid(row=6, column=0, columnspan=3, sticky='new', padx=5)
    mycanvas = Canvas(frame2)
    #mycanvas.pack(side=LEFT, fill=BOTH, expand=1)
    #mycanvas.bind('<Configure>', lambda e: mycanvas.configure(scrollregion=mycanvas.bbox('all')))
    myframe = Frame(mycanvas)
    mycanvas.create_window((0, 0), window=myframe, anchor="nw")
    #interface.format_query(myframe,formatted_query)
    
    frame3 = Frame(root, highlightbackground="black", highlightthickness=3, height=1500)
    frame3.grid(row=6,column=3, columnspan=3, sticky="new", padx=5)
    mycanvas2 = Canvas(frame3)
    #mycanvas2.pack(side=LEFT, fill=BOTH, expand=1)
    #mycanvas2.bind('<Configure>', lambda e: mycanvas2.configure(scrollregion=mycanvas2.bbox('all')))
    myframe2 = Frame(mycanvas2)
    mycanvas2.create_window((0, 0), window=myframe2, anchor="nw")
    #interface.annotate(myframe2,annotation_list)

    mscrollbar = ttk.Scrollbar(frame2, orient="vertical", command=multiple_yview)
    mscrollbar.pack(side=RIGHT, fill=Y)
    mycanvas.configure(yscrollcommand=mscrollbar.set)
    mscrollbar2 = ttk.Scrollbar(frame3, orient="vertical", command=multiple_yview)
    mscrollbar2.pack(side=LEFT, fill=Y)
    mycanvas2.configure(yscrollcommand=mscrollbar2.set)

    query_formatted = Label(root, text="FORMATTED QUERY")
    query_formatted.grid(row=5, column=0, columnspan=3)

    annotated = Label(root, text="ANNOTATIONS")
    annotated.grid(row=5, column=3, columnspan=3)

    # final = Label(root, text="-------------------------------")
    # final.grid(row=10, column=0, columnspan=6)

    execute = Button(root, text="EXECUTE", command=lambda: get_json(retrieveInput()))
    execute.grid(row=4, column=1)

    root.mainloop()
