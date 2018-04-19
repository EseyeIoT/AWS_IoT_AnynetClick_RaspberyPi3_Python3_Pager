import time
import py3_aws_click as aws
import py3_oled as oled
import ctypes
import ctypes.util
import json


# want to use atoi() from run-time
mylib = ctypes.util.find_library('c')
clib = ctypes.cdll.LoadLibrary(mylib)


# def recvdata(waitstr):
#     response = ''.encode('utf-8')
#     while waitstr.encode('utf-8') not in response:
#         ch = ser.read()
#         response += ch


# def sendcmd(data):
#     ser.write(data.encode('utf-8'))

    
# def resetaws():
#     print("Resyncing with AWS please wait")
#     ser.timeout = 0.01
#     for i in range(1,50):
#         idx = 0
#         sendcmd(echooff)
#         response = "".encode('utf-8')
#         while ok.encode('utf-8') not in response:
#             idx += 1
#             ch = ser.read()
#             response += ch
#             if idx == 20:
#                 break
#         if ok.encode('utf-8') in response:
#             break
#     ser.timeout = 2

    
    

def setup():
    print("setting up AWS")

    aws.sendcmd('AT+AWSSUBCLOSE=0\r\n')
    aws.recvdata('+AWSSUBCLOSE:0,')

    aws.sendcmd('AT+AWSSUBOPEN=0,"msgout"\r\n')
    aws.recvdata('+AWSSUBOPEN:0,0\r\n')

    oled.OLED_M_Init()
    oled.OLED_Clear()


def main():
    setup()
    aws.resetaws()
    aws.setup()
    print("ready to receive...")
    while True:
        awsmessage = ''
        lenstr = ''
        msglen = 0

        aws.recvdata('+AWS:0,')
        lenstr = aws.recvMessageDataLen('\r\n')
        msglen = clib.atoi(lenstr)

        awsmessage = aws.recvMessageData(msglen)

        jsonformat = True
        jsondata = None
        try:
            jsondata = json.loads(awsmessage.decode('utf-8'))
        except Exception as ex:
            jsonformat = False
        
        oled.OLED_Clear()
        if jsonformat == True:
            oled.OLED_Puts(0, 1, jsondata['message'])
        else:
            oled.OLED_Puts(0, 1, awsmessage)
    
    ser.close()

if __name__=="__main__":
    main()

