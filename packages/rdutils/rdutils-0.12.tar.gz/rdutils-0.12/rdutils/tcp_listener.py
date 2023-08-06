"""
TCP listener designed to mimic the netstat command in ubuntu
"""
import socket
import time
import argparse
from threading import Thread


class TCPListener:

    def __init__(self, port, threaded=True, print_flag=False):
        """Constructor

        Args:
            port (int): Port to start the TCP Listener on
            threaded (bool, optional): Defines if the Lister should run in its own thread or not. Defaults to True.
            print_flag (bool, optional): Enables print outs for debug. Defaults to False.
        """
        self.port = port
        self.listening = False
        self.print_flag = print_flag
        self.threaded = threaded

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind(('', self.port))
        self.thread = None

    def is_alive(self):
        """Returns if the thread is alive

        Returns:
            bool: true if alive and false if not or no thread is created
        """
        if self.thread is not None:
            return self.thread.is_alive()
        else:
            return False

    def start(self, callback, args=None):
        """Starts the listener

        Args:
            callback (function): function with no return which takes as input the message received by the listener and optionally some required args
            args (various optional): if the callback requires additional args. Defaults to None.
        """
        # CHECK THREAD IS NOT STILL ALIVE SOMEHOW
        if self.threaded:
            if self.is_alive():
                self.stop()
                time.sleep(2)
            self.thread = Thread(target=self.listen, args=(callback, args))
            self.listening = True
            self.thread.start()
        else:
            self.listening = True
            self.listen(callback, args)

    def stop(self):
        """When threaded stops the listener by breaking the while loop based on the listening var and resets the connection
        """
        self.listening = False
        # CREATE SECOND SOCKET TO CONNET TO THE TCP LISTENER TO FORCE self.s.accept() TO PROCESS
        try:
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(('localhost', self.port))
        except Exception as e:
            print('TCP Listener: failed to stop the thread: {}'.format(e))

    def listen(self, callback, args=None):
        """Main loop for the listener. Data is received, decoded and added to a final message. 
        The defined callback is run on the message.

        Args:
            callback (function): function with no return which takes as input the message received by the listener and optionally some required args
            args (various optional): if the callback requires additional args. Defaults to None.
        """
        self.s.listen(4)
        while self.listening:
            if self.print_flag: print('TCP Listener: waiting for connection')
            connection, client_address = self.s.accept()
            if self.print_flag: print('TCP Listener: connection received from {}'.format(client_address))
            try:
                # Receive the data in small chunks
                message = ''
                while self.listening:
                    data = connection.recv(16).decode()
                    if data:
                        message = message + data
                    else:
                        # NOTHING ELSE IN THE DATA, PASS MESSAGE TO callback
                        callback(message, args)
                        if self.print_flag: print('Data received:\n {}'.format(message))
                        break
            except Exception as e:
                print('TCP Listener: error whilst processing connection. {}'.format(e))
            finally:
                if self.print_flag: print('TCP Listener: closing connection')
                # Clean up the connection
                connection.close()
        print('TCP Listener: no longer listening')


# PARSE APPLICATION ARGUMENTS
parser = argparse.ArgumentParser()
parser.add_argument('-p', '--port', help='Port to run the TCP listener on', type=int, default=6969)
parser.add_argument('-t', '--threaded', help='Bool defining if the TCP listener should be run in its own thread',
                    type=bool, default=True)
parser.add_argument('-v', '--verbose', help='Bool defining if output should be printed', type=bool, default=True)

if __name__ == '__main__':

    args = parser.parse_args()
    print('Started on localhost, port {}'.format(args.port))
    listener = TCPListener(args.port, threaded=args.threaded, print_flag=args.verbose)
    listener.start(lambda message, arg: print('TCP Listener Callback Function: {}, {}'.format(message, arg)))
    # IF NOT THREADED APPLICATION WILL WAIT INDEFINITLEY FOR MESSAGES.
    time.sleep(10)
    print("Sending stop")
    listener.stop()
