workers = 3    # 进程数
worker_class = "gevent"   # 异步模式
bind = "0.0.0.0:5200" #监听的端口
loglevel = 'debug' #级别
timeout = 300 #超时上限

# 将标准访问日志输出到标准输出
accesslog = '-'

# 将错误日志输出到标准错误
errorlog = '-'