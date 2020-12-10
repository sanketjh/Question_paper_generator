'''
Assumption- Column Names: qno, question_text, answers, paramaters
This is a basic GUI program which displays the contents of a table and opens its field
in an editor.
To select a row in the table, click on the corresponding row number.
To open a field in a text editor, select a row and click on the Markdown button
'''
import PySimpleGUIQt as sg
import sqlite3

sg.theme('Reddit')  # please make your windows colorful

#----Initial Window - asks for the source of database
layout1 = [[sg.Text('Source for database ', size=(15, 1)), sg.InputText(), sg.FileBrowse()],
      [sg.Stretch(),sg.Submit(), sg.Cancel(),sg.Stretch()]]

window1 = sg.Window('Choose the database', layout1)

event, values = window1.read()
window1.close()
file_path = values[0]       # get the data from the values dictionary
conn = sqlite3.connect(file_path)   #Opens connection to the database
cursor = conn.cursor()                   #To read data from the table

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tableName = cursor.fetchall()[0][0]   #Name of the table in the database
window1.close()


# ----Main Window which displays the table
data = cursor.execute("SELECT * FROM %s" %tableName).fetchall()
data=[list(i) for i in data]
layout = [[sg.Stretch()],[sg.Stretch(), sg.Table(values=data, headings=['qno','question_text','answers','parameters'],
                    # background_color='light blue',
                    auto_size_columns=True,
                    display_row_numbers=False,
                    justification='right',
                    num_rows=len(data),
                    key='-TABLE-',
                    #row_height=35,
                    tooltip='This is a table'),sg.Stretch()],#[sg.Stretch()],
          [sg.Stretch(),sg.Button('Markdown'),sg.Stretch()],
          [sg.Text('Markdown = Renders the selected row in markdown'),sg.Stretch()],
          [sg.Text('To select a row, click on the row number'), sg.Stretch()],[sg.Stretch()]]

window = sg.Window('The Table Element', layout,
                   # font='Helvetica 25',
                   ).Finalize()

while True:
    event, values = window.read()
    print(event, values)
    if event == sg.WIN_CLOSED:
        break
    if event == 'Markdown':
        if not values['-TABLE-']:
            sg.Popup('Please select a row first',keep_on_top= True)
            continue
        editLayout =[[sg.Stretch()],[sg.Text('Which field do you want to render in Markdown?')],
        [sg.Stretch(),sg.Button('qno'),sg.Stretch()],
        [sg.Stretch(),sg.Button('question_text'),sg.Stretch()],
        [sg.Stretch(),sg.Button('answers'),sg.Stretch()],
        [sg.Stretch(),sg.Button('paramaters'),sg.Stretch()],[sg.Stretch()]]
        editWindow = sg.Window('Edit', editLayout)
        editEvent, editValue = editWindow.read()
        editWindow.close()
        if editEvent == 'qno':
            editLayout1 =[[sg.Multiline(str(data[int(values['-TABLE-'][0])][0]), pad=(
                        1, 1))],[sg.Stretch(),sg.Button('Done'),sg.Stretch()]]
            editWindow1 = sg.Window('Edit qno', editLayout1)
            editEvent1, editValue1 = editWindow1.read()
            editWindow1.close()
        elif editEvent == 'question_text':
            editLayout1 =[[sg.Multiline(str(data[int(values['-TABLE-'][0])][1]),pad=(
                        1, 1))],[sg.Stretch(),sg.Button('Done'),sg.Stretch()]]
            editWindow1 = sg.Window('Edit question_text', editLayout1)
            editEvent1, editValue1 = editWindow1.read()
            editWindow1.close()
        elif editEvent == 'answers':
            editLayout1 =[[sg.Multiline(str(data[int(values['-TABLE-'][0])][2]), pad=(
                        1, 1))],[sg.Stretch(),sg.Button('Done'),sg.Stretch()]]
            editWindow1 = sg.Window('Edit answers', editLayout1)
            editEvent1, editValue1 = editWindow1.read()
            editWindow1.close()
        elif editEvent == 'paramaters':
            editLayout1 =[[sg.Multiline(str(data[int(values['-TABLE-'][0])][3]), pad=(
                        1, 1))],[sg.Stretch(),sg.Button('Done'),sg.Stretch()]]    #, justification='left' removed
            editWindow1 = sg.Window('Edit paramaters', editLayout1)
            editEvent1, editValue1 = editWindow1.read()
            editWindow1.close()
window.close()
