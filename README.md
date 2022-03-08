## cs5293sp22-project0

## Author: Varshitha Choudary Vasireddy

## Setting up the Initial installations 
We run the following installations in the project's virtual environment. Even if the installations are done in the Python environment, in the project's virtual environment, there might be an error popping up "no module named nltk"
~~~
pipenv install nltk
pipenv install re
pipenv install CommonRegex
pipenv install numpy
~~~

## Description of the project:

The Norman, Oklahoma police department regularly reports incidents, arrests, and other activities. This data is distributed to the public in the form of PDF files.
The website contains three types of summaries arrests, incidents, and case summaries. In this project a function is built that collects only the incidents. And Following operations are to be done

- To download the data given one incident pdf
- To Extract the below fields:
  - Date / Time
  - Incident Number
  - Location
  - Nature
  - Incident ORI
- To create a SQLite database to store the data;
- To Insert the data into the database;
- To Print each nature and the number of times it appears

## Packages Required for Project:

- urllib.request
- tempfile
- PyPDF2
- re
- sqlite3
\
The projects have below files: 
## 1. main.py 
 
project0.py is imported into this file and below mentioned functions will be executed by function calling. The URL will be accepted as an input argumnent.
\
Data downloaded function - incident_data = project0.fetchincidents(url)
Data Extract function - incidents = project0.extractincidents(incident_data)
New database creation function - db = project0.createdb()
Insert data function - project0.populatedb(db, incidents)
Print incident counts function - print(project0.status(db))

## 2. project0.py


### **fetchincidents(url)**

url will be the input for this function, url data will be read using urllib.request (extensible library for opening URLs) is used to read the data in the url given. The url that is given will be the incident data url.

### **extractincidents(incident_data)**

A temporary file is created using tempfile package (generates temporary files and directory), and onto that temporary file the input argument that this function takes i.e incident data is written into it.
PyPDF2 is used to read the pdf file where that data is stored in temporary file that is created in the previous steps. Total page numbers in the pdf file is read.
I divided my function into 2 parts where on first page I conducted few operations and onto rest of the pdf file pages I did few operations.

On the first page of pdf below operations will be done
**Screenshot1**
replace() method is used to removed unwanted information present in the first pdf page of the incident file. In order to read the second lines of columns " \n" is replaced
to just space so that I can perform operations on the edited data. Then using regex function and sub() function are used to put || operators
between each row. So now the data is split into list near the "\n||" operator. So this will create a list, where the each row is considered as list.
A new empty list is created and this list data is appended to it.

On the remaining pages of pdf below operations will be done
**Screenshot2**

So the same operations that are mentioned above are performed onto all pages. Since there will be no unwanted data in reamining pages the function to replace unwanted data is not used in this.

**Screenshot3**

**handling the missing values in the data**
We need the data to be present as a list of 5, beacuse there are 5 columns in the pdf, so upon research from the pdf's given I could see that only 3rd column and 4th column i.e 
location and nature will only be the missing columns. A new 5 length list is created where when the list is of 5 length then the same is copied into the list and if the
the list length is 4, I assumed that nature is missing in the row, and left the 4th list element empty and filled the other list elements.
When the list length is 3, I assumed that both location and nature columns are missing so 3rd and 4th list elements are kept empty, and other list elements are filled.

Finally as part of this function data which consists of the list of data as its elements will be returned.


### **createdb()**

**SS4**

Database is named as data.db. Then connection is made to the SQLite database using **sqlite3.connect ()** and then this connection will be called as cursor and statement are executed on it.
A new table is created namely "incident" as shown above, table will be dropped if it exists before creating the table, so that we don't get error telling that table is already present.
This table is commited and connection is closed. Database name will be returned as part of this function.

### **populatedb(db_name, incidents)**

The list from extractincidents() and  db name from createdb() is passed as input parameters to **populatedb()**,
**SS5**

In this function a connection is made to the database that is passed. 
And list elements of the incident data file will be read into the varibables and these will be used to insert data into the table.

### **status(db)**

**ss6**

Database is taken as the input parameter. A connection is made to the database. And the **SELECT** statement is executed, where nature is selected and it is counted. 
And the list is sorted first by the total number of incidents and secondarily, alphabetically by the nature. Each field of the row is separated by the pipe character (|).

## Pytest framework for the project :
I used the Pytest framework in Python to check for the individual test cases. To run the pytest framework, we need to first ensure if we have the pytest installed in our current project directory. I used the following command to install the pytest in my project's execution virtual environment.
~~~
pipenv install pytest
~~~

## 3.test_project0.py

The test_project0.py file contains the unit testcases to test each method of project0.py if it is working are not, in this file we written the below 5 testcases to test each method.
Below are imported for this file
- pytest
- NoneType from types
- os
- io
- sqlite3
- project0

**SS7**

### **test_fetchincidents():**

**SS8**

In this test method operations of fetchincidents method will be done on the "sample file" and then it is checked if the file is of type bytes from assert isinstance.
As the fetchincidents function should have bytes as data.

### **test_extractincidents():**

**SS9**

In this test case we test the extractincidents, the sample will be opened and operations of extractincidents method will be performed on this file. The list data lenght of the sample file I used is 237 so after performing the method to the data, it is checked if the result is same as the len of the data that I used to check the method.


### **test_createdb():**

**SS10**


In this testcase we would test the **createdb()**,

### **test_populatedb( ):**

**SS11**

In this method we test the **populated()** method,


## **test_status( ):**

In this method we test the **status()** method.
 **ss12**

## To run the Pytest : 
I used the following command to run my python tests for the given function.
~~~
 pipenv run python -m pytest
 ~~~

## 4.Assumptions/Bugs:

- In this project we assumed that only location and nature columns have missing values in the pdf document and we handled only the missing values in those columns, if any other column has the missing values in the pdf the code will fail. 
- After splitting the data by date the maximum length of the list we observed is 7, if the length of list is > 7 then the code may fail in this case.
- I assumed that among location and nature, if my data gives only list of length 4 then nature column is missing, this assumption is made after looking into the files, but if location is missed instead of nature then this code will fail.


## Steps to Run project0

- **Step1** \
clone the project directory using below command 
> git clone  https://github.com/PurushothamVadde/NLP_working_With_PDF_SQLite.git

- **Step2** \
Navigate to directory that we cloned from git **NLP_working_With_PDF_SQLite** and run the below command by providing URL

> pipenv run python project0/main.py --incidents **URL**

- **Step3** 

From **NLP_working_With_PDF_SQLite** run the below command to test the testcases. 

> pytest -v

## Git Repository commands :
Initially we create a private repository in ouy github accounts using the name cs5293p20-project1. We clone the repository link into our Linux environment by using the following command :
~~~
https://github.com/jwalareddy/cs5293sp20-project1.git
~~~
Further changes made to the directory structure are committed to github using the following commands :
~~~
git add -A
git commit -m " appropriate message to be displayed if it is the initial commit or the final commit"
git push origin master 
git pull origin master
~~~
If any errors occur while pushing the data from the linux environment to the github repository, we can use 
~~~
git push origin master --force
~~~
to pull the changes, if any, made from the github repository to our local environment, we use the following command :
~~~
git pull origin master
~~~

