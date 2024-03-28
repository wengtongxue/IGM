import requests
from concurrent.futures import *
import IGM,os,threading
class dir_burp:      # 子域名爆破
    def __init__(self) -> None:
        self.lock = threading.Lock()

    def show_options(self):
        self.target_domain = input("请输入要扫描的URL（如baidu.com）or  返回上一个选项框(输入'exit'即可): ")  
        if self.target_domain.lower() == 'exit':
            IGM.main()
        elif self.target_domain:
            self.default_domain=self.target_domain
        else:
            print("\033[31m请输入URL！！！\033[0m")
            self.run_all()
        self.num_threads_input = input("请输入线程数(默认为10): ")  
        self.max_workers = int(self.num_threads_input) if self.num_threads_input.isdigit() else 10  # 转换输入为整数，或默认为10  
    
    def dir_choice(self):
        selection2 = input("\033[32m请选择要爆破的类型\033[0m\n1) 列出可使用的工具自带字典\n2) 自定义字典路径\n3) 返回上一个选项框\n4) 退出该功能模块\n请选择：")
        if selection2 == '1':
            pass_list = os.listdir("./Dict/dir")
            array = []
            index = 0
            for item in pass_list:
                array.append(item)
                print(index, ":", item)
                index += 1
            index = input("选择一个字典 or 返回上一个选项框（输入'exit'即可）:")
            if index.lower() == 'exit':
                print("\033[32m返回成功\033[0m")
                self.dir_choice()
            elif index == index:
                a=int(index)
                self.password_path = array[a]
                print(f"您选用了{self.password_path}字典\n开始爆破......")
                with open(f'./Dict/dir/{self.password_path}') as passwords_file:   
                        self.passwords = passwords_file.readlines() 
        elif selection2 == '2': 
            while True:
                self.password_path = input("字典文件路径(绝对路径):")
                if os.path.isfile(self.password_path):  
                    print(f"您选用了{self.password_path}字典\n开始爆破......")
                    with open(self.password_path) as passwords_file:   
                        self.passwords = passwords_file.readlines()  
                    break 
                else:    
                    print(f"文件路径不正确或文件不存在: {self.password_path}")
        elif selection2 == '3':
            print("\033[32m返回成功\033[0m")
            self.show_options()
        elif selection2 == '4':
            IGM.main() 

    def check_domain(self,url):     #定义一个检查domain状态的函数
            headers = {
            'User-Agent': 'Mozilla/5.0 (x11; Linux x86_64;rv:68.0)Gecko/20100101 Firefox/68.0'
                }
            try:            #这里使用try是因为这样才能避开不存在的url的异常，从而继续执行文件里的下一个参数
                resp = requests.get(url=url,headers=headers,timeout=3)
                if resp.status_code == 200:
                    with self.lock:
                        if '<h1>Not Found</h1>' in resp.text:  # 检查页面内容是否包含 "Not Found"
                            print(f"\033[33m{url}: Page Not Found\033[0m")
                        else:
                            print(f"\033[32m{url}\033[0m")   
                else:                       #基于目标网址存在的情况,状态码为200时返回该url，不为200时返回报错的状态码
                    with self.lock:
                        print(f"\033[41m{url}:status code: {resp.status_code}\033[0m")       #\033[41m 代表红色     \033[32m 代表绿色
            except KeyboardInterrupt:  # 捕获用户中断（如Ctrl+C）  
                with self.lock:
                    print("\n\033[31m用户中断查询。\033[0m")
                    IGM.main()
    
    def domain_bp(self,site,max_workers):       #域名字典多线程爆破       
        #跑字典对拼接的子域名进行访问测试，并配置线程池，默认线程值为10
        try:
            with open(f'./Dict/dir/{self.password_path}') as file:
                domains=[f"http://{site}/{line.strip()}" for line in file]
            with ThreadPoolExecutor(max_workers=max_workers) as executor:  #创建一个线程池，最大线程根据后面的设置进行配置
                futures = {executor.submit(self.check_domain, domain): domain for domain in domains}  #发起连接任务，进行参数的传入建立多个连接状态测试
                for future in as_completed(futures):  #按照任务完成的顺序进行结果的输出
                    domain = futures[future]  #进行判断，domain代表一个url跟里面线程执行的结果中进行遍历，从而domain跟futures[future]结果同步 
                    try:  
                        # 这里不再需要显式调用 future.result()，因为异常处理已经在 check_domain 函数中完成  
                        pass  # 如果 check_domain 没有抛出异常，这里什么也不做  
                    except Exception as e:  
                        print(f"An error occurred while processing {domain}: {e}")           
        except Exception as e:
            print(f"发生了未知错误：{e}")
    
    def run_all(self):
        self.show_options()
        self.dir_choice()
        try:
            self.domain_bp(self.default_domain,self.max_workers)
        except KeyboardInterrupt:  # 捕获用户中断（如Ctrl+C）  
            print("\n\033[31m用户中断查询。\033[0m")
            IGM.main()  
        except Exception as e:  
            print(f"发生未知错误：{e}")