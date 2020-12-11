'''
GUI for displaying and editing table contents.
Assumption- Column Names: qno, question_text, answers, paramaters
The initial window allows the user to choose the database.
In the main window, the user can edit the content of the table.
The main window also has a menu at the top.
File > Open allows the user to open another database
File > New allows the user to open a new database
File > Save allows the user to save their progress in the current database
File > Save As allows the user to copy the current content into another new database
File > Exit allows the user to exit the application
Help > Instructions outlines the instructions for the user
'''
import PySimpleGUIQt as sg
import sqlite3
import json
import sys

sg.theme('Reddit')

#Initial layout for choosing database
layout1 = [[sg.Text('Source for database ', size=(15, 1)), sg.InputText(), sg.FileBrowse()],
      [sg.Submit(), sg.Cancel()],
      [sg.Button('New')]]

window1 = sg.Window('Choose the database', layout1)

event, values = window1.read()
window1.close()
if event == 'Submit':
    file_path = values[0]       # get the data from the values dictionary
    #print(file_path,event)
    conn = sqlite3.connect(file_path)   #Opens connection to the database
    cursor = conn.cursor()                   #To read data from the table

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tableName = cursor.fetchall()[0][0]    #Gets the name of the table
    window1.close()
    data = cursor.execute("SELECT * FROM %s" %tableName).fetchall()
    data=[list(i) for i in data]
    numColumns = 4
    numRows = len(data)
    saveStatus = True    #Denotes the status of the file (saved or not saved). It isn't accurate as it can't detect whether contents in the fields have been changed.
elif event == 'New':   #Opens a new database
    saveStatus = False
    data =[[1,'Enter Question', None, '[]']]
    numRows = 1
    numColumns = 4
    tableName = None
    conn = None
    cursor =None
elif event == 'Cancel':
    sys.exit()

def TableSimulation():
    """
    Display data in a table format, allowing it to be edited.
    """
    sg.set_options(element_padding=(0, 0))

    menu_def = [['File', ['New','Open','Save', 'Save As','Exit']],
                ['Help', 'Instructions'], ]

    global numRows, numColumns, saveStatus
    MAX_ROWS = numRows
    MAX_COL = numColumns
    global data

    #Layout of the table
    columm_layout =  [[sg.Multiline(str(data[i][j]),size=(30, 6), pad=(
            1, 1), key=(i, j)) for j in range(MAX_COL)] for i in range(MAX_ROWS)]
    col_layout = [[sg.Text('qno'),sg.Text('question_text'),sg.Text('answers'),sg.Text('parameters')]]
    col_layout.extend(columm_layout)

    #Layout of the table window
    layout = [[sg.Menu(menu_def)],[sg.Stretch()],
              [sg.Stretch(),sg.Button('Save'),sg.Stretch(),sg.Text('Table of Questions and Solutions', font='Any 18'),sg.Stretch(),sg.Button('Exit'),sg.Stretch()],
              [sg.Stretch(),sg.Col(col_layout, size=(1000,750),scrollable=True),sg.Stretch()],[sg.Stretch()],
              [sg.Stretch(),sg.Button('Add row'),sg.Stretch(),sg.Button('Delete row(s)'),sg.Stretch()] ]
    global tableName
    if tableName is None:
        windowTitle = "Untitled"
    else:
        windowTitle = tableName
    if not saveStatus:
        windowTitle+=" (Unsaved Changes)"

    window = sg.Window(windowTitle, layout, return_keyboard_events=True)

    while True:
        event, values = window.read()
        # --- Process buttons --- #
        if event in (sg.WIN_CLOSED, 'Exit'):
            if event =='Exit':
                layout3=[[sg.Stretch(),sg.Text("All unsaved changes will be lost. Are you sure you want to quit?"),sg.Stretch()],[sg.Stretch(),sg.Button('Yes'),sg.Stretch(),sg.Button('No'),sg.Stretch()]]
                window3 = sg.Window('Exit',layout3,return_keyboard_events=True)
                event3, value3 = window3.read()
                if event3 =="No":
                    window3.close()
                    continue
            break
        elif event == 'New':
            saveStatus = False
            global data
            data =[[1,'Enter Question', None, '[]']]
            numRows = 1
            numColumns = 4
            tableName = None
            MAX_ROWS = numRows
            MAX_COL = numColumns
            conn = None
            cursor =None
            columm_layout =  [[sg.Multiline(str(data[i][j]),size=(30, 6), pad=(
                    1, 1), key=(i, j)) for j in range(MAX_COL)] for i in range(MAX_ROWS)]
            col_layout = [[sg.Text('qno'),sg.Text('question_text'),sg.Text('answers'),sg.Text('parameters')]]
            col_layout.extend(columm_layout)

            #Layout of the table window
            layout = [[sg.Menu(menu_def)],[sg.Stretch()],
                      [sg.Stretch(),sg.Button('Save'),sg.Stretch(),sg.Text('Table of Questions and Solutions', font='Any 18'),sg.Stretch(),sg.Button('Exit'),sg.Stretch()],
                      [sg.Stretch(),sg.Col(col_layout, size=(1000,750),scrollable=True),sg.Stretch()],[sg.Stretch()],
                      [sg.Stretch(),sg.Button('Add row'),sg.Stretch(),sg.Button('Delete row(s)'),sg.Stretch()] ]
            if tableName is None:
                windowTitle = "Untitled"
            else:
                windowTitle = tableName
            if not saveStatus:
                windowTitle+=" (Unsaved Changes)"
            window.close()
            window = sg.Window(windowTitle, layout, return_keyboard_events=True)

        elif event == 'Instructions':
            sg.popup('''Instructions for use:\n
            To work with tables, import a database using File>Open or select a databse in the beginning.\n
            It is assumed that the database contains only one table.\n
            Further, it is assumed that the table contains columns named 'qno', 'question_text', 'answers' and 'parameters'.\n
            qno is of type INTEGER, is the PRIMARY KEY and cannot be NULL.\n
            question_text is of type TEXT and cannot be NULL\n
            answers is of type TEXT (can be NULL)\n
            parameters is of type JSON\n
            While editing, if you want answers to be NULL, just type 'None' in the box. (without the quotes)\n
            If you leave the answers field blank, it won't be NULL.\n
            Similarly, if you want parameters to contain nothing, type '[]' in the box. (without the quotes)\n
            You CANNOT leave the parameters field blank and it MUST contain valid JSON objects/arrays.\n
            Before closing the application, make sure you click on 'Save' to save your progress. The program doesn't automatically save the contents in the database.\n
            After any action (like adding a row, deleting a row,etc), the original database won't be affected until and unless 'Save' is clicked.\n
            Before opening a new database (using 'Open'), press 'Save' if you want the contents to be saved in the original database.\n
            To delete row(s), press on 'Delete row(s)' and enter qnos of rows you want to delete.\n
            ''')
        elif event == 'Delete row(s)':
            layout4=[[sg.Stretch(),sg.Text("Enter the qno(s) of row(s) you want to delete (separated by commas (,))"),sg.Stretch()],[sg.InputText()],[sg.Stretch(),sg.Button('Okay'),sg.Stretch(),sg.Button('Cancel'),sg.Stretch()]]
            window4 = sg.Window('Delete Row(s)',layout4,return_keyboard_events=True)
            while True:
                event4, value4 = window4.read()
                #print(event4,value4)
                if event4 == 'Okay':
                    window4.close()
                    rowsToDelete = value4[0].split(",")
                    #print(rowsToDelete)
                    if rowsToDelete == ['']:
                        break
                    rowsToDelete = [int(ele.strip()) for ele in rowsToDelete]
                    #print(rowsToDelete)
                    inputData = []
                    for i in range(MAX_ROWS):
                        row = []
                        for j in range(4):
                            InputText=""
                            for ch in values[(i,j)]:
                                InputText+=str(ch)
                                if InputText == 'None':
                                    InputText = None
                            if j==0:
                                InputText=int(InputText)
                            row.append(InputText)
                        inputData.append(row)
                    test_list = [ inputData[i][0] for i in range(MAX_ROWS)]
                    flag = len(set(test_list)) == len(test_list)
                    if not flag:
                        sg.popup_ok('Please enter unique values for qno!')
                        continue
                    #print(inputData)
                    json_list = [inputData[i][3] for i in range(MAX_ROWS)]
                    json_string = "["
                    for i in range(len(json_list)):
                        json_string+=json_list[i]
                        if json_list[i][-1]==']' and i != len(json_list)-1:
                            json_string+=","
                    json_string+="]"
                    #print(json_string)
                    json_list = eval(json_string)
                    #print(json_list,type(json_list))
                    ##print(type(json_list[-1][0]))
                    for i in range(MAX_ROWS):
                        inputData[i][3]=json_list[i]
                    MAX_ROWS=0
                    for ele in inputData:
                        if ele[0] not in rowsToDelete:
                            MAX_ROWS+=1
                    data = [ele for ele in inputData if ele[0] not in rowsToDelete]
                    saveStatus = False
                    #Layout of the table
                    columm_layout =  [[sg.Multiline(str(data[i][j]),size=(30, 6), pad=(
                            1, 1), key=(i, j)) for j in range(MAX_COL)] for i in range(MAX_ROWS)]
                    col_layout = [[sg.Text('qno'),sg.Text('question_text'),sg.Text('answers'),sg.Text('parameters')]]
                    col_layout.extend(columm_layout)

                    #Layout of the table window
                    layout = [[sg.Menu(menu_def)],[sg.Stretch()],
                              [sg.Stretch(),sg.Button('Save'),sg.Stretch(),sg.Text('Table of Questions and Solutions', font='Any 18'),sg.Stretch(),sg.Button('Exit'),sg.Stretch()],
                              [sg.Stretch(),sg.Col(col_layout, size=(1000,750),scrollable=True),sg.Stretch()],[sg.Stretch()],
                              [sg.Stretch(),sg.Button('Add row'),sg.Stretch(),sg.Button('Delete row(s)'),sg.Stretch()] ]
                    if tableName is None:
                        windowTitle = "Untitled"
                    else:
                        windowTitle = tableName
                    if not saveStatus:
                        windowTitle+=" (Unsaved Changes)"
                    window.close()
                    window = sg.Window(windowTitle, layout, return_keyboard_events=True)
                    break
                elif event4 == 'Cancel':
                    window4.close()
                    break

        elif event == 'Open':
            global file_path
            file_name = sg.popup_get_file(
                'Choose the database to open', no_window=True)
            # --- populate table with file contents --- #
            if file_name is not None:
                file_path=file_name
                #print(file_path)
                conn.close()
                conn = sqlite3.connect(file_path)   #Opens connection to the database
                cursor = conn.cursor()                   #To read data from the table
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                try:
                    tableName = cursor.fetchall()[0][0]
                    #print(tableName)
                except:
                    continue
                try:
                        data = cursor.execute("SELECT * FROM %s" %tableName).fetchall()
                        data=[list(i) for i in data]
                        #print(data)
                        MAX_ROWS = len(data)
                except:
                        sg.popup_error('Error reading file')
                        continue
                # clear the table window
                window.close()

                #New layout with new data
                columm_layout =  [[sg.Multiline(str(data[i][j]),size=(30, 6), pad=(
                        1, 1), key=(i, j)) for j in range(MAX_COL)] for i in range(MAX_ROWS)]
                col_layout = [[sg.Text('qno'),sg.Text('question_text'),sg.Text('answers'),sg.Text('parameters')]]
                col_layout.extend(columm_layout)
                saveStatus = True


                layout = [[sg.Menu(menu_def)],[sg.Stretch()],
                          [sg.Stretch(),sg.Button('Save'),sg.Stretch(),sg.Text('Table of Questions and Solutions', font='Any 18'),sg.Stretch(),sg.Button('Exit'),sg.Stretch()],
                          [sg.Stretch(),sg.Col(col_layout, size=(1000,750),scrollable=True),sg.Stretch()],[sg.Stretch()],
                          [sg.Stretch(),sg.Button('Add row'),sg.Stretch(),sg.Button('Delete row(s)'),sg.Stretch()] ]
                if tableName is None:
                    windowTitle = "Untitled"
                else:
                    windowTitle = tableName
                if not saveStatus:
                    windowTitle+=" (Unsaved Changes)"
                window.close()
                window = sg.Window(windowTitle, layout, return_keyboard_events=True)
            else:
                continue
        elif event=='Add row':
            data = []
            for i in range(MAX_ROWS):
                row = []
                for j in range(4):
                    InputText=""
                    #print(values[(i,j)])
                    for ch in values[(i,j)]:
                        #print(ch)
                        InputText+=str(ch)
                        if InputText == 'None':
                            InputText = None
                    if j==0:
                        InputText=int(InputText)
                    row.append(InputText)
                data.append(row)
            json_list = [data[i][3] for i in range(MAX_ROWS)]
            json_string = "["
            for i in range(len(json_list)):
                json_string+=json_list[i]
                if json_list[i][-1]==']' and i != len(json_list)-1:
                    json_string+=","
            json_string+="]"
            #print(json_string)
            json_list = eval(json_string)
            #print(json_list,type(json_list))
            ##print(type(json_list[-1][0]))
            for i in range(MAX_ROWS):
                data[i][3]=json_list[i]
            data.append([max([ele[0] for ele in data])+1,'Enter Question', None, '[]'])
            #print(data)
            columm_layout =  [[sg.Multiline(str(data[i][j]),size=(30, 6), pad=(
                    1, 1), key=(i, j)) for j in range(MAX_COL)] for i in range(MAX_ROWS+1)]
            col_layout = [[sg.Text('qno'),sg.Text('question_text'),sg.Text('answers'),sg.Text('parameters')]]
            col_layout.extend(columm_layout)
            #Layout of the table window
            layout = [[sg.Menu(menu_def)],[sg.Stretch()],
                      [sg.Stretch(),sg.Button('Save'),sg.Stretch(),sg.Text('Table of Questions and Solutions', font='Any 18'),sg.Stretch(),sg.Button('Exit'),sg.Stretch()],
                      [sg.Stretch(),sg.Col(col_layout, size=(1000,750),scrollable=True),sg.Stretch()],[sg.Stretch()],
                      [sg.Stretch(),sg.Button('Add row'),sg.Stretch(),sg.Button('Delete row(s)'),sg.Stretch()] ]
            window.close()
            saveStatus = False
            if tableName is None:
                windowTitle = "Untitled"
            else:
                windowTitle = tableName
            if not saveStatus:
                windowTitle+=" (Unsaved Changes)"
            window = sg.Window(windowTitle, layout, return_keyboard_events=True)
            MAX_ROWS+=1
            #print('Working')
        elif event == 'Save':
            inputData = []
            for i in range(MAX_ROWS):
                row = []
                for j in range(4):
                    InputText=""
                    for ch in values[(i,j)]:
                        InputText+=str(ch)
                        if InputText == 'None':
                            InputText = None
                    if j==0:
                        InputText=int(InputText)
                    row.append(InputText)
                inputData.append(row)
            test_list = [ inputData[i][0] for i in range(MAX_ROWS)]
            flag = len(set(test_list)) == len(test_list)
            if not flag:
                sg.popup_ok('Please enter unique values for qno!')
                continue
            #print(inputData)
            json_list = [inputData[i][3] for i in range(MAX_ROWS)]
            json_string = "["
            for i in range(len(json_list)):
                json_string+=json_list[i]
                if json_list[i][-1]==']' and i != len(json_list)-1:
                    json_string+=","
            json_string+="]"
            #print(json_string)
            json_list = eval(json_string)
            #print(json_list,type(json_list))
            ##print(type(json_list[-1][0]))
            for i in range(MAX_ROWS):
                inputData[i][3]=json_list[i]
            ##print(inputData, type(inputData[-1][3]),type(inputData[-1][3][-1]))
            data = inputData
            try:
                if tableName is not None:
                    conn = sqlite3.connect(file_path)
                    cursor=conn.cursor()
                    cursor.execute("DELETE FROM "+ tableName)
                    for i in range(MAX_ROWS):
                        sqlCommand = "INSERT INTO "+ tableName +" (qno, question_text, answers, parameters) VALUES(?, ?, ?, ?)"
                        params = (inputData[i][0], inputData[i][1], inputData[i][2], json.dumps(inputData[i][3]))
                        #if inputData[i][2] is not None:
                        cursor.execute(sqlCommand,(inputData[i][0], inputData[i][1], inputData[i][2], json.dumps(inputData[i][3])))#.format(tableName,inputData[i][0],inputData[i][1],inputData[i][2]))#,inputData[i][3]))
                        # else:
                        #     cursor.execute("INSERT INTO {0} (qno, question_text, answers, parameters) VALUES({1},'{2}',{3},[])".format(tableName,inputData[i][0],inputData[i][1],inputData[i][2]))#,inputData[i][3]))
                        conn.commit()
                else:
                    layout2 = [[
                        sg.InputText(visible=False, enable_events=True, key='file_path'),
                        sg.FileSaveAs(
                            key='file_save',
                            file_types=(('Database (.db)', '.db'),),  # TODO: better names
                        )
                    ]]
                    window2 = sg.Window('', layout2)
                    event2, values2 = window2.read()
                    window2.close()
                    #print(event2,values2)
                    if event2 == 'file_path':
                        file_path = values2['file_path']
                        tableName = file_path.split('/')[-1]
                        if file_path[-3:] != ".db":
                            file_path = file_path+".db"
                        else:
                            tableName=tableName[:-3]
                        #print(file_path,tableName)
                        conn = sqlite3.connect(file_path)   #Opens connection to the database
                        cursor = conn.cursor()                   #To read data from the table

                        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                        try:
                            if tableName == cursor.fetchall()[0][0]:
                                cursor.execute("DELETE FROM "+ tableName)
                        except:
                            pass
                        cursor.execute("CREATE TABLE IF NOT EXISTS "+tableName+" ( qno INTEGER PRIMARY KEY, question_text TEXT NOT NULL, answers TEXT, parameters JSON);")
                        numColumns = 4
                        numRows = len(data)
                        MAX_ROWS = numRows
                        for i in range(MAX_ROWS):
                            sqlCommand = "INSERT INTO "+ tableName +" (qno, question_text, answers, parameters) VALUES(?, ?, ?, ?)"
                            params = (inputData[i][0], inputData[i][1], inputData[i][2], json.dumps(inputData[i][3]))
                            #if inputData[i][2] is not None:
                            cursor.execute(sqlCommand,(inputData[i][0], inputData[i][1], inputData[i][2], json.dumps(inputData[i][3])))#.format(tableName,inputData[i][0],inputData[i][1],inputData[i][2]))#,inputData[i][3]))
                            # else:
                            #     cursor.execute("INSERT INTO {0} (qno, question_text, answers, parameters) VALUES({1},'{2}',{3},[])".format(tableName,inputData[i][0],inputData[i][1],inputData[i][2]))#,inputData[i][3]))
                            conn.commit()
                saveStatus = True
            except sqlite3.Error as e:
                #print(e)
                sg.popup_ok('Couldn\'t Save. Please try again.')
                saveStatus = False
            columm_layout =  [[sg.Multiline(str(data[i][j]),size=(30, 6), pad=(
                    1, 1), key=(i, j)) for j in range(MAX_COL)] for i in range(MAX_ROWS)]
            col_layout = [[sg.Text('qno'),sg.Text('question_text'),sg.Text('answers'),sg.Text('parameters')]]
            col_layout.extend(columm_layout)

            #Layout of the table window
            layout = [[sg.Menu(menu_def)],[sg.Stretch()],
                      [sg.Stretch(),sg.Button('Save'),sg.Stretch(),sg.Text('Table of Questions and Solutions', font='Any 18'),sg.Stretch(),sg.Button('Exit'),sg.Stretch()],
                      [sg.Stretch(),sg.Col(col_layout, size=(1000,750),scrollable=True),sg.Stretch()],[sg.Stretch()],
                      [sg.Stretch(),sg.Button('Add row'),sg.Stretch(),sg.Button('Delete row(s)'),sg.Stretch()] ]
            if tableName is None:
                windowTitle = "Untitled"
            else:
                windowTitle = tableName
            if not saveStatus:
                windowTitle+=" (Unsaved Changes)"
            window.close()
            window = sg.Window(windowTitle, layout, return_keyboard_events=True)
        elif event =='Save As':
            inputData = []
            for i in range(MAX_ROWS):
                row = []
                for j in range(4):
                    InputText=""
                    for ch in values[(i,j)]:
                        InputText+=str(ch)
                        if InputText == 'None':
                            InputText = None
                    if j==0:
                        InputText=int(InputText)
                    row.append(InputText)
                inputData.append(row)
            test_list = [ inputData[i][0] for i in range(MAX_ROWS)]
            flag = len(set(test_list)) == len(test_list)
            if not flag:
                sg.popup_ok('Please enter unique values for qno!')
                continue
            #print(inputData)
            json_list = [inputData[i][3] for i in range(MAX_ROWS)]
            json_string = "["
            for i in range(len(json_list)):
                json_string+=json_list[i]
                if json_list[i][-1]==']' and i != len(json_list)-1:
                    json_string+=","
            json_string+="]"
            #print(json_string)
            json_list = eval(json_string)
            #print(json_list,type(json_list))
            ##print(type(json_list[-1][0]))
            for i in range(MAX_ROWS):
                inputData[i][3]=json_list[i]
            ##print(inputData, type(inputData[-1][3]),type(inputData[-1][3][-1]))
            data = inputData
            try:
                layout2 = [[
                    sg.InputText(visible=False, enable_events=True, key='file_path'),
                    sg.FileSaveAs(
                        key='file_save',
                        file_types=(('Database (.db)', '.db'),),  # TODO: better names
                    )
                ]]
                window2 = sg.Window('', layout2)
                event2, values2 = window2.read()
                window2.close()
                #print(event2,values2)
                if event2 == 'file_path':
                    file_path = values2['file_path']
                    tableName = file_path.split('/')[-1]
                    if file_path[-3:] != ".db":
                        file_path = file_path+".db"
                    else:
                        tableName=tableName[:-3]
                    #print(file_path,tableName)
                    conn = sqlite3.connect(file_path)   #Opens connection to the database
                    cursor = conn.cursor()                   #To read data from the table

                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                    try:
                        if tableName == cursor.fetchall()[0][0]:
                            cursor.execute("DELETE FROM "+ tableName)
                    except:
                        pass
                    cursor.execute("CREATE TABLE IF NOT EXISTS "+tableName+" ( qno INTEGER PRIMARY KEY, question_text TEXT NOT NULL, answers TEXT, parameters JSON);")
                    numColumns = 4
                    numRows = len(data)
                    MAX_ROWS = numRows
                    for i in range(MAX_ROWS):
                        sqlCommand = "INSERT INTO "+ tableName +" (qno, question_text, answers, parameters) VALUES(?, ?, ?, ?)"
                        params = (inputData[i][0], inputData[i][1], inputData[i][2], json.dumps(inputData[i][3]))
                        #if inputData[i][2] is not None:
                        cursor.execute(sqlCommand,(inputData[i][0], inputData[i][1], inputData[i][2], json.dumps(inputData[i][3])))#.format(tableName,inputData[i][0],inputData[i][1],inputData[i][2]))#,inputData[i][3]))
                        # else:
                        #     cursor.execute("INSERT INTO {0} (qno, question_text, answers, parameters) VALUES({1},'{2}',{3},[])".format(tableName,inputData[i][0],inputData[i][1],inputData[i][2]))#,inputData[i][3]))
                        conn.commit()
                saveStatus =True
            except sqlite3.Error as e:
                #print(e)
                sg.popup_ok('Couldn\'t Save. Please check the entries!')
                saveStatus = False
            window.close()

            #New layout with new data
            columm_layout =  [[sg.Multiline(str(data[i][j]),size=(30, 6), pad=(
                    1, 1), key=(i, j)) for j in range(MAX_COL)] for i in range(MAX_ROWS)]
            col_layout = [[sg.Text('qno'),sg.Text('question_text'),sg.Text('answers'),sg.Text('parameters')]]
            col_layout.extend(columm_layout)


            layout = [[sg.Menu(menu_def)],[sg.Stretch()],
                      [sg.Stretch(),sg.Button('Save'),sg.Stretch(),sg.Text('Table of Questions and Solutions', font='Any 18'),sg.Stretch(),sg.Button('Exit'),sg.Stretch()],
                      [sg.Stretch(),sg.Col(col_layout, size=(1000,750),scrollable=True),sg.Stretch()],[sg.Stretch()],
                      [sg.Stretch(),sg.Button('Add row'),sg.Stretch(),sg.Button('Delete row(s)'),sg.Stretch()] ]
            windowTitle = tableName
            if tableName is None:
                windowTitle = "Untitled"
            else:
                windowTitle = tableName
            if not saveStatus:
                windowTitle+=" (Unsaved Changes)"

            window = sg.Window(windowTitle, layout, return_keyboard_events=True)

    window.close()


TableSimulation()
