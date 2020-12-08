'''
This program accepts the question numbers corresponding to the questions table in questions.db
database as arguments. Also, it accepts an optional argument, which is "-s" or "--Solutions".
If this argument is passed, the solutions are also made in a markdown file.
If no argument or only '-s' (or '--Solutions') is passed, both the question paper and solutions are made.

Database: questions.db
Table: questions (columns: qno, question_text, answers, parameters)

This program requires the question_text field in the questions table to be of a non-NULL type. The answers may be NULL,
in which case 'Solution not available' is written into the corresponding question in solutions.md
'''

import sys  #Needed to read arguments from the command line
import sqlite3  #Needed to read data from the database
from datetime import date  #Needed to add today's date in the Question Paper
import random  #Needed to randomise parameters
from jinja2 import Template  #Needed to assign values to parameters in Questions and Solutions

today = date.today()
d1 = today.strftime("%B %d, %Y")   #Date in "Month date, year" format

conn = sqlite3.connect('questions.db')   #Opens connection to the database
cursor = conn.cursor()                   #To read data from the table

paramChosen = []  #Empty list to later hold the value of randomly chosen parameter
paramIndex = 0  #A global index to make sure that Solutions and Question Paper have the same parameter values

def genQP(numArgs):
    '''
    Generates a markdown file (questions.md) containing the Question Paper
    '''
    global paramChosen
    j=1
    f = open("questions.md","w")       #Opens the markdown file where we have to create the question paper
    f.write("--- \n title: Question Paper \n author: Roll No.- \n date: %s \n--- \n \n# Questions \n" % d1) #Basic Formatting

    if numArgs==1 or (numArgs==2 and sys.argv[1] in ("-s", "--Solutions")):  #If no arguments are specified or only '-s' is specified
        rows = cursor.execute("SELECT question_text FROM questions").fetchall()
        params = cursor.execute("SELECT parameters FROM questions").fetchall()

        for i in range(0,len(rows)):

            res = list(eval(params[i][0]))    #Converts the parameters into a list of dictionaries (JSON objects)
            if len(res)>0:                #If paramaters are available
                paramChosen.append(random.choice(res))    #Appends a randomly chosen parameter to the global paramChosen list
                temp = Template(rows[i][0])               #Creates a template using jinja2. rows[0][0] is assumed to have placeholders for the parameters
                f.write("\n%d. %s \n" %(j,temp.render(paramChosen[-1])))    #Replaces the placeholders with paramater values and writes into file

            else:          #If there are no parameters available
                f.write("\n%d. %s \n" %(j,rows[i][0]))
            j+=1

    else:

        for i in range(1, numArgs):

            if sys.argv[i] in ("-s", "--Solutions"):
                continue

            qNum = int(sys.argv[i])               #The question number passed in the arguments
            rows = cursor.execute("SELECT question_text FROM questions WHERE qno = ?", (qNum,),).fetchall()
            params = cursor.execute("SELECT parameters FROM questions WHERE qno = ?", (qNum,),).fetchall()
            res = list(eval(params[0][0]))    #Converts the parameters into a list of dictionaries (JSON objects)

            if len(res)>0:                #If paramaters are available
                paramChosen.append(random.choice(res))    #Appends a randomly chosen parameter to the global paramChosen list
                temp = Template(rows[0][0])               #Creates a template using jinja2. rows[0][0] has placeholders for the parameters
                f.write("\n%d. %s \n" %(j,temp.render(paramChosen[-1])))    #Replaces the placeholders with paramater values and writes into file

            else:          #If there are no parameters available
                f.write("\n%d. %s \n" %(j,rows[0][0]))

            j+=1

    f.close()

def genSolutions(numArgs):
    '''
    Generates a markdown file (solutions.md) containing Solutions
    '''
    global paramChosen
    global paramIndex
    j=1
    f = open("solutions.md","w")       #Opens the markdown file where we have to creat the solutions
    f.write("--- \n title: Solutions \n---\n") #Basic Formatting

    if numArgs==1 or numArgs==2:  #If no arguments are specified or only '-s' is specified
        rows = cursor.execute("SELECT answers FROM questions").fetchall()
        params = cursor.execute("SELECT parameters FROM questions").fetchall()

        for i in range(0,len(rows)):
            res = list(eval(params[i][0]))    #Converts the parameters into a list of dictionaries (JSON objects)

            if len(res)>0:    #If paramaters are available

                if rows[i][0]:    #If the answers field in the table is not NULL
                    temp = Template(rows[i][0])    #Creates a template using jinja2. rows[i][0] is assumed to have placeholders for the parameters
                    f.write("\n%d. %s \n" %(j,temp.render(paramChosen[paramIndex])))    #Replaces the placeholders with paramater values and writes into file

                else:     #If the answers field in the table is NULL
                    f.write("\n%d. %s \n" %(j,"Solution Not Available"))
                paramIndex+=1

            else:    #If paramaters are not available

                if rows[i][0]:
                    f.write("\n%d. %s \n" %(j,rows[i][0]))

                else:
                    f.write("\n%d. %s \n" %(j,"Solution Not Available"))
            j+=1

    else:

        for i in range(2, numArgs):
            qNum = int(sys.argv[i])               #The question number passed in the arguments
            rows = cursor.execute("SELECT answers FROM questions WHERE qno = ?", (qNum,),).fetchall()
            params = cursor.execute("SELECT parameters FROM questions WHERE qno = ?", (qNum,),).fetchall()
            res = list(eval(params[0][0]))    #Converts the parameters into a list of dictionaries (JSON objects)

            if len(res)>0:    #If paramaters are available

                if rows[0][0]:    #If the answers field in the table is not NULL
                    temp = Template(rows[0][0])    #Creates a template using jinja2. rows[0][0] is assumed to have placeholders for the parameters
                    f.write("\n%d. %s \n" %(j,temp.render(paramChosen[paramIndex])))    #Replaces the placeholders with paramater values and writes into file

                else:     #If the answers field in the table is NULL
                    f.write("\n%d. %s \n" %(j,"Solution Not Available"))
                paramIndex+=1

            else:    #If paramaters are not available

                if rows[0][0]:
                    f.write("\n%d. %s \n" %(j,rows[0][0]))

                else:
                    f.write("\n%d. %s \n" %(j,"Solution Not Available"))
            j+=1

    f.close()


n = len(sys.argv)                  #Number of arguments passed (the first argument is always the name of this python file)
genQP(n)

if (n == 1) or (sys.argv[1] in ("-s", "--Solutions")):
    genSolutions(n)
