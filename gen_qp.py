'''
This program accepts the question numbers corresponding to the questions table in questions.db
database as arguments. Also, it accepts an optional argument, which is "-s" or "--Solutions".
If this argument is passed, the solutions are also made in a markdown file.
If no argument or only '-s' (or '--Solutions') is passed, both the question paper and solutions are made.
'''

import sys  #Needed to read arguments from the command line
import sqlite3  #Needed to read data from the database
from datetime import date  #Needed to add today's date in the Question Paper


today = date.today()
d1 = today.strftime("%B %d, %Y")   #Date in "Month date, year" format

conn = sqlite3.connect('questions.db')   #Opens connection to the database
cursor = conn.cursor()                   #To read data from the table

#Database: questions.db
#Table: questions (columns: qno, question_text, answers)

def genQP(numArgs):
    '''
    Generates a markdown file (questions.md) containing the Question Paper
    '''
    j=1
    f = open("questions.md","w")       #Opens the markdown file where we have to creat the question paper
    f.write("--- \n title: Question Paper \n author: Roll No.- \n date: %s \n--- \n \n# Questions \n" % d1) #Basic Formatting
    if numArgs==1 or (numArgs==2 and sys.argv[1] in ("-s", "--Solutions")):  #If no arguments are specified or only '-s' is specified
        rows = cursor.execute("SELECT question_text FROM questions").fetchall()
        for i in range(0,len(rows)):
            f.write("\n%d. %s \n" %(j,rows[i][0]))
            j+=1

    else:
        for i in range(1, numArgs):
            if sys.argv[i] in ("-s", "--Solutions"):
                continue
            qNum = int(sys.argv[i])               #The question number passed in the arguments
            rows = cursor.execute("SELECT question_text FROM questions WHERE qno = ?", (qNum,),).fetchall()
            f.write("\n%d. %s \n" %(j,rows[0][0]))
            j+=1

    f.close()

def genSolutions(numArgs):
    '''
    Generates a markdown file (solutions.md) containing Solutions
    '''
    j=1
    f = open("solutions.md","w")       #Opens the markdown file where we have to creat the solutions
    f.write("--- \n title: Solutions \n---\n") #Basic Formatting
    if numArgs==1 or numArgs==2:  #If no arguments are specified or only '-s' is specified
        rows = cursor.execute("SELECT answers FROM questions").fetchall()
        for i in range(0,len(rows)):
            f.write("\n%d. %s \n" %(j,rows[i][0]))
            j+=1

    else:
        for i in range(2, numArgs):
            qNum = int(sys.argv[i])               #The question number passed in the arguments
            rows = cursor.execute("SELECT answers FROM questions WHERE qno = ?", (qNum,),).fetchall()
            f.write("\n%d. %s \n" %(j,rows[0][0]))
            j+=1

    f.close()


n = len(sys.argv)                  #Number of arguments passed (the first argument is always the name of this python file)
genQP(n)
if (n == 1) or (sys.argv[1] in ("-s", "--Solutions")):
    genSolutions(n)
