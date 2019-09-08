import tkinter
import tkinter.ttk
from PIL import ImageTk, Image
import socket
import select
import time


# finish the codes for RPI communication first

def Authenticate_Plate(license_plate):
    """takes in the License plate number as argument
       and communicates with the main server to check if the received
       license plate exists in the database of registered user
       returns :
       --> True  - if license plate is already registered
       --> False - if license plate is not registered
       --> None  - in case any sort of error arises or miscommunication happens between the server and function """

    # initialize the credentials of the main server, ie, the credentials 
    # IP address of the main server 
    # The port number being used by the main server

    main_server_ip = "127.0.0.1"
    main_server_port = 1234
    print("function called")

    # Create a socket to connect to the main server 
    # The same socket will be used in order to communicate back and forth
    # with the main server
    # socket.AF_INET - address family, IPv4
    # socket.SOCK_STREAM - TCP, connection based

    main_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect with the main server
    main_server.connect((main_server_ip, main_server_port))
    
    # Send the first message to authenticate self identity with the main_server
    main_server.send("Hi SeRvEr".encode())
    message = main_server.recv(2048).decode('utf-8')

    if message == "request type" :
        # the server has acknowledged us
        main_server.send("Authenticate Entry".encode())

        message = main_server.recv(2048).decode('utf-8')

        if message == "License Plate Number":
            # everything is correct until now 
            # send the License plate number
            main_server.send(str(license_plate).encode())

            message = main_server.recv(1024).decode('utf-8')

            if message == "Present":
                # The car requesting entry/exit is registered with us
                # Allow entry/exit
                print("RECORD FOUND")
                main_server.close()
                return True
            elif message == "No Record Found":
                # The car requesting entry/exit is not registered with us
                # register new user
                main_server.close()
                return False
    
    # Return None in case any exception arises at any point, or the verification
    # Does not proceed as expected
    main_server.close()
    return None

def Authenticate_Plate_exit(license_plate):
    """takes in the License plate number as argument
       and communicates with the main server to check if the received
       license plate exists in the database of registered user
       returns :
       --> True  - if license plate is already registered
       --> False - if license plate is not registered
       --> None  - in case any sort of error arises or miscommunication happens between the server and function """

    # initialize the credentials of the main server, ie, the credentials 
    # IP address of the main server 
    # The port number being used by the main server

    main_server_ip = "127.0.0.1"
    main_server_port = 1234
    print("function called")

    # Create a socket to connect to the main server 
    # The same socket will be used in order to communicate back and forth
    # with the main server
    # socket.AF_INET - address family, IPv4
    # socket.SOCK_STREAM - TCP, connection based

    main_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect with the main server
    main_server.connect((main_server_ip, main_server_port))
    
    # Send the first message to authenticate self identity with the main_server
    main_server.send("Hi SeRvEr".encode())
    message = main_server.recv(2048).decode('utf-8')

    if message == "request type" :
        # the server has acknowledged us
        main_server.send("Authenticate Exit".encode())

        message = main_server.recv(2048).decode('utf-8')

        if message == "License Plate Number":
            # everything is correct until now 
            # send the License plate number
            main_server.send(str(license_plate).encode())

            message = main_server.recv(1024).decode('utf-8')

            if message == "Present":
                # The car requesting entry/exit is registered with us
                # Allow entry/exit
                print("RECORD FOUND")
                main_server.close()
                return True
            elif message == "No Record Found":
                # The car requesting entry/exit is not registered with us
                # register new user
                main_server.close()
                return False
    
    # Return None in case any exception arises at any point, or the verification
    # Does not proceed as expected
    main_server.close()
    return None

def Register_new_user(license_plate, Name, phone_number, owner_type):
    """ Input List :
        License_plate - the license plate number of the vehicle
        Name          - the name of the owner of the vehicle
        phone_number  - the phone number of the owner of the vehicle
        owner_type    - The type of owner, ie, student/faculty/other
        Returns True --> upon the succesfull registeration of the new user
        Returns False --> upon unsuccesfull registration of the new user
        """
    # initialize the credentials of the main server, ie, the credentials 
    # IP address of the main server 
    # The port number being used by the main server

    main_server_ip = "127.0.0.1"
    main_server_port = 1234

    # Create a socket to connect to the main server 
    # The same socket will be used in order to communicate back and forth
    # with the main server
    # socket.AF_INET - address family, IPv4
    # socket.SOCK_STREAM - TCP, connection based

    main_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect with the main server
    main_server.connect((main_server_ip, main_server_port))
    
    # Send the first message to authenticate self identity with the main_server
    main_server.send("Hi SeRvEr".encode())

    message = main_server.recv(1024).decode('utf-8')
    
    if message == "request type":
        # The server has acknowledged us
        # Send the request type
        main_server.send("Register user".encode())

        message = main_server.recv(1024).decode('utf-8')
        
        if message == "Send Info":
            print("HI")
            if(owner_type==1):
                owner_type = "student"
            elif owner_type==2:
                owner_type = "faculty"
            else:
                owner_type = "other"
            info = str(license_plate+";"+Name+";"+phone_number+";"+owner_type)
            print(info)
            main_server.send(info.encode())

            message = main_server.recv(1024).decode('utf-8')
            if message == "registration complete":
                # everything went as desired
                main_server.close()
                return True

    main_server.close() 
    return False

def Take_entry_photograph():
    """ Gives instruction to the rpi to take image from the entry camera
        The rpi then invokes the web API to detect the license plate number
        The license plate number is then sent back to this PC
        which communicates with the main_server to further check if the plate exists in our records
        This function also receives and saves the photograph taken by the rpi"""
    
    # Define the credentials of the Rpi 
    Rpi_ip = "192.168.165.169"
    Rpi_port = 3000

    # Create a socket which will be used to communicate with the rpi in this function

    # AF_INET - address famaily IPv4
    # SOCK_STREAM - TCP, connection based
    Rpi_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to the Rpi
    Rpi_socket.connect(("192.168.165.169",3000))

    # send the first message to authenticate yourself with the Rpi  
    Rpi_socket.send("obey me".encode())

    message = Rpi_socket.recv(1024).decode('utf-8')
    print('t')
    if message == "yes master":
        # The rpi acknowledges our command
        # send the command
        Rpi_socket.send("initiate entry procedure".encode())

        print("h")
        message = Rpi_socket.recv(1024).decode('utf-8')
        if message == "initiating entry procedure":
            # the Rpi successfully got and interpreted our messade 
            # it will initiate the entry procedure as required

            message = Rpi_socket.recv(1024).decode('utf-8')
            print(" fdfgdfgfd")
            if message == "picture taken and plate identified":
                # upon coming here, we can be sure that the photograph has been clicked 
                # and the number plate extracted by the Rpi
                print(message)
                Rpi_socket.send("License Plate".encode())

                license_plate_number = Rpi_socket.recv(1024).decode('utf-8')

                Rpi_socket.send("photograph".encode())
                print(license_plate_number)
                image = open("1.jpg", 'wb')
                header_length = 10
                header = Rpi_socket.recv(header_length).decode('utf-8')
                header = int(header)
                print(header) #debug
                Image_len = 0
                while (Image_len)!=header:
                    image_data = Rpi_socket.recv(102400)
                    image.write(image_data)
                    Image_len+=len(image_data)
                image.close()
                if(license_plate_number=="Error"):
                    Rpi_socket.send("error".encode())
                    return "123"
                else:
                    Rpi_socket.send("Received".encode())
                
                over = Authenticate_Plate(license_plate_number)
                myfile = open("plate.txt",'w')
                myfile.write(license_plate_number)
                myfile.close()
                if(license_plate_number=="Error"):
                    return "123"
                if over == True:
                    Rpi_socket.send("found".encode())
                    return True
                else:
                    return False

def Take_exit_photograph():
    """ Gives instruction to the rpi to take image from the entry camera
        The rpi then invokes the web API to detect the license plate number
        The license plate number is then sent back to this PC
        which communicates with the main_server to further check if the plate exists in our records
        This function also receives and saves the photograph taken by the rpi"""
    
    # Define the credentials of the Rpi 
    Rpi_ip = '192.168.165.169'
    Rpi_port = 3000

    # Create a socket which will be used to communicate with the rpi in this function

    # AF_INET - address famaily IPv4
    # SOCK_STREAM - TCP, connection based
    Rpi_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to the Rpi
    Rpi_socket.connect((Rpi_ip,Rpi_port))

    # send the first message to authenticate yourself with the Rpi  
    Rpi_socket.send("obey me".encode())

    message = Rpi_socket.recv(1024).decode('utf-8')
    print('t')
    if message == "yes master":
        # The rpi acknowledges our command
        # send the command
        Rpi_socket.send("initiate exit procedure".encode())

        print("h")
        message = Rpi_socket.recv(1024).decode('utf-8')
        if message == "initiating entry procedure":
            # the Rpi successfully got and interpreted our messade 
            # it will initiate the entry procedure as required

            message = Rpi_socket.recv(1024).decode('utf-8')
            print(" fdfgdfgfd")
            if message == "picture taken and plate identified":
                # upon coming here, we can be sure that the photograph has been clicked 
                # and the number plate extracted by the Rpi
                print(message)
                Rpi_socket.send("License Plate".encode())

                license_plate_number = Rpi_socket.recv(1024).decode('utf-8')

                Rpi_socket.send("photograph".encode())
                image = open("1.jpg", 'wb')
                header_length = 10
                header = Rpi_socket.recv(header_length).decode('utf-8')
                header = int(header)
                print(header) #debug
                Image_len = 0
                while (Image_len)!=header:
                    image_data = Rpi_socket.recv(102400)
                    image.write(image_data)
                    Image_len+=len(image_data)
                image.close()
                if(license_plate_number=="Error"):
                    Rpi_socket.send("error".encode())
                    print("Ho gai bakchodi")
                    return False
                else:
                    Rpi_socket.send("Received".encode())
                
                over = Authenticate_Plate_exit(license_plate_number)
                myfile = open("plate.txt",'w')
                myfile.write(license_plate_number)
                myfile.close()
                if over == True:
                    Rpi_socket.send("found exit".encode())
                    return True
                else:
                    return False

def call_start_frame_only_for_entry_allowed_frame():
    myfile = open('plate.txt', 'r')
    plate = myfile.read()
    plate = plate.rstrip()
    myfile.close()
    Register_new_user(plate, string_form_name.get(), string_form_phone_no.get(), var.get())
    Rpi_ip = "192.168.165.169"
    Port = 3000
    Rpi_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    Rpi_socket.connect((Rpi_ip,Port))
    Rpi_socket.send("Allow Entry".encode())
    Rpi_socket.close()
    call_start_frame_on_top()


# Whole Code works on single main window, but different frames, which could be removed and called
#Data required is in the form of 4 variables right now i.e 1) string_form_no_plate, 2) string_form_no_plate_2
#3) string_form_phone_no, 4)var(var takes value 1,2,3 for student,faculty and other respectively)

def func_name():# Import the function which creates a server query(also a script of running webcam thru python, and also alpr code to be placed here)
                # If possible make the function return boolean values, True for a successful updation in library
    return Take_entry_photograph()

def func_checher():
    return_value = Take_exit_photograph()
    print("EXIT code " + str(return_value))
    return return_value

def decider_for_entry_button():
    decide = func_name()
    if decide == True:
        call_entry_allowed_frame_on_top()
    elif decide== False:
        call_verify_no_plate_frame_on_top()
    else:
        call_new_user_not_detected_frame_on_top()

def decider_for_exit_button():
    if func_checher():
        call_exit_allowed_frame_on_top()
    else:
        call_exit_if_plate_not_recognised_frame_on_top()
        
def check_database_again():# This function just queries in the server(without alpr) and returns true for a succesful updation
    myfile = open("plate.txt", 'r')
    plate = myfile.read()
    myfile.close()
    if plate == "Error":
        return False
    return Authenticate_Plate(plate)


def decider_for_new_user_not_registered_frame():
    myfile = open("plate.txt", 'r')
    plate = myfile.read()
    myfile.close()
    if plate == "Error":
        return Take_entry_photograph()
    decide = Authenticate_Plate(plate)
    if decide == True:
        Rpi_ip = "192.168.165.169"
        Port = 3000
        Rpi_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        Rpi_socket.connect((Rpi_ip,Port))
        Rpi_socket.send("Allow Entry".encode())
        Rpi_socket.close()
        call_entry_allowed_frame_on_top()
    else:
        call_complete_entry_database_frame_on_top()


def decide_for_new_user_not_detected_frame():
    plate = string_form_no_plate.get()
    lic_plate = open('plate.txt', 'w')
    lic_plate.write(plate)
    lic_plate.close()
    decide = Authenticate_Plate(plate)
    if decide == True:
        Rpi_ip = "192.168.165.169"
        Port = 3000
        Rpi_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        Rpi_socket.connect((Rpi_ip,Port))
        Rpi_socket.send("Allow Entry".encode())
        Rpi_socket.close()
        call_entry_allowed_frame_on_top()
    else:
        call_complete_entry_database_frame_on_top()

def decide_for_Exit_if_plate_not_detected_properly():
    Rpi_ip = "192.168.165.169"
    Port = 3000
    Rpi_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Rpi_socket.connect((Rpi_ip,Port))
    Rpi_socket.send("ALLOW EXIT".encode())
    Rpi_socket.close()
    call_exit_allowed_frame_on_top()

def create_widgets_in_start_frame():
    # Create the label for the frame
    start_window_label = tkinter.ttk.Label(start_frame, text='Welcome')
    start_window_label.grid(column=0, row=0, pady=10, padx=10, sticky=(tkinter.N))
    logo="logo.png" # Specify path
    logo_iiitd=ImageTk.PhotoImage(Image.open(logo))# Creates the photo as a Tkinter object
    canvas_photo = tkinter.Canvas(start_frame, width = 1500, height = 300)# Creates a Canvas where the photo is placed
    canvas_photo.grid(row=0,column=0, pady=10, padx=10, sticky=(tkinter.N))# Places the Canvas in the Frame
    canvas_photo.image=logo_iiitd# Saves an instance of the image so the Garbage Collector doesn't pick it up
    canvas_photo.create_image(0,0, anchor=tkinter.NW, image=logo_iiitd)# Puts the Photo in the canvas
    start_window_quit_button = tkinter.Button(start_frame, text = "Quit", command = quit_program,activebackground='DarkSeaGreen3')# Create the button for the frame
    start_window_quit_button.grid(column=0, row=3, pady=10, sticky=(tkinter.N))# Place the Button in th Frame
    start_window_next_button = tkinter.Button(start_frame, text = "Entry Camera", command = decider_for_entry_button,activebackground='DarkSeaGreen3')# Create the button for the frame
    start_window_next_button.grid(column=0, row=1, pady=10, sticky=(tkinter.N))# Place the Button in th Frame
    start_window_next_button = tkinter.Button(start_frame, text = "Exit Camera", command = decider_for_exit_button,activebackground='DarkSeaGreen3')# Create the button for the frame
    start_window_next_button.grid(column=0, row=2, pady=10, sticky=(tkinter.N))# Place the Button in th Frame

def create_widgets_new_user_not_detected_frame():
    new_user_not_detected_window_label_1 = tkinter.ttk.Label(new_user_not_detected_frame, text='Enter User License Plate No.')
    new_user_not_detected_window_label_1.grid(column=0, row=0, pady=10, padx=10, sticky=(tkinter.N))# Placement of widget
    e1.grid(column=1,row=0,pady=10,sticky=(tkinter.N))
    new_user_not_detected_window_label_2 = tkinter.ttk.Label(new_user_not_detected_frame, text='Number: ')
    new_user_not_detected_window_label_2.grid(column=1, row=1, pady=10, padx=10, sticky=(tkinter.N))# Placement of widget
    img="1.jpg" # Specify path
    license_plate=ImageTk.PhotoImage(Image.open(img))# Creates the photo as a Tkinter object
    canvas_photo = tkinter.Canvas(new_user_not_detected_frame, width = 1920, height = 960)# Creates a Canvas where the photo is placed
    canvas_photo.grid(row=2,column=1, pady=10, padx=10, sticky=(tkinter.N))# Places the Canvas in the Frame
    canvas_photo.image=license_plate# Saves an instance of the image so the Garbage Collector doesn't pick it up
    canvas_photo.create_image(0,0, anchor=tkinter.NW, image=license_plate)# Puts the Photo in the canvas
    # Create the button for the frame
    new_user_not_detected_window_next_button = tkinter.Button(new_user_not_detected_frame, text = "Contiue", command = decide_for_new_user_not_detected_frame,activebackground='DarkSeaGreen3')
    new_user_not_detected_window_next_button.grid(column=0, row=1, pady=10, sticky=(tkinter.N),)# Placement of widget
    photo_bad_button=tkinter.Button(new_user_not_detected_frame,text='Take Photo Again',command=decider_for_entry_button,activebackground='DarkSeaGreen3')
    photo_bad_button.grid(column=0, row=2, pady=10, sticky=(tkinter.N))   

def create_widgets_in_verify_no_plate_frame():
    #Put lic value from file
    plate = open('plate.txt', 'r')

    lic_plate_str=plate.read()
    plate.close()

    verify_no_plate_window_label = tkinter.ttk.Label(verify_no_plate_frame, text='The Verified No. Plate is : ')
    verify_no_plate_window_label.grid(column=0, row=0, pady=10, padx=10, sticky=(tkinter.N))# Placement of widget

    verify_no_plate_window_label_2 = tkinter.ttk.Label(verify_no_plate_frame, text=lic_plate_str,width=15)
    verify_no_plate_window_label_2.grid_forget()#plz check
    verify_no_plate_window_label_2.grid(column=1, row=0, pady=10, padx=10, sticky=(tkinter.N))# Placement of widget
    img="1.jpg" # Specify path
    license_plate=ImageTk.PhotoImage(Image.open(img))# Creates the photo as a Tkinter object
    canvas_photo = tkinter.Canvas(verify_no_plate_frame, width = 1920, height = 960)# Creates a Canvas where the photo is placed
    canvas_photo.grid(row=2,column=1, pady=10, padx=10, sticky=(tkinter.N))# Places the Canvas in the Frame
    canvas_photo.image=license_plate# Saves an instance of the image so the Garbage Collector doesn't pick it up
    canvas_photo.create_image(0,0, anchor=tkinter.NW, image=license_plate)# Puts the Photo in the canvas
    # Create the button for the frame
    verify_no_plate_window_next_button= tkinter.Button(verify_no_plate_frame, text = "Verify", command = decider_for_new_user_not_registered_frame,activebackground='DarkSeaGreen3')
    verify_no_plate_window_next_button.grid(column=0, row=1, pady=10, sticky=(tkinter.N),)# Placement of widget
    photo_bad_button=tkinter.Button(verify_no_plate_frame,text='Take Photo Again',command=decider_for_entry_button,activebackground='DarkSeaGreen3')
    photo_bad_button.grid(column=0, row=2, pady=10, sticky=(tkinter.N)) 

def create_widgets_in_entry_allowed_frame():
    # Create the label for the frame
    entry_allowed_window_label = tkinter.ttk.Label(entry_allowed_frame, text='User Registered, Entry is allowed')
    entry_allowed_window_label.grid(column=0, row=0, pady=10, padx=10, sticky=(tkinter.N))
    # Create the button for the frame
    entry_allowed_window_back_button = tkinter.Button(entry_allowed_frame, text = "Back", command = call_start_frame_on_top)
    entry_allowed_window_back_button.grid(column=0, row=1, pady=10, sticky=(tkinter.N))

def create_widgets_in_complete_entry_database_frame():
    complete_entry_database_window_label_2 = tkinter.ttk.Label(complete_entry_database_frame, text='Please Enter the following Details')
    complete_entry_database_window_label_2.grid(column=0, row=0, pady=10, padx=10, sticky=(tkinter.N))
    complete_entry_database_window_label_3 = tkinter.ttk.Label(complete_entry_database_frame, text='Phone Number: ')
    complete_entry_database_window_label_3.grid(column=0, row=2, pady=10, padx=10, sticky=(tkinter.N))
    complete_entry_database_window_label_4 = tkinter.ttk.Label(complete_entry_database_frame, text='Name: ')
    complete_entry_database_window_label_4.grid(column=0, row=1, pady=10, padx=10, sticky=(tkinter.N))
    e4.grid(column=1,row=1,pady=10,sticky=(tkinter.N))
    e2.grid(column=1,row=2,pady=10,sticky=(tkinter.N))
    complete_entry_database_back_button_1 = tkinter.Button(complete_entry_database_frame, text = "Submit", command = call_start_frame_only_for_entry_allowed_frame)
    complete_entry_database_back_button_1.grid(column=1, row=6, pady=10, sticky=(tkinter.N))
    r1=tkinter.Radiobutton(complete_entry_database_frame,text="Student",padx = 20,variable=var, value=1)
    r1.grid(sticky=(tkinter.W),row=3)
    r2=tkinter.Radiobutton(complete_entry_database_frame,text="Faculty",padx = 20,variable=var,value=2)
    r2.grid(sticky=(tkinter.W),row=4)
    r3=tkinter.Radiobutton(complete_entry_database_frame,text="Other",padx = 20,variable=var,value=3)
    r3.grid(sticky=(tkinter.W),row=5)

def create_widgets_in_exit_allowed_frame():
    exit_allowed_window_label = tkinter.ttk.Label(exit_allowed_frame, text='Exit is allowed')
    exit_allowed_window_label.grid(column=0, row=0, pady=10, padx=10, sticky=(tkinter.N))# Placement of widget
    exit_allowed_window_back_button_1 = tkinter.Button(exit_allowed_frame, text = "OK", command = call_start_frame_on_top)
    exit_allowed_window_back_button_1.grid(column=0, row=1, pady=10, sticky=(tkinter.N))# Placement of widget
    #green light here(actually turn off red light here)

def create_widgets_in_exit_if_plate_not_recognised_frame():
    exit_if_plate_not_recognised_window_label_1 = tkinter.ttk.Label(exit_if_plate_not_recognised_frame, text='Enter User License Plate No.')
    exit_if_plate_not_recognised_window_label_1.grid(column=0, row=0, pady=10, padx=10, sticky=(tkinter.N))# Placement of widget
    e3.grid(column=1,row=0,pady=10,sticky=(tkinter.N))
    exit_if_plate_not_recognised_window_label_2 = tkinter.ttk.Label(exit_if_plate_not_recognised_frame, text='Number: ')
    exit_if_plate_not_recognised_window_label_2.grid(column=1, row=1, pady=10, padx=10, sticky=(tkinter.N))# Placement of widget
    img="1.jpg" # Specify path
    print("ya1y")
    license_plate=ImageTk.PhotoImage(Image.open(img))# Creates the photo as a Tkinter object
    canvas_photo = tkinter.Canvas(exit_if_plate_not_recognised_frame, width = 1920, height = 960)# Creates a Canvas where the photo is placed
    canvas_photo.grid(row=2,column=1, pady=10, padx=10, sticky=(tkinter.N))# Places the Canvas in the Frame
    canvas_photo.image=license_plate# Saves an instance of the image so the Garbage Collector doesn't pick it up
    canvas_photo.create_image(0,0, anchor=tkinter.NW, image=license_plate)# Puts the Photo in the canvas
    # Create the button for the frame
    print("ya2y")
    exit_if_plate_not_recognised_window_next_button = tkinter.Button(exit_if_plate_not_recognised_frame, text = "Contiue", command = decide_for_Exit_if_plate_not_detected_properly,activebackground='DarkSeaGreen3')
    exit_if_plate_not_recognised_window_next_button.grid(column=0, row=1, pady=10, sticky=(tkinter.N),)# Placement of widget
    print("ya3y")
    photo_bad_button_1=tkinter.Button(exit_if_plate_not_recognised_frame,text="Take Photo Again",command = decider_for_exit_button,activebackground='DarkSeaGreen3')
    photo_bad_button_1.grid(column=0, row=2, pady=10, sticky=(tkinter.N)) 
    print("ya4y")
    print(string_form_no_plate.get())
    print("ya5y")

def call_start_frame_on_top():
    entry_allowed_frame.grid_forget()
    exit_allowed_frame.grid_forget()
    complete_entry_database_frame.grid_forget()
    create_widgets_in_start_frame()
    start_frame.grid(column=0, row=0, padx=20, pady=5, sticky=(tkinter.W, tkinter.N, tkinter.E))

def call_new_user_not_detected_frame_on_top():
    e1.delete(0,tkinter.END)
    start_frame.grid_forget()
    create_widgets_new_user_not_detected_frame()
    new_user_not_detected_frame.grid(column=0, row=0, padx=20, pady=5, sticky=(tkinter.W, tkinter.N, tkinter.E))

def call_verify_no_plate_frame_on_top():
    start_frame.grid_forget()
    verify_no_plate_frame.grid_forget()
    create_widgets_in_verify_no_plate_frame()
    verify_no_plate_frame.grid(column=0, row=0, padx=20, pady=5, sticky=(tkinter.W, tkinter.N, tkinter.E))

def call_entry_allowed_frame_on_top():
    start_frame.grid_forget()
    complete_entry_database_frame.grid_forget()
    verify_no_plate_frame.grid_forget()
    new_user_not_detected_frame.grid_forget()
    create_widgets_in_entry_allowed_frame()
    entry_allowed_frame.grid(column=0, row=0, padx=20, pady=5, sticky=(tkinter.W, tkinter.N, tkinter.E))

def call_complete_entry_database_frame_on_top():
    e2.delete(0,tkinter.END)
    e4.delete(0,tkinter.END)
    verify_no_plate_frame.grid_forget()
    new_user_not_detected_frame.grid_forget()
    create_widgets_in_complete_entry_database_frame()
    complete_entry_database_frame.grid(column=0, row=0, padx=20, pady=5, sticky=(tkinter.W, tkinter.N, tkinter.E))

def call_exit_allowed_frame_on_top():
    start_frame.grid_forget()
    exit_if_plate_not_recognised_frame.grid_forget()
    create_widgets_in_exit_allowed_frame()
    exit_allowed_frame.grid(column=0, row=0, padx=20, pady=5, sticky=(tkinter.W, tkinter.N, tkinter.E))

def call_exit_if_plate_not_recognised_frame_on_top():
    e3.delete(0,tkinter.END)
    start_frame.grid_forget()
    create_widgets_in_exit_if_plate_not_recognised_frame()
    exit_if_plate_not_recognised_frame.grid(column=0, row=0, padx=20, pady=5, sticky=(tkinter.W, tkinter.N, tkinter.E))


def quit_program():
    root_window.destroy()

###############################
# Main program starts here  #
###############################





# Create the root GUI window.
root_window = tkinter.Tk()
root_window.title("Gate Entry Exit System")
string_form_no_plate=tkinter.StringVar()
string_form_no_plate_2=tkinter.StringVar()
string_form_phone_no=tkinter.StringVar()
string_form_name=tkinter.StringVar()
var=tkinter.IntVar()
# Define window size
window_width = 1500
window_heigth = 300



# Create frames inside the root window to hold other GUI elements. All frames must be created in the main program, otherwise they are not accessible in functions. 
start_frame=tkinter.ttk.Frame(root_window, width=window_width, height=window_heigth)
start_frame['borderwidth'] = 2
start_frame['relief'] = 'sunken'
start_frame.grid(column=0, row=0, padx=20, pady=5, sticky=(tkinter.W, tkinter.N, tkinter.E))

new_user_not_detected_frame=tkinter.ttk.Frame(root_window, width=window_width, height=window_heigth)
new_user_not_detected_frame['borderwidth'] = 2
new_user_not_detected_frame['relief'] = 'sunken'
new_user_not_detected_frame.grid(column=0, row=0, padx=20, pady=5, sticky=(tkinter.W, tkinter.N, tkinter.E))
e1=tkinter.Entry(new_user_not_detected_frame,textvariable=string_form_no_plate)

verify_no_plate_frame=tkinter.ttk.Frame(root_window, width=window_width, height=window_heigth)
verify_no_plate_frame['borderwidth'] = 2
verify_no_plate_frame['relief'] = 'sunken'
verify_no_plate_frame.grid(column=0, row=0, padx=20, pady=5, sticky=(tkinter.W, tkinter.N, tkinter.E))

entry_allowed_frame=tkinter.ttk.Frame(root_window, width=window_width, height=window_heigth)
entry_allowed_frame['borderwidth'] = 2
entry_allowed_frame['relief'] = 'sunken'
entry_allowed_frame.grid(column=0, row=0, padx=20, pady=5, sticky=(tkinter.W, tkinter.N, tkinter.E))

complete_entry_database_frame=tkinter.ttk.Frame(root_window, width=window_width, height=window_heigth)
complete_entry_database_frame['borderwidth'] = 2
complete_entry_database_frame['relief'] = 'sunken'
complete_entry_database_frame.grid(column=0, row=0, padx=20, pady=5, sticky=(tkinter.W, tkinter.N, tkinter.E))
e2=tkinter.Entry(complete_entry_database_frame,textvariable=string_form_phone_no)
e4=tkinter.Entry(complete_entry_database_frame,textvariable=string_form_name)

exit_allowed_frame=tkinter.ttk.Frame(root_window, width=window_width, height=window_heigth)
exit_allowed_frame['borderwidth'] = 2
exit_allowed_frame['relief'] = 'sunken'
exit_allowed_frame.grid(column=0, row=0, padx=20, pady=5, sticky=(tkinter.W, tkinter.N, tkinter.E))

exit_if_plate_not_recognised_frame=tkinter.ttk.Frame(root_window, width=window_width, height=window_heigth)
exit_if_plate_not_recognised_frame['borderwidth'] = 2
exit_if_plate_not_recognised_frame['relief'] = 'sunken'
exit_if_plate_not_recognised_frame.grid(column=0, row=0, padx=20, pady=5, sticky=(tkinter.W, tkinter.N, tkinter.E))
e3=tkinter.Entry(exit_if_plate_not_recognised_frame,textvariable=string_form_no_plate_2)


# Creating widhets for the start frame
create_widgets_in_start_frame()

# Hide all frames in reverse order, but leave start frame visible (unhidden).
exit_if_plate_not_recognised_frame.grid_forget()
exit_allowed_frame.grid_forget()
complete_entry_database_frame.grid_forget()
entry_allowed_frame.grid_forget()
verify_no_plate_frame.grid_forget()
new_user_not_detected_frame.grid_forget()

# Start tkinter event - loop
root_window.mainloop()
