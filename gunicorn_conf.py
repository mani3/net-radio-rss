import multiprocessing

bind = '127.0.0.1:4002'
workers = multiprocessing.cpu_count() * 2 + 1
timeout = 30
accesslog = '/var/log/net_radio_rss/access.log'
errorlog = '/var/log/net_radio_rss/error.log'
proc_name = 'gunicorn_net_radio_rss'
