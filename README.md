# Question_paper_generator
A GUI application which generates a question paper and corresponding solutions from an SQLite database.

## Instructions for use:
- Upon opening the application, the first screen which will appear is shown below

![Start up screen](https://github.com/sjshetti/Question_paper_generator/blob/main/startUp.jpg?raw=true)

- The user can either open an existing database or open a new one
- If the user opens a new database, the following window appears. Upon opening an existing database, the cells will be filled with different values.

![Main Window](https://github.com/sjshetti/Question_paper_generator/blob/main/new.jpg?raw=true)

- The user can fill values for different columns like qno (Question Number), question_text (The actual question. Can put {{ paramName }} wherever the user wishes for variable parameters to appear in the question. paramName can be any valid identifier), answers (solution to the question), parameters (a JSON array containing paramaters for use in making the question) and marks (marks alloted to that particular question)
- The user can add or delete rows using the buttons in the bottom
- If user clicks on File > Open and opens an existing database, it will be displayed as shown below

![Open an existing database](https://github.com/sjshetti/Question_paper_generator/blob/main/open.jpg?raw=true)

- The user can also opt for other functions like Save, Save As, Exit and New whose functions are obvious. One can also access short Instructions from the Help menu.

- To generate the question paper and its solutions, one has to click on Generate at the bottom. Upon clicking it, the following window will be rendered

![Generate Documents](https://github.com/sjshetti/Question_paper_generator/blob/main/generate.jpg?raw=true)

- The user now has to select the questions which they want to include in the question paper. The user also has the option to randomize the order of the questions.

- Upon selecting the questions, the user is greeted by the following window

![Preview Markdown](https://github.com/sjshetti/Question_paper_generator/blob/main/preview.jpg?raw=true)

- Here, the user can edit the question paper and solutions (in Markdown) and also preview them by clicking on the rescpective preview buttons. An example of a preview is shown below

![Example Question Paper Preview](https://github.com/sjshetti/Question_paper_generator/blob/main/previewEx.jpg?raw=true)

- When the user is done editing, they can click on Done and select the format of the output in the following window

![Choose Output Format](https://github.com/sjshetti/Question_paper_generator/blob/main/opFormat.jpg?raw=true)

- Upon choosing the formats, click on Okay and choose the destination for the zip file containing output. Then, read the content on the popup and click OK and wait till a zip file is created. The user has to make sure that they don't click anything while the zip file is being made otherwise the program may crash.

![Warning](https://github.com/sjshetti/Question_paper_generator/blob/main/warning.jpg?raw=true)

- Once the zip file has been created, the main (table) window will reappear.
