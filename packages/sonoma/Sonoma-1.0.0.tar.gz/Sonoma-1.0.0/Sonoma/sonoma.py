import socket
import threading
from http import HTTPStatus
from logging import basicConfig
import email.utils as eut
from defaults import defaults
from default_handler import defaultHandler

SERVER_THREADS = []

basicConfig()

class httpServer(object):
    def __init__(self, address, port, handler=None) -> None:

        # HANDLER ASSIGNMENT
        self.handler = handler

        # GET DEFAULT HANDLER
        self.defaultHandler = defaultHandler

        # GET CLIENT ADDRESS
        self.vector = (address, port)
        
        # SET CONTENT TYPES DICT
        self.contentTypes = {
            'json': 'application/json',
            'text': 'text/plain',
            'html': 'text/html'
        }
        
        # DEFINE THE SOCKET
        self.sock_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock_.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # METHOD FOR GETTING HTTP RESPONSE HEADERS AND STATUSLINE
    def httpHeaders(self, httpStatus, origin="*", contentType="text"):

        # SETS CONTENT TYPE IF FOUND ELSE SETS VALUE TO THE CONTENTTYPE VARIABLE
        if contentType in self.contentTypes:
            contentType = self.contentTypes[contentType]

        # GET TIMESTAMP NOW, FORMATTED BY IETF STANDARDS 
        date = str(eut.formatdate())
        date = date.replace(date.split(' ')[5], "GMT")

        # RETURNS (responsestatusLine, [headers])
        return ( f"HTTP/{defaults.httpVersion} {httpStatus.value} {httpStatus.phrase}\r\n",
        [
            f"Access-Control-Allow-Origin: {origin}",
            "Connection: Close",
            #"Content-Encoding: gzip",
            f"Content-Type: {contentType}",
            f"Date: {date}",
            f"Last-Modified: {date}",
            f"Server: {defaults.serverName}",
            "Vary: Cookie, Accept-Encoding",
            "X-Frame-Options: DENY"
        ])

    # UTILITY METHOD THAT SETS A CUSTOM HANDLER
    def set_handler(self, handler):
        """
        # Required format for custom handler:
        
        - Parameters
        ```
        myHandler(self, str requestStatusLine, list requestHeaders, bytes or str requestBody, socket.socket clientConnection, tuple clientAddress)
        ```
        - Return Value
        ```
        return (str responseStatusLine, list responseHeaders, bytes or str responseBody)
        ```
        """
        self.handler = handler
    
    # START SERVER THREAD
    def run(self):
        # SERVER THREAD
        def thread():            
            self.sock_.bind(self.vector)
            self.sock_.listen(1)

            print('Listening on %s:%s ...' % self.vector)

            # [*i*] USE self.sock.close to close entire server socket. [*i*] 

            while True:    

                # Wait for client connections
                client_connection, client_address = self.sock_.accept()

                # Get the client request
                try:
                    request = client_connection.recv(1024).decode()
                except:
                    client_connection.close()
                    continue

                requestHeaders_buffer = request.split("\r\n")

                try:
                    requestBody = request.split('\r\n\r\n')[1]
                except:
                    requestBody = ""
                    
                try:
                    requestStatusLine = requestHeaders_buffer.pop(0)
                except:
                    client_connection.close()
                    continue

                requestHeaders = []
                for unit in requestHeaders_buffer:
                    if unit != "" and ": " in unit:
                        requestHeaders.append([unit.split(': ')[0], unit.split(': ')[1]])
        
                # PROCESS REQUEST - VOID
                if self.handler is not None:
                    responseStatusLine, responseHeaders, responseBody = self.handler(self, requestStatusLine, requestHeaders, requestBody, client_connection, client_address)

                else:
                    responseStatusLine, responseHeaders, responseBody = self.defaultHandler(requestStatusLine, requestHeaders, requestBody, client_connection, client_address)
                
                if len(responseBody):
                    responseHeaders.append(f'Content-Length: {str(len(responseBody))}')    
                
                response = responseStatusLine + ("\r\n".join(responseHeaders)) + "\r\n\r\n" + responseBody
                
                client_connection.sendall(response.encode())

                client_connection.close()

        
        t = threading.Thread(target=thread)
        t.start()
        SERVER_THREADS.append(t)












