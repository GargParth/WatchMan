import socket
import select
import os
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)


# get the name and the address of the host
host_name = socket.gethostname()
host_ip = '192.168.165.169'

# define a PORT
host_port = 3000

# define a server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Allow the address to be used again and again
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind the ip and port to this socket to inform the os
# which socket is going to be used
server_socket.bind((host_ip,host_port))

# This makes the server listen for new connections
server_socket.listen()

# List of sockets
sockets_list = [server_socket]

print("listening for new connections on {host_ip}:{host_port} ...")

# main while loop to check for connections
while True:
    read_sockets, write_sockets, error_list = select.select(sockets_list, sockets_list, sockets_list)

    for notified_socket in read_sockets:
        # checking all the sockets in the reading_list returned by select

        if notified_socket == server_socket:
            # This means that another client triend to connect to the RPi

            client_socket, client_address = server_socket.accept()
            print("got connection from " + client_address[0])

            # Now receive the first message to authenticate the client
            first_check = client_socket.recv(1024).decode('utf-8')
            
            if first_check == "Allow Entry":
                GPIO.output(11,GPIO.HIGH)
                time.sleep(5)
                GPIO.output(11,GPIO.LOW)
                
            if first_check == "ALLOW EXIT":
                print("EXITYYYY")
                GPIO.output(12,GPIO.HIGH)
                time.sleep(5)
                GPIO.output(12,GPIO.LOW)

            if first_check == "obey me":
                # the client has been authenticated
                # send an acknowledgement
                client_socket.send("yes master".encode())

                message = client_socket.recv(1024).decode('utf-8')

                if message == "initiate entry procedure":
                    # a car is requesting entry 
                    client_socket.send("initiating entry procedure".encode())
                    # take a picture from the entry camera
                    os.system("fswebcam -r 1920 -d /dev/video0 --no-banner /home/pi/Desktop/img.jpg")
                    os.system("python3 openalpr.py")
                    myfile = open("license plate.txt",'rb')
                    data = myfile.read() #Store the license plate in byte form
                    myfile.close()
                    client_socket.send("picture taken and plate identified".encode())
                    print("HI")
                    message = client_socket.recv(1024).decode('utf-8')
                    print(message)

                    if message == "License Plate":
                        # send the license plate number to the masters
                        myfile = open("license plate.txt", 'rb')
                        data = myfile.read()
                        myfile.close()
                        client_socket.send(data)

                        message = client_socket.recv(1024).decode('utf-8')
                        

                        if message == "photograph":
                            image = open("img.jpg", 'rb')
                            data = image.read()
                            header = str(len(data))
                            header_length = 10
                            while(len(header)<header_length):
                                header+=" "
                            client_socket.send(str(header).encode())
                            print(header)

                            client_socket.send(data)
                            image.close()

                            message = client_socket.recv(1024).decode('utf-8')
                            if(message=="error"):
                                break
                            
                            message = client_socket.recv(1024).decode('utf-8')
                            if message == "found":
                                GPIO.output(11,GPIO.HIGH)
                                print("hello")
                                time.sleep(5)
                                GPIO.output(11,GPIO.LOW)
                            elif message == "found exit":
                                GPIO.output(12,GPIO.HIGH)
                                time.sleep(5)
                                GPIO.output(12, GPIO.LOW)
                
                elif message == "initiate exit procedure":
                    # a car is requesting entry 
                    client_socket.send("initiating entry procedure".encode())
                    # take a picture from the entry camera
                    os.system("fswebcam -r 1920 -d /dev/video2 --no-banner /home/pi/Desktop/img.jpg")
                    os.system("python3 openalpr.py")
                    myfile = open("license plate.txt",'rb')
                    data = myfile.read() #Store the license plate in byte form
                    myfile.close()
                    client_socket.send("picture taken and plate identified".encode())
                    print("HI")
                    message = client_socket.recv(1024).decode('utf-8')
                    print(message)

                    if message == "License Plate":
                        # send the license plate number to the masters
                        myfile = open("license plate.txt", 'rb')
                        data = myfile.read()
                        myfile.close()
                        client_socket.send(data)

                        message = client_socket.recv(1024).decode('utf-8')
                        

                        if message == "photograph":
                            image = open("img.jpg", 'rb')
                            data = image.read()
                            header = str(len(data))
                            header_length = 10
                            while(len(header)<header_length):
                                header+=" "
                            client_socket.send(str(header).encode())
                            print(header)

                            client_socket.send(data)
                            image.close()

                            message = client_socket.recv(1024).decode('utf-8')
                            if(message=="error"):
                                break
                            
                            message = client_socket.recv(1024).decode('utf-8')
                            if message == "found":
                                GPIO.output(11,GPIO.HIGH)
                                print("hello")
                                time.sleep(5)
                                GPIO.output(11,GPIO.LOW)
                            elif message == "found exit":
                                GPIO.output(12,GPIO.HIGH)
                                time.sleep(5)
                                GPIO.output(12, GPIO.LOW)
                                
                            
                            

                            
                            
