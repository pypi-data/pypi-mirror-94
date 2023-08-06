from distutils.core import setup
from setuptools.command.install import install
import os


class CustomInstallCommand(install):
    def run(self):
        print(os.getcwd())
        print("")
        print("")
        print("")
        print(os.listdir())
        install.run(self)


setup(
  name = 'pyfuck',
  packages = ['pyfuck'],
  version = '0.6',
  license='MIT',
  description = 'Python Brainfuck Implementation to Execute as well as Convert Brainfuck Code',
  author = 'Jaysmito Mukherjee',
  author_email = 'jaysmito101@gmail.com',
  url = 'https://github.com/Jaysmito101/PyFuck',
  download_url = 'https://github.com/Jaysmito101/PyFuck/archive/v_03.tar.gz',
  keywords = ['brainfuck', 'interpreter', 'code-converter'],
  install_requires=[
          'numpy',
      ],
  cmdclass={
        'install': CustomInstallCommand,
    },
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)
