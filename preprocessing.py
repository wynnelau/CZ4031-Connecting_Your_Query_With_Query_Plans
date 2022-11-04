def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# PREPROCESSING .TBL FILES TO CSV
def tbl_to_csv(filename):
    csv = open("".join([filename, ".csv"]), "w+")

    tbl = open("".join([filename, ".tbl"]), "r")

    lines = tbl.readlines()
    for line in lines:
        length = len(line)
        line = line[: length - 2] + line[length - 1:]
        csv.write(line)
    tbl.close()
    csv.close()

def extract_csv():
    filenames = [
        "customer",
        "lineitem",
        "nation",
        "orders",
        "part",
        "partsupp",
        "region",
        "supplier",
    ]

    for filename in filenames:
        tbl_to_csv(filename)


if __name__ == '__main__':
    extract_csv()
