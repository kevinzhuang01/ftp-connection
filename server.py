import socket # Used for socket connection
import sys # Used to get size of object in bytes
import time 
import os # Used for Operating System functions
import struct # Used for data exchange with external sources( Files/ Network Connections)

print("\nWelcome to the FTP server.\n\nTo get started, connect a client.")

"""
Initialize socket pre-reqs
Then create socket connection

"""

tcp_ip = '127.0.0.1' 
tcp_port = 2371
buffer_size = 1024

socket_connection =socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Indicates this is socket is TCP (connection-oriented protocol)
socket_connection.bind((tcp_ip,tcp_port))


socket_connection.listen(1)

connection,address = socket_connection.accept()
print('\nConnected to by address: {}'.format(address))

"""
Upload Function:
- Establish connection
- Receives file size and processes content inside file
- Send upload details
"""

def upload_files() -> None:
    connection.send('1')

    file_name_size = struct.unpack('h',connection.recv(2))[0]
    file_name = connection.recv(file_name_size)

    connection.send('1')
   
    file_size = struct.unpack("i", connection.recv(4))[0]
    
    start_time = time.time()
    output_file = open(file_name, "wb")
    
    bytes_received = 0

    print("\nReceiving...")

    while bytes_received < file_size:
        l = connection.recv(buffer_size)
        output_file.write(l)
        bytes_received += buffer_size
        output_file.close()

    print("\nReceived file: {}".format(file_name))
    
    connection.send(struct.pack("f", time.time() - start_time))
    connection.send(struct.pack("i", file_size))
    return

"""
List Files:
- List the files in the current directory
- Sends over the number of files so client knows what to expect
- File contains size,name,content size
"""

def list_files()-> None:
    print("Listing files...")

    listing = os.listdir(os.getcwd())

    connection.send(struct.pack("i", len(listing)))
    total_directory_size = 0
    
    for i in listing:
    
        connection.send(struct.pack("i", sys.getsizeof(i)))
       
        connection.send(i)
        
        connection.send(struct.pack("i", os.path.getsize(i)))
        total_directory_size += os.path.getsize(i)
        
        connection.recv(buffer_size)
        
        connection.send(struct.pack("i", total_directory_size))
        
        connection.recv(buffer_size)
    print("Successfully sent file listing")
    return

def download_files()-> None:
    connection.send('1')

    file_name_length = struct.unpack('h',connection.recv(2))[0]

    print(file_name_length)

    file_name = connection.recv(file_name_length)

    print(file_name)

    if os.path.isfile(file_name):
        connection.send(struct.pack('i',os.path.getsize(file_name)))
    else:
        print('File name not valid')
        connection.send(struct.pack('i',-1))
        return

    connection.recv(buffer_size)
  
    #Sending file and unpacking content (current_time vs start_time)
    #TO-DO: Send download details and break data into chunks


"""
Delete Files:
- Checks if file details and checks if directory exists
- If client presses 'Y' , it confirms the deletion of file
"""

def delete_files()-> None:
    connection.send(1)

    file_name_length = struct.unpack("h", connection.recv(2))[0]
    file_name = connection.recv(file_name_length)

    if os.path.isfile(file_name):
        connection.send(struct.pack("i", 1))
    else:
        connection.send(struct.pack("i", -1))
        
        confirm_delete= connection.recv(buffer_size)
        if confirm_delete == 'Y':
            try:
                os.remove(file_name)
                connection.send(struct.pack('i',1))
            except:
                print("Failed to delete {}".format(file_name))
                connection.send(struct.pack("i", -1))
        else:
            print('Deleting Process Canceled by Client!')
    return

"""
Quit Program:
- Sends a connection to confirm to quit
- Closes and restarts the server
"""

def quit_program()-> None:
    #TO-DO: Getting Errors
    connection.send(1)
    connection.close()
    socket.close()
    return



"""
 Enter into a while loop to receive commands from client
"""
while True:

    print("\n\nWaiting for instruction")
    data = connection.recv(buffer_size)
    print("\nReceived instruction: {}".format(data))
    
    if data == "Upload":
        upload_files()
    elif data == "List":
        list_files()
    elif data == "Download":
        download_files()
    elif data == "Delete":
        delete_files()
    elif data == "QUIT":
        quit_program()

    # Reset the data to loop
    data = None