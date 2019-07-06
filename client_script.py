import socket
import sys
import time

def main():
    open("./message_back.txt","w").close()
    for x in range(0,150):
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = "10.0.0.2"
        port = 42000

        try:
            soc.connect((host, port))
        except:
            print("Connection error")
            sys.exit()

        #print("Enter 'quit' to exit")
        #message = input(" -> ")
        message = "bruh"

        soc.sendall(message.encode("utf8"))
        data = soc.recv(65000)
        with open("./message_back.txt","a+") as f:
            f.write(data.decode()+"\n")
        #print(data.decode())
        time.sleep(1)
        soc.close()

if __name__ == "__main__":
    main()
