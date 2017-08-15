try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

config = [
	'description':'A bunch of fun with trees',
	'author': 'Itai Maimon',
	'url':'addlater',
	'download_url':'make new'
	'author_email':'itaimaimon@gmail.com'
	'version':'0.1',
	'install_requires':['nose'],
	'packages':['treefun'],
	'scripts':[],
	'name':'treefun'
	]
	setup(**config)
	