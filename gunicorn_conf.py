import multiprocessing

bind = '127.0.0.1:4002'
workers = multiprocessing.cpu_count() * 2 + 1
timeout = 30
accesslog = '/var/log/internet_radio/access.log'
errorlog = '/var/log/internet_radio/error.log'
proc_name = 'gunicorn_internet_radio'
