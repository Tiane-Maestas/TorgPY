import tkinter as tk
from tkinter import *
from Events import *
import datetime

darkgray = '#1B1D1F'
offwhite = '#AEBFC7'
lightergray = '#333739'

class Frame():
    screenwidth = 1920
    screenheight = 1080
    allFramesInUse = []
    def __init__(self, window):
        #creates a frame object in the 'window'
        self.frame = tk.Frame(window, bg='black')
        #initializes grid placements of title and arrow buttons
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=64)
        self.frame.columnconfigure(2, weight=1)
        self.frame.rowconfigure(0, weight=1)
        #creates title
        self.title = tk.Label(self.frame, text='Title', bg='#0C273F', font=('Arial', 22), fg=offwhite)
        #creates buttons
        self.decrementBtn = tk.Button(self.frame, text='<',command=lambda:self.decrementPressed(),bg='#02427A', relief='groove', activebackground='orange', fg=offwhite)
        self.incrementBtn = tk.Button(self.frame, text='>',command=lambda:self.incrementPressed(),bg='#02427A', relief='groove', activebackground='orange', fg=offwhite)

    def place(self):
        #placing frame in window
        self.frame.grid(row=0,column=0,sticky='nsew')
        #placing title
        self.title.grid(column=1, row=0, sticky='nsew')
        #placing buttons
        self.decrementBtn.grid(column=0, row=0, sticky='nsew')
        self.incrementBtn.grid(column=2, row=0, sticky='nsew')

    def getFrame(self):
        return self.frame

    def setAllFrames(self, frames):
        Frame.allFramesInUse = frames

    def decrementPressed(self):
        pass

    def incrementPressed(self):
        pass



class TimeFrame(Frame):
    labelHeight = 32
    timelabelX = 0
    timelabelWidth = 64
    timesInADay = ['1:00AM','1:30AM','2:00AM','2:30AM','3:00AM','3:30AM','4:00AM','4:30AM',
                   '5:00AM','5:30AM','6:00AM','6:30AM','7:00AM','7:30AM','8:00AM','8:30AM',
                   '9:00AM','9:30AM','10:00AM','10:30AM','11:00AM','11:30AM','12:00PM','12:30PM',
                   '1:00PM','1:30PM','2:00PM','2:30PM','3:00PM','3:30PM','4:00PM','4:30PM',
                   '5:00PM','5:30PM','6:00PM','6:30PM','7:00PM','7:30PM','8:00PM','8:30PM',
                   '9:00PM','9:30PM','10:00PM','10:30PM','11:00PM','11:30PM','12:00AM','12:30AM']
    def __init__(self, window):
        Frame.__init__(self, window)
        #configures grid placements of time and scrollbar
        self.frame.rowconfigure(1, weight=64)
        #initializes time and event canvas
        self.timeEventCanvas = Canvas(self.frame, bg='black', highlightthickness=0)
        #initializes a scroll bar and configures canvas
        self.scrollbar = Scrollbar(self.frame, orient=VERTICAL, bg='#02427A', command=self.timeEventCanvas.yview)
        self.timeEventCanvas.configure(yscrollcommand=self.scrollbar.set)
        self.timeEventCanvas.bind('<Configure>', lambda e: self.timeEventCanvas.configure(scrollregion = self.timeEventCanvas.bbox('all')))
        #initializes a working canvas to enable proper use of scrollbar through a canvas window in the timeEventCanvas
        #this uses a canva packed into a frame within the timeEventCanvas window
        self.workingFrame = tk.Frame(self.timeEventCanvas, bg='black')
        self.timeEventCanvas.create_window((0,0), window=self.workingFrame, anchor='nw')
        self.workingCanvas = Canvas(self.workingFrame, height=Frame.screenheight*2, width=Frame.screenwidth, bg='black', highlightthickness=0)
        self.workingCanvas.pack()
        #initializes all time labels in an array
        self.timeLabels = []
        self.createTimeLabels()
        #using screen resolution creates label dimensions
        TimeFrame.labelHeight = (2*Frame.screenheight)/len(self.timeLabels)

    def place(self):
        Frame.place(self)
        #places time and event canvas
        self.timeEventCanvas.grid(row=1, column=0, sticky='nsew', columnspan=2)
        #places a scroll bar
        self.scrollbar.grid(row=1, column=2, sticky='nsew')
        #place time labels in working frame
        self.placeTimeLabels()

    def createTimeLabels(self):
        for time in TimeFrame.timesInADay:
            #adds the time label to the canvas in order to use the place command
            self.timeLabels.append(Label(self.workingCanvas, text=time, relief='flat', bg='#02427A', fg=offwhite))

    def placeTimeLabels(self):
        currentY = 0
        for label in self.timeLabels:
            label.place(x=TimeFrame.timelabelX, y=currentY, width=TimeFrame.timelabelWidth, height=TimeFrame.labelHeight)
            currentY+=TimeFrame.labelHeight



class DayFrame(TimeFrame):
    eventlabelX = TimeFrame.timelabelWidth
    eventlabelWidth = Frame.screenwidth - TimeFrame.timelabelWidth
    def __init__(self, window):
        TimeFrame.__init__(self, window)
        #creates and intializes empty events for every time slot
        #the first label corrseponds to first time slot
        self.eventLabels = []
        self.createEventSlots()
        #keeps track of a workingDate and today's date
        today = datetime.date.today()
        self.workingDate = self.formatDate(today)
        self.todaysDate = self.workingDate
        self.changeTitle(self.workingDate)

    def place(self):
        TimeFrame.place(self)
        self.displayEventSlots()

    def createEventSlots(self):
        for i in range(len(self.timeLabels)):
            self.eventLabels.append(Label(self.workingCanvas, text='', anchor='w', relief='flat', bg=darkgray, fg=offwhite, font=('Arial',12)))
            self.eventLabels[i].bind('<Enter>', self.entered)
            self.eventLabels[i].bind('<Leave>', self.exit)
            self.eventLabels[i].bind('<Button-1>', self.clicked)

    def entered(self, event):
        event.widget['bg'] = 'orange'

    def exit(self, event):
        event.widget['bg'] = darkgray
        #puts back events to their color and not darkgray
        self.changeWorkingDay(self.workingDate)

    def clicked(self, event):
        Frame.allFramesInUse[3].getFrame().tkraise()
        index = self.eventLabels.index(event.widget)
        time = TimeFrame.timesInADay[index]
        Frame.allFramesInUse[3].setFrame(self.workingDate, time)

    def displayEventSlots(self):
        currentY = 0
        for label in self.eventLabels:
            label.place(x=DayFrame.eventlabelX, y=currentY, width=DayFrame.eventlabelWidth, height=TimeFrame.labelHeight)
            currentY+=TimeFrame.labelHeight

    def updateEventSlots(self, dayEvent):
        self.clearAllSlots()
        for event in dayEvent.eventlist:
            slotindex = TimeFrame.timesInADay.index(event.startTime)
            endindex = TimeFrame.timesInADay.index(event.endTime)
            self.eventLabels[slotindex]['text'] = event
            while slotindex < endindex:
                self.eventLabels[slotindex]['bg'] = event.color
                slotindex += 1

    def clearAllSlots(self):
        for label in self.eventLabels:
            label['text'] = ''
            label['bg'] = darkgray

    def changeWorkingDay(self, date):
        self.workingDate = date
        self.changeTitle(self.workingDate)
        try:
	        day = DayEvent.allDayEvents[date]
        except KeyError:
            self.clearAllSlots()
            return
        self.updateEventSlots(day)

    #needs more cases for between months and years
    def changeTitle(self, date):
        dd = int(self.todaysDate[3:5])
        mm = int(self.todaysDate[0:2])
        yyyy = int(self.todaysDate[6:len(self.todaysDate)])
        minusDay = self.formatDate(datetime.datetime(yyyy, mm, dd) - datetime.timedelta(days=1))
        plusDay = self.formatDate(datetime.datetime(yyyy, mm, dd) + datetime.timedelta(days=1))
        if self.todaysDate == date:
            self.title['text'] = "Today: " + date
        elif minusDay == date:
            self.title['text'] = "Yesturday: " + date
        elif plusDay == date:
            self.title['text'] = "Tomorrow: " + date
        else:
            self.title['text'] = getDayOfTheWeek(date) + ": " + date

    def formatDate(self, date):
        dd = str(date.day)
        mm = str(date.month)
        yyyy = str(date.year)
        if date.day < 10:
            dd = '0' + dd
        if date.month < 10:
            mm = '0' + mm
        return mm + '/' + dd + '/' + yyyy

    def decrementPressed(self):
        dd = int(self.workingDate[3:5])
        mm = int(self.workingDate[0:2])
        yyyy = int(self.workingDate[6:len(self.workingDate)])
        minusDay = datetime.datetime(yyyy, mm, dd) - datetime.timedelta(days=1)
        self.changeWorkingDay(self.formatDate(minusDay))

    def incrementPressed(self):
        dd = int(self.workingDate[3:5])
        mm = int(self.workingDate[0:2])
        yyyy = int(self.workingDate[6:len(self.workingDate)])
        plusDay = datetime.datetime(yyyy, mm, dd) + datetime.timedelta(days=1)
        self.changeWorkingDay(self.formatDate(plusDay))



class CreateFrame(Frame):
    possibleDays = ['01','02','03','04','05','06','07','08','09','10',
                    '11','12','13','14','15','16','17','18','19','20',
                    '21','22','23','24','25','26','27','28','29','30',
                    '31']
    possibleMonths = ['January','February','March','April','May','June',
                      'July','August','September','October','November','December']
    monthsInNum = ['01','02','03','04','05','06','07','08','09','10','11','12']
    possibleYears = ['2021','2022','2023','2024','2025','2026','2027','2028','2029',
                     '2030','2031']
    possibleRepeats = ['Yearly','Weekly','Every 10 Weeks'] #eventually add every 'n' weeks through options
    possibleReminders = ['1 Week Before', '3 Days Before', '1 Day Before', 'The Day Of']
    possibleColors = ['pink','black','red','green','blue','purple','darkgreen','magenta']
    def __init__(self, window):
        Frame.__init__(self, window)
        #configures grid placements of allwidgets
        self.frame.rowconfigure(1, weight=64)
        #initializes a working canvas
        self.workingCanvas = Canvas(self.frame, bg=darkgray, highlightthickness=0)
        #creates sidebars
        self.sidebar1 = Label(self.frame, text='', bg='#02427A', relief='raised')
        self.sidebar2 = Label(self.frame, text='', bg='#02427A', relief='raised')

    def place(self):
        Frame.place(self)
        #placing sidebars
        self.sidebar1.grid(column=0, row=1, sticky='nsew')
        self.sidebar2.grid(column=2, row=1, sticky='nsew')
        #places working canvas
        self.workingCanvas.grid(column=1, row=1, sticky='nsew')



class CreateSingleEventFrame(CreateFrame):
    def __init__(self, window):
        CreateFrame.__init__(self, window)
        #changes title
        self.title['text'] = 'Create Event'
        #creates title label and entry box
        self.promptTitle = Label(self.workingCanvas, text='Enter Title:', bg='#02427A', relief='flat', fg=offwhite, font=('Arial',14))
        self.titleEntry = tk.Entry(self.workingCanvas, width=32, font=('Arial',14))
        #creates date label and selection boxes
        self.promptDate = Label(self.workingCanvas, text='Enter Date:', bg='#02427A', relief='flat', fg=offwhite, font=('Arial',14))
        self.dd = StringVar()
        self.dd.set('dd')
        self.dayOptions = OptionMenu(self.workingCanvas, self.dd, *CreateFrame.possibleDays)
        self.mm = StringVar()
        self.mm.set('mm')
        self.monthOptions = OptionMenu(self.workingCanvas, self.mm, *CreateFrame.possibleMonths)
        self.yyyy = StringVar()
        self.yyyy.set('yyyy')
        self.yearOptions = OptionMenu(self.workingCanvas, self.yyyy, *CreateFrame.possibleYears)
        #creates start and end time label and selection boxes
        self.promptStart = Label(self.workingCanvas, text='Enter Start Time:', bg='#02427A', relief='flat', fg=offwhite, font=('Arial',14))
        self.start = StringVar()
        self.start.set('start')
        self.startOptions = OptionMenu(self.workingCanvas, self.start, *TimeFrame.timesInADay)
        self.promptEnd = Label(self.workingCanvas, text='Enter End Time:', bg='#02427A', relief='flat', fg=offwhite, font=('Arial',14))
        self.end = StringVar()
        self.end.set('end')
        self.endOptions = OptionMenu(self.workingCanvas, self.end, *TimeFrame.timesInADay)
        #creates note label and entry box
        self.promptNote = Label(self.workingCanvas, text='Notes:', bg='#02427A', relief='flat', fg=offwhite, font=('Arial',14))
        self.noteBox = Text(self.workingCanvas, width=48, height=5, font=('Arial',14))
        #creates repeat prompt and selection box
        self.promptRepeat = Label(self.workingCanvas, text='Repeat:', bg='#02427A', relief='flat', fg=offwhite, font=('Arial',14))
        self.repeat = StringVar()
        self.repeat.set('repeat')
        self.repeatOptions = OptionMenu(self.workingCanvas, self.repeat, *CreateFrame.possibleRepeats)
        #creates Reminder prompt and selection box
        self.promptReminder = Label(self.workingCanvas, text='Remind Me:', bg='#02427A', relief='flat', fg=offwhite, font=('Arial',14))
        self.reminder = StringVar()
        self.reminder.set('reminder')
        self.reminderOptions = OptionMenu(self.workingCanvas, self.reminder, *CreateFrame.possibleReminders)
        #creates color prompt and selection box
        self.promptColor = Label(self.workingCanvas, text='Color:', bg='#02427A', relief='flat', fg=offwhite, font=('Arial',14))
        self.color = StringVar()
        self.color.set('color')
        self.colorOptions = OptionMenu(self.workingCanvas, self.color, *CreateFrame.possibleColors)
        #creates concrete prompt and check box
        self.promptConcrete = Label(self.workingCanvas, text='Concrete Event:', bg='#02427A', relief='flat', fg=offwhite, font=('Arial',14))
        self.concrete = tk.IntVar()
        self.concreteBut = Checkbutton(self.workingCanvas, variable=self.concrete, text='   ', font=('Arial',10), indicatoron=False, bg=darkgray)
        self.concreteBut.select()
        #creates a button to save information and quit page
        self.saveBut = Button(self.workingCanvas, text='Save and Quit', font=('Arial',14), command=lambda:self.saveandquit())
    
    def place(self):
        CreateFrame.place(self)
        #places title info
        self.promptTitle.place(anchor='n', relx=.5, rely=.015)
        self.titleEntry.place(anchor='n', relx=.5, rely=.08)
        #places date info
        self.promptDate.place(anchor='n', relx=.15, rely=.2)
        self.monthOptions.place(anchor='n', relx=.28, rely=.2)
        self.dayOptions.place(anchor='n', relx=.37, rely=.2)
        self.yearOptions.place(anchor='n', relx=.45, rely=.2)
        #places time info
        self.promptStart.place(anchor='n', relx=.6, rely=.15)
        self.promptEnd.place(anchor='n', relx=.6, rely=.25)
        self.startOptions.place(anchor='n', relx=.75, rely=.15)
        self.endOptions.place(anchor='n', relx=.75, rely=.25)
        #places notes info
        self.promptNote.place(anchor='n', relx=.5, rely=.35)
        self.noteBox.place(anchor='n', relx=.5, rely=.42)
        #places repeat info
        self.promptRepeat.place(anchor='n', relx=.15, rely=.7)
        self.repeatOptions.place(anchor='n', relx=.26, rely=.7)
        #places reminder info
        self.promptReminder.place(anchor='n', relx=.6, rely=.7)
        self.reminderOptions.place(anchor='n', relx=.75, rely=.7)
        #places color info
        self.promptColor.place(anchor='n', relx=.15, rely=.8)
        self.colorOptions.place(anchor='n', relx=.26, rely=.8)
        #places concrete info
        self.promptConcrete.place(anchor='n', relx=.6, rely=.8)
        self.concreteBut.place(anchor='n', relx=.75, rely=.8)
        #places save button
        self.saveBut.place(anchor='n', relx=.5, rely=.9)

    def saveandquit(self):
        #need to check inputs to see if valid
        title = self.titleEntry.get()

        dd = self.dd.get()
        mm = CreateFrame.monthsInNum[CreateFrame.possibleMonths.index(self.mm.get())]
        yyyy = self.yyyy.get()
        date = mm + '/' + dd + '/' + yyyy
        
        startTime = self.start.get()
        endTime = self.end.get()

        notes = self.noteBox.get(1.0, END)

        repeat = self.repeat.get()
        reminder = self.reminder.get()
        color = self.color.get()

        concrete = self.concrete.get()

        #need to check if the event already exists
        event = SingleEvent(title, date, startTime, endTime, notes, repeat, reminder, color, concrete)
        event.save()
        Frame.allFramesInUse[0].getFrame().tkraise()
        #bring up the day that was just added too
        Frame.allFramesInUse[0].changeWorkingDay(date)

    def setFrame(self, date, sTime):
        dd = date[3:5]
        mm = date[0:2]
        index = self.monthsInNum.index(mm)
        mm = self.possibleMonths[index]
        yyyy = date[6:len(date)]
        self.dd.set(dd)
        self.mm.set(mm)
        self.yyyy.set(yyyy)
        self.start.set(sTime)
        self.end.set('end')
        self.repeat.set('repeat')
        self.reminder.set('reminder')
        self.color.set('color')
        self.concreteBut.deselect()
        self.titleEntry.delete(0, END)
        self.noteBox.delete(1.0, END)

    def decrementPressed(self):
        Frame.allFramesInUse[5].getFrame().tkraise()

    def incrementPressed(self):
        Frame.allFramesInUse[4].getFrame().tkraise()



class CreateDayEventFrame(CreateFrame):
    def __init__(self, window):
        CreateFrame.__init__(self, window)
        #changes title
        self.title['text'] = 'Create Day Event'
    
    def place(self):
        CreateFrame.place(self)

    def decrementPressed(self):
        Frame.allFramesInUse[3].getFrame().tkraise()

    def incrementPressed(self):
        Frame.allFramesInUse[5].getFrame().tkraise()



class CreateWeekEventFrame(CreateFrame):
    def __init__(self, window):
        CreateFrame.__init__(self, window)
        #changes title
        self.title['text'] = 'Create Week Event'
    
    def place(self):
        CreateFrame.place(self)

    def decrementPressed(self):
        Frame.allFramesInUse[4].getFrame().tkraise()

    def incrementPressed(self):
        Frame.allFramesInUse[3].getFrame().tkraise()



class WeekFrame(TimeFrame):
    def __init__(self, window):
        TimeFrame.__init__(self, window)

    def place(self):
        TimeFrame.place(self)



class MonthFrame(Frame):
    def __init__(self, window):
        Frame.__init__(self, window)

    def place(self):
        Frame.place(self)