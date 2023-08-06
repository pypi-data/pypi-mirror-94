

class Worker():

    def __init__(self, id_: str, pool: int = 1, stage: int = 1, mode: str = 'thread'):
        self.id_ = id_
        self.pool = pool
        self.stage = stage

    def add_service(self, service, template):
        self.service = service
        self.template = template

    def pre(self):
        pass

    def post(self):
        pass
    
    def apply(self):
        print(self.service)


class Plugin():

    def __init__(self, plugin):
        self.plugin_id = plugin
        self.pools = set()
        self.stages = set()
        self.service = {}
        self.template = {}
        self.workers = {}
        self.enabled_workers = []

    def add_service(self, service, template):
        self.service = service
        self.template = template
        
    def iterate_workers(self, enabled_workers: set = None):

        setup = {}
        
        keys = set(self.workers.keys())
        
        if enabled_workers:
            keys = keys.intersection(enabled_workers)

        for key in keys:
            worker = self.workers.get(key)
            w = worker()
            w.add_service(self.service, self.template)
            self.enabled_workers.append(w)
            
        for worker in self.enabled_workers:

            pool = worker.pool
            stage = worker.stage

            if pool not in setup:
                setup[pool] = {}

            if stage not in setup[pool]:
                setup[pool][stage] = []

            setup[pool][stage].append(worker)
            
        return setup
            
    def apply(self):
        print(self.plugin_id)
