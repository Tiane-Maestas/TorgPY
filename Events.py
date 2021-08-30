import datetime
weekDays=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

#formate of date needs to be mm/dd/yyyy
def getDayOfTheWeek(date):
    day = int(date[3:5])
    month = int(date[0:2])
    year = int(date[6:len(date)])
    weekNum = datetime.date(year,month,day).weekday()
    return weekDays[weekNum]

#holds a single event at a single time group and date
class SingleEvent():
    #list of all single events created
    allSingleEvents = []
    lastSavedIndex = 0
    def __init__(self, title, date, startTime, endTime, notes, repeat, reminder, color, concreteBool):
        #data kept for a single event
        self.title = title
        self.date = date
        self.dayOfTheWeek = getDayOfTheWeek(date)
        self.startTime = startTime
        self.endTime = endTime
        self.notes = notes
        self.repeat = repeat
        self.reminder = reminder
        self.concreteBool = concreteBool
        self.color = color
        #used to quickly access even info through day events
        self.eventNum = len(SingleEvent.allSingleEvents)
        self.eventNum = str(self.eventNum)
        SingleEvent.allSingleEvents.append(self)
        self.addToDayEvent()

    def __str__(self):
        return self.title + ': ' + self.notes

    def addToDayEvent(self):
        try:
	        day = DayEvent.allDayEvents[self.date]
        except KeyError:
            DayEvent.allDayEvents[self.date] = DayEvent(self.date, self)
            return
        day.addEvent(self)

    def save(self):
        with open("singleEvents.csv", "w") as f:
            if SingleEvent.lastSavedIndex == 0:
                f.write('#,Title,Date,StartTime,EndTime,Notes,Repeat,Reminder,Color,ConcreteBool\n')
            for index in range(SingleEvent.lastSavedIndex, len(SingleEvent.allSingleEvents)):
                line = SingleEvent.allSingleEvents[index].eventNum + ','
                line = line + SingleEvent.allSingleEvents[index].title + ","
                line = line + SingleEvent.allSingleEvents[index].date + ","
                line = line + SingleEvent.allSingleEvents[index].startTime + ','
                line = line + SingleEvent.allSingleEvents[index].endTime + ','
                line = line + repr(SingleEvent.allSingleEvents[index].notes) + ','
                line = line + SingleEvent.allSingleEvents[index].repeat + ','
                line = line + SingleEvent.allSingleEvents[index].reminder + ','
                line = line + SingleEvent.allSingleEvents[index].color + ','
                line = line + str(SingleEvent.allSingleEvents[index].concreteBool) + '\n'
                f.write(line)

    def changeTime(self, startTime, endTime):
        self.startTime = startTime
        self.endTime = endTime

    def changeColor(self, color):
        self.color = color

    def editNotes(self, newNote):
        self.notes = newNote

#holds a day event that has a list of single events by eventNum
class DayEvent():
    #holds all day events created in a dictionary where dates are keys and their values
    #are the day events
    allDayEvents = {}
    def __init__(self, date, event):
        self.date = date
        self.dayOfTheWeek = getDayOfTheWeek(date)
        #a list of single events associated with this day
        self.eventlist = [event]

    def addEvent(self, event):
        self.eventlist.append(event)
