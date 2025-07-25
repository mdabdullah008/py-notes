from datetime import datetime
import sqlite3
from tkinter import *

root = Tk()
root.geometry('320x600')
root.title('Notes')

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

def noteedit():
    global editor
    global txttitle_edit
    global txtnote_edit
    editor = Tk()
    editor.geometry('320x400')
    editor.title('Edit Note')

    lblspace_edit01 = Label(editor)
    lblspace_edit01.grid(row=0, column=0)

    lbltitle_edit = Label(editor, text='Title:')
    lbltitle_edit.grid(row=11, column=0)
    txttitle_edit = Entry(editor, width = 30)
    txttitle_edit.grid(row=11, column=1)

    lblspace03_edit = Label(editor)
    lblspace03_edit.grid(row=12, column=0)

    lblnote_edit = Label(editor, text='Note:')
    lblnote_edit.grid(row=13, column=0)
    txtnote_edit = Text(editor, height=10, width=30)
    txtnote_edit.grid(row=13, column=1)

    lblspace04_edit = Label(editor)
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

def noteupdate():
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

def destroy():
    editor.destroy()

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

def notedelete():
    con = sqlite3.connect('notes.db')
    cursor = con.cursor()
    cursor.execute("DELETE FROM Notes WHERE No=" + txtno.get())
    con.commit()
    print('Note Deleted Successfully!')
    txtno.delete(0, END)
    con.close()
    noteshow()

lblspace01 = Label(root)
lblspace01.grid(row=0, column=0)

lbltitle = Label(root, text='Title:')
lbltitle.grid(row=11, column=0)
txttitle = Entry(root, width = 30)
txttitle.grid(row=11, column=1)

lblspace03 = Label(root)
lblspace03.grid(row=12, column=0)

lblnote = Label(root, text='Note:')
lblnote.grid(row=13, column=0)
txtnote = Text(root, height=10, width=30)
txtnote.grid(row=13, column=1)

lblspace04 = Label(root)
lblspace04.grid(row=14, column=0)

lblno = Label(root, text='No:')
lblno.grid(row=15, column=0)
txtno = Entry(root, width = 30)
txtno.grid(row=15, column=1)

lblspace05 = Label(root)
lblspace05.grid(row=16, column=0)

btnSave = Button(root, text='Save', command=notesave)
btnSave.grid(row=17, column=0)

btnEdit = Button(root, text='Edit/View', command=noteedit)
btnEdit.grid(row=17, column=1)

btnShow = Button(root, text='Show', command=noteshow)
btnShow.grid(row=18, column=0)

btnDelete = Button(root, text='Delete', command = notedelete)
btnDelete.grid(row=18, column=1)

lblspace04 = Label(root)
lblspace04.grid(row=19, column=0)

lblrecordtable= Label(text='No.                    Title                    Date')
lblrecordtable.grid(row=20, column=0, columnspan=2)

root.mainloop()