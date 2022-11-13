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




if __name__ == '__main__':
    # global annotations
    # global formatted_query

    root = Tk()
    root.title('Query Panel Annotator')
    root.iconphoto(False, PhotoImage(file='utils/bob.png'))
    root.geometry('800x600')

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
    frame1.grid(row=1, rowspan=3, column = 0, columnspan=2)

    query_label = Label(root, text="ENTER QUERY HERE")
    query_label.grid(row=0, column=0, columnspan=2)

    query_text = Text(frame1, height=15, width=50)
    query_text.grid(row=0, column=1)

    query_scrollbar = ttk.Scrollbar(frame1, orient='vertical', command=query_text.yview)
    query_text.configure(yscrollcommand=query_scrollbar.set)
    query_scrollbar.grid(row=0, rowspan=3, column=0, sticky='ns')

    execute = Button(root, text="EXECUTE", command=lambda: get_json(retrieveInput()))
    execute.grid(row=4, column=1)

    frame4 = Frame(root)
    frame4.grid(row=1, rowspan=2, column=2, columnspan=2)

    img = ImageTk.PhotoImage(Image.open("utils/sponge.png").resize((300, 200)))
    my_img = Label(frame4, image=img)
    my_img.grid(row=0, columnspan=2, padx=40)

    img2 = ImageTk.PhotoImage(Image.open("utils/bob.png").resize((100, 100)))
    my_img2 = Label(root, image=img2)
    my_img2.grid(row=1, column = 6, columnspan=3, padx=40)

    # query_label2 = Label(root, text = "ENTER QUERY HERE")
    # query_label2.grid(row=0, column=3, columnspan =3 )

    # query_text2 = Text(frame4, height = 8, width=90)
    # query_text2.grid(row=0,  column=4)

    # query_scrollbar2 = ttk.Scrollbar(frame4, orient='vertical', command=query_text2.yview)
    # query_text2.configure(yscrollcommand=query_scrollbar2.set)
    # query_scrollbar2.grid(row=0, rowspan = 3, column=3, sticky='ns')

    frame2 = Frame(root, highlightbackground="black", highlightthickness=3, height=1500)
    frame2.grid(row=6, column=0, columnspan=2, sticky='new', padx=5)

    mycanvas = Canvas(frame2)
    mycanvas.pack(side=LEFT, fill=BOTH, expand=1)

    # yscrollbar = ttk.Scrollbar(frame2, orient="vertical", command=mycanvas.yview)
    # yscrollbar.pack(side=RIGHT, fill=Y)

    # mycanvas.configure(yscrollcommand=yscrollbar.set)
    mycanvas.bind('<Configure>', lambda e: mycanvas.configure(scrollregion=mycanvas.bbox('all')))

    myframe = Frame(mycanvas)
    mycanvas.create_window((0, 0), window=myframe, anchor="nw")
    interface.format_query(myframe,formatted_query)

    frame3 = Frame(root, highlightbackground="black", highlightthickness=3, height=1500)
    frame3.grid(row=6, column=2, columnspan=2, sticky="new", padx=5)
    # frame3.grid_propagate(True)

    mycanvas2 = Canvas(frame3)
    mycanvas2.pack(side=LEFT, fill=BOTH, expand=1)

    # yscrollbar2 = ttk.Scrollbar(frame3, orient="vertical", command=mycanvas2.yview)
    # yscrollbar2.pack(side=RIGHT, fill=Y)

    # mycanvas2.configure(yscrollcommand=yscrollbar2.set)
    mycanvas2.bind('<Configure>', lambda e: mycanvas2.configure(scrollregion=mycanvas2.bbox('all')))

    myframe2 = Frame(mycanvas2)
    mycanvas2.create_window((0, 0), window=myframe2, anchor="nw")
    interface.annotate(myframe2,annotation_list)

    mscrollbar = ttk.Scrollbar(frame2, orient="vertical", command=multiple_yview)
    mscrollbar.pack(side=RIGHT, fill=Y)
    mycanvas.configure(yscrollcommand=mscrollbar.set)

    # mycanvas = Canvas(frame2)
    # # mycanvas.grid(row = 6,rowspan = 3, column= 5)

    # yscrollbar = ttk.Scrollbar(root, orient="vertical", command=mycanvas.yview)
    # yscrollbar.grid(row=6, rowspan = 6, column= 3)

    # mycanvas.configure(yscrollcommand=yscrollbar.set)
    # mycanvas.bind('<Configure>', lambda e:mycanvas.configure(scrollregion = mycanvas.bbox('all')))

    # myframe = Frame(mycanvas)
    # mycanvas.create_window((0,0), window=myframe, anchor="nw")

    # query_scrollbar2 = Scrollbar(root, orient='vertical')
    # frame2.configure(yscrollcommand=query_scrollbar2.set)
    # query_scrollbar2.grid(row=6, rowspan = 3, column=3, sticky='ns', padx=(0, 12))

    query_formatted = Label(root, text="FORMATTED QUERY")
    query_formatted.grid(row=5, column=0, columnspan=2)

    annotated = Label(root, text="ANNOTATIONS")
    annotated.grid(row=5, column=2, columnspan=2)

    final = Label(root, text="-------------------------------")
    final.grid(row=8, column=0, columnspan=5)

    root.mainloop()
