from zipfile import ZipFile
import tempfile
import shutil
import os
import sublime

PKG_SUFFIX = '.sublime-package'


def _zipdir(path, zip):
    for root, dirs, files in os.walk(path):
        for file in files:
            loc = os.path.join(root, file)
            # Make sure plugin files are at root
            arcname = os.path.relpath(loc, start=path)
            zip.write(loc, arcname=arcname)


def _make_zip_file(data):
    zip_file = tempfile.mkstemp()[1]
    with open(zip_file, 'wb') as f:
        f.write(data)
    return zip_file


def install_zip(package, zip_data):
    try:
        zip_file = _make_zip_file(zip_data)
        prefix = ''

        tmpname = tempfile.mkdtemp()

        # Extract files from zip data
        with ZipFile(zip_file, 'r') as myzip:
            prefix = os.path.commonprefix(myzip.namelist())
            myzip.extractall(path=tmpname)

        # Repackage with correct name, location and folder tree
        pkg = package.name + PKG_SUFFIX
        install_path = os.path.join(sublime.installed_packages_path(), pkg)
        with ZipFile(install_path, 'w') as myzip:
            _zipdir(os.path.join(tmpname, prefix), myzip)

    except Exception as e:
        raise e
    finally:
        shutil.rmtree(tmpname)
        os.remove(zip_file)
    return True


def remove_zip(package_name):
    pkg = package_name + PKG_SUFFIX
    pkg_path = os.path.join(sublime.installed_packages_path(), pkg)
    try:
        os.remove(pkg_path)
    except Exception:
        return False
    return True
