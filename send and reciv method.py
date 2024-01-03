from my_udp_adapted import MyUDP

socket = MyUDP()

def send_file(file,dest_addr):
    file = open(file,"r")
    data = file.read()
    file.close()
    socket.send(data.encode(),dest_addr)

def send_message(message,dest_addr):
    socket.send(message.encode(),dest_addr)


def recv_file(file_name,buffer_size):
    data = socket.recv(buffer_size)
    file = open(file_name,"w")
    file.write(data)
    file.close()

def recv_message(buffer_size):
    data = socket.recv(buffer_size)
    return data.decode()
