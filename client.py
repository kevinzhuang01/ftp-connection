import socket # Used for socket connection
import sys # Used to get size of object in bytes
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

def connect() -> None:
    print('Sending server request')

    try:
        socket_connection.connect((tcp_ip,tcp_port))
        print('Connection Succeeded!')
    except:
        print('Connection Unsuccessful. Check if server is online!')

#TO-DO: Upload File
def upload_file(file_name)-> None:
    print("\nUploading file: {}...".format(file_name))

    # Check if the file exists
    try:
        
        content = open(file_name, "rb")
    except FileNotFoundError:
        print("Couldn't open file. Make sure the file name was entered correctly.")
        return
    
    # Make upload request
    try:
        
        socket_connection.send("Upload".encode())
    except Exception as e:
        print(f"Couldn't make server request. Make sure a connection has been established. Error: {e}")
        return
    
    # Wait for server acknowledgement then send file details and wait for server 'OK'
    try:
        
        socket_connection.recv(buffer_size)

        # Send file name size and file name
        socket_connection.send(struct.pack("h", len(file_name)))  # Send the length of the file name
        socket_connection.send(file_name.encode())  # Send the file name

        # Wait for server 'OK' then send file size
        socket_connection.recv(buffer_size)
        file_size = os.path.getsize(file_name)
        socket_connection.send(struct.pack("i", file_size))  
    except Exception as e:
        print(f"Error sending file details. Error: {e}")
        return

    # Send the file in chunks defined by buffer size and allows sending files of unlimited size
    try:
        
        print("\nSending...")
        while (chunk := content.read(buffer_size)):
            s.send(chunk)
        content.close()

        # Gets file upload time and upload file size
        upload_time = struct.unpack("f", s.recv(4))[0]  
        upload_size = struct.unpack("i", s.recv(4))[0]  

        print("\nSent file: {}\nTime elapsed: {}s\nFile size: {}b".format(file_name, upload_time, upload_size))
    except Exception as e:
        print(f"Error sending file. Error: {e}")
        return


def list_files()-> None:
    print('Requesting Files...\n')

    try:
        socket_connection.send('List')
    except:
        print("Couldn't make server request. Make sure a connection has been established")
        return
    
    try:
        number_of_files = struct.unpack("i", socket_connection.recv(4))[0]

        for i in range(int(number_of_files)):
            file_name_size = struct.unpack("i", socket_connection.recv(4))[0]
            file_name = socket_connection.recv(file_name_size)
            file_size = struct.unpack("i", s.recv(4))[0]
            print("\t{} - {}b".format(file_name, file_size))

        socket_connection.send('1')

        total_directory_size = struct.unpack("i", socket_connection.recv(4))[0]
        print( "Total directory size: {}b".format(total_directory_size))
    except:
        print("Couldn't retrieve listing")
        return
    try:
        socket_connection.send('1')
        return
    except:
        print("Server couldn't get confirmation")
        return
    