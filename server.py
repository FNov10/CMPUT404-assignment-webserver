#  coding: utf-8 
import socketserver,os

# Copyright 2023 Abram Hindle, Eddie Antonio Santos, Fahad Naveed
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        #print(str(self.data))
        if "GET" in str(self.data):
            index1 = str(self.data).index("GET")
            index2 = str(self.data).index("HTTP")   
            rest = ''
            for idx in range(index1 + 3 + 1, index2):
                rest = rest + str(self.data)[idx]
            #print(rest)
            path = 'www'+rest.strip()
            path = path.replace('..','')
            x = False      
            print ("Got a request of: %s\n" % self.data)
            try:
                if path[-1] != '/' and '.css' not in path and '.html' not in path:
                    
                    path +='/'
                    if os.path.exists(path):

                        header = "HTTP/1.1 301 Moved Permanently \n"
                        header = header + "Location: " + path[3:]
                        print(path[3:])
                        self.request.sendall(header.encode())
                    else: raise FileNotFoundError
                else:
                    x = True
                    self.Handle200OK(path)
            except FileNotFoundError:
                self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\nContent type: text/html"+ "\n\n"+ "404 Path not found :(", "utf-8"))
            except IsADirectoryError:
                path+='index.html'
                if x:
                    self.Handle200OK(path)
                #print('skibididobdobdoboyesyesyesyes')     
        else:
            self.request.sendall(bytearray("HTTP/1.1 405 Method Not Allowed\r\nContent type: text/html"+ "\n\n"+ "405!!", "utf-8"))

    def Handle200OK(self,path):
        f = open((path),'r' )           
        fa=f.read()
        if '.css' in path:
            final =  "HTTP/1.1 200 OK \nContent-type:text/css; charset=utf-8\n\n"
        elif '.html' in path':
            final =  "HTTP/1.1 200 OK \nContent-type:text/html; charset=utf-8\n\n"
        final = final + fa
        self.request.sendall(final.encode())
        
if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
