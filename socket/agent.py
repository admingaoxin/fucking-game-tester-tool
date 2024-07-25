import socket
import time
import threading 
import errno
class Agent(object):
    def __init__(self, agent_host, server_host, agent_port_range, server_port):
        """
        , agent_port
        , server_port
        代理初始化一个实例
        :param agent_host: 代理绑定的ip
        :param agent_port: 代理绑定的端口
        :param server_host: 游戏服务器的ip
        :param server_port: 游戏服务器的端口
        """

        self.client_socket = None
        self.server_socket = None
        self.server_host = server_host
        self.server_port = server_port

        

        # 监听所有网络接口
        if agent_host == '':
            agent_host = '0.0.0.0'

        for port in range(agent_port_range[0], agent_port_range[1] + 1):
            try:
                self.socket_service = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                # 解包元组以获取端口号
                self.socket_service.bind((agent_host, port))
                self.socket_service.listen(5)
                print(f"成功绑定到端口: {port}")
                break  # 成功绑定后跳出循环
            except socket.error as e:
                if e.errno == errno.EADDRINUSE:  # Address already in use
                    print(f"端口 {port} 已被占用，尝试下一个...")
                else:
                    raise  # 抛出其他类型的错误
            else:
                raise Exception("无法在给定的端口范围内找到空闲端口")



        # # 设置一个socket server，以便后续监听客户端请求
        # self.socket_service = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # # 将socket server绑定指定的ip和端口号
        # print(f"代理绑定到 {agent_host}:{port}")
        # self.socket_service.bind(agent_host,port) # , agent_port
        # self.socket_service.listen(5)
        # # 设置客户端socket属性，先把它设置成一个空对象，后续有客户端请求过来之后再更新
        # self.client_socket = None
        # # 设置服务器socket属性，生成一个socket对象
        # self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # # 将server_socket连接到游戏服务器
        # self.server_socket.connect(server_host, server_port) #, server_port
        # # 给代理设置一个是否存活的状态，用于在遇到某些异常的时候终止转发线程
        # self.alive = True
 
        # 创建代理服务器的socket对象
        self.socket_service = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # 绑定到代理服务器地址和端口
        self.socket_service.bind((agent_host, port))
        print(f"成功绑定到端口: {port}")

        # 创建连接到游戏服务器的socket对象
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # 连接到游戏服务器地址和端口
        self.server_socket.connect((server_host, server_port))
        print(f"成功连接到游戏服务器: {server_host}:{server_port}")
    


    def start_forwarding(self):
    # """
    # 启动转发线程
    # """
    # 使用threading.Thread代替Timer
        t1 = threading.Thread(target=self.client_to_server)
        t2 = threading.Thread(target=self.server_to_client)
        t1.start()
        t2.start()


    def client_to_server(self):
        """
        转发客户端发送给服务器的包
        1.获取客户端发起的字节流
        2.通过server socket进行转发
        3.循环此步骤
        :return:
        """
        while self.alive:
            # 从客户端处接收客户端发送的协议内容
            data = self.client_socket.recv (65535)
            if data:
                print (data)
                # 将客户端的协议通过server_socket转发给服务器
                self.server_socket.send (data)
            else:
                print (f'收到了空字节流，socket连接可能断开')
                # 收到空字节流，说明socket已断开，将alive设置成False，停止转发
                # 还有其他的异常，后续会慢慢补充
                self.alive = False
            time.sleep (0.01)

    def server_to_client(self):
        """
        转发服务器返回给客户端的包
        1.获取服务器返回的字节流
        2.调用client socket，将服务器返回的字节流直接转发给客户端
        3.循环此步骤
        :return:
        """
        while self.alive:
            # 从服务器处等待返回的协议
            data = self.server_socket.recv (65535)
            if data:
                print(data)
                # 将服务器返回的协议通过client_socket转发给客户端
                self.client_socket.send (data)
            else:
                print (f'收到了空字节流，socket连接已经断开')
                self.alive = False
            time.sleep (0.01)

    def start(self):
        """
        代理启动方法
        :return:
        """
        # 接受客户端的连接
        self.client_socket, addr = self.socket_service.accept()
        print(f"客户端连接到代理: {addr}")
        # 启动转发线程
        self.start_forwarding()

    def stop(self):
        """
        代理结束方法
        :return:
        """
        # 在代理停止运行时，关闭客户端、服务器与代理之间的socket连接
        self.server_socket.shutdown(2)
        self.server_socket.close()
        self.socket_service.shutdown(2)
        self.socket_service.close()



if __name__ == '__main__':

    agent = Agent("192.160.29.185", "39.98.196.51", (10812, 10888), 42708)
    agent.start()