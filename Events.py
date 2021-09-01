import datetime
import os
weekDays=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

#notes on saving and writing events: always call save after creating an event and make 
#sure there is an extra empty line at the end of the csv file. 
#Additionally, if there are no events yet the csv file should be empty.

#formate of date needs to be mm/dd/yyyy
def getDayOfTheWeek(date):
    day = int(date[3:5])
    month = int(date[0:2])
    year = int(date[6:len(date)])
    weekNum = datetime.date(year,month,day).weekday()
    return weekDays[weekNum]

#uploads all events in the events csv file that have been saved
def uploadEvents():
    if os.path.isfile("singleEvents.csv"):
        with open("singleEvents.csv", "r") as f:
            contents = f.readlines()
            if len(contents) > 1:
                for line in contents:
                    if line[0] == '#':
                        continue
                    info = line.split(',')
                    SingleEvent(info[1],info[2],info[3],info[4],info[5],info[6],info[7],info[8],info[9])

#holds a single event at a single time group and date
class SingleEvent():
    #list of all single events created
    allSingleEvents = []
    def __init__(self, title, date, startTime, endTime, notes, repeat, reminder, color, concreteBool):
        #data kept for a single event
        self.title = title
        self.date = date
        self.dayOfTheWeek = getDayOfTheWeek(date)
        self.startTime = startTime
        self.endTime = endTime
        self.notes = notes.replace('\n', ' ')
        self.repeat = repeat
        self.reminder = reminder
        self.concreteBool = concreteBool
        self.color = color
        #used to quickly access info through day events
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

    #saves self to csv file of events
    #notes: always call save after creating an event and make sure there is an extra empty line at the end
    #of the csv file
    def save(self):
        with open("singleEvents.csv", "a") as f:
            if len(SingleEvent.allSingleEvents) == 1:
                f.write('#,Title,Date,StartTime,EndTime,Notes,Repeat,Reminder,Color,ConcreteBool\n')
            
            line = self.eventNum + ','
            line = line + self.title + ","
            line = line + self.date + ","
            line = line + self.startTime + ','
            line = line + self.endTime + ','
            line = line + self.notes + ','
            line = line + self.repeat + ','
            line = line + self.reminder + ','
            line = line + self.color + ','
            line = line + str(self.concreteBool) + '\n'
            f.write(line)
            f.close()

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
