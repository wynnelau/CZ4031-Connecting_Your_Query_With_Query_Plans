## About

• Integrated an SQL query and its query plan-related information by efficiently retrieving relevant information from a QEP and AQPs using Python to explain how different components of the query are executed by the underlying query processor and why the operators are chosen among other alternatives.  
• Designed and implemented a user-friendly GUI to visualize the results obtained from the comparison between the QEP and AQPs.

SQLink, links a SQL query to its Query Execution Plan (QEP) and Alternate Query Plans (AQPs), and explains why a certain join/scan algorithm was used in the final query plan. 

SQLink was built as part of the coursework for CZ4031: Database Systems Principles and is built on Python and PostgreSQL, and is optimized for usage on Windows machines. 

In this project, the broad goal is to integrate by retrieving relevant information from a QEP and AQP to annotate the corresponding SQL query to explain how different components of the query are executed by the underlying query processor and why the operators are chosen among other alternatives. In SQLink, we implemented this idea by annotating at each line  why each operator was chosen. The achience this, it is important to retrieve representative AQPs associated with a SQL query. 

The TPC-H database was used for querying purposes.

This project was exectued with the help of 4 other team members: Vincent, Jerome, Wynne and Ruo Qing.
 
## Running the app


* Change the host, database, user and password in the database.ini file according to the
user's setup.
* Create the tables and import data for each table in PostgreSQL database (pgAdmin4): You can choose to use the TPC-H Database, the details in downloading the TPC-H data is given below.

* Step 1: Click the run button for project.py.
* Step 2: Input the query in the ‘ENTER QUERY HERE’ box. Please take note that the SQL
query should only be in lower case for the algorithm to work except for keywords, for
example ‘SELECT’, ‘FROM’ and ‘AND’, which can be in upper case.
* Step 3: Click the EXECUTE button to generate the result. Do note that, on average, the
processing time for each query is 15 seconds before the results are displayed.
* Step 4: Move the scroll bar to view the Formatted Query and the corresponding Annotations.
There are some example queries that are given in the appendix of the project report document.


## Creating TPC-H database
Follow the following steps to generate the TPC-H data:

1. Goto
http://www.tpc.org/tpc_documents_current_versions/current_specifications5.asp
and download TPC-H Tools v2.18.0.zip. Note that the version may defer as the tool
may have been updated by the developer.
2. Unzip the package. You will find a folder “dbgen” in it.
3. To generate an instance of the TPC-H database:
4. Open up tpch.vcproj using visual studio software.
5. Build the tpch project. When the build is successful, a command prompt will
appear with “TPC-H Population Generator <Version 2.17.3>” and several *.tbl files will be generated. You should expect the following .tbl files: customer.tbl, lineitem.tbl, nation.tbl, orders.tbl, part.tbl, partsupp.tbl, region.tbl, supplier.tbl
6. Save these .tbl files as .csv files
7. These .csv files contain an extra “|” character at the end of each line. These
“|” characters are incompatible with the format that PostgreSQL is expecting. Write a small piece of code to remove the last “|” character in each line. Now you are ready to load the .csv files into PostgreSQL
8. Open up PostgreSQL. Add a new database “TPC-H”.
9. Create new tables for “customer”, “lineitem”, “nation”, “orders”, “part”,
“partsupp”, “region” and “supplier”
10. Import the relevant .csv into each table. Note that pgAdmin4 for PostgreSQL
(windows version) allows you to perform import easily. You can select to view the first 100 rows to check if the import has been done correctly.
If encountered error (e.g., ERROR: extra data after last expected column) while importing, create columns of each table first before importing. Note that the types of each column has to be set appropriately. You may use the SQL commands in the SQL_Commands.txt file to create the tables.

