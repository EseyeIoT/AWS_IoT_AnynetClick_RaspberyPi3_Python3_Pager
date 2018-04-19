import serial

# setup serial for AWS click
ser = serial.Serial(
    port='/dev/serial0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=0.5,
)

ser.xonxoff = False
ser.rtscts = False
ser.dsrdtr = False

reset = ser.readline()

echooff = "ATE0\r\n"
ok = "OK\r\n"
pubclose = 'AT+AWSPUBCLOSE=0\r\n'
pubopen = 'AT+AWSPUBOPEN=0,"WEATHER"\r\n'
publish = "AT+AWSPUBLISH=0,%d\r\n"


def recvdata(waitstr):
    response = "".encode('utf-8')

    while waitstr.encode('utf-8') not in response:
        ch = ser.read()
        response += ch

def sendcmd(data):
    ser.write(data.encode('utf-8'))

def setup():
    sendcmd(echooff)
    recvdata(ok)
    sendcmd(pubclose)
    recvdata(ok)
    sendcmd(pubopen)
    recvdata(ok)


def resetaws():
    print("Resyncing with AWS please wait")
    ser.timeout = 0.01
    for i in range(1,50):
        idx = 0
        sendcmd(echooff)
        response = "".encode('utf-8')
        while ok.encode('utf-8') not in response:
            idx += 1
            ch = ser.read()
            response += ch
            if idx == 20:
                break
        if ok.encode('utf-8') in response:
            break
    ser.timeout = 2

def recvMessageDataLen(waitstr):
    response = ''.encode('utf-8')
    while waitstr.encode('utf-8') not in response:
        ch = ser.read()
        response += ch
    return response


def recvMessageData(len):
    message = ''.encode('utf-8')
    for i in range(0,len):
        message += ser.read()

    return message
