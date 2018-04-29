import serial
import time
import numpy as np
import matplotlib.pyplot as plt
import cv2
#mport winsound


def open_port():
    ser = serial.Serial('/dev/ttyUSB0', 115200) # o "COM12" en windows

    return ser


def close_port(port):
    port.close()

def read_buffer(port):
    buff = ""
    size = 0
    while (port.in_waiting != 0):
        size_toread =port.in_waiting
        size = size+size_toread
        string = str(port.read(size_toread))
        string = string.replace("b'", "")
        string = string.replace("'", "")
        buff = buff+string
        time.sleep(0.01)

    return  buff, size

def read_F(port): # leer paquete tipo f (raw image)
    buff = np.array([], dtype="uint8")
    size = 0
    while (port.in_waiting != 0):
        size_toread =port.in_waiting
        data = port.read(size_toread)
        for bytes in data:
            buff = np.append(buff, [bytes], 0)
        time.sleep(0.5)

    return  buff

def decode_F(packet):
    state = "INIT"
#  print("Canvas = {}".format(canvas))
    if (state == "INIT"):
        header = chr(packet[0])+chr(packet[1])+chr(packet[2]) #ACK
        new_frame = packet[4] # new frame btye
        print(header)
        if (header == "ACK") and (new_frame == 1):
            print("Header e inicio de Frame ok")
            state = "Read_frame" # y  cambiar de estado a leer frame
        else:
            print("Error en la cabecera")
            return 0
    if (state == "Read_frame"):
        cols_index , = np.where(packet == 2)
        n_cols = cols_index.size
        n_rows = int((cols_index[1]-cols_index[0]- 1)/3) # restar indices de columnas -1, es el numero de filas*3
        print("Filas = {}, Columnas = {}".format(n_rows, n_cols))
        # Crear imagen
        canvas = np.zeros((n_rows, n_cols, 3), dtype="uint8")
        for col in range(n_cols):
            i = cols_index[col] - n_rows * 3  # indice del primer elemento (color r) en la trama de la columna
            for row in range(n_rows):
                r = i+row*3
                canvas[row, col] = [packet[r+2], packet[r+1],packet[r]]  # bgr (formato opencv)
        return canvas



def main():
    port = open_port()
    port.reset_input_buffer()
    print("Bienvenido\nEscriba el comando a enviar a la camara: (q para salir)")
    command = input()
    while (command != "q"):

        if (command == "DF"):
            port.write((command + "\r").encode("utf-8"))
            time.sleep(0.1)
            tini = time.time()
            data = read_F(port)
            print(data)
            canvas = decode_F(data)
            canvas_raw = cv2.flip(canvas, -1) # Reajuste a la imagen original vista por la camara
            print(time.time() - tini)
            plt.figure("CMUcam1")
            image = cv2.flip(canvas, 0)
            plt.subplot(1, 2, 1)
            plt.title("Imagen cruda")
            plt.imshow(canvas_raw[..., ::-1])
            plt.subplot(1, 2, 2)
            plt.title("Imagen Flip")
            plt.imshow(image[..., ::-1])
            plt.show()


            print("\nEscriba otro comando a enviar a la camara: (q para salir)")
            command = input()



        else :
            port.write((command+"\r").encode("utf-8"))
            time.sleep(0.1)
            tini = time.time()
            data, size = read_buffer(port)
            if data != 0:
                print("Se ha recibido:")
                print(data)
                print (size)
            print(time.time()-tini)

            print("\nEscriba otro comando a enviar a la camara: (q para salir)")
            command = input()

    print("Finished")
    close_port(port)






if __name__ == "__main__": main()
