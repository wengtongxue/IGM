import requests
from concurrent.futures import *
import IGM,threading
class domain_burp:      # 子域名爆破
    def __init__(self) -> None:
        self.lock = threading.Lock()

    def check_domain(self,url):     #定义一个检查domain状态的函数
        headers = {
        'User-Agent': 'Mozilla/5.0 (x11; Linux x86_64;rv:68.0)Gecko/20100101 Firefox/68.0'
            }
        try:            #这里使用try是因为这样才能避开不存在的url的异常，从而继续执行文件里的下一个参数
            resp = requests.get(url=url,headers=headers,timeout=3)
            if resp.status_code == 200:
                with self.lock:
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
            with open('./Dict/domain.txt') as file:
                domains=[f"http://{line.strip()}.{site}" for line in file]
            with ThreadPoolExecutor(max_workers=max_workers) as executor:  #创建一个线程池，最大线程根据后面的设置进行配置
                futures = {executor.submit(self.check_domain, domain): domain for domain in domains}  #发起连接任务，进行参数的传入建立多个连接状态测试    
        except Exception as e:
            print(f"发生了未知错误：{e}")
    
    def run_all(self):
        try:
            target_domain = input("请输入要爆破的子域名（如baidu.com）or  返回上一个选项框(输入'exit'即可): ")  
            if target_domain.lower() == 'exit':
                IGM.main()
            elif target_domain:
                default_domain=target_domain
            else:
                print("\033[31m请输入域名！！！\033[0m")
                self.run_all()
            num_threads_input = input("请输入线程数(默认为10): ")  
            max_workers = int(num_threads_input) if num_threads_input.isdigit() else 10  # 转换输入为整数，或默认为10  
            self.domain_bp(default_domain,max_workers)
        except KeyboardInterrupt:  # 捕获用户中断（如Ctrl+C）  
            print("\n\033[31m用户中断查询。\033[0m")
            IGM.main()  
        except Exception as e:  
            print(f"发生未知错误：{e}")