import tkinter as tk
from Frames import *
from Events import *

windowDefaultGeometry = '850x500+300+175'
windowMinWidth = 850
windowMinHeight = 500
allFrames = []
allMenus = []
darkgray = '#1B1D1F'
offwhite = '#AEBFC7'
lightergray = '#333739'

def createFrames(window):
    allFrames.append(DayFrame(window))
    allFrames.append(WeekFrame(window))
    allFrames.append(MonthFrame(window))
    allFrames.append(CreateSingleEventFrame(window))
    allFrames.append(CreateDayEventFrame(window))
    allFrames.append(CreateWeekEventFrame(window))

def placeFrames():
    for frame in allFrames:
        frame.place()

def showFrame(frame):
    frame.tkraise()

def doNothing():
    pass

def configureNavigationBar(menu):
    viewMenu = Menu(menu, tearoff=0, activebackground='orange')
    menu.add_cascade(label='View', menu=viewMenu)
    viewMenu.add_command(label='Day View', command=lambda:showFrame(allFrames[0].getFrame()))
    viewMenu.add_command(label='Week View', command=lambda:showFrame(allFrames[1].getFrame()))
    viewMenu.add_command(label='Month View', command=lambda:showFrame(allFrames[2].getFrame()))
    allMenus.append(viewMenu)

    createMenu = Menu(menu, tearoff=0, activebackground='orange')
    menu.add_cascade(label='Create', menu=createMenu)
    createMenu.add_command(label='Single Event', command=lambda:showFrame(allFrames[3].getFrame()))
    createMenu.add_command(label='Day Event', command=lambda:showFrame(allFrames[4].getFrame()))
    createMenu.add_command(label='Week Event', command=lambda:showFrame(allFrames[5].getFrame()))
    allMenus.append(createMenu)

    optionMenu = Menu(menu, tearoff=0, activebackground='orange')
    menu.add_cascade(label='Options', menu=optionMenu)
    optionMenu.add_command(label='Nothing Yet', command=doNothing)
    allMenus.append(optionMenu)

def main():
    #initializes window information
    rootWindow = tk.Tk()
    rootWindow.title('Organizer')
    rootWindow.geometry(windowDefaultGeometry)
    rootWindow.minsize(windowMinWidth, windowMinHeight)
    rootWindow.iconbitmap("Images/TorgLogo.ico")
    rootWindow.tk_setPalette(darkgray)
    rootWindow.rowconfigure(0, weight=1)
    rootWindow.columnconfigure(0, weight=1)
    Frame.screenwidth = rootWindow.winfo_screenwidth()
    Frame.screenheight = rootWindow.winfo_screenheight()

    #creates and places all frames
    createFrames(rootWindow)
    placeFrames()
    #allows access of all working frames to all frames through inheritence
    allFrames[0].setAllFrames(allFrames)

    #create and places a navigation bar
    menuBar = Menu(rootWindow)
    rootWindow.config(menu=menuBar)
    configureNavigationBar(menuBar)

    #places dayview on top
    showFrame(allFrames[0].getFrame())
    #begins GUI loop
    rootWindow.mainloop()


if __name__ == '__main__':
    main()