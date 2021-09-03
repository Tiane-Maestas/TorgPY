import tkinter as tk
from tkinter import *
from tkinter import messagebox
from Events import *
import datetime
import math

#Colors
LRGRAY = '#333739' 
DGRAY = '#1B1D1F' 
RGRAY = '#10121f'
OFFWHITE = '#AEBFC7'
HIGHLIGHTCOLOR = 'orange'

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
        self.frame.rowconfigure(0, weight=8)
        #creates title
        self.title = tk.Label(self.frame, text='Title', bg=LRGRAY, font=('Arial', 22), fg=OFFWHITE)
        #creates buttons
        self.decrementBtn = tk.Button(self.frame, text='<',command=lambda:self.decrementPressed(),bg=LRGRAY, relief='groove', activebackground=HIGHLIGHTCOLOR, fg=OFFWHITE)
        self.incrementBtn = tk.Button(self.frame, text='>',command=lambda:self.incrementPressed(),bg=LRGRAY, relief='groove', activebackground=HIGHLIGHTCOLOR, fg=OFFWHITE)

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
        #configures grid placements of time and scrollbar and allows room for week view frame configuration
        self.frame.rowconfigure(1, weight=128)
        #initializes time and event canvas
        self.timeEventCanvas = Canvas(self.frame, bg='black', highlightthickness=0)
        #initializes a scroll bar and configures canvas
        self.scrollbar = Scrollbar(self.frame, orient=VERTICAL, bg='black', command=self.timeEventCanvas.yview)
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
        TimeFrame.labelHeight = (2*Frame.screenheight)/(len(self.timeLabels)) #MIGHT NEED TO FIND CLOSEST DIVISIBLE HEIGHT OF LENGTH

    def place(self, startingy):
        Frame.place(self)
        #places time and event canvas
        self.timeEventCanvas.grid(row=1, column=0, sticky='nsew', columnspan=2)
        #places a scroll bar
        self.scrollbar.grid(row=1, column=2, sticky='nsew')
        #place time labels in working frame
        self.placeTimeLabels(startingy)

    def createTimeLabels(self):
        for time in TimeFrame.timesInADay:
            #adds the time label to the canvas in order to use the place command
            self.timeLabels.append(Label(self.workingCanvas, text=time, relief='flat', bg=LRGRAY, fg=OFFWHITE))

    def placeTimeLabels(self, startingy):
        currentY = startingy
        for label in self.timeLabels:
            label.place(x=TimeFrame.timelabelX, y=currentY, width=TimeFrame.timelabelWidth, height=TimeFrame.labelHeight)
            currentY+=TimeFrame.labelHeight



class DayFrame(TimeFrame):
    eventlabelX = TimeFrame.timelabelWidth
    eventlabelWidth = Frame.screenwidth
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
        #param 2 allows room for week day names
        TimeFrame.place(self, 0)
        self.displayEventSlots()

    def createEventSlots(self):
        for i in range(len(self.timeLabels)):
            self.eventLabels.append(Label(self.workingCanvas, text='', anchor='w', relief='flat', bg=DGRAY, fg=OFFWHITE, font=('Arial',12)))
            self.eventLabels[i].bind('<Enter>', self.entered)
            self.eventLabels[i].bind('<Leave>', self.exit)
            self.eventLabels[i].bind('<Button-1>', self.clicked)

    def entered(self, event):
        event.widget['bg'] = HIGHLIGHTCOLOR
        event.widget['fg'] = 'black'

    def exit(self, event):
        event.widget['bg'] = DGRAY
        event.widget['fg'] = OFFWHITE
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
            label['bg'] = DGRAY

    def changeWorkingDay(self, date):
        self.workingDate = date
        self.changeTitle(self.workingDate)
        try:
	        day = DayEvent.allDayEvents[date]
        except KeyError:
            self.clearAllSlots()
            return
        self.updateEventSlots(day)

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
    possibleColors = ['pink','black','red','green','blue','yellow','darkgreen','magenta']
    def __init__(self, window):
        Frame.__init__(self, window)
        #configures grid placements of allwidgets
        self.frame.rowconfigure(1, weight=64)
        #initializes a working canvas
        self.workingCanvas = Canvas(self.frame, bg=DGRAY, highlightthickness=0)
        #creates sidebars
        self.sidebar1 = Label(self.frame, text='', bg=LRGRAY, relief='raised')
        self.sidebar2 = Label(self.frame, text='', bg=LRGRAY, relief='raised')

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
        self.promptTitle = Label(self.workingCanvas, text='Enter Title:', bg=DGRAY, relief='flat', fg=OFFWHITE, font=('Arial',14))
        self.titleEntry = tk.Entry(self.workingCanvas, width=32, font=('Arial',14))
        #creates date label and selection boxes
        self.promptDate = Label(self.workingCanvas, text='Enter Date:', bg=DGRAY, relief='flat', fg=OFFWHITE, font=('Arial',14))
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
        self.promptStart = Label(self.workingCanvas, text='Enter Start Time:', bg=DGRAY, relief='flat', fg=OFFWHITE, font=('Arial',14))
        self.start = StringVar()
        self.start.set('start')
        self.startOptions = OptionMenu(self.workingCanvas, self.start, *TimeFrame.timesInADay)
        self.promptEnd = Label(self.workingCanvas, text='Enter End Time:', bg=DGRAY, relief='flat', fg=OFFWHITE, font=('Arial',14))
        self.end = StringVar()
        self.end.set('end')
        self.endOptions = OptionMenu(self.workingCanvas, self.end, *TimeFrame.timesInADay)
        #creates note label and entry box
        self.promptNote = Label(self.workingCanvas, text='Notes:', bg=DGRAY, relief='flat', fg=OFFWHITE, font=('Arial',14))
        self.noteBox = Text(self.workingCanvas, width=48, height=5, font=('Arial',14))
        #creates repeat prompt and selection box
        self.promptRepeat = Label(self.workingCanvas, text='Repeat:', bg=DGRAY, relief='flat', fg=OFFWHITE, font=('Arial',14))
        self.repeat = StringVar()
        self.repeat.set('repeat')
        self.repeatOptions = OptionMenu(self.workingCanvas, self.repeat, *CreateFrame.possibleRepeats)
        #creates Reminder prompt and selection box
        self.promptReminder = Label(self.workingCanvas, text='Remind Me:', bg=DGRAY, relief='flat', fg=OFFWHITE, font=('Arial',14))
        self.reminder = StringVar()
        self.reminder.set('reminder')
        self.reminderOptions = OptionMenu(self.workingCanvas, self.reminder, *CreateFrame.possibleReminders)
        #creates color prompt and selection box
        self.promptColor = Label(self.workingCanvas, text='Color:', bg=DGRAY, relief='flat', fg=OFFWHITE, font=('Arial',14))
        self.color = StringVar()
        self.color.set('color')
        self.colorOptions = OptionMenu(self.workingCanvas, self.color, *CreateFrame.possibleColors)
        #creates concrete prompt and check box
        self.promptConcrete = Label(self.workingCanvas, text='Concrete Event:', bg=DGRAY, relief='flat', fg=OFFWHITE, font=('Arial',14))
        self.concrete = tk.IntVar()
        self.concreteBut = Checkbutton(self.workingCanvas, variable=self.concrete, text='   ', font=('Arial',10), indicatoron=False, bg=DGRAY)
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
        #handles title inputs
        title = self.titleEntry.get()
        if title == "":
            answer = messagebox.askretrycancel('Incorect Input','No Title! Try Again.')
            if(answer == True):
                return
            else:
                Frame.allFramesInUse[0].getFrame().tkraise()
                return

        #handles date inputs
        dd = self.dd.get()
        mm = self.mm.get()
        yyyy = self.yyyy.get()
        if dd == "dd" or mm == "mm" or yyyy == "yyyy":
            answer = messagebox.askretrycancel('Incorect Input','Missing Date! Try Again.')
            if(answer == True):
                return
            else:
                Frame.allFramesInUse[0].getFrame().tkraise()
                return

        mm = CreateFrame.monthsInNum[CreateFrame.possibleMonths.index(mm)]
        date = mm + '/' + dd + '/' + yyyy
        
        #handles time inputs
        startTime = self.start.get()
        endTime = self.end.get()
        if startTime == "start" or endTime == "end":
            answer = messagebox.askretrycancel('Incorect Input','Missing Time! Try Again.')
            if(answer == True):
                return
            else:
                Frame.allFramesInUse[0].getFrame().tkraise()
                return

        notes = self.noteBox.get(1.0, END)

        repeat = self.repeat.get()
        reminder = self.reminder.get()

        #handles color input
        color = self.color.get()
        if color == "color":
            color = 'purple'

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
        #adds a scroll bar in place of one sidebar
        self.scrollbar = Scrollbar(self.frame, orient=VERTICAL, bg='black', command=self.workingCanvas.yview)
        self.workingCanvas.configure(yscrollcommand=self.scrollbar.set)
        self.workingCanvas.bind('<Configure>', lambda e: self.workingCanvas.configure(scrollregion = self.workingCanvas.bbox('all')))
        #initializes a scrolling canvas to enable proper use of scrollbar through a canvas window in the working canvas
        #this uses a canva packed into a frame within the timeEventCanvas window
        self.workingFrame = tk.Frame(self.workingCanvas, bg='black')
        self.workingCanvas.create_window((0,0),window=self.workingFrame, anchor='nw')
        #self.workingFrame.pack(expand=1) #centers but disables scrollbar
        self.scrollingCanvas = Canvas(self.workingFrame, height=Frame.screenheight*2, bg=DGRAY, highlightthickness=0)
        self.scrollingCanvas.pack(expand=1)
        #creates a frame for each line to allow easy packing
        self.lines = []
        for i in range(len(TimeFrame.timesInADay)+2):
            self.lines.append(tk.Frame(self.scrollingCanvas, bg=DGRAY))
        #first line will select date and how often to repeat the day event
        self.promptDate = Label(self.lines[0], text='Enter Date: ', bg=DGRAY, relief='flat', fg=OFFWHITE, font=('Arial',14))
        self.dd = StringVar()
        self.dd.set('dd')
        self.dayOptions = OptionMenu(self.lines[0], self.dd, *CreateFrame.possibleDays)
        self.mm = StringVar()
        self.mm.set('mm')
        self.monthOptions = OptionMenu(self.lines[0], self.mm, *CreateFrame.possibleMonths)
        self.yyyy = StringVar()
        self.yyyy.set('yyyy')
        self.yearOptions = OptionMenu(self.lines[0], self.yyyy, *CreateFrame.possibleYears)
        self.promptRepeat1 = Label(self.lines[1], text='Repeat this Day Event every ', bg=DGRAY, relief='flat', fg=OFFWHITE, font=('Arial',14))
        self.promptRepeat2 = Label(self.lines[1], text=' days for ', bg=DGRAY, relief='flat', fg=OFFWHITE, font=('Arial',14))
        self.promptRepeat3 = Label(self.lines[1], text=' iterations.', bg=DGRAY, relief='flat', fg=OFFWHITE, font=('Arial',14))
        self.dayRepeat = IntVar()
        self.dayRepeat.set(0)
        self.dayRepeatOptions = OptionMenu(self.lines[1], self.dayRepeat, 0,1,2,3,4,5,6,7)
        self.dayRepeatInterval = IntVar()
        self.dayRepeatInterval.set(0)
        iter = []
        for i in range(52):
            iter.append(i)
        self.dayRepeatIntervalOptions = OptionMenu(self.lines[1], self.dayRepeatInterval, *iter)
        #double array to hold a list of widgets to place on each line
        self.linesInfo = []
        self.endTimes = []
        self.colors = []
        for i in range(len(TimeFrame.timesInADay)+2):
            if i == 0 or i == 1:
                continue
            lineInfo = [] 
            #line start time
            lineInfo.append(Label(self.lines[i], text=TimeFrame.timesInADay[i-2]+': ', bg=DGRAY, relief='flat', fg=OFFWHITE, font=('Arial',14)))
            #line title entry
            lineInfo.append(tk.Entry(self.lines[i], width=32, font=('Arial',14), bg='black'))
            #line end entry
            self.endTimes.append(StringVar())
            self.endTimes[i-2].set('End Time')
            lineInfo.append(OptionMenu(self.lines[i], self.endTimes[i-2], *TimeFrame.timesInADay))
            #line color entry
            self.colors.append(StringVar())
            self.colors[i-2].set('Color')
            lineInfo.append(OptionMenu(self.lines[i], self.colors[i-2], *CreateFrame.possibleColors))
            #adds line of widgets to list of all lines
            self.linesInfo.append(lineInfo)
    
    def place(self):
        CreateFrame.place(self)
        #places the scrollbar in place of sidebar
        self.scrollbar.grid(row=1,column=2,sticky='nsew')
        #paces all line frames
        for line in self.lines:
            line.pack()
        #places first line of options
        self.promptDate.pack(side=LEFT, fill=X)
        self.monthOptions.pack(side=LEFT, fill=X)
        self.dayOptions.pack(side=LEFT, fill=X)
        self.yearOptions.pack(side=LEFT, fill=X)
        self.promptRepeat1.pack(side=LEFT, fill=X)
        self.dayRepeatOptions.pack(side=LEFT, fill=X)
        self.promptRepeat2.pack(side=LEFT, fill=X)
        self.dayRepeatIntervalOptions.pack(side=LEFT, fill=X)
        self.promptRepeat3.pack(side=LEFT, fill=X)
        #places widgets on remaining lines
        for line in self.linesInfo:
            for widgets in line:
                widgets.pack(side=LEFT, fill=X)

    def setFrame(self, date):
        dd = date[3:5]
        mm = date[0:2]
        index = self.monthsInNum.index(mm)
        mm = self.possibleMonths[index]
        yyyy = date[6:len(date)]
        self.dd.set(dd)
        self.mm.set(mm)
        self.yyyy.set(yyyy)
        self.clearFrame()

    def clearFrame(self):
        self.dayRepeatInterval.set(0)
        self.dayRepeat.set(0)
        for widget in self.endTimes:
            widget.set('End Time')
        for widget in self.colors:
            widget.set('Color')
        for line in self.linesInfo:
            line[1].delete(0, END)

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
    daysInAWeek = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    widthPad = TimeFrame.timelabelWidth/7
    labelWidth = (Frame.screenwidth-TimeFrame.timelabelWidth)/(len(daysInAWeek)) #Default fallback value
    def __init__(self, window):
        TimeFrame.__init__(self, window)
        #Allows placements of a second scrollbar and labels for days of the week
        self.frame.rowconfigure(2, weight=1)
        #scrollbar for view of days
        self.scrollbarx = Scrollbar(self.frame, orient=HORIZONTAL, bg='black', command=self.timeEventCanvas.xview)
        self.timeEventCanvas.configure(xscrollcommand=self.scrollbarx.set)
        self.timeEventCanvas.bind('<Configure>', lambda e: self.timeEventCanvas.configure(scrollregion = self.timeEventCanvas.bbox('all')))
        #fills the corners of the scrollbar and above time labels
        self.dayNameLabel = Label(self.workingFrame,text="Day:",relief='flat', bg=LRGRAY, fg=OFFWHITE, font=('Arial',12))
        self.fillLabel1 = Label(self.frame,text="",relief='flat', bg=LRGRAY, fg=OFFWHITE, font=('Arial',12))
        self.fillLabel2 = Label(self.frame,text="",relief='flat', bg=LRGRAY, fg=OFFWHITE, font=('Arial',12))
        #the first index of each array is the day title the rest are the events
        self.dayLabels = []
        self.createDaySlots()
        #deals with weird math of divide by 7
        self.setLabelWidth()
        #change title
        today = datetime.date.today()
        self.todaysDate = self.formatDate(today)
        self.workingDate = self.findMon(today)
        self.thisWeek = self.workingDate
        self.changeTitle(self.workingDate, self.nextWeek)
        self.changeWorkingWeek(self.thisWeek, self.nextWeek)

    def findMon(self, date):
        day = getDayOfTheWeek(self.todaysDate)
        changeBy = WeekFrame.daysInAWeek.index(day)
        self.nextWeek = self.formatDate((date - datetime.timedelta(days=changeBy)) + datetime.timedelta(weeks=1))
        self.lastWeek = self.formatDate((date - datetime.timedelta(days=changeBy)) - datetime.timedelta(weeks=1))
        thisMon = self.formatDate(date - datetime.timedelta(days=changeBy))
        return thisMon

    def setLabelWidth(self):
        multiple = 0
        closestMultiple = 0
        index=0
        while multiple <= Frame.screenwidth:
            multiple = index * len(WeekFrame.daysInAWeek)
            if abs(Frame.screenwidth-multiple) < abs(Frame.screenwidth-closestMultiple):
                closestMultiple = multiple
            index+=1
        WeekFrame.labelWidth = closestMultiple/len(WeekFrame.daysInAWeek) - WeekFrame.widthPad
            

    def place(self):
        #param 2 allows room for week day names
        TimeFrame.place(self, TimeFrame.labelHeight)
        #places scrollbar
        self.scrollbarx.grid(row=2, column=1, sticky='nsew')
        self.fillLabel1.grid(row=2, column=0, sticky='nsew')
        self.fillLabel2.grid(row=2, column=2, sticky='nsew')

        #places day name label
        self.dayNameLabel.place(x=TimeFrame.timelabelX, y=0, width=TimeFrame.timelabelWidth, height=TimeFrame.labelHeight)

        self.displayDaySlots()

    def createDaySlots(self):
        for i in range(len(WeekFrame.daysInAWeek)):
            self.dayLabels.append([Label(self.workingCanvas, text=WeekFrame.daysInAWeek[i], anchor='center', relief='flat', bg=LRGRAY, fg=OFFWHITE, font=('Arial',12))])
            self.dayLabels[i][0].bind('<Enter>', self.enteredTitle)
            self.dayLabels[i][0].bind('<Leave>', self.exitTitle)
            self.dayLabels[i][0].bind('<Button-1>', self.clickedTitle)
            for j in range(len(self.timeLabels)-1):
                self.dayLabels[i].append(Label(self.workingCanvas, text='', anchor='w', relief='flat', bg=DGRAY, fg=OFFWHITE, font=('Arial',12)))
                self.dayLabels[i][j+1].bind('<Enter>', self.entered)
                self.dayLabels[i][j+1].bind('<Leave>', self.exit)
                self.dayLabels[i][j+1].bind('<Button-1>', self.clicked)

    def enteredTitle(self, event):
        event.widget['bg'] = DGRAY

    def exitTitle(self, event):
        event.widget['bg'] = LRGRAY

    def clickedTitle(self, event):
        index = WeekFrame.daysInAWeek.index(event.widget['text'])
        dd = int(self.workingDate[3:5])
        mm = int(self.workingDate[0:2])
        yyyy = int(self.workingDate[6:len(self.workingDate)])
        date = self.formatDate(datetime.datetime(yyyy, mm, dd) + datetime.timedelta(days=index))
        Frame.allFramesInUse[4].getFrame().tkraise()
        Frame.allFramesInUse[4].setFrame(date)

    def entered(self, event):
        event.widget['bg'] = HIGHLIGHTCOLOR
        event.widget['fg'] = 'black'

    def exit(self, event):
        event.widget['bg'] = DGRAY
        event.widget['fg'] = OFFWHITE
        #puts back events to their color and not darkgray
        dd = int(self.workingDate[3:5])
        mm = int(self.workingDate[0:2])
        yyyy = int(self.workingDate[6:len(self.workingDate)])
        dateE = self.formatDate(datetime.datetime(yyyy, mm, dd) + datetime.timedelta(days=7))
        self.changeWorkingWeek(self.workingDate, dateE)

    def clicked(self, event):
        tindex = 0
        dindex = 0
        for list in self.dayLabels:
            try:
                tindex = list.index(event.widget) - 1
                break
            except ValueError:
                dindex+=1 
               
        time = TimeFrame.timesInADay[tindex]
        dd = int(self.workingDate[3:5])
        mm = int(self.workingDate[0:2])
        yyyy = int(self.workingDate[6:len(self.workingDate)])
        date = self.formatDate(datetime.datetime(yyyy, mm, dd) + datetime.timedelta(days=dindex))
        #brings up day view of day clicked
        Frame.allFramesInUse[0].getFrame().tkraise()
        Frame.allFramesInUse[0].changeWorkingDay(date)

    def displayDaySlots(self):
        currentY = 0
        currentX = DayFrame.eventlabelX
        for list in self.dayLabels:
            for label in list:
                label.place(x=currentX, y=currentY, width=WeekFrame.labelWidth, height=TimeFrame.labelHeight)
                currentY+=TimeFrame.labelHeight
            currentX+=WeekFrame.labelWidth
            currentY=0

    def clearAllSlots(self):
        titleIndex = True
        for day in self.dayLabels:
            for label in day:
                if titleIndex == True:
                    titleIndex = False
                    continue
                label['text'] = ''
                label['bg'] = DGRAY
            titleIndex = True

    def changeWorkingWeek(self, dateS, dateE):
        self.workingDate = dateS
        self.changeTitle(dateS, dateE)
        self.clearAllSlots()
        dd = int(self.workingDate[3:5])
        mm = int(self.workingDate[0:2])
        yyyy = int(self.workingDate[6:len(self.workingDate)])
        dates = []
        for i in range(7):
            dates.append(self.formatDate(datetime.datetime(yyyy, mm, dd) + datetime.timedelta(days=i)))
        #mon, tu, wed, th, fri, sat, sun
        daysToFill = [None,None,None,None,None,None,None]
        for i in range(len(dates)):
            try:
	            daysToFill[i] = DayEvent.allDayEvents[dates[i]]
            except KeyError:
                continue

        for day in daysToFill:
            if day != None:
                self.updateDaySlot(day)

    def updateDaySlot(self, day):
        dayIndex = WeekFrame.daysInAWeek.index(day.dayOfTheWeek)
        for event in day.eventlist:
            slotindex = TimeFrame.timesInADay.index(event.startTime) + 1
            endindex = TimeFrame.timesInADay.index(event.endTime) + 1
            self.dayLabels[dayIndex][slotindex]['text'] = day.dayOfTheWeek[0] +': ' + event.title + ', ' + event.startTime
            while slotindex < endindex:
                self.dayLabels[dayIndex][slotindex]['bg'] = event.color
                slotindex += 1

    def changeTitle(self, dateS, dateE):
        #finds the new week number
        dd = int(dateS[3:5])
        mm = int(dateS[0:2])
        yyyy = int(dateS[6:len(dateS)])
        newWeek = datetime.datetime(yyyy, mm, dd)
        yr = newWeek.year
        weekNumber = ((newWeek - datetime.datetime(yr,1,1)).days/7) + 1
        self.weekNumber = str(int(weekNumber))
        if self.workingDate == self.thisWeek:
            self.title['text'] = "This Week: " + dateS + "-" + dateE + " (" + self.weekNumber + ")"
        elif self.workingDate == self.nextWeek:
            self.title['text'] = "Next Week: " + dateS + "-" + dateE + " (" + self.weekNumber + ")"
        elif self.workingDate == self.lastWeek:
            self.title['text'] = "Last Week: " + dateS + "-" + dateE + " (" + self.weekNumber + ")"
        else:
            self.title['text'] = "Week: " + dateS + "-" + dateE + " (" + self.weekNumber + ")"

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
        minusWeekS = datetime.datetime(yyyy, mm, dd) - datetime.timedelta(weeks=1)
        minusWeekE = self.workingDate
        self.changeWorkingWeek(self.formatDate(minusWeekS), minusWeekE)

    def incrementPressed(self):
        dd = int(self.workingDate[3:5])
        mm = int(self.workingDate[0:2])
        yyyy = int(self.workingDate[6:len(self.workingDate)])
        plusWeekS = datetime.datetime(yyyy, mm, dd) + datetime.timedelta(weeks=1)
        plusWeekE = datetime.datetime(yyyy, mm, dd) + datetime.timedelta(weeks=2)
        self.changeWorkingWeek(self.formatDate(plusWeekS), self.formatDate(plusWeekE))


class MonthFrame(Frame):
    def __init__(self, window):
        Frame.__init__(self, window)
        today = datetime.date.today()
        #configures a working frame to display weeks
        self.frame.rowconfigure(1, weight=160)
        self.workingFrame = tk.Frame(self.frame, bg=DGRAY)
        #days
        self.workingFrame.columnconfigure(0, weight=1)
        self.workingFrame.columnconfigure(1, weight=1)
        self.workingFrame.columnconfigure(2, weight=1)
        self.workingFrame.columnconfigure(3, weight=1)
        self.workingFrame.columnconfigure(4, weight=1)
        self.workingFrame.columnconfigure(5, weight=1)
        self.workingFrame.columnconfigure(6, weight=1)
        #weeks
        self.workingFrame.rowconfigure(0, weight=1)
        self.workingFrame.rowconfigure(1, weight=16)
        self.workingFrame.rowconfigure(2, weight=16)
        self.workingFrame.rowconfigure(3, weight=16)
        self.workingFrame.rowconfigure(4, weight=16)
        self.workingFrame.rowconfigure(5, weight=16)
        #two dimensional array holding Labels of days
        self.days = []
        self.createDays()
        #creates a working date as the first of the month
        today = datetime.date.today()
        self.todaysDate = self.formatDate(today)
        self.workingDate = self.findTheFirst(today)
        self.workingDay = getDayOfTheWeek(self.workingDate)
        self.lastDay = self.findTheLast(today) #NEED THE LAST DAY OF THE MONTH!!!
        print(self.lastDay)

    def findTheFirst(self, today):
        d = today.day - 1
        return self.formatDate(today-datetime.timedelta(days=d))
        
    def findTheLast(self, today):
        d = today.day - 1
        firstDay = today-datetime.timedelta(days=d)
        return self.formatDate(firstDay+datetime.timedelta(weeks=4))

    def createDays(self):
        for i in range(7):
            self.days.append([Label(self.workingFrame, text=WeekFrame.daysInAWeek[i],relief="raised")])
            for j in range(6):
                self.days[i].append(Label(self.workingFrame, text=CreateFrame.possibleDays[0]+":\n\n\n\t          ", justify=LEFT,font=('arial', 12), fg=OFFWHITE)) #limit character
                self.days[i][len(self.days[i])-1].bind('<Enter>', self.entered)
                self.days[i][len(self.days[i])-1].bind('<Leave>', self.exit)
                self.days[i][len(self.days[i])-1].bind('<Button-1>', self.clicked)

    def entered(self, event):
        event.widget['bg'] = HIGHLIGHTCOLOR
        event.widget['fg'] = 'black'

    def exit(self, event):
        event.widget['bg'] = DGRAY
        event.widget['fg'] = OFFWHITE

    def clicked(self, event):
        dDelta = event.widget['text'][0:2]
        if dDelta[0] == '0':
             dDelta = dDelta[1]
        dDelta = int(dDelta) - 1

        dd = int(self.workingDate[3:5])
        mm = int(self.workingDate[0:2])
        yyyy = int(self.workingDate[6:len(self.workingDate)])
        date = self.formatDate(datetime.datetime(yyyy, mm, dd) + datetime.timedelta(days=dDelta))
        #brings up day view of day clicked
        Frame.allFramesInUse[0].getFrame().tkraise()
        Frame.allFramesInUse[0].changeWorkingDay(date)

    def place(self):
        Frame.place(self)
        self.workingFrame.grid(row=1, column=0, columnspan=3, sticky='nsew')
        self.displayDays()

    def displayDays(self):
        for i in range(7):
            for j in range(6):
                self.days[i][j].grid(row=j,column=i,sticky='nsew')

    def formatDate(self, date):
        dd = str(date.day)
        mm = str(date.month)
        yyyy = str(date.year)
        if date.day < 10:
            dd = '0' + dd
        if date.month < 10:
            mm = '0' + mm
        return mm + '/' + dd + '/' + yyyy