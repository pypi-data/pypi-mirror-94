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

        pymodules = [f.replace('/', '.')[:-3] for f in self.pyfiles]
        self.add_modules([f.strip('.__init__') for f in pymodules])

    def add_modules(self, modules):
        self.pymodules = self.pymodules.union(set(modules))

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

                for export in imported_module.EXPORTS:

                    self.add_plugin(export)

            except Exception as e:
                msg = f'Error importing module: {module}: {e!r}'
                print(msg)

        
        
            
