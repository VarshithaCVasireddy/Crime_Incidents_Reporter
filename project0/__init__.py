import urllib.request
import tempfile
import PyPDF2
import re
import sqlite3


def fetchincidents(url):
    headers = {}
    headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
    data = urllib.request.urlopen(
        urllib.request.Request(
            url, headers=headers)).read()
    return data


def extractincidents(incident_data):
    # temporary file is created to store data
    fp = tempfile.TemporaryFile()

    # Write the pdf data to a temp file
    fp.write(incident_data)

    # Set the curser of the file back to the begining
    fp.seek(0)

    # Reading the PDF
    pdfReader = PyPDF2.pdf.PdfFileReader(fp)
    # Getting the total page numbers in PDF
    pagecount = pdfReader.getNumPages()
    print(f'Extracting data from {pagecount} pages')

    page_contents = pdfReader.getPage(0).extractText()
    page_contents = page_contents.replace(
        "Date / Time\nIncident Number\nLocation\nNature\nIncident ORI\n", "")
    page_contents = page_contents.replace(
        "\nNORMAN POLICE DEPARTMENT\nDaily Incident Summary (Public)\n", "")
    page_contents = page_contents.replace(" \n", " ")

    page_contents = re.sub(
        '\n(\\d?\\d/\\d?\\d/\\d{4} )',
        lambda x: f'\n||{x.group(1)}',
        page_contents)
    data = []
    for i in page_contents.split('\n||'):
        data.append(i.split('\n'))

    # Now getting text from all the other pages
    for pagenum in range(1, pagecount):
        page_contents = pdfReader.getPage(pagenum).extractText()
        page_contents = page_contents.replace(" \n", " ")
        page_contents = re.sub(
            '\n(\\d?\\d/\\d?\\d/\\d{4} )',
            lambda x: f'\n||{x.group(1)}',
            page_contents)
        for i in str.strip(page_contents).split('\n||'):
            data.append(i.split('\n'))

    special_data1 = [[i[0], i[1], '', '', i[2]] for i in data if len(i) == 3]
    special_data2 = [[i[0], i[1], i[2], '', i[3]] for i in data if len(i) == 4]
    data = [i for i in data if len(i) == 5]
    data += special_data1
    data += special_data2

    return data


def createdb():
    db_name = 'data.db'
    # To connect to SQLite database
    connection = sqlite3.connect(db_name)

    # To create the database
    cursor = connection.cursor()
    # To delete the database if it already exists
    cursor.execute('DROP TABLE IF EXISTS incident')
    # To create a database
    cursor.execute(
        'CREATE TABLE incident (date_Time TEXT, incident_Number TEXT, location TEXT, nature TEXT, incident_ORI TEXT);')

    connection.commit()
    connection.close()
    return db_name


def populatedb(db_name, incidents):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    for i, row in enumerate(incidents):
        date_Time = row[0]
        incident_Number = row[1]
        location = row[2]
        nature = row[3]
        incident_ORI = row[4]

        cursor.execute(
            "INSERT INTO incident VALUES (?,?,?,?,?)",
            (date_Time, incident_Number, location, nature, incident_ORI)
        )

    connection.commit()
    return connection.total_changes


def status(db_name):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    rows = cursor.execute(
        "SELECT nature, count(*) as count FROM incident group by nature order by count(*) desc, nature ASC"
    ).fetchall()

    out_str = "\nNature|Count\n"
    for row in rows:
        out_str += f'{row[0]}|{row[1]}\n'

    print(out_str)
