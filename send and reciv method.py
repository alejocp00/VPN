from my_udp_adapted import MyUDP
import os

socket = MyUDP()

def send_file(self,file,dest_addr):

    current_dir = os.getcwd()

    file_path = os.path.join(current_dir,"SEND", file)
    file_name = file

    file = open(file_path,"r")
    data="*"+file_name+"*"
    data += file.read()
    file.close()
    self.socket.udp_send(data.encode(),dest_addr)

def send_message(self,message,dest_addr):
    message="*msg*"+message
    self.socket.udp_send(message.encode(),dest_addr)


def recv(self,buffer_size):
    data,addr = self.socket.udp_recv(buffer_size)

    if(data[0:5]=="*msg*"):
        return data[5:],addr
    elif(data==""):
        return "ERROR",addr
    else:
        file_name =""
        i = 1
        while data[i] != "*":
            file_name += data[i]
            i+=1

        print(file_name)
            

        data=data[i+1:]

        current_dir = os.getcwd()

        receive_dir = os.path.join(current_dir, "RECEIVE")
        if not os.path.exists(receive_dir):
            os.makedirs(receive_dir)
    

        file_path = os.path.join(receive_dir, file_name)

        with open(file_path, "w") as file:
            file.write(data)

        return file_name,addr

