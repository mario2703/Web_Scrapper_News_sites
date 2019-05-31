"""
Lee los 'sites' del archivo config.yaml
"""

import yaml 
__config = None

address='config.yaml'
def config(address):
	global __config
	if not __config:
		with open(address, mode='r') as f:
			config = yaml.load(f)
	return config
