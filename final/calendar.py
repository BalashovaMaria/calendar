from tkinter import *
import calendar
import datetime
import tkinter as tk
import database
root = tk.Tk()
root.title('Medication calendar')
photo = tk.PhotoImage(file ='pill.png')
root.iconphoto(False, photo)
days = []
now = datetime.datetime.now()
year = now.year
month = now.month
count = 2
myBase = database.BaseHandler('records.db')
day = -1

# Функции для создания календаря в главном окне
def prew():
    # Создание кнопки для переключения на предыдущий месяц
    global month, year
    month -= 1
    if month == 0:
        month = 12
        year -= 1
    fill()

def next():
    # Создание кнопки для переключения на следующий месяц
    global month, year
    month += 1
    if month == 13:
        month = 1
        year += 1
    fill()
    
def fill():
    # Перерисовывает календарь. Она будет вызываться в начале работы программы и каждый раз после изменения месяца, для которого нужно вывести календарь
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
        days[n + week_day].bind(f'<Button-1>', new_win)
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
        
def new_win(event):
    # Появление дочернего окна после нажатия на календаре даты
    newWindow = tk.Toplevel(root)
    newWindow.title('Medication Data')
    newWindow.iconphoto(False, photo)
    newWindow.geometry(f"300x400")
    interface(newWindow, int(event.widget.cget('text')))

def interface(y, day):
    # Интерфейс дочернего окна
    global count
    count = 2
    addmed = tk.Button(y, text = 'Add medication', command= lambda: [addmd(), counter()])
    addmed.grid(row=0, column=4)
    savebuttn = tk.Button(y, text = 'Save', command=lambda: add_r())
    savebuttn.grid(row=1, column=4)
    date = f"{day}:{month}:{year}"
    data = myBase.find(date)
    name = []
    dosage = []
    t = []

    def add_r():
        # Добавление введенных пользователем данных в базу данных
        myBase.delete(date)
        for i in range(len(name)):
            myBase.add_record(name[i].get(), dosage[i].get(), [t[i].get()], date)

    def namefunc(rw1):
        # Функция для добавления лейбла 'Name' и строки ввода для 'Name'
        pill_name = tk.Label(y, text='Name')
        pill_name.grid(row =rw1,column=0)
        tt = StringVar()
        name.append(tt)
        pillname = tk.Entry(y, textvariable=tt)
        pillname.grid(row=rw1, column=1)
        dosagefunc(rw1+1)

    def dosagefunc(rw2):
        # Функция для добавления лейбла 'Dosage' и строки ввода для 'Dosage'
        pill_dosage = tk.Label(y, text='Dosage')
        pill_dosage.grid(row =rw2, column=0)
        tt = StringVar()
        dosage.append(tt)
        pilldosage = tk.Entry(y, textvariable=tt)
        pilldosage.grid(row=rw2, column=1)
        time(rw2+2)

    def time(rw):
        # Функция для добавления лейбла 'Time', строки ввода для 'Time' и флажка, который может находиться в отмеченном и неотмеченном состоянии
        global c
        pill_time = tk.Label(y, text='Time')
        pill_time.grid(row=rw, column=0)
        tt = StringVar()
        t.append(tt)
        pilltime = tk.Entry(y, textvariable=tt)
        pilltime.grid(row=rw, column=1)
        donebutton = Checkbutton(y, command=(lambda: myBase.delete(date, tt.get())))
        donebutton.grid(row=rw, column=2)

    def counter():
        # Функция подсчета нажатий для кнопки, для того, чтобы лейблы со строками ввода распределялись равномерно в дочернем окне
        global count
        count +=2

    def addmd():
        # Функция для работы кнопки 'Add medication'
        namefunc(count-2)
        counter()

    for i in range(len(data)):
        # Добавление введенных данных в базу данных
        addmd()
        counter()
        name[i].set(data[i][0])
        dosage[i].set(data[i][1])
        t[i].set(data[i][2])





prew_button = Button(root, text = '<', command = prew)
prew_button.grid(row=0, column=0, sticky='nsew')
next_button = Button(root, text='>', command=next)
next_button.grid(row=0, column=6, sticky='nsew')
info_label = Label(root, text='0', width=1, height=1,
            font=('ATC Maple', 16, 'bold'), fg='blue')
info_label.grid(row=0, column=1, columnspan=5, sticky='nsew')

# Заполнение календаря в главном окне:
for n in range(7):
    lbl = tk.Label(root, text=calendar.day_abbr[n], width=1, height=1,
                font=('ATC Maple', 10, 'normal'), fg='darkblue')
    lbl.grid(row=1, column=n, sticky='nsew')
for row in range(6):
    for col in range(7):
        lbl = tk.Button(root, text='0', width=4, height=2,
                    font=('ATC Maple', 16, 'bold'))

        lbl.grid(row=row+2, column=col, sticky='nsew')
        days.append(lbl)
fill()
root.mainloop()
