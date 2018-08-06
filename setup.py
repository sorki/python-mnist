import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

NAME = 'python-mnist'
VERSION = '0.6'

# Compile the list of packages available, because distutils doesn't have
# an easy way to do this.
packages, data_files = [], []
root_dir = os.path.dirname(__file__)
if root_dir:
    os.chdir(root_dir)

srcdir = 'mnist'

for dirpath, dirnames, filenames in os.walk(srcdir):
    # Ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'):
            del dirnames[i]
    if '__init__.py' in filenames:
        pkg = dirpath.replace(os.path.sep, '.')
        if os.path.altsep:
            pkg = pkg.replace(os.path.altsep, '.')
        packages.append(pkg)
    elif filenames:
        prefix = dirpath[(len(srcdir) + 1):]  # Strip "$srcdir/" or "$srcdir\"
        for f in filenames:
            data_files.append(os.path.join(prefix, f))


try:
    f = open(os.path.join(os.path.dirname(__file__), 'README.rst'))
    long_description = f.read().strip()
    f.close()
except:
    long_description = ''

setup(name=NAME,
      version=VERSION,
      description='Simple MNIST and EMNIST data parser written in pure Python',
      long_description=long_description,
      author='Richard Marko',
      author_email='srk@48.io',
      license='BSD',
      url='https://github.com/sorki/python-mnist',
      package_dir={'mnist': 'mnist'},
      packages=packages,
      package_data={'mnist': data_files},

      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Programming Language :: Python'],
      )
