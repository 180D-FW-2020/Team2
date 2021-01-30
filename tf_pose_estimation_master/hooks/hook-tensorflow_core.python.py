# from PyInstaller.utils.hooks import collect_submodules, collect_data_files

# hiddenimports = collect_submodules('tensorflow_core')
# datas = collect_data_files('tensorflow_core', subdir=None, include_py_files=True)

from PyInstaller.utils.hooks import collect_data_files, collect_submodules

hiddenimports = collect_submodules('tensorflow_core.core.framework')
hiddenimports += collect_submodules('tensorflow_core.core')
hiddenimports += collect_submodules('tensorflow_core')
hiddenimports += collect_submodules('tensorflow_core.lite.experimental.microfrontend.python.ops')