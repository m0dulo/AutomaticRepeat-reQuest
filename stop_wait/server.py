import socket
import threading
base = [str(x) for x in range(10)] + [chr(x) for x in range(ord('A'), ord('A')+6)]


def dec2bin(string_num):
    num = int(string_num)
    mid = []
    while True:
        if num == 0: break
        num, rem = divmod(num, 2)
        mid.append(base[rem])

    return ''.join([str(x) for x in mid[::-1]])


def hex2dec(string_num):
    return str(int(string_num.upper(), 16))


def hex2bin(string_num):
    return dec2bin(hex2dec(string_num.upper()))


def CRC(bb):

    ans = int(bb[3])
    it = 4
    while it < len(bb):
        ans = ans ^ int(bb[it])
        it = it + 1
    #print("ans = %d" % ans)
    if ans == 0:
        return True
    else:
        return False


def Receive(conn):                                               # 将接收定义成一个函数
    global true
    # 声明全局变量，当接收到的消息为quit时，则触发全局变量 true = False，则会将socket关闭
    info = []
    global ns
    ns = 0
    while true:
        global start
        global vr

        #global info
        data = conn.recv(1024).decode('utf8')
        print("<client>: " + data)

        if data == 'quit':
            true = False

        if data == 'show data':
            start = 0
            print("receive the data:")
            i = 0
            while i < len(info):
                print(info[i], end=" ")
                i = i+1
            print()
        if start:
            if CRC(data):
                info.append(data)
                vr = 1 - vr
                ack = "ack" + str(vr)

                conn.send(ack.encode('utf8'))
                print("<server>: " + ack)
            else:
                print("data is wrong!")
        if data == 'send':
            vr = 0
            start = 1


# 导入多线程模块
print("Waitting to be connected......")
HostPort = ('127.0.0.1', 2222)
start = 0
vr = 0
ns = 0
info = []
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)            # 创建socket实例
s.bind(HostPort)
s.listen(5)

while True:
    conn, addr = s.accept()
    true = True
    addr = str(addr)
    print('Connecting by : %s ' % addr)
    thrd = threading.Thread(target=Receive, args=(conn,))           # 线程实例化，target为方法，args为方法的参数
    thrd.start()                                                    # 启动线程
    while true:
        user_input = input('>>>: ')
        conn.send(user_input.encode('utf8'))                        # 循环发送消息
        if user_input == 'quit':                                    # 当发送为‘quit’时，关闭socket
            true = False
    s.close()
