from pathlib import Path
import importlib
import glob
import pysquid.plugin


class PluginCollector():

    def __init__(self, paths: list = [Path('plugins')]):

        self.paths = set()
        self.pyfiles = set()
        self.pymodules = set()
        self.plugins = {}
        self.get_paths(paths)
        self.get_py_files()

    def get_paths(self, paths):
        
        for path in paths:

            if not isinstance(path, Path):
                continue

            if not path.exists():
                continue

            if not path.is_dir():
                continue

            self.paths.add(path)

    def get_py_files(self):

        all_files = set()

        for path in self.paths:
            files = set(glob.glob(str(path) + '/**/*.py', recursive=True))
            all_files = all_files.union(files)

        self.pyfiles = all_files

        files = [f.replace('.py', '') for f in all_files]
        self.add_modules([f.replace('/__init__', '') for f in files])

    def add_modules(self, modules):
        self.pymodules = self.pymodules.union(set([f.replace('/', '.') for f in modules]))

    def add_plugin(self, plugin):

        try:
            ti = plugin()

            if isinstance(ti, pysquid.plugin.Plugin):
                self.plugins[ti.plugin_id] = plugin

        except Exception as e:
            msg = f'Error adding plugin: {e!r}'
            print(msg)

    def add_plugins(self, plugins: list = []):

        for plugin in plugins:
            self.add_plugin(plugin)

    def collect(self):

        for module in self.pymodules:

            try:
                imported_module = importlib.import_module(module)

                exports = []

                try:
                    exports = imported_module.EXPORTS
                except:
                    pass

                for export in exports:

                    self.add_plugin(export)

            except Exception as e:
                msg = f'Error importing module: {module}: {e!r}'
                print(msg)

        
        
            
