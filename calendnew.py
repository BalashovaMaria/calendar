from tkinter import *
import calendar
import datetime
import tkinter as tk
root = tk.Tk()
root.title('Medication calendar')
days = []
now = datetime.datetime.now()
year = now.year
month = now.month
count = 2
def prew():
    global month, year
    month -= 1
    if month == 0:
        month = 12
        year -= 1
    fill()

def next():
    global month, year
    month += 1
    if month == 13:
        month = 1
        year += 1
    fill()
    
def fill():
    ''',,заполнение,, создание календаря'''
    info_label['text'] = calendar.month_name[month] + ', ' + str(year)
    month_days = calendar.monthrange(year, month)[1]
    if month == 1:
        prew_month_days = calendar.monthrange(year-1, 12)[1]
    else:
        prew_month_days = calendar.monthrange(year, month - 1)[1]
    week_day = calendar.monthrange(year, month)[0]
    for n in range(month_days):
        days[n + week_day]['text'] = n+1
        days[n + week_day]['fg'] = 'black'
        if year == now.year and month == now.month and n == now.day:
            days[n + week_day]['background'] = 'darkturquoise'
        else:
            days[n + week_day]['background'] = 'lightgray'
    for n in range(week_day):
        days[week_day - n - 1]['text'] = prew_month_days - n
        days[week_day - n - 1]['fg'] = 'gray'
        days[week_day - n - 1]['background'] = '#f3f3f3'
    for n in range(6*7 - month_days - week_day):
        days[week_day + month_days + n]['text'] = n+1
        days[week_day + month_days + n]['fg'] = 'gray'
        days[week_day + month_days + n]['background'] = '#f3f3f3'

def new_win():
    '''добавление нового окна после нажимания на дату'''   
    newWindow = tk.Toplevel(root)
    newWindow.title('Medication Data')
    newWindow.geometry(f"300x400")
    interface(newWindow)
    
def interface(y):
    '''ячейки в новом окне'''
    addmed = tk.Button(y, text = 'Add medication', command= lambda: [addmd(), counter()])
    addmed.grid(row=0, column=4)
    def namefunc(rw1):
    '''название лекарства'''
        pill_name = tk.Label(y, text='Name')
        pill_name.grid(row =rw1,column=0)
        pillname = tk.Entry(y)
        pillname.grid(row=rw1, column=1)
        dosagefunc(rw1+1)

    def dosagefunc(rw2):
    '''дозировка'''
        pill_dosage = tk.Label(y, text='Dosage')
        pill_dosage.grid(row =rw2, column=0)
        pilldosage = tk.Entry(y)
        pilldosage.grid(row=rw2, column=1)
        time(rw2+2)

    def time(rw):
    '''время принятия лекарств'''
        pill_time = tk.Label(y, text='Time')
        pill_time.grid(row=rw, column=0)
        pilltime = tk.Entry(y)
        pilltime.grid(row=rw, column=1)
        donebutton = Checkbutton(y)
        donebutton.grid(row=rw, column=2)
        plus = tk.Button(y, text='+', command=lambda: [plsfunction(), counter()])
        plus.grid(row=rw, column=3)

    def counter():
        global count
        count +=2

    def plsfunction():
        time(count)

    def addmd():
        namefunc(count)
        counter()


    namefunc(0)
prew_button = Button(root, text = '<', command = prew)
prew_button.grid(row=0, column=0, sticky='nsew')
next_button = Button(root, text='>', command=next)
next_button.grid(row=0, column=6, sticky='nsew')
info_label = Label(root, text='0', width=1, height=1,
            font=('ATC Maple', 16, 'bold'), fg='blue')
info_label.grid(row=0, column=1, columnspan=5, sticky='nsew')
for n in range(7):
    lbl = tk.Label(root, text=calendar.day_abbr[n], width=1, height=1,
                font=('ATC Maple', 10, 'normal'), fg='darkblue')
    lbl.grid(row=1, column=n, sticky='nsew')
for row in range(6):
    for col in range(7):
        lbl = tk.Button(root, text='0', width=4, height=2,
                    font=('ATC Maple', 16, 'bold'),
                        command = new_win)
        lbl.grid(row=row+2, column=col, sticky='nsew')
        days.append(lbl)
fill()
root.mainloop()
