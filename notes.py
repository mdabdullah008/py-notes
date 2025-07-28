# imports the required packages for this code
from datetime import datetime
import sqlite3
from tkinter import *

root = Tk()
root.geometry('320x600') # determining the resolution of the window
root.title('Notes') # title of the window
root.configure(bg='lightgray') # background color for better view
# ----------------------------------------------------------------------------------------------

# every 'lblspaceXX' here indicates a blank space.
lblspace01 = Label(root, bg='lightgray') 
lblspace01.grid(row=0, column=0)

lbltitle = Label(root, text='Title:', bg='lightgray')
lbltitle.grid(row=11, column=0)
txttitle = Entry(root, width = 30)
txttitle.grid(row=11, column=1)

lblspace03 = Label(root, bg='lightgray')
lblspace03.grid(row=12, column=0)

lblnote = Label(root, text='Note:', bg='lightgray')
lblnote.grid(row=13, column=0)
txtnote = Text(root, height=10, width=30)
txtnote.grid(row=13, column=1)

lblspace04 = Label(root, bg='lightgray')
lblspace04.grid(row=14, column=0)

lblno = Label(root, text='No:', bg='lightgray')
lblno.grid(row=15, column=0)
txtno = Entry(root, width = 30)
txtno.grid(row=15, column=1)

lblspace05 = Label(root, bg='lightgray')
lblspace05.grid(row=16, column=0)

# ----------------------------------------------------------------------------------------------
# This helps group related buttons together visually and structurally
button_frame = Frame(root, bg='lightgray')
button_frame.grid(row=18, column=0, columnspan=2, pady=10)
# ----------------------------------------------------------------------------------------------
# button and function for saving note.
def notesave():
    con = sqlite3.connect('notes.db')
    cursor = con.cursor()
    cursor.execute("INSERT INTO Notes ('Title', 'Content', 'Date') VALUES(:title, :content, :date)", 
                    {   
                            'title' : txttitle.get(),
                            'content' : txtnote.get(1.0 , END),
                            'date' : datetime.now().strftime("%d-%m-%Y")
                    })
    con.commit()
    print("Note Saved Successfully!")
    con.close()

    txttitle.delete(0, END)
    txtnote.delete(1.0, END)

btnSave = Button(button_frame, text='Save', command=notesave)
btnSave.grid(row=17, column=0, padx=5)

# ----------------------------------------------------------------------------------------------
# button and popup function for editing note.

# ----------------------------------------------------------------------------------------------
# function for the update and cancel buttons in the edit popup window.
def noteupdate(): # function for the update button
    con = sqlite3.connect('notes.db')
    cursor = con.cursor()
    cursor.execute("""UPDATE Notes SET
                    Title = :title,
                    Content = :content
                    WHERE No= :no""",
                    {
                        'title' : txttitle_edit.get(),
                        'content' : txtnote_edit.get(1.0, END),
                        'no' : txtno.get()
                    }
                    )
    con.commit()
    print('Note Updated Successfully!')
    con.close()

def destroy(): # function for cancel button
    editor.destroy()
# ----------------------------------------------------------------------------------------------

def noteedit(): # creating a popup window for editing and viewing.
    global editor
    global txttitle_edit
    global txtnote_edit
    editor = Tk()
    editor.geometry('320x400')
    editor.title('Edit Note')
    editor.configure(bg='lightgray')

    lblspace_edit01 = Label(editor, bg='lightgray')
    lblspace_edit01.grid(row=0, column=0)

    lbltitle_edit = Label(editor, text='Title:', bg='lightgray')
    lbltitle_edit.grid(row=11, column=0)
    txttitle_edit = Entry(editor, width = 30)
    txttitle_edit.grid(row=11, column=1)

    lblspace03_edit = Label(editor,bg='lightgray')
    lblspace03_edit.grid(row=12, column=0)

    lblnote_edit = Label(editor, text='Note:', bg='lightgray')
    lblnote_edit.grid(row=13, column=0)
    txtnote_edit = Text(editor, height=10, width=30)
    txtnote_edit.grid(row=13, column=1)

    lblspace04_edit = Label(editor, bg='lightgray')
    lblspace04_edit.grid(row=14, column=0)

    con = sqlite3.connect('notes.db')
    cursor = con.cursor()
    cursor.execute("SELECT * FROM Notes WHERE No=" + txtno.get())
    record = cursor.fetchall()
    for data in record:
        txttitle_edit.insert(0, data[1])
        txtnote_edit.insert(1.0, data[2])

    

    btnupdate = Button(editor, text='Update', command=noteupdate)
    btnupdate.grid(row=15, column=1)
    
    btnclose = Button(editor, text='Cancel', command=destroy)
    btnclose.grid(row=16, column=1)

btnEdit = Button(button_frame, text='Edit/View', command=noteedit)
btnEdit.grid(row=17, column=1, padx=5)
# ----------------------------------------------------------------------------------------------

# button and function for showing the entries of saved notes.
def noteshow():
    con = sqlite3.connect('notes.db')
    cursor = con.cursor()
    cursor.execute("SELECT * FROM Notes")
    records = cursor.fetchall()
    print_record = ""
    for record in records:
        print_record += str(record[0]) + "      " + str(record[1]) + "      " + str(record[3]) + "\n"
    
    lblrecordShow = Label(text=print_record)
    lblrecordShow.grid(row = 130, column=0, columnspan=2)

btnShow = Button(button_frame, text='Show', command=noteshow)
btnShow.grid(row=17, column=2, padx=5)

# ----------------------------------------------------------------------------------------------

# button and function for deleting note.
def notedelete():
    con = sqlite3.connect('notes.db')
    cursor = con.cursor()
    cursor.execute("DELETE FROM Notes WHERE No=" + txtno.get())
    con.commit()
    print('Note Deleted Successfully!')
    txtno.delete(0, END)
    con.close()
    noteshow()

btnDelete = Button(button_frame, text='Delete', command = notedelete)
btnDelete.grid(row=17, column=3, padx=5)

# ----------------------------------------------------------------------------------------------

# label for showing the information in the table.
lblrecordtable= Label(text='No.                    Title                    Date', bg='lightgray')
lblrecordtable.grid(row=19, column=0, columnspan=2)

root.mainloop()