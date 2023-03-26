import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter import messagebox



def populate_table(table):
    # Connect to the SQLite tos
    conn = sqlite3.connect('tos.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS data(id integer, hours real, percentage real, items real)")

    # Retrieve data from the tos
    c.execute('SELECT * FROM data ORDER BY id')
    rows = c.fetchall()

    # Delete existing rows in the table
    for row in table.get_children():
        table.delete(row)

    # Populate the table with the retrieved data
    for row in rows:
        table.insert('', 'end', values=row)

    # Close the tos connection
    conn.close()

def addData():
    # Connect to the SQLite tos
    conn = sqlite3.connect('tos.db')
    c = conn.cursor()
    #check if the id exists
    c.execute("""SELECT id FROM data WHERE id=?""",(lsnumber.get(),))
    result = c.fetchone()
    if result:
        messagebox.showwarning("Warning", "Lesson Number exists Already")
    # Insert data into the tos
    else:
        if hours.get() == 0 and totalItems.get() == 0:
            messagebox.showwarning("Warning", "Lesson Hours cannot be empty!")
        else:

            insertQuery= "INSERT INTO data(id, hours, percentage, items ) VALUES(?,?,?,?)"
            conn.execute(insertQuery,(lsnumber.get(), hours.get(), 0, 0))
            # messagebox.showinfo("Success Operation", "Data Inserted Successfully!")

            # Compute the total hours and items
            c.execute('SELECT SUM(hours), SUM(items) FROM data')
            total_hours,items_per_lesson = c.fetchone()

            # Update the percentage and items per lesson for all rows
            c.execute('SELECT * FROM data ORDER BY id')
            rows = c.fetchall()
            for row in rows:
                lesson_id, lesson_hours, _, _ = row
                percentage = round((lesson_hours / total_hours) * 100, 2)
                # items_per_lesson = round(total_items * (percentage / 100), 2)
                items_per_lesson = round(totalItems.get()*(percentage/100),0)
                c.execute('UPDATE data SET percentage = ?, items = ? WHERE id = ?', (percentage, items_per_lesson, lesson_id))


            
            
    # Commit the changes and close the tos connection
    conn.commit()
    conn.close()
    # Populate the table with the updated data
    populate_table(table)

def delete_data(table, index):
    # Get the selected row from the table
    selected_item = table.selection()[0]
    row = table.item(selected_item)['values']

    # Connect to the SQLite database
    conn = sqlite3.connect('tos.db')
    c = conn.cursor()

    # Delete the row from the database
    c.execute('DELETE FROM data WHERE id = ?', (row[0],))

    # Commit the changes and close the database connection
    conn.commit()
    conn.close()

    # Delete the row from the table
    table.delete(selected_item)

def deleteAll():
    conn = sqlite3.connect('tos.db')
    c = conn.cursor()
    c.execute('DELETE FROM data')
    conn.commit()
    conn.close()
    populate_table(table)

    
# Create a root window
root = Tk()

# Create a frame to hold the table widget and the "Add" button
addForm = ttk.Frame(root, padding=10)
addForm.pack()
frame = ttk.Frame(root, padding = 10)
frame.pack()
bottomFrame = ttk.Frame(root, padding=10)
bottomFrame.pack()


#Variables
lsnumber = IntVar()
hours = DoubleVar()
totalItems = IntVar()

# Create an "Add" button
lblLessonNum = Label(addForm, text = "Lesson Number").grid(column=0, row=0)
entLessonNum = Entry(addForm, width = 30,textvariable = lsnumber, relief = GROOVE, border = 1).grid(column=1, row=0, pady=5)
lblLessonHours = Label(addForm, text = "Lesson Number").grid(column=0, row=1)
entLessonHours = Entry(addForm, width = 30,textvariable = hours, relief = GROOVE, border = 1).grid(column=1, row=1, pady = 5)


entTotalItems = Entry(addForm, width = 30,textvariable = totalItems, relief = GROOVE, border = 1).grid(column=1, row=3, pady=5)
lblTotalItems = Label(addForm, text="Number of Items").grid(column = 0, row = 3)

btnAdd = Button(addForm, text="Add Data", command=addData).grid(column=0, row=4)
btnQuit = Button(addForm, text="Quit", command=root.destroy).grid(column=1, row=4)

# Create a table widget
table = ttk.Treeview(frame, columns=('colLessonNo', 'colHours', 'colPercentage', 'colItems'), show='headings')
table.heading('colLessonNo', text='Number of Lessons')
table.heading('colHours', text='Hours Spent')
table.heading('colPercentage', text='Percentage (%)')
table.heading('colItems', text='Items Per Lesson')
table.pack()

# Populate the table with data from the tos
populate_table(table)

#Delete All Button
btnDeleteAll = Button(bottomFrame, text = "Empty Table", command = deleteAll)
btnDeleteAll.grid(column=0, row = 0)



# Start the event loop
root.title("TOS Calculator Developed By Jhunel B Penaflorida")
root.mainloop()
