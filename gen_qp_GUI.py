'''
GUI for displaying and editing table contents.
Assumption- Column Names: qno, question_text, answers, paramaters
The initial window allows the user to choose the database.
In the main window, the user can edit the content of the table.
The main window also has a menu at the top.
File > Open allows the user to open another database
File > Exit allows the user to exit the application
'''
import PySimpleGUIQt as sg
import sqlite3

sg.theme('Reddit')

#Initial layout for choosing database
layout1 = [[sg.Text('Source for database ', size=(15, 1)), sg.InputText(), sg.FileBrowse()],
      [sg.Submit(), sg.Cancel()]]

window1 = sg.Window('Choose the database', layout1)

event, values = window1.read()
window1.close()
file_path = values[0]       # get the data from the values dictionary
conn = sqlite3.connect(file_path)   #Opens connection to the database
cursor = conn.cursor()                   #To read data from the table

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tableName = cursor.fetchall()[0][0]
window1.close()
data = cursor.execute("SELECT * FROM %s" %tableName).fetchall()
data=[list(i) for i in data]
numColumns = 4
numRows = len(data)

def TableSimulation():
    """
    Display data in a table format
    """
    sg.set_options(element_padding=(0, 0))

    menu_def = [['File', ['Open', 'Exit']],    #removed  'Save',
                #['Edit', ['Paste', ['Special', 'Normal', ], 'Undo'], ],
                ['Help', 'About...'], ]

    MAX_ROWS = numRows
    MAX_COL = numColumns
    global data

    #Layout of the table
    columm_layout =  [[sg.Multiline(str(data[i][j]),size=(25, 5), pad=(
            1, 1), key=(i, j)) for j in range(MAX_COL)] for i in range(MAX_ROWS)]
    col_layout = [[sg.Text('qno'),sg.Text('question_text'),sg.Text('answers'),sg.Text('paramaters')]]
    col_layout.extend(columm_layout)

    #Layout of the table window
    layout = [[sg.Menu(menu_def)],[sg.Stretch()],
              [sg.Stretch(),sg.Text('Table of Questions and Solutions', font='Any 18'),sg.Stretch()],
              [sg.Stretch(),sg.Col(col_layout, size=(800,600),scrollable=True),sg.Stretch()],[sg.Stretch()]]

    window = sg.Window('Table', layout, return_keyboard_events=True)

    while True:
        event, values = window.read()
        # --- Process buttons --- #
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        elif event == 'About...':
            sg.popup('Demo of table capabilities')
        elif event == 'Open':
            filename = sg.popup_get_file(
                'Choose the database to open', no_window=True)
            # --- populate table with file contents --- #
            if filename is not None:
                global conn
                conn.close()
                conn = sqlite3.connect(filename)   #Opens connection to the database
                cursor = conn.cursor()                   #To read data from the table
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                try:
                    tableName = cursor.fetchall()[0][0]
                except:
                    sg.popup_ok('No file selected')
                    continue
                try:
                        data = cursor.execute("SELECT * FROM %s" %tableName).fetchall()
                        data=[list(i) for i in data]
                        MAX_ROWS = len(data)
                except:
                        sg.popup_error('Error reading file')
                        continue
                # clear the table window
                window.close()

                #New layout with new data
                columm_layout =  [[sg.Multiline(str(data[i][j]),size=(25, 5), pad=(
                        1, 1), key=(i, j)) for j in range(MAX_COL)] for i in range(MAX_ROWS)]
                col_layout = [[sg.Text('qno'),sg.Text('question_text'),sg.Text('answers'),sg.Text('paramaters')]]
                col_layout.extend(columm_layout)


                layout = [[sg.Menu(menu_def)],[sg.Stretch()],
                          [sg.Stretch(),sg.Text('Table of Questions and Solutions', font='Any 18'),sg.Stretch()],
                          [sg.Stretch(),sg.Col(col_layout, size=(800,600),scrollable=True),sg.Stretch()],[sg.Stretch()]]

                window = sg.Window('Table', layout, return_keyboard_events=True)
            else:
                continue

    window.close()


TableSimulation()
