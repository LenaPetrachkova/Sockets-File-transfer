import socket
import logging
import datetime
import os


HOST = '127.0.0.1'   # Host address
PORT = 1025 + 2      # Port
utf = 'utf-8'        # Enoding
BUFSIZE = 1024       # Buffer size

class Server:
    def __init__(self):

        # Create a socket object:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:

            # Configure event logging:
            logging.getLogger("Server")
            logging.basicConfig(filename="myServer.log",
                                level=logging.INFO,
                                format='%(asctime)s - %(levelname)s - %(message)s',
                                filemode='a',
                                )
            logging.info("Server started")

            # Bind the socket to the host address and port:
            try:
                sock.bind((HOST, PORT))
            except OSError:
                print("Host is used.")
                logging.warning("HOST IS USED. ")
                exit()

            # Listen for incoming connections:
            sock.listen(10)
            connection, client_address = sock.accept()

            print("Connected: ", client_address)
            logging.info("Connected to a client. ")

            # Send a welcome message to the client:
            for sentence in self.welcomeMessage():
                connection.send(sentence.encode(utf))
            logging.info("Sent a welcome message.")

            print("Listening")
            logging.info('Listening to a client.')

            try:
                while True:

                    # Receive data from the client:
                    data = connection.recv(256).decode(utf)
                    logging.info(f'Received message: {data}')
                    print(data)
                    if not data:
                        break
                    if data == "who":
                        results = self.whoInfo()
                        connection.send(results.encode(utf))
                        logging.info("Sent message: " + results)
                    elif data == "Send file":
                        results = "Received file"
                        connection.send(results.encode(utf))
                        file_name = connection.recv(BUFSIZE).decode()
                        logging.info("Sent message: " + results + " " + file_name)

                        # Receive and save the file sent by the client:
                        f = open(file_name, 'wb')
                        file_size = os.path.getsize("C:\\Users\\Professional\\PycharmProjects\\laba_Socket\\Client\\" + file_name)

                        take_file_size = 0
                        time = datetime.datetime.now()
                        while True:
                            taken_data = connection.recv(BUFSIZE)
                            f.write(taken_data)
                            time1: int = (datetime.datetime.now() - time).microseconds   # Calculate the time elapsed since receiving the first block of data.
                            take_file_size += len(taken_data)  # Calculate the total size of received data by adding the length of the last block of data.
                            file_size1 = take_file_size
                            if time1 > 0:    # Calculate the data transfer speed as the ratio of the length of the last block of data to the time elapsed.
                                speed = len(taken_data) / time1
                            else:
                                speed = 0
                            print("За цей раз прийнято: ", len(taken_data))
                            print("Загалом прийнято: ", take_file_size)
                            print(100 / (file_size / file_size1), "%")  # Calculate the percentage of file transfer completion as the ratio of the current file size to the total size.
                            print("Speed = ", speed)
                            print("")
                            if take_file_size == file_size:
                                break
                    elif data == "End":
                        results = "Stop"
                        connection.send(results.encode(utf))
                        logging.info("Sent message: " + results)
                        logging.info("The end of session")
                        break
                    else:
                        results = "Unknown command, please try again"
                        connection.send(results.encode(utf))
                        logging.info("Sent message: " + results)
            except Exception as e:
                print(f"ERROR.{e}")
                connection.send("STOP".encode(utf))
                logging.error("Caught en error. Closing connection.")
        finally:
            try:
                connection.close()
            except Exception as e:
                print(f' !Exception {e}')
                logging.warning(f'{e}')
            print("Connection closed.")

    def welcomeMessage(self):
        welcome = [
            "Welcome! With this program you can send selected files to the server.\n",

            "List of commands available in this program:\n"
            "1. Enter 'Send file' and path to your file to send file to server.\n"
            "2. Enter 'who' to read information about me.\n"
            "3. Enter 'End' to stop the program\n",
        ]
        return welcome

    def whoInfo(self):
        who = 'Hello! My name is Lena Petrachkova. My group is K-16. File transfer, №2'
        return who


def main():
    root = Server()


if __name__ == "__main__":
    main()
