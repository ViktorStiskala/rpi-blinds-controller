bind = '0.0.0.0:4000'
workers = 1
worker_class = 'sync'

def worker_exit(server, worker):
    worker.app.app_uri
    blinds = worker.app.callable.config['blinds']
    blinds.cleanup()
