bind = ['0.0.0.0:443','0.0.0.0:80']
workers = 4
worker_class = 'gevent'
worker_connections = 1000
keepalive = 5

keyfile = '/etc/letsencrypt/live/multi-pass.org/privkey.pem'
certfile = '/etc/letsencrypt/live/multi-pass.org/cert.pem'
ca_certs = '/etc/letsencrypt/live/multi-pass.org/chain.pem'
