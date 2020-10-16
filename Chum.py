from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
from tkinter import filedialog as fd
from subprocess import *
import time
from time import strftime
import datetime
from datetime import date
import pickle
import wikipedia
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from datetime import datetime, timedelta
import datefinder
from tkinter import filedialog
import pyperclip

def googlecalender():
    Popen('python google_calender.py')
    time.sleep(1)
    return


def create(name):
    credentials = {'name': name}
    tasks = []
    pickle.dump(credentials, open("credentials.pkl", "wb"))
    pickle.dump(tasks, open("tasks_list.pkl", "wb"))
    response = messagebox.askquestion(
        "SignIn Successful", "Do you wish to continue?")
    if (response == 'yes'):
        app()


def app():
    root.wm_state('iconic')
    main = Toplevel()
    main.title("Chum")
    main.geometry("1200x800")
    main.resizable(width=False, height=False)
    main.iconbitmap('chum_ico.ico')
    frame = LabelFrame(main, width=1200, height=800)
    frame.pack(expand=True, side=LEFT, fill=BOTH)

    def time():
        string_time = strftime('%H:%M:%S %p')
        t.config(text=string_time)
        t.after(1000, time)
        today = date.today()
        string_date = today.strftime("%d %b %Y")
        tod_date.config(text=string_date)
        weekDays = ("Monday", "Tuesday", "Wednesday",
                    "Thursday", "Friday", "Saturday", "Sunday")
        day_num = today.weekday()
        string_day = weekDays[day_num]
        tod_day.config(text=string_day)

    def clearFrame():
        # destroy all widgets from frame
        for widget in content_frame.winfo_children():
             widget.destroy()

    def wiki_fun():
        clearFrame()

        def encylopedia():
            result.delete(1.0, END)
            wiki_result = wikipedia.summary(
                search_entry.get(), sentences=int(lines_entry.get()))
            result.insert(INSERT, wiki_result)
        
        search_label = Label(content_frame, text="Topic:",
                         font=('calibri', 20, 'bold'))
        search_label.grid(row=0, column=0, padx=10)
        search_entry = Entry(content_frame, font=('calibri', 20))
        search_entry.grid(row=0, column=1)
        lines_label = Label(content_frame, text="Count of lines:",
                        font=('calibri', 20, 'bold'))
        lines_label.grid(row=1, column=0, padx=10)
        lines_entry = Entry(content_frame, font=('calibri', 20))
        lines_entry.grid(row=1, column=1)
        global search_im
        search_im = Image.open("search_im.png")
        search_im = search_im.resize((50, 50))
        search_im = ImageTk.PhotoImage(search_im)
        search_symbol = Button(content_frame, image=search_im, command=encylopedia)
        search_symbol.grid(row=0, column=2, padx=5, rowspan=2)
        result = Text(content_frame, height=23, width=102,
                  font=('calibri', 15), wrap=WORD)
        result.grid(row=2, column=0, columnspan=20)
    
    def assig_fun():

        clearFrame()
        
        def create_reminder():
            google_credentials =pickle.load(open("token.pkl", "rb"))
            service = build("calendar","v3",credentials=google_credentials)
            matches = list(datefinder.find_dates(due_time.get()))
            if len(matches):
                start_time = matches[0]
                end_time = start_time + timedelta(minutes=10)

            event = {
                'summary': assignment.get(),
                'description': 'assignment',
                'start': {
                    'dateTime': start_time.strftime("%Y-%m-%dT%H:%M:%S"),
                    'timeZone': 'Asia/Kolkata',
                },
                'end': {
                    'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
                    'timeZone': 'Asia/Kolkata',
                },
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'email', 'minutes': int(email_notif.get())*60},
                        {'method': 'popup', 'minutes': int(mobile_notif.get())*60},
                    ],
                },
            }
            return service.events().insert(calendarId='primary', body=event).execute()
        
        def get_assinment():
            assign_list.delete(1.0, END)
            google_credentials = pickle.load(open("token.pkl", "rb"))
            service = build("calendar", "v3", credentials=google_credentials)
            result = service.events().list(calendarId='primary', q="assignment").execute()
            for i in result['items']:
                item = i['summary']
                temp_dic = i['start']
                matches = datefinder.find_dates(temp_dic['dateTime'])
                x = list(matches)
                start = x[0].strftime("%A %d %B %Y %H:%M ")
                assign_list.insert(INSERT,"-->"+item+", "+"due date: "+start+"\n")
    

        title_frame = LabelFrame(content_frame,relief='flat')
        title_frame.pack(side=TOP,fill=BOTH)

        title = Label(title_frame,text="Create Assignment Reminder",font=('calibri', 20,'bold'),pady=5)
        title.pack(fill=X)

        create_frame = LabelFrame(content_frame)
        create_frame.pack(side=TOP,fill=BOTH)

        assignment_lab = Label(
            create_frame,text="Assignment Name  :",font=('calibri', '15','bold'),pady=5,padx=150)
        assignment_lab.grid(row=1,column=0)
        assignment = Entry(create_frame, font=('calibri', '15'))
        assignment.grid(row=1,column=1,columnspan=3)

        due_time_lab = Label(
            create_frame, text="Due Date and Time  :", font=('calibri', '15','bold'),pady=5,padx=150)
        due_time_lab.grid(row=2, column=0)
        due_time = Entry(create_frame, font=('calibri', '15'))
        due_time.grid(row=2, column=1, columnspan=3)

        email_notif_lab = Label(
            create_frame, text="Email Notification Before :", font=('calibri', '15','bold'),pady=5,padx=150)
        email_notif_lab.grid(row=3, column=0)
        email_notif = Entry(create_frame,font=('calibri', '15'))
        email_notif.grid(row=3, column=1, columnspan=3)

        mobile_notif_lab = Label(
            create_frame,text="Mobile Notification Before :",font=('calibri', '15','bold'),pady=5,padx=150)
        mobile_notif_lab.grid(row=4,column=0)
        mobile_notif = Entry(create_frame, font=('calibri', '15'))
        mobile_notif.grid(row=4,column=1,columnspan=3)

        submit_button = Button(content_frame,text = "SUBMIT",font=('calibri', '15','bold'),pady=5,padx=20,command = create_reminder)
        submit_button.pack()

        get_button = Button(content_frame,text="Get Assignments",font=('calibri', 20,'bold'),command = get_assinment)
        get_button.pack(fill=X)

        assign_list = Text(content_frame, font=('calibri', 15), wrap=WORD,height=13,width=101)
        assign_list.pack()

    def to_do_list():
        
        clearFrame()
        
        def show_task():
            tasks =pickle.load(open("tasks_list.pkl", "rb"))
            for i in range(len(tasks)):
                tasks_list.insert(INSERT, str(i+1)+". " +tasks[i]+"\n")

        def add_task():
            tasks =pickle.load(open("tasks_list.pkl", "rb"))
            task = (add_name_entry.get() + ", Due by: " + add_time_entry.get())
            tasks.append(task)
            pickle.dump(tasks, open("tasks_list.pkl", "wb"))
            tasks_list.delete(1.0, END)
            show_task()
        
        def delete_task():
            tasks = pickle.load(open("tasks_list.pkl", "rb"))
            tasks.pop(int(task_no_entry.get())-1)
            pickle.dump(tasks, open("tasks_list.pkl", "wb"))
            tasks_list.delete(1.0, END)
            show_task()

        def create_event():
            google_credentials = pickle.load(open("token.pkl", "rb"))
            service = build("calendar", "v3", credentials=google_credentials)
            start_match = list(datefinder.find_dates(start.get()))
            start_time = start_match[0]
            end_match = list(datefinder.find_dates(end.get()))
            end_time = end_match[0]

            event = {
                'summary': summary.get(),
                'description': description.get(),
                'start': {
                    'dateTime': start_time.strftime("%Y-%m-%dT%H:%M:%S"),
                    'timeZone': 'Asia/Kolkata',
                },
                'end': {
                    'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
                    'timeZone': 'Asia/Kolkata',
                },
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'email', 'minutes': int(
                            email.get())*60},
                        {'method': 'popup', 'minutes': int(
                            mobile.get())*60},
                    ],
                },
            }
            return service.events().insert(calendarId='primary', body=event).execute()


        my_tdl_list = LabelFrame(content_frame,relief="flat")
        my_tdl_list.pack(side=TOP)
        tasks_to_do = Label(my_tdl_list,text="Tasks Pending",font=('calibri', 20,'bold'),padx=10,pady=10)
        tasks_to_do.grid(row=0,column=0,columnspan=3)
        tasks_list = Text(my_tdl_list,height=11,width=50,font=('calibri', 15))
        tasks_list.grid(row=1,column=0,columnspan=3,rowspan=6)
        tasks = pickle.load(open("tasks_list.pkl", "rb"))
        tasks_list.delete(1.0, END)
        show_task()
        add_label = Label(my_tdl_list,text="Add Task",font=('calibri', 20,'bold'),padx=200,pady=10)
        add_label.grid(row=0,column=3,columnspan=3)
        add_name_label = Label(my_tdl_list,text="Task Name: ",font=('calibri', 17,'bold'))
        add_name_label.grid(row=1,column=3)
        add_name_entry = Entry(my_tdl_list,font=('calibri', 15))
        add_name_entry.grid(row=1,column=4)
        add_time_label = Label(my_tdl_list, text="Due by: ", font=('calibri', 17, 'bold'))
        add_time_label.grid(row=2, column=3)
        add_time_entry = Entry(my_tdl_list, font=('calibri', 15))
        add_time_entry.grid(row=2, column=4)
        add_button = Button(my_tdl_list,text="ADD",font=('calibri', 15,'bold'),command=add_task,padx=30,pady=15)
        add_button.grid(row=1,column=5,rowspan=2)
        delete_label = Label(my_tdl_list,text="Enter Completed Task's No.",font=('calibri', 20,'bold'),padx=75,pady=10)
        delete_label.grid(row=3,column=3,columnspan=3)
        task_no_entry = Entry(my_tdl_list, font=('calibri', 15))
        task_no_entry.grid(row=4, column=3,columnspan=3)
        delete_button = Button(my_tdl_list,text="DELETE",font=('calibri', 15,'bold'),command=delete_task)
        delete_button.grid(row=5,column=3,columnspan=3)

        add_event_frame = LabelFrame(content_frame,relief="flat")
        add_event_frame.pack(side=TOP)
        add_event_label = Label(add_event_frame,text="ADD EVENT",font=('calibri', 30,'bold'),pady=10)
        add_event_label.grid(row=0,column=0,columnspan=4)
        summary_label = Label(add_event_frame,text="Summary:",font=('calibri', 20,'bold'))
        summary_label.grid(row=1,column=0)
        summary = Entry(add_event_frame,font=('calibri', 15))
        summary.grid(row=1,column=1)
        description_label = Label(add_event_frame, text="Description:",font=('calibri', 20, 'bold'),pady=10,padx=20)
        description_label.grid(row=1, column=2)
        description = Entry(add_event_frame, font=('calibri', 15))
        description.grid(row=1, column=3)
        Start_label = Label(add_event_frame, text="Start Date and time:",font=('calibri', 20, 'bold'),pady=10,padx=20)
        Start_label.grid(row=2, column=0)
        start = Entry(add_event_frame, font=('calibri', 15))
        start.grid(row=2, column=1)
        end_label = Label(add_event_frame, text="End Date and time:",font=('calibri', 20, 'bold'),pady=10,padx=20)
        end_label.grid(row=2, column=2)
        end = Entry(add_event_frame, font=('calibri', 15))
        end.grid(row=2, column=3)
        email_label = Label(add_event_frame, text="Email Notification: ", font=('calibri', 20, 'bold'),pady=10,padx=20)
        email_label.grid(row=3, column=0)
        email = Entry(add_event_frame, font=('calibri', 15))
        email.grid(row=3, column=1)
        mobile_label = Label(add_event_frame, text="Mobile Notification: ", font=('calibri', 20, 'bold'),pady=10,padx=20)
        mobile_label.grid(row=3, column=2)
        mobile = Entry(add_event_frame, font=('calibri', 15))
        mobile.grid(row=3, column=3)
        add_event_button = Button(add_event_frame,text="ADD",font=('calibri',15,'bold'),padx=60,pady=15,command=create_event)
        add_event_button.grid(row=4,column=0,columnspan=4)

    def convert_file():
        
        clearFrame()

        def get_files():
            names = fd.askopenfilenames()
            global im1
            image1 = Image.open(names[0])
            im1 = image1.convert('RGB')
            for i in range(1,len(names)):
                image = Image.open(names[i])
                im = image.convert('RGB')
                images_list.append(im)
        
        def im2pdf_convert():
            global im1
            tagret = filedialog.asksaveasfilename(defaultextension='.pdf')
            im1.save(tagret,save_all=True,append_images=images_list)
            status.config(text="Files converted Successfully!")

        im2pdf_frame = LabelFrame(content_frame,relief="flat")
        im2pdf_frame.pack(side=TOP)
        im2pdf_Label = Label(im2pdf_frame,text="IMAGE TO PDF CONVERSION",font=('calibri',20,'bold'),padx=100,pady=50)
        im2pdf_Label.grid(row=0,column=0)
        select_file_button = Button(im2pdf_frame, text="Select files", font=('calibri', 20, 'bold'),padx=25,pady=15,command=get_files)
        select_file_button.grid(row=1,column=0)
        images_list=[]
        im2pdf_convert_button = Button(im2pdf_frame, text="Convert", font=('calibri', 20, 'bold'),padx=40,pady=15,command=im2pdf_convert)
        im2pdf_convert_button.grid(row=2,column=0)
        status = Label(im2pdf_frame,font=('calibri', 20, 'bold'),pady=20)
        status.grid(row=3,column=0)

    def library():
        clearFrame()

        def show():
            books_list.delete(1.0, END)
            books = pickle.load(open("books_list.pkl", "rb"))
            for i in range (len(books)):
                temp = str(i+1)+") "+books[i]+"\n"
                books_list.insert(INSERT,temp)

        def add_book():
            book_path = pickle.load(open("books_list_file_path.pkl", "rb"))
            books = pickle.load(open("books_list.pkl", "rb"))
            file_path = fd.askopenfilename()
            book_path.append(file_path)
            books.append(add_entry.get())
            pickle.dump(book_path, open("books_list_file_path.pkl", "wb"))
            pickle.dump(books,open("books_list.pkl","wb"))
            show()
        
        def delete_book():
            book_path = pickle.load(open("books_list_file_path.pkl", "rb"))
            books = pickle.load(open("books_list.pkl", "rb"))
            del books[int(delete_entry.get())-1]
            del book_path[int(delete_entry.get())-1]
            pickle.dump(book_path, open("books_list_file_path.pkl", "wb"))
            pickle.dump(books, open("books_list.pkl", "wb"))
            show()
        
        def open_name():
            book_path = pickle.load(open("books_list_file_path.pkl", "rb"))
            books = pickle.load(open("books_list.pkl", "rb"))
            index = books.index(open_entry.get())
            path = book_path[index]
            Popen(path,shell=True)
        
        def open_no():
            book_path = pickle.load(open("books_list_file_path.pkl", "rb"))
            books = pickle.load(open("books_list.pkl", "rb"))
            index=int(open_no_entry.get())-1
            path = book_path[index]
            Popen(path, shell=True)


        library_frame = LabelFrame(content_frame, relief="flat")
        library_frame.pack()

        lib_label = Label(library_frame,text="My Library",font=('calibri', 30, 'bold'))
        lib_label.pack(side=TOP)

        books_frame = LabelFrame(library_frame,relief = "flat")
        books_frame.pack(side=LEFT)
        books_label = Label(books_frame,text="Books",font=('calibri', 30, 'bold'),padx=300)
        books_label.grid(row=0,column=0)
        books_list = Text(books_frame, font=('calibri', 15),height=21,width=60)
        books_list.grid(row=1,column=0,rowspan=5)

        operations_frame = LabelFrame(library_frame, relief = "flat")
        operations_frame.pack(side=LEFT)

        open_label = Label(operations_frame, text="Open book by name", font=('calibri', 20, 'bold'))
        open_label.grid(row=0, column=0, columnspan=2)

        open_entry = Entry(operations_frame, font=('calibri', 15))
        open_entry.grid(row=1, column=0, rowspan=2)

        open_button = Button(operations_frame, text="OPEN",command=open_name)
        open_button.grid(row=1, column=1, rowspan=2)


        open_label_no = Label(operations_frame, text="Open book by serial no.", font = ('calibri', 20, 'bold'))
        open_label_no.grid(row=3,column=0,columnspan=2)

        open_no_entry = Entry(operations_frame,font=('calibri', 15))
        open_no_entry.grid(row=4,column=0,rowspan=2)

        open_no_button = Button(operations_frame,text="OPEN",command=open_no)
        open_no_button.grid(row=4,column=1,rowspan=2)


        add_label = Label(operations_frame, text="Enter book's name", font = ('calibri', 20, 'bold'))
        add_label.grid(row=6,column=0,columnspan=2)

        add_entry = Entry(operations_frame,font=('calibri', 15))
        add_entry.grid(row=7,column=0,rowspan=2)

        add_button = Button(operations_frame,text="ADD",command=add_book)
        add_button.grid(row=7,column=1,rowspan=2)

        delete_label = Label(operations_frame, text="Enter book's serial no.",font=('calibri', 20, 'bold'))
        delete_label.grid(row=9, column=0,columnspan=2)

        delete_entry = Entry(operations_frame, font=('calibri', 15))
        delete_entry.grid(row=10, column=0,rowspan=2)

        delete_button = Button(operations_frame, text="DELETE",command=delete_book)
        delete_button.grid(row=10, column=1,rowspan=2)

        show()
    
    def feedback():
        clearFrame()

        def contact(n):
            if (n==1):
                pyperclip.copy("palnatit@gmail.com")
                temp = Label(feedback_frame,text="""My E-mail id has been copied to your clipboard\n""",pady=20,font=('calibri', 15,'bold'))
                temp.grid(row=2,column=0,columnspan=5)
                temp_1 = Label(feedback_frame,text="""Please find time and give your valuable feedback on CHUM\n
                Regards :),\n
                Palnati Teja Krishna Sai""",pady=10,font=('calibri', 15,'bold'))
                temp_1.grid(row=3,column=0,columnspan=5)
            if (n==2):
                pyperclip.copy("https://github.com/tejkrish22")
                temp = Label(feedback_frame, text="""My Github link has been copied to your clipboard""", pady=20, font=('calibri', 15, 'bold'))
                temp.grid(row=2, column=0, columnspan=5)
                temp_1 = Label(feedback_frame,text="""Please find time and give your valuable feedback on CHUM\n
                Regards :),\n
                Palnati Teja Krishna Sai""",pady=10,font=('calibri', 15,'bold'))
                temp_1.grid(row=3,column=0,columnspan=5)
            if (n==3):
                pyperclip.copy(
                    f"https://api.whatsapp.com/send?phone=+919885917919&text=Hello%20{credentials['name']}%20,%20please%20provide%20your%20valuable%20feedback.")
                temp = Label(feedback_frame, text="""My WhatsApp link has been copied to your clipboard""", pady=20, font=(
                    'calibri', 15, 'bold'))
                temp.grid(row=2, column=0, columnspan=5)
                temp_1 = Label(feedback_frame,text="""Please find time and give your valuable feedback on CHUM\n
                Regards :),\n
                Palnati Teja Krishna Sai""",pady=10,font=('calibri', 15,'bold'))
                temp_1.grid(row=3,column=0,columnspan=5)
            if (n == 5):
                pyperclip.copy(f"https://www.instagram.com/tejakrishna19/")
                temp = Label(feedback_frame, text="""My Instagram profile link has been copied to your clipboard""", pady=20, font=(
                    'calibri', 15, 'bold'))
                temp.grid(row=2, column=0, columnspan=5)
                temp_1 = Label(feedback_frame,text="""Please find time and give your valuable feedback on CHUM\n
                Regards :),\n
                Palnati Teja Krishna Sai""",pady=10,font=('calibri', 15,'bold'))
                temp_1.grid(row=3,column=0,columnspan=5)
            if (n == 4):
                pyperclip.copy(
                    f"https://www.linkedin.com/in/teja-krishna-sai-palnati-3417541b3/")
                temp = Label(feedback_frame, text="""My Linkedin profile link has been copied to your clipboard""", pady=20, font=(
                    'calibri', 15, 'bold'))
                temp.grid(row=2, column=0, columnspan=5)
                temp_1 = Label(feedback_frame, text="""Please find time and give your valuable feedback on CHUM\n
                Regards :),\n
                Palnati Teja Krishna Sai""", pady=10, font=('calibri', 15, 'bold'))
                temp_1.grid(row=3, column=0, columnspan=5)
    

        body = f"""Hello {credentials['name']} !!!\n
        Myself Palnati Teja krishna Sai pursuing B.Tech in Electronics and Computer Engineering at Amrita Vishwa Vidyapeetham,  \n
        Amritapuri. I have created Chum to help you in this situation where everything is going online. I hope Chum will help    \n
        you in enhancing your productivity. Please give your valuable suggestions and drop your precious feedback at any of \n
        below given social accounts.\n\n"""

        feedback_frame = LabelFrame(content_frame,relief="flat")
        feedback_frame.pack(side=TOP)
        my_label = Label(feedback_frame,text=body,font=('calibri', 12),pady=30)
        my_label.grid(row=0,column=0,columnspan=4)

        global clg
        clg = Image.open("clg logo.jpg")
        clg = clg.resize((200,200))
        clg = ImageTk.PhotoImage(clg)
        clg_label = Label(feedback_frame,image=clg)
        clg_label.grid(row=0,column=4)

        global gmail
        gmail = Image.open("gmail.png")
        gmail = gmail.resize((100,100))
        gmail = ImageTk.PhotoImage(gmail)
        gmail_button = Button(feedback_frame, image=gmail,command=lambda:contact(1))
        gmail_button.grid(row=1,column=0)

        global github
        github = Image.open("github.png")
        github = github.resize((100,100))
        github = ImageTk.PhotoImage(github)
        github_button = Button(feedback_frame, image=github,command=lambda:contact(2))
        github_button.grid(row=1, column=1)

        global whatsapp
        whatsapp = Image.open("whatsapp.png")
        whatsapp = whatsapp.resize((100,100))
        whatsapp = ImageTk.PhotoImage(whatsapp)
        whatsapp_button = Button(feedback_frame, image=whatsapp,command=lambda:contact(3))
        whatsapp_button.grid(row=1, column=2)

        global linkedin
        linkedin = Image.open("linkedin.png")
        linkedin = linkedin.resize((100,100))
        linkedin = ImageTk.PhotoImage(linkedin)
        linkedin_button = Button(
            feedback_frame, image=linkedin, command=lambda: contact(4))
        linkedin_button.grid(row=1, column=3)

        global instagram
        instagram = Image.open("instagram.png")
        instagram = instagram.resize((100,100))
        instagram = ImageTk.PhotoImage(instagram)
        instagram_button = Button(
            feedback_frame, image=instagram, command=lambda: contact(5))
        instagram_button.grid(row=1, column=4)
    
    def logout():
        temp_name = pickle.load(open("credentials.pkl", "rb"))
        flag=messagebox.askyesno(f"Bye {temp_name['name']} !", f"Do you want to Log out {temp_name['name']} ?")
        if (flag==1):
            credentials = {}
            pickle.dump(credentials, open("credentials.pkl", "wb"))
            main.after(1000, main.destroy)
            root.after(1000,root.quit())
            

    credentials = pickle.load(open("credentials.pkl", "rb"))

    frame_menu = LabelFrame(frame)
    frame_menu.pack(side=LEFT, fill=Y)

    global wiki_im
    wiki_im = Image.open("wikipedia.png")
    wiki_im = wiki_im.resize((150, 165))
    wiki_im = ImageTk.PhotoImage(wiki_im)
    wiki_button = Button(frame_menu, image=wiki_im, command=wiki_fun)
    wiki_button.pack(side=TOP, fill=Y)

    global assignment_im
    assignment_im = Image.open("ass.jpg")
    assignment_im = assignment_im.resize((150, 150))
    assignment_im = ImageTk.PhotoImage(assignment_im)
    assignments = Button(frame_menu, image=assignment_im,command = assig_fun)
    assignments.pack(side=TOP, fill=Y)

    global to_do_im
    to_do_im = Image.open("tdl.png")
    to_do_im = to_do_im.resize((150, 150))
    to_do_im = ImageTk.PhotoImage(to_do_im)
    to_do = Button(frame_menu, image=to_do_im,command=to_do_list)
    to_do.pack(side=TOP, fill=Y)

    global file_con
    file_con = Image.open("file.png")
    file_con = file_con.resize((150, 150))
    file_con = ImageTk.PhotoImage(file_con)
    file_converter = Button(frame_menu, image=file_con,command=convert_file)
    file_converter.pack(side=TOP, fill=Y)

    global lib_img
    lib_img = Image.open("lib].jpg")
    lib_img = lib_img.resize((150, 150))
    lib_img = ImageTk.PhotoImage(lib_img)
    lib = Button(frame_menu, image=lib_img,command=library)
    lib.pack(side=TOP, fill=Y)

    frame_user = LabelFrame(frame)
    frame_user.pack(fill=X)

    global logout_im
    logout_im = Image.open("logout.png")
    logout_im = logout_im.resize((100, 100))
    logout_im = ImageTk.PhotoImage(logout_im)
    logout_button = Button(frame_user, image=logout_im,command=logout)
    logout_button.pack(side=RIGHT)

    global feedback_im
    feedback_im = Image.open("feedback.png")
    feedback_im = feedback_im.resize((100, 100))
    feedback_im = ImageTk.PhotoImage(feedback_im)
    feedback_button = Button(frame_user, image=feedback_im,command=feedback)
    feedback_button.pack(side=RIGHT)

    ddt = LabelFrame(frame_user, relief="flat")
    ddt.pack(side=RIGHT)
    tod_day = Label(ddt, font=('calibri', 18, 'bold'))
    tod_day.pack(side=TOP)
    tod_date = Label(ddt, font=('calibri', 18, 'bold'))
    tod_date.pack(side=TOP)
    t = Label(ddt, font=('calibri', 18, 'bold'))
    t.pack(side=TOP)
    time()

    greet_frame = LabelFrame(frame_user, relief="flat")
    greet_frame.pack(side=LEFT)

    global chum_greet_im
    chum_greet_im = Image.open("chum.png")
    chum_greet_im = chum_greet_im.resize((100, 100))
    chum_greet_im = ImageTk.PhotoImage(chum_greet_im)
    chum_greet = Label(greet_frame, image=chum_greet_im)
    chum_greet.grid(row=0, column=0, rowspan=2, columnspan=2)
    welcome = Label(greet_frame, text="Welcome,", font=('calibri', 25, 'bold'))
    welcome.grid(row=0, column=2)
    greet = Label(greet_frame, text=credentials['name'].capitalize(), font=(
        'calibri', 30, 'bold'), padx=20)
    greet.grid(row=1, column=2)

    content_frame = LabelFrame(frame)
    content_frame.pack(side=TOP,fill=BOTH)
    wiki_fun()
    my_frame = LabelFrame(frame)
    my_frame.pack(side=BOTTOM, fill=BOTH)
    my = Label(my_frame, text="Developed by Palnati Teja Krishna Sai",
               font=('calibri', 14))
    my.pack(fill=BOTH)


root = Tk()
root.title("Chum")
root.geometry("500x750")
root.resizable(width=False, height=False)
root.iconbitmap('chum_ico.ico')

pic_frame = LabelFrame(root)
pic_frame.pack(fill=X)


login_im = Image.open("chum_sq.png")
login_im = login_im.resize((500, 500))
login_im = ImageTk.PhotoImage(login_im)
pic = Label(pic_frame, image=login_im)
pic.pack(side=TOP)

already_frame = LabelFrame(root)
already_frame.pack(fill=X)

login_info = Label(already_frame, text="Already logged in?",
                   relief=GROOVE, pady=4)
login_info.pack(side=TOP, fill=X)

login = Button(already_frame, text="CLICK HERE!", command=app)
login.pack(side=TOP, fill=X)

info_frame = LabelFrame(root)
info_frame.pack(fill=X)

name = Label(info_frame, text="Name",padx=80)
name.grid(row=1, column=0, columnspan=3)

nam = Entry(info_frame, bd=5)
nam.grid(row=2, column=0, columnspan=3)

google = Label(
    info_frame, text="To give permission to access Google calender", padx=20)
google.grid(row=1, column=3, columnspan=2)
google.click = Button(info_frame, text="Click Here", command=googlecalender)
google.click.grid(row=2, column=3, columnspan=2)

infor_1 = Label(info_frame, text="Copy the link that is dispalyed on terminal")
infor_1.grid(row=3, column=3, columnspan=2)

infor_2 = Label(info_frame, text="Enter the authorization code and hit enter")
infor_2.grid(row=4, column=3, columnspan=2)

sign_frame = LabelFrame(root)
sign_frame.pack(fill=BOTH)

sign_up = Button(sign_frame, text="SIGN UP", command=lambda: create(nam.get()))
sign_up.pack(fill=BOTH)

disclaimer_frame = LabelFrame(root)
disclaimer_frame.pack(side=BOTTOM, fill=BOTH)

disclaimer = Label(
    disclaimer_frame, text="Disclaimer:- All the above given credentials cant be accessed by the developer")
disclaimer.pack(fill=X, side=TOP)

my_frame = LabelFrame(root)
my_frame.pack(side=BOTTOM, fill=BOTH)

my = Label(my_frame, text="Developed by Palnati Teja Krishna Sai")
my.pack(fill=BOTH)

root.mainloop()
