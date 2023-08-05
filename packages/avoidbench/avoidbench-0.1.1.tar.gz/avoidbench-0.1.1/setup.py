from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import os

class CMakeExtension(Extension):
	def __init__(self, name, sourcedir=""):
		Extension.__init__(self, name, sources=[])
		self.sourcedir = os.path.abspath(sourcedir)
		print(self.sourcedir)

		
setup(
    name='avoidbench',
    version='0.1.1',
    author='Rano Veder',
	author_email="rano.veder@gmail.com",
	url = 'https://github.com/RanoVeder/AvoidBench',
	license='MIT',
    description='Python client for the UE4 avoidbench benchmark simulator',
    long_description='',
	ext_modules=[CMakeExtension("avoidbench")],
    zip_safe=False,
)