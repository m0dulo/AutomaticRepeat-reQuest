import socket
import threading
import time
import random

base = [str(x) for x in range(10)] + [chr(x) for x in range(ord('A'), ord('A')+6)]

def dec2bin(string_num):
    num = int(string_num)
    mid = []
    while True:
        if num == 0: break
        num,rem = divmod(num, 2)
        mid.append(base[rem])

    return ''.join([str(x) for x in mid[::-1]])


def hex2dec(string_num):
    return str(int(string_num.upper(), 16))


def hex2bin(string_num):
    return dec2bin(hex2dec(string_num.upper()))


def crc16(x):
    a = 0xFFFF
    b = 0xA001
    for byte in x:
        a ^= ord(byte)
        for i in range(8):
            last = a % 2
            a >>= 1
            if last == 1:
                a ^= b
    s = hex(a).upper()

    return s[4:6] + s[2:4]


def remain(min):
    count = 0
    while (count < min):
        count += 1
        n = min - count
        time.sleep(1)
        print(n)


def Receive(s):
    global true
    global ttime
    global data
    while true:
        data = s.recv(1024).decode('utf8')
        ttime = -1
        if data == 'quit':
            true = False
        print('<server>: %s' % data)


def SendData():
    global data
    global ttime
    global vs
    #CRC
    datainit = []
    for i in range(5):
        datainit.append(i)
    dataset = []
    print("dataset: ")
    for si in datainit:
        bb = bin(si)
        ans = int(bb[2])
        it = 3
        while it < len(bb):
            ans = ans ^ int(bb[it])
            it = it + 1
        if ans == 1:
            bb += '1'
        dataset.append(bb)
        print(bb, end=" ")
    print()

    vs = 0
    data = ""
    iv = 0
    while iv < len(dataset):
        #print("loop")
        #print("iv=%d" % iv)
        it = str(iv%2) + dataset[iv]
        #随机数 产生错误数据帧、丢失数据帧
        # 1 是数据帧错误
        # 2 是丢失数据帧
        srd = random.randint(1, 10)
        print("srd=%d" % srd)
        senddata = str(it)
        if srd == 1:
            print(">>> send data is error: " + senddata)
            senddata += '1'
            s.send(senddata.encode('utf8'))
        else:
            if srd != 2:
                print(">>>send data: " + senddata)
                s.send(senddata.encode('utf8'))
            else:
                print(">>> not send data: " + senddata)

        while 1:
            #print("vs=%s" % vs)
            data = "no"
            ttime = TIME
            while ttime > 0:
                print(ttime)
                time.sleep(1)
                ttime = ttime - 1

            if ttime == 0:
                print("time out, resend!")
                break
            else:
                #print("ackx".replace('x', str(1-vs)))
                #print("data")
                #print(data)
                if data == "ackx".replace('x', str(1-vs)):
                    print("succeed sending data: " + str(it))
                    vs = 1 - vs
                    iv = iv + 1
                    break
                else:
                    print("receive wrong ack, continue waiting!")


hostport = ("127.0.0.1", 2222)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(hostport)
data = ""
ttime = 0
true = True
TIME = 5

thrd = threading.Thread(target=Receive, args=(s,))
thrd.start()
while true:
    user_input = input('>>>: ')
    s.send(user_input.encode('utf8'))
    if user_input == 'quit':
        true = False
    if user_input == 'send':
        SendData()
        user_input = "show data"
        s.send(user_input.encode('utf8'))
s.close()