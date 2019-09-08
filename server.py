import time
import socket
import select
import datetime
import os

#get the name and the address of the host
host_name = socket.gethostname()
host_ip = str(socket.gethostbyname(host_name))
host_ip = "127.0.0.1"

# define a port
PORT = 1234

# define a server socket
# socket.AF_INET - address family, IPv4
# socket.SOCK_STREAM - TCP, connection based
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# SO_ - socket option
# SOL - socket option level
# Sets REUSADDR (as socket option) to 1
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind the IP and the port to this socket to inform the OS
# which IP and port is going to be used
server_socket.bind((host_ip, PORT))

#This makes the server listen for new connections
server_socket.listen()

# List of sockets
sockets_list = [server_socket]


print(f'Listening for connections on {host_ip}:{PORT} ...')


# main while loop coming up ahead
while True:

    # calls Unix select() system call or windows select() winsock call with three parameters:
    #   - rlist - sockets to be monitored for incoming data
    #   - wlist - sockets for data to be send to (checks if for example buffers are not full and the socket is ready to send/recieve some data)
    #   - xlist - sockets to be monitored for any form of exceptions (we want to monitor all sockets for errors, so we can use rlist)
    # Returns 3 lists:
    #   - reading - sockets we recieved any form of data on (so that we dont have to check sockets manually)
    #   - writing - sockets ready for data to be sent through them
    #   - errors  - sockets with any form of exceptions
    # This is a blocking call, code execution will "wait" here and "get" notified in case any action is to be taken

    read_sockets, write_sockets, error_list = select.select(sockets_list, sockets_list, sockets_list)

    for notified_socket in read_sockets:
        #checking all the sockets in the reading list returned by select.celect()

        if notified_socket == server_socket:
            # this means that another client tried to connect to the server
            # accept the new connection
            # that gives us a new socket, the client socket - accept and connect to it
            # the other returned socket is the ip/port set
            client_socket, client_address = server_socket.accept()

            # now recieve the first message right way
            first_check = client_socket.recv(2048).decode('utf-8')

            # now check if the first message recieved is the one intended
            # else, close the connection

            if first_check == "Hi SeRvEr":
                # correct message was sent, the client is one of the recognized clients
                # add this client to the list of sockets available to us for I/O
                sockets_list.append(client_socket)
                print('Accepted new connection from '+client_address[0])

                # connection succesfully established, ask the type of request being made
                client_socket.send("request type".encode())

                # now read the message from the client
                message = client_socket.recv(1024).decode()

                if message == "Authenticate Entry":
                    duplicate = False
                    flag = False
                
                    # The client wants to authenticate the precense of a license 
                    # plate in our databse
                    # ask the client for the license plate number
                    client_socket.send("License Plate Number".encode())

                    # Receive the license plate from the client
                    License_plate_number = client_socket.recv(1024).decode('utf-8')
                    # check if this number exists in your records here
                    records = open('registered users.txt', 'r')
                    myfile = open("in campus.txt",'r')
                    data = open("user data.txt", 'r')
                    logs = open("logs.txt", 'a')
                   
                    print("Step 1    ")
                    for plates in myfile:
                        print("Step 2    ")
                        plates = plates.rstrip()
                        # check all the plates in myfile
                        if plates == License_plate_number:
                            # this record is a duplicatte one
                            duplicate = True
                            print("Step 3    ")
                            break
                    myfile.close()

                    myfile = open("in campus.txt", 'a')
                
                    print("Step 4    ")
                    if duplicate==False:
                        plate = License_plate_number+str("\n")
                        myfile.write(plate)
                        print("Step 5    ")
                    
                    for plates in records:
                        print("Step 6    ")
                        plates = plates.rstrip()
                        if plates == License_plate_number:
                            # The record exists in our records
                            flag = True
                            #now update the log file
                            print("Step 7    ")
                            data_value = None
                            for record in data:
                                entry = record.split(',')
                                print("Step 8    ")
                                if entry[0] == License_plate_number and duplicate==False:
                                    print("Step 9    ")
                                    ts_epoch = time.time()
                                    ts = datetime.datetime.fromtimestamp(ts_epoch).strftime('%d-%m-%y %H:%M:%S')
                                    data_value = record[0 : len(record)-1] + "," + str(ts)+"\n"
                                    logs.write(data_value)
                                    logs.flush()

                    records.close()
                    myfile.close()
                    data.close()
                    logs.close()
                    print("Step 10    ")

                    if (flag==True):
                        # record found, tell the client
                        client_socket.send("Present".encode())

                    else:
                        # record not found, tell the client
                        client_socket.send("No Record Found".encode())

                
                
                
                elif message == "Authenticate Exit":
                    # The client wants to authenticate the precense of a license 
                    # plate in our databse
                    # ask the client for the license plate number
                    client_socket.send("License Plate Number".encode())

                    # Receive the license plate from the client
                    License_plate_number = client_socket.recv(1024).decode('utf-8')
                    # check if this number exists in your records here
                    in_campus = open("in campus.txt", 'r')
                    
                    exit_checker = False
                    for plate in in_campus:
                        plate = plate.rstrip()
                        print(plate)
                        print(License_plate_number)
                        if plate == License_plate_number:
                            # The car is authorised for entry, its entry was registered
                            # everything went fine with it
                            client_socket.send("Present".encode())
                            exit_checker = True
                            
                    print(str(exit_checker)+"  my name s parth")
                    if exit_checker == True:
                        # we need to update the log file to account for exit time
                        exit_epoch = time.time()
                        exit_time = datetime.datetime.fromtimestamp(exit_epoch).strftime('%d-%m-%y %H:%M:%S')
                        updated_logs = open("new_logs.txt", "w")
                        current_logs = open("logs.txt",'r')

                        for entry in current_logs:
                            value = entry.split(",")
                            plate = value[0]
                            plate = plate.rstrip()
                            print("step 1")
                            print(len(License_plate_number))
                            if plate == License_plate_number:
                                entry = str(entry)
                                entry = entry[0:len(entry)-1]
                                entry = entry + ","+str(exit_time)+"\n"
                                print(entry)

                            updated_logs.write(entry)

                        updated_logs.close()
                        current_logs.close()
                        os.remove("logs.txt")
                        os.rename('new_logs.txt', 'logs.txt')

                        #now delete that entry from the in_campus file
                        current = open("in campus.txt", 'r')
                        new = open('in_campus_new.txt', 'w')
                        
                        for plate in current:
                            plate = plate.rstrip()
                            if plate != License_plate_number:
                                plate=plate+"\n"
                                new.write(plate)
                        
                        current.close()
                        new.close()
                        os.remove('in campus.txt')
                        os.rename('in_campus_new.txt', "in campus.txt")

                    else:
                        # There was some problem either while entry registeration
                        # or exit detection of this car, allow exit, but keep track
                        # of this error
                        client_socket.send("Present".encode())
                        error_file = open("errors.txt", 'a')
                        plate = License_plate_number + "\n"
                        error_file.write(plate)
                        error_file.close()

                        



                elif message == "Register user":
                    # the client side wants to register a user
                    # ask all the essential details
                    client_socket.send("Send Info".encode())
                    info = client_socket.recv(1024).decode('utf-8')
                    info = info.split(";")
                    print(info)
                    License_plate_number = info[0]
                    Name = info[1]
                    phone_number = info[2]
                    owner_type = info[3]

                    records = open('registered users.txt', 'a')
                    final_value = str(License_plate_number)+"\n"
                    records.write(final_value)
                    records.flush()
                    records.close()

                    fin_string = License_plate_number + ","+Name+","+phone_number+","+owner_type+"\n"
                    database = open('user data.txt', 'a')
                    database.write(fin_string)
                    database.flush()
                    database.close()


                    # test code starts
                    in_campus = open('in campus.txt', 'a')
                    writer = License_plate_number + "\n"
                    in_campus.write(writer)
                    in_campus.flush()
                    in_campus.close()

                    logs = open("logs.txt", 'a')
                    writer = License_plate_number+","+Name+","+owner_type+","
                    ts_epoch = time.time()
                    in_time = datetime.datetime.fromtimestamp(ts_epoch).strftime('%d-%m-%Y %H:%M:%S')
                    writer = writer + str(in_time) + "\n"
                    logs.write(writer)
                    logs.flush()
                    logs.close()

                    client_socket.send("registration complete".encode())
            else:
                # client failed the first check
                # close its connection
                client_socket.close()
                print('Rejected a new connection from '+client_address[0])

                