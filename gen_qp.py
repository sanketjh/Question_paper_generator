import sys  #Needed to read arguments from the command line
import sqlite3  #Needed to read data from the database
from datetime import date  #Needed to add today's date in the Question Paper


today = date.today()
d1 = today.strftime("%B %d, %Y")   #Date in "Month date, year" format
n = len(sys.argv)                  #Number of arguments passed
f = open("questions.md","w")       #Opens the markdown file where we have to creat the question paper
f.write("--- \n title: Question Paper \n author: Roll No.- \n date: %s \n--- \n \n# Questions \n" % d1) #Basic Formatting

conn = sqlite3.connect('questions.db')   #Opens connection to the database
cursor = conn.cursor()                   #To read data from the table

#Database: questions.db
#Table: questions

for i in range(1, n):
  qNum = int(sys.argv[i])               #The question number passed in the arguments
  rows = cursor.execute("SELECT question_text FROM questions WHERE qno = ?", (qNum,),).fetchall()
  f.write("\n%d. %s \n" %(i,rows[0][0]))

f.close()
