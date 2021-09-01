import tkinter as tk
from Frames import *
from Events import *
from ctypes import windll

#Colors
LRGRAY = '#333739' 
DGRAY = '#1B1D1F' 
RGRAY = '#10121f'
OFFWHITE = '#AEBFC7'
HIGHLIGHTCOLOR = 'orange'

#Window Info
tk_title = "Torg"
windowDefaultGeometry = '850x500+300+175'
windowMinWidth = 850
windowMinHeight = 500

#List of working Menus and Frames
allFrames = []
allMenus = []

#creates working frames
def createFrames(window):
    allFrames.append(DayFrame(window))
    allFrames.append(WeekFrame(window))
    allFrames.append(MonthFrame(window))
    allFrames.append(CreateSingleEventFrame(window))
    allFrames.append(CreateDayEventFrame(window))
    allFrames.append(CreateWeekEventFrame(window))

#places working frames
def placeFrames():
    for frame in allFrames:
        frame.place()

#shows a given frame
def showFrame(frame):
    frame.tkraise()

#placeholder
def doNothing():
    pass

def main():
    #initializing tkinter base
    root=Tk()
    root.title(tk_title)
    root.overrideredirect(True) #turns off title bar, geometry
    root.geometry(windowDefaultGeometry) 
    root.iconbitmap("Images/TorgLogo.ico")
    root.minsize(windowMinWidth, windowMinHeight)
    root.tk_setPalette(DGRAY)
    #initializes screen resolution in my Frame classes
    Frame.screenwidth = root.winfo_screenwidth()
    Frame.screenheight = root.winfo_screenheight()

    #uploads events data
    uploadEvents()

    #--------------------Start of Custom Title Bar by Anthony Terrano and edited by Me--------------------
    root.minimized = False #only to know if root is minimized
    root.maximized = False #only to know if root is maximized

    title_bar = tk.Frame(root, bg='black', relief='raised',bd=0,highlightthickness=0)

    def set_appwindow(mainWindow): # to display the window icon on the taskbar, even when using root.overrideredirect(True)
        # Some WindowsOS styles, required for task bar integration
        GWL_EXSTYLE = -20
        WS_EX_APPWINDOW = 0x00040000
        WS_EX_TOOLWINDOW = 0x00000080
        # Magic
        hwnd = windll.user32.GetParent(mainWindow.winfo_id())
        stylew = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        stylew = stylew & ~WS_EX_TOOLWINDOW
        stylew = stylew | WS_EX_APPWINDOW
        res = windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, stylew)
        mainWindow.wm_withdraw()
        mainWindow.after(10, lambda: mainWindow.wm_deiconify())

    def minimize_me():
        root.overrideredirect(0) # so you can't see the window when is minimized
        root.iconify()      

    def deminimize(event):
        root.overrideredirect(1)# so you can see the window when is not minimized                             

    def maximize_me():
        if root.maximized == False: # if the window was not maximized
            root.normal_size = root.geometry()
            expand_button.config(text=" 🗗 ")
            root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")
            root.maximized = not root.maximized 
            # now it's maximized
        else: # if the window was maximized
            expand_button.config(text=" 🗖 ")
            root.geometry(root.normal_size)
            root.maximized = not root.maximized
            # now it is not maximized

    #put widgets on title bar
    close_button = Button(title_bar, text='  🗙  ', command=root.destroy,bg='black',padx=2,pady=2,font=("arial", 13),bd=0,fg=OFFWHITE,highlightthickness=0)
    expand_button = Button(title_bar, text=' 🗖 ', command=maximize_me,bg='black',padx=2,pady=2,bd=0,fg=OFFWHITE,font=("arial", 13),highlightthickness=0)
    minimize_button = Button(title_bar, text=' − ',command=minimize_me,bg='black',padx=2,pady=2,bd=0,fg=OFFWHITE,font=("arial", 13),highlightthickness=0)
    title_bar_title = Label(title_bar, text=tk_title, bg='black',bd=0,fg=OFFWHITE,font=("arial", 13),highlightthickness=0, anchor=CENTER)

    viewMenu = Menubutton(title_bar, activebackground='orange',text='View',font=("arial", 13), fg=OFFWHITE, bg='black', bd=0)
    viewOptions = Menu(viewMenu, tearoff=0, activebackground='orange', bg='black', bd=0, relief='solid', border=0)
    viewMenu["menu"] = viewOptions
    viewOptions.add_command(label='Day View', command=lambda:showFrame(allFrames[0].getFrame()))
    viewOptions.add_command(label='Week View', command=lambda:showFrame(allFrames[1].getFrame()))
    viewOptions.add_command(label='Month View', command=lambda:showFrame(allFrames[2].getFrame()))
    allMenus.append(viewMenu)

    createMenu = Menubutton(title_bar, activebackground='orange',text='Create',font=("arial", 13), fg=OFFWHITE, bg='black')
    createOptions = Menu(createMenu, tearoff=0, activebackground='orange', bg='black')
    createMenu["menu"] = createOptions
    createOptions.add_command(label='Single Event', command=lambda:showFrame(allFrames[3].getFrame()))
    createOptions.add_command(label='Day Event', command=lambda:showFrame(allFrames[4].getFrame()))
    createOptions.add_command(label='Week Event', command=lambda:showFrame(allFrames[5].getFrame()))
    allMenus.append(createMenu)

    optionMenu = Menubutton(title_bar, activebackground='orange',text='Options',font=("arial", 13), fg=OFFWHITE, bg='black')
    optionOptions = Menu(optionMenu, tearoff=0, activebackground='orange', bg='black')
    optionMenu["menu"] = optionOptions
    optionOptions.add_command(label='Nothing Yet', command=doNothing)
    allMenus.append(optionMenu)

    # a frame for the main area of the window, this is where the actual app will go
    window = tk.Frame(root, bg=DGRAY,highlightthickness=0)
    window.rowconfigure(0, weight=128)
    window.rowconfigure(1, weight=1)
    window.columnconfigure(0, weight=128)
    window.columnconfigure(1, weight=1)

    # pack the widgets
    title_bar.pack(fill=X)
    close_button.pack(side=RIGHT,ipadx=7,ipady=1)
    expand_button.pack(side=RIGHT,ipadx=7,ipady=1)
    minimize_button.pack(side=RIGHT,ipadx=7,ipady=1)
    title_bar_title.pack(side=RIGHT, expand=1)
    viewMenu.pack(side=LEFT)
    createMenu.pack(side=LEFT)
    optionMenu.pack(side=LEFT)
    window.pack(expand=1, fill=BOTH) #replace this with your main Canvas/Frame/etc.
  
    # bind title bar motion to the move window function
    def changex_on_hovering(event):
        close_button['bg']='red'
    def returnx_to_normalstate(event):
        close_button['bg']='black'

    def change_size_on_hovering(event):
        expand_button['bg']=HIGHLIGHTCOLOR
    def return_size_on_hovering(event):
        expand_button['bg']='black'

    def changem_size_on_hovering(event):
        minimize_button['bg']=HIGHLIGHTCOLOR
    def returnm_size_on_hovering(event):
        minimize_button['bg']='black'

    def get_pos(event): # this is executed when the title bar is clicked to move the window

        if root.maximized == False:
            xwin = root.winfo_x()
            ywin = root.winfo_y()
            startx = event.x_root
            starty = event.y_root

            ywin = ywin - starty
            xwin = xwin - startx

            def move_window(event): # runs when window is dragged
                root.config(cursor="fleur")
                root.geometry(f'+{event.x_root + xwin}+{event.y_root + ywin}')

            def release_window(event): # runs when window is released
                root.config(cursor="arrow")
            
            title_bar.bind('<B1-Motion>', move_window)
            title_bar.bind('<ButtonRelease-1>', release_window)
            title_bar_title.bind('<B1-Motion>', move_window)
            title_bar_title.bind('<ButtonRelease-1>', release_window)
        else:
            expand_button.config(text=" 🗖 ")
            root.maximized = not root.maximized
        
    title_bar.bind('<Button-1>', get_pos) # so you can drag the window from the title bar
    title_bar_title.bind('<Button-1>', get_pos) # so you can drag the window from the title 

    # button effects in the title bar when hovering over buttons
    close_button.bind('<Enter>',changex_on_hovering)
    close_button.bind('<Leave>',returnx_to_normalstate)
    expand_button.bind('<Enter>', change_size_on_hovering)
    expand_button.bind('<Leave>', return_size_on_hovering)
    minimize_button.bind('<Enter>', changem_size_on_hovering)
    minimize_button.bind('<Leave>', returnm_size_on_hovering)

    #resize the window width
    resizex_widget = tk.Frame(window,bg=DGRAY,cursor='sb_h_double_arrow')
    resizex_widget.grid(column=1, row=0, sticky='nsew', ipadx=2)

    def resizex(event):

        xwin = root.winfo_x()

        difference = (event.x_root - xwin) - root.winfo_width()

        if root.winfo_width() > 150 : # 150 is the minimum width for the window
            try:
                root.geometry(f"{ root.winfo_width() + difference }x{ root.winfo_height() }")
            except:
                pass
        else:
            if difference > 0: # so the window can't be too small (150x150)
                try:
                    root.geometry(f"{ root.winfo_width() + difference }x{ root.winfo_height() }")
                except:
                    pass


        resizex_widget.config(bg=DGRAY)

    resizex_widget.bind("<B1-Motion>",resizex)

    #resize the window height
    resizey_widget = tk.Frame(window,bg=DGRAY,cursor='sb_v_double_arrow')
    resizey_widget.grid(column=0, row=1, columnspan=2, sticky='nsew', ipadx=2)

    def resizey(event):

        ywin = root.winfo_y()

        difference = (event.y_root - ywin) - root.winfo_height()

        if root.winfo_height() > 150: # 150 is the minimum height for the window
            try:
                root.geometry(f"{ root.winfo_width()  }x{ root.winfo_height() + difference}")
            except:
                pass
        else:
            if difference > 0: # so the window can't be too small (150x150)
                try:
                    root.geometry(f"{ root.winfo_width()  }x{ root.winfo_height() + difference}")
                except:
                    pass

        resizey_widget.config(bg=DGRAY)

    resizey_widget.bind("<B1-Motion>",resizey)

    # some settings
    title_bar.bind("<Map>", deminimize) # to view the window by clicking on the window icon on the taskbar
    root.after(10, lambda:set_appwindow(root)) # to see the icon on the task bar (IDK if this works)
    #--------------------End of Custom Title Bar by Anthony Terrano and edited by Me--------------------

    #creates and places all frames
    createFrames(window)
    placeFrames()
    #allows access of all working frames to all frames through inheritence
    allFrames[0].setAllFrames(allFrames)

    #Create menus!

    #places dayview on top
    showFrame(allFrames[0].getFrame())
    #begins GUI loop
    root.mainloop()

if __name__ == '__main__':
    main()