import socket
import logging
import datetime
import os

HOST = '127.0.0.1'
PORT = 1025 + 2
ADDR = (HOST, PORT)
BUFSIZE = 1024


class Client:
    def __init__(self):
        try:

            # Create a socket object to connect to the server:
            sock = socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM,
            )

            # Configure event logging:
            logging.getLogger("Client")
            logging.basicConfig(filename="myClient.log",
                                level=logging.INFO,
                                format='%(asctime)s - %(levelname)s - %(message)s',
                                filemode='a',
                                )
            logging.info('Client started.')

            # Connect to the server:
            sock.connect((HOST, PORT))
            logging.info("Connected to a server.")
            while True:
                # Отримання повідомлень від сервера:
                data = sock.recv(256).decode('utf-8')
                print(data)

                if data.__contains__("to stop the program"):
                    break

            logging.info('Got welcome message.')
            while True:
                # Receive messages from the server:
                data = input('Send request:\n')
                sock.send(data.encode('utf-8'))

                if data == "Send file":
                    file_name = input('Enter file name: ')
                    file_size = os.path.getsize(file_name)
                    send_file_size = 0
                    sock.send(file_name.encode())
                    f = open(file_name, 'rb')  # Open the file for reading in binary mode
                    sent_data = ""
                    time = datetime.datetime.now()

                    while sent_data != b'':
                        sent_data = f.read(BUFSIZE)  # Read a block of data from the file
                        sock.send(sent_data)
                        time1: int = (datetime.datetime.now() - time).microseconds   # Measure the time of data transfer
                        send_file_size += len(sent_data)  # Calculate the total size of sent data
                         # Calculate the transfer speed:
                        if time1 != 0:
                            speed = (len(sent_data) / time1)
                        else:
                            speed = 0
                        print("Надіслано за цей раз: ", len(sent_data))
                        print("Надіслано всього: ", send_file_size)
                        print(100 / (file_size / send_file_size), "%")    # Percentage of data transfer
                        print("Speed = ", speed)
                        print("")

                    time0 = datetime.datetime.now().microsecond - time.microsecond  # Total transfer time of the file
                    print("Загальний час передачі файлу (microseconds): ", time0)
                    print("Передано всього байтів: ", send_file_size)

                logging.info('Sent request: ' + data)
                
                # Receive and process the response from the server:
                data = sock.recv(256).decode('utf-8')
                logging.info('Received message: ' + data)
                print('Answer: ', data)
                if 'Stop' in data or 'STOP' in data:
                    sock.close()
                    logging.info("End of session")
                    break
                else:
                    continue

            print('Connection closed.')
            logging.info('Connection closed.')

        except Exception as e:
            print(f'Happened exception: {e}')
            logging.info('Caught an error. Closing connection.')


def main():
    client = Client()


if __name__ == "__main__":
    main()
