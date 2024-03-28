import socket,whois
from concurrent.futures import *
from burp import SSH_bp,MySQL_bp,dirsearch,domain_bp
from scanner import scanner
banner='''
   ____ ____        _              
  / ___|  _ \ _ __ (_)_ __   ___   
 | |  _| | | | '_ \| | '_ \ / _ \  
 | |_| | |_| | | | | | | | |  __/_ 
  \____|____/|_| |_|_|_| |_|\___(_)
        关注公众号The security
        本工具由GDnine开发，仅用于日常学习使用，禁止非法用途，否则后果由使用者承担！！！
'''

def show_options():  #选项框视图
    # print("本工具为多功能信息收集脚本，请您选择要执行的功能：")
    options='''
        1. Whois 查询
        2. CDN 检测
        3. 子域名收集
        4. MySQL服务爆破
        5. SSH服务爆破
        6. 后台扫描
        7. 端口扫描'''
    try:
        while True:
            a=input(f"\033[32m本工具为多功能信息收集脚本,功能如下：\033[0m\033[31m{options}\033[0m\n\033[32m请您选择要执行的功能：\033[0m")
            if a == "1":
                whois_check()
            elif a == "2":
                check_CDN()
            elif a == "3":
                domians=domain_bp.domain_burp()
                domians.run_all()
            elif a == "4":
                mysql=MySQL_bp.connection_mysql()
                mysql.run_all()
            elif a == '5':
                ssh=SSH_bp.SSH_bp()
                ssh.run_all()
            elif a == '6':
                dir_bp=dirsearch.dir_burp() 
                dir_bp.run_all()
            elif a == '7':
                scanner1 = scanner.scanner()
                scanner1.scan_options()
            # elif a == '8':
            else:
                print("\033[31m请输入正确的选项！！！\033[0m")
    except KeyboardInterrupt:  # 捕获用户中断（如Ctrl+C）  
            print("\n\033[31m用户中断查询。\033[0m")  
    except Exception as e:  
            print(f"发生未知错误：{e}")

def whois_check():  #whois域名邮箱注册查找
    try:
        while True:
            domain=input("请输入要查询的域名（如baidu.com）或输入'exit'退出: ")
            if domain.lower() == 'exit':
                main()
            elif domain.strip():
                try:
                    data=whois.whois(domain)
                    print(f"Whois {domain}的查询结果如下：")
                    print(data)
                    # print("\n\n美观后为以下内容:")
                    # for key,value in data.items():
                    #     print(f"\033[31m{key}\033[0m:\033[32m{value}\033[0m")
                except Exception as e:
                    print(f"Whois 查询失败，可能是网络问题或域名不存在：{e}")  
            else:  
                print("\033[31m输入内容不能为空，请重新输入。\033[0m")
                whois_check()  
    except KeyboardInterrupt:  # 捕获用户中断（如Ctrl+C）  
            print("\n\033[31m用户中断查询。\033[0m")
            main()
    except Exception as e:  
            print(f"发生未知错误：{e}")
    
def check_CDN():  # CDN检测
    try:
        while True:
            ip_list = []
            number = 0
            domain=input("请输入要检查的域名CDN（如baidu.com）或输入'exit'退出: ")
            if domain.lower() == 'exit':
                main()
            elif domain.strip():
                try:
                    addrs = socket.getaddrinfo(domain, 'http')  #[(<AddressFamily.AF_INET: 2>, <SocketKind.SOCK_STREAM: 1>, 0, '', ('10.20.10.13', 80)), (<AddressFamily.AF_INET: 2>, <SocketKind.SOCK_STREAM: 1>, 0, '', ('10.20.10.13', 80))]
                    for item in addrs:                           
                        if item[4][0] not in ip_list:
                            ip_list.append(item[4][0])          #获取到的形式以列表进行返回，后面进行一步一步的内容获取，把列表细拆分为多个内元组，在把元组里的值进行筛选，得到我们想要的ip
                            number += 1                         #进行添加判断，以列表的形式进行去重存储
                except Exception as e:
                    print(str(e))
                if number > 1:  # getaddrinfo的返回结果中，多于一个ip，即存在cdn    #最后进行对数量的判断
                    for i in ip_list:
                        print(f'IP:{i}')
                    print(f"\033[31m{domain}部署了CDN!!!请使用CDN测试网站进一步查看:\033[0m\n\033[32mhttp://www.cdnplanet.com/tools/cdnfinder/\nhttps://ping.chinaz.com/\033[0m")
                else:
                    print(f"\033[32m不存在CDN,IP地址为：{ip_list}\033[0m")
            else:
                print("\033[31m输入内容不能为空，请重新输入。\033[0m")
    except KeyboardInterrupt:  # 捕获用户中断（如Ctrl+C）  
            print("\n\033[31m用户中断查询。\033[0m")
            main()  
    except Exception as e:  
            print(f"\033[31m发生未知错误：{e}\033[0m")







def main():
    options='''
        1. Whois 查询
        2. CDN 检测
        3. 子域名收集
        4. MySQL服务爆破
        5. SSH服务爆破
        6. 后台扫描
        7. 端口扫描'''
    a=input(f"\033[31m操作成功!\033[0m\033[31m{options}\033[0m\n请继续输入您的选择（输入数字即可）：")  
    try:
        while True:
        # a=input(f"执行完毕!{options}\n请继续输入您的选择（输入数字即可）：")   
            if a == "1":
                whois_check()
            elif a == "2":
                check_CDN()
            elif a == "3":
                domians=domain_bp.domain_burp()
                domians.run_all()
            elif a == "4":
                mysql=MySQL_bp.connection_mysql()
                mysql.run_all()
            elif a == "5":
                ssh=SSH_bp.SSH_bp()
                ssh.run_all()
            elif a == "6":
                dir_bp=dirsearch.dir_burp()
                dir_bp.run_all()
            elif a == "7":
                scanner1 = scanner.scanner()
                scanner1.scan_options()
            elif a == "8":
                pass
            else:
                print("\033[31m请输入正确的选项！！！\033[0m")
                main()
    except KeyboardInterrupt:  # 捕获用户中断（如Ctrl+C）  
        print("\n\033[31m用户中断查询。\033[0m")
        main()
    except Exception as e:  
        print(f"\n\033[31m出错{e}。\033[0m")
        main()

      
if __name__ == '__main__':
    print(banner)
    show_options()
    main()
    check_CDN()
    # print(os.getcwd())    