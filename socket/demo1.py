from scapy.all import *
import time
import optparse
import datetime


nowtime = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
print(nowtime)
# 回调打印函数
def PackCallBack(packet, hostIP):
    print('*' * 30)
    # 打印源IP，源端口，目的IP，目的端口
    direction = "Outgoing" if packet[IP].src == hostIP else "Incoming"
    print("[%s] %s: %s:%s ----> %s:%s" % (TimeStamp2Time(packet.time), direction, packet[IP].src, packet.sport, packet[IP].dst, packet.dport))
    # 打印数据包
    print('packet',packet.show())
    # 打印协议内容
    if Raw in packet:
        print("Protocol Content: ", packet[Raw].load)
    print('*' * 30)


# 时间戳转换函数
def TimeStamp2Time(timeStamp):
    timeTmp = time.localtime(timeStamp)  # time.localtime()格式化时间戳为本地时间
    myTime = time.strftime("%Y-%m-%d %H:%M:%S", timeTmp)  # 将本地时间格式化为字符串
    return myTime

if __name__ == '__main__':
    parser = optparse.OptionParser("Example:python %prog -i 39.98.196.51 -c 5 -o {nowtime}.pcap\n")
    # 添加IP参数 -i
    parser.add_option('-i', '--IP', dest='hostIP', default='39.98.196.51', type='string', help='IP address [default=39.98.196.51]')
    # 添加数据包总参数 -c
    parser.add_option('-c', '--count', dest='packetCount', default=5, type='int', help='Packet count [default = 5]')
    # 添加保存文件名参数 -o
    parser.add_option('-o', '--output', dest='fileName', default=f'{nowtime}.pcap', type='string', help=f'save filename [default = {nowtime}.pcap]')
    (options, args) = parser.parse_args()
    defFilter = "host " + options.hostIP

    # 使用 PcapWriter 以追加模式打开文件
    writer = PcapWriter(options.fileName, append=True, sync=True)

    # 修改为无限循环捕获数据包
    while True:
        packets = sniff(filter=defFilter, prn=lambda x: PackCallBack(x, options.hostIP), count=options.packetCount)
        # 追加保存输出文件
        for packet in packets:
            writer.write(packet)