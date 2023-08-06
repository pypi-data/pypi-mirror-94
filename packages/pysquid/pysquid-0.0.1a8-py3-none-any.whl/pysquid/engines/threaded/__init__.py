import threading
from concurrent.futures import ThreadPoolExecutor, wait


class ThreadedEngine():

    def __init__(self, template, plugins):
        self.template = template
        self.plugins = plugins
        self.pools = {}

    def build(self):

        services = self.template.get('services')
        plugins = self.plugins
        
        pools = {
            'thread': {}
        }

        playbook = {}

        for sid, service in services.items():

            pool = service.get('__pool__')
            mode = service.get('__mode__')
            plugin = service.get('__plugin__')
            workers = service.get('__workers__')

            if not mode in pools or not plugin in plugins:
                continue

            enabled_workers = set(workers.keys())

            plugin_ = plugins.get(plugin)()
            plugin_.add_service(service, self.template)

            setup = plugin_.iterate_workers(enabled_workers)

            for pid, stages in setup.items():
                if pid not in playbook:
                    playbook[pid] = {}
                    
                for sid, stage in stages.items():
                    if sid not in playbook[pid]:
                        playbook[pid][sid] = []

                    playbook[pid][sid] = playbook[pid][sid] + setup[pid][sid] 

        pools['thread'] = playbook
        self.pools = pools
        
    def exec_pool(self):

        pools = self.pools.get('thread')        
        futures = []

        for pid, pool in pools.items():
            print(f'Running pool {pid}')
            e = ThreadPoolExecutor()
            future = e.submit(self.exec_workers, pool)
            futures.append(future)

        for future in futures:
            print(f'Waiting on {future}')
            wait({future})
            print(f'Future done: {future}')
            
    def exec_workers(self, pool):

        e = ThreadPoolExecutor()
        futures = set()
        
        for sid, stage in pool.items():
            
            for worker in stage:
                futures.add(e.submit(worker.apply))
                
            wait(futures)
                
        return True
    
