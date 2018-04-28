import serial
import time
#mport winsound


def open_port():
    ser = serial.Serial('/dev/ttyUSB0', 115200) # o "COM12" en windows

    return ser


def close_port(port):
    port.close()

def read_buffer(port):
    if (port.in_waiting != 0):
        string = str(port.read(port.in_waiting))
        string = string.replace("b'", "")
        string = string.replace("'", "")
        return  string
    else:
        return 0




def main():
    port = open_port()
    port.write("\r".encode("utf-8"))
    ini = time.time()
    fin = time.time()
    delta = fin-ini
    while(delta < 3):
        time.sleep(0.1)
        data = read_buffer(port)
        if data != 0:
            print(data)


           # if (buff  != 0):
           # port.write("GV\r".encode("utf-8"))

        delta = time.time()-ini

    close_port(port)





if __name__ == "__main__": main()
