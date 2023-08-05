import pysquid.plugin


class SampleWorker1(pysquid.plugin.Worker):
    def __init__(self):
        super().__init__('sample_worker_1')

        
class SampleWorker2(pysquid.plugin.Worker):
    def __init__(self):
        super().__init__('sample_worker_1', 1, 3)
        
    def apply(self):
        import time
        time.sleep(10)

class SampleWorker3(pysquid.plugin.Worker):
    def __init__(self):
        super().__init__('sample_worker_3', 1, 2)

    def apply(self):
        import time
        time.sleep(10)


class SampleWorker4(pysquid.plugin.Worker):
    def __init__(self):
        super().__init__('sample_worker_4')

    def apply(self):
        from pathlib import Path

        p = Path('test/e2e/out/simple_1')

        if p.exists():
            p.unlink()

        p.touch()

        
class SamplePlugin1(pysquid.plugin.Plugin):
    def __init__(self):
        super().__init__('sample_plugin_1')
        
        self.workers = {
            'sample_worker_1': SampleWorker1,
            'sample_worker_2': SampleWorker2,
            'sample_worker_3': SampleWorker3
        }

        
class SamplePlugin2(pysquid.plugin.Plugin):
    def __init__(self):
        super().__init__('sample_plugin_2')
        
        self.workers = {
            'sample_worker_4': SampleWorker4,
        }

        
EXPORTS = [
    SamplePlugin1,
    SamplePlugin2
]
