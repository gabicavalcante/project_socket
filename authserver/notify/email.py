from socket import *
import base64
import time

msg = "\r\n Test email socket"
endmsg = "\r\n.\r\n"

# a mail server (e.g. Google mail server)
mailserver = ("smtp.gmail.com", 587)

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(mailserver)

recv = clientSocket.recv(1024)
recv = recv.decode()
print("Message after connection request: " + recv)

if recv[:3] != '220':
    print('220 reply not received from server.')

heloCommand = 'EHLO Alice\r\n'
clientSocket.send(heloCommand.encode())
recv1 = clientSocket.recv(1024)
recv1 = recv1.decode()
print("Message after EHLO command:" + recv1)

if recv1[:3] != '250':
    print('250 reply not received from server.')


# Info for username and password
username = "gabicavalcantesilva@gmail.com"
password = "75759597"
base64_str = ("\x00"+username+"\x00"+password).encode()
base64_str = base64.b64encode(base64_str)
authMsg = "AUTH PLAIN ".encode()+base64_str+"\r\n".encode()
clientSocket.send(authMsg)
recv_auth = clientSocket.recv(1024)
print(recv_auth.decode())

mailFrom = "MAIL FROM:<gabicavalcantesilva@gmail.com>\r\n"
clientSocket.send(mailFrom.encode())
recv2 = clientSocket.recv(1024)
recv2 = recv2.decode()
print("After MAIL FROM command: " + recv2)

rcptTo = "RCPT TO:<gabicavalcantesilva@gmail.com>\r\n"
clientSocket.send(rcptTo.encode())
recv3 = clientSocket.recv(1024)
recv3 = recv3.decode()
print("After RCPT TO command: "+recv3)

data = "DATA\r\n"
clientSocket.send(data.encode())
recv4 = clientSocket.recv(1024)
recv4 = recv4.decode()
print("After DATA command: "+recv4)

subject = "Subject: testing my client\r\n\r\n"
clientSocket.send(subject.encode())
date = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())
date = date + "\r\n\r\n"
clientSocket.send(date.encode())
clientSocket.send(msg.encode())
clientSocket.send(endmsg.encode())
recv_msg = clientSocket.recv(1024)
print("Response after sending message body:"+recv_msg.decode())

quit = "QUIT\r\n"
clientSocket.send(quit.encode())
recv5 = clientSocket.recv(1024)
print(recv5.decode())

clientSocket.close()