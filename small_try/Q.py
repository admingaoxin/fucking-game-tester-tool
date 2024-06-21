
class WpeTools(Ui_MainWindow, QMainWindow):  
  def __init__(self, parent=None):  
    super(WpeTools, self).__init__(parent)  
    self.ui = Ui_MainWindow()  
    self.ui.setupUi(self)  
    self.agent = None # 先给它个空对象，占个属性名  
    # 绑定按钮方法  
    self.ui.start_btn.clicked.connect(self.start)  
    self.ui.stop_btn.clicked.connect(self.stop)  
    
  def start(self):  
    """  
    代理启动方法  
    :return:  
    """  
    # 获取文本框中的ip和端口等信息  
    agent_host = self.ui.agent_host_line.text()  
    agent_port = int(self.ui.agent_port_line.text())  
    game_host = self.ui.game_host_line.text()  
    game_port = int(self.ui.game_port_line.text())  
    # 生成Q线程  
    self.agent_thread = BeginAgentService(agent_host, agent_port, game_host, game_port, ui=self)  
    # 绑定线程信号  
    self.agent_thread.send_signal.connect(self.send_proto_view)  
    self.agent_thread.recv_signal.connect(self.recv_proto_view)  
    # 启动Q线程  
    self.agent_thread.start()  
    
  def stop(self):  
    """  
    代理停止方法  
    :return:  
    """  
    self.agent.stop()  
    
  def send_proto_view(self, send_proto):  
    """  
    将发送协议的内容展示到文本框中  
    :param send_proto::return:  
    """  
    self.ui.send_browser.append(send_proto)  
    
  def recv_proto_view(self, recv_proto):  
    """  
    将发送协议的内容展示到文本框中  
    :param recv_proto::return:  
    """  
    self.ui.recv_browser.append(recv_proto)


def client_to_server(self):
    """
    转发客户端发送给服务器的包
    1.获取客户端发起的字节流
    2.通过server socket进行转发
    3.循环此步骤
    :return:
    """
    while self.alive:
        # 首先读取2个字节，这两个字节代表的是协议长度
        length_buff = self.client_socket.recv(2)
        # 将长度的数值解析出来
        proto_length = struct.unpack('!H', length_buff)[0]
        # 再读取4个字节，这4个字节代表的是协议号
        id_buff = self.client_socket.recv(4)
        # 将协议号解析出来
        proto_id = struct.unpack('!I', id_buff)[0]
        # 然后再根据proto_length读取相应长度的字节
        proto_buff = self.client_socket.recv(proto_length)
        # 然后根据协议号proto_id生成协议对象，这个协议对象初始化的时候不传入参数，使用默认值
        # 这里我用了eval方法，这个方法可以将字符串当作代码运行，获取到对应的值（需要提前import）
        # 你也可以创造一个字典，用协议号作为key， 协议类作为value，通过协议号获取到对应的对象
        proto_obj = eval(f'C{proto_id}()')
        # 调用decode方法，将字节进行解析，并将值赋予协议对象的对应的属性
        proto_obj.decode(proto_buff)
        # 然后再调用对象明文化的方法， 获取到对象的明文字典
        self.ui_thread.send_signal.emit(f'Send C{proto_id}: {dispose_obj(proto_obj)}\n')
        # 将协议转发给服务器
        self.server_socket.send(length_buff + id_buff + proto_buff)


        def server_to_client(self):
    """
    处理服务器发送给客户端的包
    1.获取服务器返回的字节流
    2.调用client socket，将服务器返回的字节流直接转发给客户端
    3.循环此步骤
    :return:
    """
    while self.alive:
        # 首先读取2个字节，这两个字节代表的是协议长度
        length_buff = self.server_socket.recv(2)
        # 将长度的数值解析出来
        proto_length = struct.unpack('!H', length_buff)[0]
        # 再读取4个字节，这4个字节代表的是协议号
        id_buff = self.server_socket.recv(4)
        # 将协议号解析出来
        proto_id = struct.unpack('!I', id_buff)[0]
        # 然后再根据proto_length读取相应长度的字节
        proto_buff = self.server_socket.recv(proto_length)
        # 然后根据协议号proto_id生成协议对象，这个协议对象初始化的时候不传入参数，使用默认值
        # 这里我用了eval方法，这个方法可以将字符串当作代码运行，获取到对应的值（需要提前import）
        # 你也可以创造一个字典，用协议号作为key， 协议类作为value，通过协议号获取到对应的对象
        proto_obj = eval(f'S{proto_id}()')
        # 调用decode方法，将字节进行解析，并将值赋予协议对象的对应的属性
        proto_obj.decode(proto_buff)
        # 然后再调用对象明文化的方法， 获取到对象的明文字典
        self.ui_thread.recv_signal.emit(f'Recv S{proto_id}: {dispose_obj(proto_obj)}\n')
        # 将协议转发给客户端
        self.client_socket.send(length_buff + id_buff + proto_buff)

# 模拟服务器响应客户端的握手请求

def client_handshake_response(self):
    """
    模拟响应客户端的握手请求
    :return:
    """
    # 获取并解析握手请求
    data = self.client_socket.recv(1024)
    request = data.decode()
    # 解析握手请求中的关键信息：Sec-WebSocket-Key，并保存下来备用
    for line in request.split('\r\n'):
        if line.startswith('Sec-WebSocket-Key:'):
            self.key = line.split(':')[1].strip()
            break
    # 生成响应的key
    response_key = base64.b64encode(hashlib.sha1((self.key + '258EAFA5-E914-47DA-95CA-C5AB0DC85B11').
                                                 encode()).digest()).decode()
    # 生成握手响应信息
    response = 'HTTP/1.1 101 Switching Protocols\r\n'
    response += 'Upgrade: websocket\r\n'
    response += 'Connection: Upgrade\r\n'
    response += 'Sec-WebSocket-Accept: ' + response_key + '\r\n\r\n'
    # 发送握手响应给客户端
    self.client_socket.send(response.encode())


#   代理模拟客户端发送的请求
def server_handshake_request(self, host, port):
    """
    向服务器发起握手请求
    :param host:
    :param port:
    :return:
    """
    request = 'GET / HTTP/1.1\r\n'
    request += f'Host: {host}:{port}\r\n'
    request += 'Upgrade: websocket\r\n'
    request += 'Connection: Upgrade\r\n'
    request += 'Sec-Websocket-Extensions: permessage-deflate; client_max_window_bits\r\n'
    request += 'Sec-WebSocket-Key: ' + self.key + '\r\n'
    request += 'Sec-WebSocket-Version: 13\r\n\r\n'
    # 发送握手请求给服务器
    self.server_socket.send(request.encode())
    # 接收服务器的握手响应
    self.server_socket.recv(1024)


    
def start(self):
    """
    代理启动方法
    :return:
    """
    # 等待客户端连接
    self.client_socket, addr = self.socket_service.accept()
    # 代理模拟服务器，向客户端响应握手
    self.client_handshake_response()
    # 代理模拟客户端，向服务器发起握手请求
    # 由于这里要传入服务器的ip和端口
    # 因此需要我们在__init__方法中，将ip和端口保存成自己的属性以备后用
    self.server_handshake_request(self.server_host, self.server_port)
    # 启动转发线程，这里用的是Timer定时器，它也是继承自thread线程类，所以会单独起两个线程
    Timer(0, self.client_to_server).start()
    Timer(0, self.server_to_client).start()


class Agent(object):
    def __init__(self, agent_host, agent_port, server_host, server_port, ui_thread):
        """
        代理初始化一个实例
        :param agent_host: 代理绑定的ip
        :param agent_port: 代理绑定的端口
        :param server_host: 游戏服务器的ip
        :param server_port: 游戏服务器的端口
        """
        self.ui_thread = ui_thread
        # 设置一个socket server，以便后续监听客户端请求
        self.socket_service = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 将socket server绑定指定的ip和端口号
        self.socket_service.bind((agent_host, agent_port))
        self.socket_service.listen(5)
        # 设置客户端socket属性，先把它设置成一个空对象，后续有客户端请求过来之后再更新
        self.client_socket = None
        self.server_host = server_host
        self.server_port = server_port
        # 设置服务器socket属性，生成一个socket对象
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 创建SSL Context
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        # 使用 SSL context 包装 server_socket，创建一个 SSL socket
        self.server_socket = context.wrap_socket(self.server_socket,
                                                 server_hostname=f'{server_host}:{server_port}')
        # 将server_socket连接到游戏服务器
        self.server_socket.connect((self.server_host, self.server_port))
        # 给代理设置一个是否存活的状态，用于在遇到某些异常的时候终止转发线程
        self.alive = True



def server_to_client(self):
    """
    处理服务器发送给客户端的包
    1.获取服务器返回的字节流
    2.获取原始的封包内容
    3.调用协议明文化方法
    4.将服务器返回的字节流通过client socket转发给客户端
    3.循环此步骤
    :return:
    """
    while self.alive:
        # 获取协议头
        head_data = self.server_socket.recv(2)
        # 解析类型和长度
        opcode = head_data[0] & 0x0f
        payload_length = head_data[1] & 0x7f
        # 如果是bytes类型，则根据payload_length判断协议长度
        # 解释一下：payload_length保存的是数据的长度，如果长度小于126
        #         则payload_length就是真正的协议长度
        #         如果长度解析出来是126，则说明长度比较大，是用2个字节来保存
        #         我们需要读取2个字节来解析出真正的协议字节长度
        #         如果长度解析出来是127，说明长度巨大，用4个字节来保存的长度信息
        #         我们需要读取4个字节来解析出真正的协议长度
        if opcode == 0x2:
            if payload_length == 126:
                length_data = self.server_socket.recv(2)
                payload_length = struct.unpack(">H", length_data)[0]
            elif payload_length == 127:
                length_data = self.server_socket.recv(8)
                payload_length = struct.unpack(">Q", length_data)[0]
            elif payload_length < 126:
                length_data = b''
            else:
                length_data = b''
                # 正常来讲不会到这里来，但还是加个打印吧，防止出现解析错误的情况
                print(f'出错了，长度信息无法解析')
            # 再根据真实的协议长度，读取出ws协议的字节流，这个字节流中包含的是原始的游戏协议
            proto_data = self.server_socket.recv(payload_length)
            # 解析出协议号（需要与前后端协议封装方式一致，以4个字节保存协议号为例）
            # ps:此例协议结构为：协议号+协议参数 封装的字节流
            proto_id = struct.unpack('!I', proto_data[:4])[0]
            # 然后根据协议号proto_id生成协议对象，这个协议对象初始化的时候不传入参数，使用默认值
            # 这里我用了eval方法，这个方法可以将字符串当作代码运行，获取到对应的值（需要提前import）
            # 你也可以创造一个字典，用协议号作为key， 协议类作为value，通过协议号获取到对应的对象
            proto_obj = eval(f'S{proto_id}()')
            # 调用decode方法，将字节进行解析，并将值赋予协议对象的对应的属性
            proto_obj.decode(proto_data[4:])
            # 然后再调用对象明文化的方法， 获取到对象的明文字典
            self.ui_thread.recv_signal.emit(f'Recv S{proto_id}: {dispose_obj(proto_obj)}\n')
            # 将协议转发给客户端
            self.client_socket.send(head_data + length_data + proto_data)
        else:
            # 如果收到的不是bytes类型，说明已经出错了，直接关闭吧
            print(f'出错了，收到了非bytes类型的数据')
            self.alive = False


def client_to_server(self):
    """
    转发客户端发送给服务器的包
    1.获取发送的封包头信息
    2.获取发送封包的长度信息
    3.获取掩码内容
    4.获取加密后的协议内容
    5.协议解密
    6.调用协议明文化方法
    7.将协议转发给服务器
    8.重复此步骤
    :return:
    """
    while self.alive:
        # 获取协议头
        head_data = self.client_socket.recv(2)
        # 解析类型和长度
        opcode = head_data[0] & 0x0f
        payload_length = head_data[1] & 0x7f
        # 解析是否掩码加密，正常来讲客户端发给服务器的协议是掩码加密的，如果不是可能就出错了
        masked = head_data[1] & 0x80
        if not masked:
            print(f"处理字节流失败，masked类型为非加密类型{masked}，可能不是客户端发送的协议内容")
            self.alive = False
            return
        # 如果是bytes类型，则根据payload_length判断协议长度
        if opcode == 0x2:
            # 如果长度是126，则需要再读取2个字节解析真正的长度
            if payload_length == 126:
                length_data = self.client_socket.recv(2)
                payload_length = struct.unpack(">H", length_data)[0]
            elif payload_length == 127:
                length_data = self.client_socket.recv(8)
                payload_length = struct.unpack(">Q", length_data)[0]
            elif payload_length < 126:
                length_data = b''
            else:
                length_data = b''
                # 正常来讲不会到这里来，但还是加个打印吧，防止出现解析错误的情况
                print(f'出错了，长度信息无法解析')
            # 读取4位掩码
            masks_data = self.client_socket.recv(4)
            # 读取真正的协议封包内容
            proto_data = self.client_socket.recv(payload_length)
            # 创建一个字节流对象，用于保存还原后的真实的协议封包内容
            true_proto_data = bytearray()
            # 对掩码后的协议进行还原操作
            for proto_byte in proto_data:
                proto_byte ^= masks_data[len(true_proto_data) % 4]
                true_proto_data.append(proto_byte)
            # 解析出协议号（需要与前后端协议封装方式一致，以4个字节保存协议号为例）
            # ps:此例协议结构为：协议号+协议参数 封装的字节流
            proto_id = struct.unpack('!I', true_proto_data[:4])[0]
            # 然后根据协议号proto_id生成协议对象
            proto_obj = eval(f'C{proto_id}()')
            # 调用decode方法，将字节进行解析，并将值赋予协议对象的对应的属性
            proto_obj.decode(true_proto_data[4:])
            # 然后再调用对象明文化的方法，获取到对象的明文字典
            self.ui_thread.send_signal.emit(f'Send C{proto_id}: {dispose_obj(proto_obj)}\n')
            # 将协议转发给服务器
            self.server_socket.send(head_data + length_data + masks_data + proto_data)
        else:
            # 如果收到的不是bytes类型，说明已经出错了，直接关闭吧
            print(f'出错了，收到了非bytes类型的数据')
            self.alive = False


return re.sub(r"(?<=\w)(?=(?:\w\w)+$)", " ", str(binascii.b2a_hex(data))[2:-1].upper())




return re.sub(r"(?<=\w)(?=(?:\w\w)+$)", " ", str(binascii.b2a_hex(data))[2:-1].upper())



def insert_tcp_bytes(self, data):
    """
    通过server_socket发送一个tcp字节流（包含了协议号和协议内容）
    说明一下，按照我们之前定义的协议格式里面，一个完整的tcp封包分别包含：
    长度：除去协议号之外的，实际的协议内容的长度
    协议号：用4位int32表示协议号
    协议内容：实际的协议参数等内容
    有些可能还包含用来验证的验证码什么的，在这里我们先不考虑
    所以一个tcp封包的长度，实际指的是协议内容的长度，而我们传进来的协议内容是包含协议号的
    所以在下面的方法里面，我们在对长度进行转化和拼接时，需要减去4
    这个要根据项目的实际情况来做对应的调整
    :param data: 包含了协议号和协议内容的字节流
    :return:
    """
    self.server_socket.send(struct.pack('!H', len(data)-4) + data)


    
def insert_ws_bytes(self, data):
    """
    通过server_socket发送一个websocket字节流（包含了协议号和协议内容）
    跟tcp的封包格式不同的是，ws的网络封包是包含了mask掩码加密的
    并且ws的封包中，长度是包含了协议号的
    如果要让我们的封包能正常通过服务器的验证，我们需要实现一套跟它一样的加密方法
    :param data: 包含了协议号和协议内容的字节流
    :return:
    """
    ws_data = b'\x82'       # 代表二进制序列帧
    length = len(data)      # ws协议的长度是需要包含协议号的
    if length < 126:
        ws_data += chr(128 | length).encode('latin-1')
    elif length < 65535:
        ws_data += chr(128 | 0x7e).encode('latin-1')
        ws_data += struct.pack("!H", length)
    else:
        ws_data += chr(128 | 0x7f).encode('latin-1')
        ws_data += struct.pack("!Q", length)
    # 生成4位掩码
    mask_key = os.urandom(4)
    # 将mask_key和data字节流分别转化成字节数组
    mask_value = array.array("B", mask_key)
    data_value = array.array("B", data)
    # 获取系统默认的字节序
    native_byteorder = sys.byteorder
    # 获取协议数据的长度
    data_len = len(data_value)
    # 将协议数据从字节转换为整数
    data_value = int.from_bytes(data_value, native_byteorder)
    # 扩展掩码值的长度，使其与数据值的长度相匹配
    mask_value = int.from_bytes(mask_value * (data_len // 4) + mask_value[: data_len % 4], native_byteorder)
    # 对数据和掩码值进行异或操作，得到经过加密处理后的数据值，然后和之前的内容进行拼接
    ws_send_data = ws_data + mask_key + (data_value ^ mask_value).to_bytes(data_len, native_byteorder)
    # 通过server_socket将字节流发送给服务器
    self.server_socket.send(ws_send_data)



def check_data(self, data):
    """
    判断数据是否可以正常被解析
    :param data:
    :return:
    """
    # 根据字节流解析出协议号
    proto = struct.unpack(f"!H", data[0:4])[0]
    try:
        # 生成协议对象，调用decode方法，查看字节流是否可以正常被协议对象解析
        # 如果可以，则返回true，如果报错了，则返回false
        obj = eval(f'C{proto}')()
        obj.decode(data[4:])
        return True
    except Exception as e:
        print(f'协议检测失败：协议解析出现{e}错误，请检查是否可以通过 {proto} 协议进行解析！封包数据为：\n{data}')
        return False
    


def on_once_send_btn_click(self):
    """
    点击发送一次按钮之后的处理方法，以ws方法为例，tcp只是换个方法名而已
    读取文本框中的内容，转换为bytes，组合成一个完整协议，并发送给服务器
    :return:
    """

    try:
        try:
            # 首先从发送框获得字符串，并将其转化成字节流（这个文本框的组件名是textEdit）
            data = str_to_bytes(self.ui.textEdit.toPlainText())
            # 检查一下封包内容是否符合正确格式，如果是，则发送，否则，提醒格式不正确
            if self.agent.alive:
                if self.check_data(data):
                    self.agent.insert_ws_bytes(data)
                else:
                    print("协议检查失败，填入的协议无法正常解析")
            else:
                print("代理服务未启动，请先启动代理服务！")
        except SyntaxError:
            print("协议解析失败，请填入正确的WPE格式字节流数据")
        except AttributeError:
            print("协议发送失败，请先确保客户端已正常通过代理连接到服务器！")
        except Exception as e:
            print(f"协议检查出错，错误内容为：{e}")
    except Exception as e:
        print(f'协议发送失败，错误信息为：{e}')


def on_creat_proto_btn_click(self):
    """
    点击生成协议按钮之后的处理方法
    1.首先判断协议编号是否正确
    2.判断参数格式是否正确
    3.生成一个实例，然后调用对应的协议编号的encode方法，看是否正确返回
    4.将生成的字节流转换成WPE字符串显示格式
    :return:
    """
    # 判断协议号和协议参数是否有内容
    if self.ui.proto_id_line.text() and self.ui.proto_msg_line.toPlainText():
        try:
            # 解析出协议号，这里加个try，预防输入错误
            proto_id = int(self.ui.proto_id_line.text())
            try:
                # 解析参数列表，同样加个try，预防输入错误
                args = eval(self.ui.proto_msg_line.toPlainText())
                try:
                    # 看参数是否赋予协议对象，并调用encode方法
                    obj = eval(f'C{proto_id}')(*args)
                    proto, length, buf = obj.encode()
                    # 将协议号和协议内容的字节流，转化成WPE十六进字符串，填入指定位置
                    self.ui.textEdit.setText(bytes_to_str(struct.pack('!I', proto) + buf))
                except Exception:
                    print("协议生成失败：如确认填写正确，则可能是参数不符合协议格式，请检查对应的协议格式！")
            except Exception:
                print("协议生成失败：协议参数不正确，请输入正确的参数，并以列表[]形式填入")
        except Exception:
            print("协议生成失败：协议编号格式不正确，请输入正确的数字")
    else:
        self.ui.textEdit.setText("协议号和协议内容不能为空！！！")


def socks_connect_server(self):
    """
    与服务器创建连接，socks5代理方式通过请求获取
    :return:
    """
    # 连接前先握手
    self.handshake()
    # 接收客户端的连接请求
    request = self.client_socket.recv(4096)
    # 解析请求，获取版本号，连接类型，目标地址和端口
    ver, cmd, _, address_type = request[:4]
    if address_type == 1:  # IPv4地址
        target_address = socket.inet_ntoa(request[4:8])
        target_port = int.from_bytes(request[8:10], byteorder='big')
    elif address_type == 3:  # 域名
        address_length = request[4]
        target_address = request[5:5 + address_length].decode()
        target_port = int.from_bytes(request[5 + address_length:7 + address_length], byteorder='big')
    else:
        # 不支持的地址类型
        print(f'地址类型{address_type}不支持，socket即将主动关闭，请检查或添加对应类型的处理办法')
        self.client_socket.close()
        return
    # 生成响应包头
    response = b"\x05\x00\x00\x01"  # 版本、响应码、保留字段、地址类型（IPv4）
    if cmd == 1:    # Tcp连接类型
        # 让server_socket与目标服务器创建连接
        self.server_socket.connect((target_address, target_port))
        # 补全响应包，响应的ip和端口都填0就可以了
        response += socket.inet_aton('0.0.0.0') + (0).to_bytes(2, byteorder='big')  # 绑定的地址和端口
        # 响应客户端连接成功
        self.client_socket.sendall(response)
        # 启动转发线程，这里用的是Timer定时器，它也是继承自thread线程类，所以会单独起两个线程
        Timer(0, self.client_to_server).start()
        Timer(0, self.server_to_client).start()
    elif cmd == 3:  # Udp连接类型
        # 补全响应包，响应的ip和端口不能填0，要填Udp的监听地址
        response += socket.inet_aton(UDP_BIND_HOST) + UDP_BIND_PORT.to_bytes(2, byteorder='big')  # 绑定的地址和端口
        # 响应客户端连接成功
        self.client_socket.sendall(response)
        # 启动Udp处理逻辑，这部分代码有点问题，我还没有处理好
        self.udp_handler()
        # 未完成的代码……，如有同学知道这里如何处理，还望赐教

class Agent(object):
    def __init__(self, agent_host, agent_port, ui_thread):
        """
        代理初始化一个实例
        :param agent_host: 代理绑定的ip
        :param agent_port: 代理绑定的端口
        """
        self.ui_thread = ui_thread
        # 设置一个socket server，以便后续监听客户端请求
        self.socket_service = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 将socket server绑定指定的ip和端口号
        self.socket_service.bind((agent_host, agent_port))
        self.socket_service.listen(5)
        # 设置客户端socket属性，先把它设置成一个空对象，后续有客户端请求过来之后再更新
        self.client_socket = None
        # 设置服务器socket属性，生成一个socket对象
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # 以下代码进行了注释
        # # 将server_socket连接到游戏服务器，socks5一开始不知道服务器地址，所以不需连接，注释掉
        # self.server_socket.connect((server_host, server_port))

        # 给代理设置一个是否存活的状态，用于在遇到某些异常的时候终止转发线程
        self.alive = True


def on_loop_send_begin_btn_click(self):
    """
    点击循环开始按钮之后的处理方法
    读取文本框中的内容，转换为bytes，组合成完整的协议，循环发送给服务器
    :return:
    """
    # 首先从发送框获取封包内容
    data = str_to_bytes(self.ui.textEdit.toPlainText())
    # 判断代理当前是否正常在运行
    if self.agent.alive:
        # 检查一下封包内容是否符合正确格式，如果是，则发送，否则，提醒格式不正确
        if self.check_data(data):
            try:
                # 从填写次数的文本框中读取次数信息，并转换成int值
                times = int(self.ui.lineEdit.text())
                if times == 0:
                    # 设置一个打断开关，用于主动停止循环
                    self.agent.loop_send = True
                try:
                    # 从填写间隔时间的文本框中读取间隔时长文本，并转换成int值
                    sleep_time = int(self.ui.lineEdit_2.text())
                    # 设置一个最小时间，防止太快卡死，我这里设置了最小间隔10ms
                    if sleep_time < 10:
                        sleep_time = 10
                    # 这里我用了个线程，专门用来循环发送协议，主要懒得再写个Q线程类了
                    Timer(0, self.agent.agent_insert_send,
                          [data, times, sleep_time]).start()
                except ValueError:
                    print("循环间隔时长无法正确转化成int值，请检查间隔填写是否正确！")
            except ValueError:
                print("请检查次循环数填写是否正确！")
        else:
            print("协议检查失败，填入的协议无法正常解析")
    else:
        print("代理服务未启动，请先启动代理服务！")



# 绑定循环开始按钮事件
self.ui.loop_send_begin_btn.clicked.connect(self.on_loop_send_begin_btn_click)




def agent_insert_send(self, data, times=1, delay_time=100):
    """
    插入一个伪造的数据包，并发送
    :param data:伪造的数据包
    :param times:发送次数
    :param delay_time:发送间隔时间
    :return:
    """
    try:
        if self.alive:
            # 如果设置了发送次数，则适用for循环，循环一定的次数
            # 否则适用while循环，在手动停止之前会无限循环
            if times:
                for i in range(times):
                    # 这里直接调用了insert_tcp_bytes方法，如果是ws，则调用ws的对应方法即可
                    self.insert_tcp_bytes(data)
                    # 休息，休息一下
                    time.sleep(delay_time / 1000.0)
            else:
                # 这里用到了loop_send的属性
                # 在点击循环开始按钮的时候，会将这个属性设置为True
                # 在点击循环结束的时候，会将它设为False，这样while循环就停止了
                while self.loop_send:
                    self.insert_tcp_bytes(data)
                    time.sleep(delay_time / 1000.0)
    except Exception as e:
        print(f"插包出错了！错误信息为：{e}")

class Agent(object):
    def __init__(self, agent_host, agent_port, server_host, server_port, ui_thread):
        """
        代理初始化一个实例
        :param agent_host: 代理绑定的ip
        :param agent_port: 代理绑定的端口
        :param server_host: 游戏服务器的ip
        :param server_port: 游戏服务器的端口
        """
        # 设置两个开关，分别用来控制发送延迟和接收延迟，默认关闭
        self.send_delay = False
        self.recv_delay = False
        # 设置两个延迟时间，你想延迟多少秒，就设置成多少，也可以是小数
        self.send_delay_time = 1.5
        self.recv_delay_time = 2

        self.ui_thread = ui_thread
        # 以下为原来的代码……，略略略



def client_to_server(self):
    """
    转发客户端发送给服务器的包
    :return:
    """
    while self.alive:
        try:
            # 首先读取2个字节，这两个字节代表的是协议长度
            length_buff = self.client_socket.recv(2)
            # 将长度的数值解析出来
            proto_length = struct.unpack('!H', length_buff)[0]
            # 再读取4个字节，这4个字节代表的是协议号
            id_buff = self.client_socket.recv(4)
            # 将协议号解析出来
            proto_id = struct.unpack('!I', id_buff)[0]
            # 然后再根据proto_length读取相应长度的字节
            proto_buff = self.client_socket.recv(proto_length)
            # 然后根据协议号proto_id生成协议对象，这个协议对象初始化的时候不传入参数，使用默认值
            # 这里我用了eval方法，这个方法可以将字符串当作代码运行，获取到对应的值（需要提前import）
            # 你也可以创造一个字典，用协议号作为key， 协议类作为value，通过协议号获取到对应的对象
            proto_obj = eval(f'C{proto_id}()')
            # 调用decode方法，将字节进行解析，并将值赋予协议对象的对应的属性
            proto_obj.decode(proto_buff)
            # 然后再调用对象明文化的方法， 获取到对象的明文字典
            self.ui_thread.send_signal.emit(f'Send C{proto_id}: {dispose_obj(proto_obj)}\n')
            # 将协议转发给服务器,这里做了修改，如果延迟是开启状态，则调用定时器延迟发送，否则直接发送
            if self.send_delay:
                # 调用定时器，并传入参数，注意参数作为元组形式，里面那个小逗号不能丢
                Timer(self.send_delay_time, self.server_socket.send,
                      (length_buff + id_buff + proto_buff,)).start()
            else:
                self.server_socket.send(length_buff + id_buff + proto_buff)
        except (socket.error, OSError):
            print('网络已断开')
            break

def delay_send_proto(self):
    """
    发包延迟的方法
    :return:
    """
    if self.agent.alive:
        # 首先判断按钮当前是什么状态，如果按钮文本是发包延迟，则在点击后开启发包延迟，并将文本设置为取消延迟
        if self.ui.delay_send_btn.text() == '发包延迟':
            self.ui.delay_send_btn.setText('取消延迟')
            self.agent.delay_send = True
        else:
            # 否则判断当前已开启了延迟，再次点击需要关闭延迟，并把按钮文本恢复为初始文字
            self.ui.delay_send_btn.setText('发包延迟')
            self.agent.delay_send = False
    else:
        print('目前还没有客户端连接，请连接后再试')

def delay_recv_proto(self):
    """
    收包延迟方法
    :return:
    """
    if self.agent.alive:
        # 首先判断按钮当前是什么状态，如果按钮文本是收包延迟，则在点击后开启收包延迟，并将文本设置为取消延迟
        if self.ui.delay_recv_btn.text() == '收包延迟':
            self.ui.delay_recv_btn.setText('取消延迟')
            self.agent.delay_recv = True
        else:
            # 否则判断当前已开启了延迟，再次点击需要关闭延迟，并把按钮文本恢复为初始文字
            self.ui.delay_recv_btn.setText('收包延迟')
            self.agent.delay_recv = False
    else:
        print('目前还没有客户端连接，请连接后再试')


class Agent(object):
    def __init__(self, agent_host, agent_port, server_host, server_port, ui_thread):
        """
        代理初始化一个实例
        :param agent_host: 代理绑定的ip
        :param agent_port: 代理绑定的端口
        :param server_host: 游戏服务器的ip
        :param server_port: 游戏服务器的端口
        """
        # 设置两个开关，分别用来控制发送延迟和接收延迟，默认关闭
        self.send_delay = False
        self.recv_delay = False
        # 设置两个延迟时间，你想延迟多少秒，就设置成多少，也可以是小数
        self.send_delay_time = 1.5
        self.recv_delay_time = 2

        self.ui_thread = ui_thread

        # 设置一个socket server，以便后续监听客户端请求
        self.socket_service = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 将socket server绑定指定的ip和端口号
        self.socket_service.bind((agent_host, agent_port))
        self.socket_service.listen(5)
        # 保存服务器地址
        self.server_host = server_host
        self.server_port = server_port
        # 设置客户端socket属性，先把它设置成一个空对象，后续有客户端请求过来之后再更新
        self.client_socket = None
        # 设置服务器socket属性，生成一个socket对象
        self.server_socket = None
        # 给代理设置一个是否存活的状态，用于在遇到某些异常的时候终止转发线程
        self.alive = True
        # 设置一个标识，默认为0，当代理与客户端或服务器的任一转发线程中断时+1，值为2时表示全部中断
        self.net_state = 0



def start(self):
    """
    代理启动方法
    :return:
    """
    while True:
        # 等待客户端连接
        self.client_socket, addr = self.socket_service.accept()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 将server_socket连接到游戏服务器
        self.server_socket.connect((self.server_host, self.server_port))
        self.alive = True
        # 初始化网络标识
        self.net_state = 0
        # 启动转发线程
        Timer(0, self.client_to_server).start()
        Timer(0, self.server_to_client).start()


def client_to_server(self):
    """
    转发客户端发送给服务器的包
    :return:
    """
    while self.alive:
        try:
            # 首先读取2个字节，这两个字节代表的是协议长度
            length_buff = self.client_socket.recv(2)
            # 将长度的数值解析出来
            proto_length = struct.unpack('!H', length_buff)[0]
            # 再读取4个字节，这4个字节代表的是协议号
            id_buff = self.client_socket.recv(4)
            # 将协议号解析出来
            proto_id = struct.unpack('!I', id_buff)[0]
            # 然后再根据proto_length读取相应长度的字节
            proto_buff = self.client_socket.recv(proto_length)
            # 然后根据协议号proto_id生成协议对象，这个协议对象初始化的时候不传入参数，使用默认值
            # 这里我用了eval方法，这个方法可以将字符串当作代码运行，获取到对应的值（需要提前import）
            # 你也可以创造一个字典，用协议号作为key， 协议类作为value，通过协议号获取到对应的对象
            proto_obj = eval(f'C{proto_id}()')
            # 调用decode方法，将字节进行解析，并将值赋予协议对象的对应的属性
            proto_obj.decode(proto_buff)
            # 然后再调用对象明文化的方法， 获取到对象的明文字典
            self.ui_thread.send_signal.emit(f'Send C{proto_id}: {dispose_obj(proto_obj)}\n')
            # 将协议转发给服务器,这里做了修改，如果延迟是开启状态，则调用定时器延迟发送，否则直接发送
            if self.send_delay:
                Timer(self.send_delay_time, self.server_socket.send,
                      (length_buff + id_buff + proto_buff)).start()
            else:
                self.server_socket.send(length_buff + id_buff + proto_buff)
        except (socket.error, OSError):
            print('网络已断开')
            break
    # 将网络状态标识符+1
    self.net_state += 1



self.ui.flash_disconnect_btn.clicked.connect(self.on_flash_disconnect_btn_click)