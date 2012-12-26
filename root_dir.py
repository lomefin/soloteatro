import os

def root_directory():
	return  os.path.dirname(__file__)

def from_root_directory(path):
	return os.path.join(os.path.dirname(__file__),path)