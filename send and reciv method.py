from my_udp_adapted import MyUDP

socket = MyUDP()

def send_file(file,dest_addr):
    file = open(file,"r")
    data="**{file.name}**}"######
    data += file.read()
    file.close()
    socket.send(data.encode(),dest_addr)

def send_message(message,dest_addr):
    message="*msg*"+message
    socket.send(message.encode(),dest_addr)


def recv(buffer_size):
    data = socket.recv(buffer_size)

    if(data[0:5].decode()=="*msg*"):
        return data[5:].decode()
    else:
        file_name = data[2:data.find("}**")]########
        data=data[data.find("}**")+3:]##########

        file = open(file_name,"w")
        file.write(data)
        file.close()





    

def recv_message(buffer_size):
    data = socket.recv(buffer_size)
    return data.decode()

