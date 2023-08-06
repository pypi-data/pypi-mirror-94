import sys
import os
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication
from PySide2.QtQml import QQmlApplicationEngine
from .PluginLoader import scan_plugins


params = {
    'verbose': False
}


def debug_print(msg):
    if params['verbose']:
        print(msg)


class App(object):
    def __init__(self, argv):
        import os
        os.environ['QT_SCALE_FACTOR'] = '0'
        QApplication.setAttribute(Qt.AA_UseDesktopOpenGL)
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
        self._argv = argv

    def run(self, path):
        # Create an instance of the application
        # QApplication MUST be declared in global scope to avoid segmentation
        # fault
        app = QApplication(self._argv)

        # Create QML engine
        engine = QQmlApplicationEngine()

        plugin_dir = path / 'plugins'
        imports_dir = path / 'imports'
        entry_path = path / 'src' / 'main.qml'
        
        sys.path.append(str(plugin_dir))
        if os.path.isdir(str(plugin_dir)):
            plugins = scan_plugins(str(plugin_dir))
            # install all
            for p in plugins:
                p.install()
                debug_print('Plugin %s loaded' % p.uri)
        else:
            debug_print('No plugin folder found!')

        engine.addImportPath(str(plugin_dir))
        engine.addImportPath(str(imports_dir))

        # Load the qml file into the engine
        debug_print('Start from entry %s' % str(entry_path))
        engine.load(str(entry_path))

        # Qml file error handling
        if not engine.rootObjects():
            sys.exit(-1)

        return app.exec_()


def boilerplate(path):
    if not os.path.isdir(str(path / 'imports')):
        os.mkdir(str(path / 'imports'))
    if not os.path.isdir(str(path / 'plugins')):
        os.mkdir(str(path / 'plugins'))
    if not os.path.isdir(str(path / 'src')):
        os.mkdir(str(path / 'src'))
    with open(str(path / 'src' / 'main.qml'), 'w') as f:
        f.write("""import QtQuick 2.12
import QtQuick.Controls 2.12

ApplicationWindow {
    width: 800
    height: 600
    visible: true
    title: 'PyQMLApp'
}
"""
        )


def run():
    import pathlib
    import argparse

    parser = argparse.ArgumentParser(description='PyQMLApp')
    parser.add_argument('path', type=str, help='project root')
    parser.add_argument('--boilerplate', action='store_true', help='boilerplate new project')
    parser.add_argument('--verbose', action='store_true', help='display more info')

    args = parser.parse_args()
    path = pathlib.Path(args.path)
    if args.verbose:
        params['verbose'] = True
    if args.boilerplate:
        boilerplate(path)
        sys.exit(0)
    app = App(sys.argv)
    sys.exit(app.run(path))
