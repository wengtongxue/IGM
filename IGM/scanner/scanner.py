import nmap
import IGM

# python3 port_scan.py <host> <start_port>-<end_port>
class scanner:
    def scan_options(self):
        self.scan_function = input("1) 主机发现\n2) 端口扫描\n3) 返回菜单\n\033[32m请选择你要扫描的功能:\033[0m")
        if self.scan_function == '1':
            self.scan_host()
        elif self.scan_function == '2':
            self.scan_port()
        elif self.scan_function == '3':
            IGM.main()
        else:
            print("\033[31m请选择正确的选项！！！\033[0m")
            self.scan_options()

    def scan_host(self):
        nm = nmap.PortScanner()
        IPS = input("请输入目标网络范围 (例: 192.168.1.0/24)：")
        print("扫描中......")
        if 9 > len(IPS) or len(IPS) > 18:
            print("\033[31mIP格式有问题，请重新输入！！！\033[0m")
            self.scan_host() 
        else:
            nm.scan(hosts=IPS, arguments='-sn')
        for host in nm.all_hosts():
            print(f'\033[32m发现主机: {host}\033[0m')
        self.scan_function=input("扫描完毕！请继续你的选择：\n1) 主机发现\n2) 端口扫描\n3) 返回菜单\n请选择你要扫描的功能:")
        if self.scan_function == '1':
            self.scan_host()
        elif self.scan_function == '2':
            self.scan_port()
        elif self.scan_function == '3':
            IGM.main()
        else:
            print("\033[31m请选择正确的选项！！！\033[0m")
            self.scan_options()
    
    def scan_port(self):
        nm = nmap.PortScanner()
        IP = input("请输入要扫描的IP：")
        print("扫描中......")
        if 7 > len(IP) or len(IP) > 15:
            print("\033[31mIP格式有问题，请重新输入！！！\033[0m")
            self.scan_port()
        else:
            nm.scan(hosts=IP,arguments='-sV')

        for host in nm.all_hosts():
            print(f'\033[32m----------------------------------------------------\nHost : {host}\nState : {nm[host].state()}\033[0m')
            for proto in nm[host].all_protocols():
                print(f'\033[32m----------\nProtocol : {proto}\033[0m')
                lport = list(nm[host][proto].keys())
                for port in lport:
                    print(f'\033[31mPort : {port} \t State : {nm[host][proto][port]["state"]}\033[0m')                  
                    service = nm[host][proto][port]['product']
                    version = nm[host][proto][port]['version']
                    extrainfo = nm[host][proto][port]['extrainfo']
                    print(f'\033[32mService: {service}\nVersion: {version}\nExtra Info: {extrainfo}\033[0m')
        self.scan_function2=input("扫描完毕！请继续你的选择：\n1) 主机发现\n2) 端口扫描\n3) 返回菜单\n请选择你要扫描的功能:")
        if self.scan_function2 == '1':
            self.scan_host()
        elif self.scan_function2 == '2':
            self.scan_port()
        elif self.scan_function2 == '3':
            IGM.main()
        else:
            print("\033[31m请选择正确的选项！！！\033[0m")
            self.scan_options()
