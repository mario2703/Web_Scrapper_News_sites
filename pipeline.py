import yaml
import logging
logging.basicConfig(level=logging.INFO)
import subprocess

from extract.common import config


logger = logging.getLogger(__name__)

#Extrae la lista de nombres del sitio
address='extract/config.yaml'
news_sites_uids=list(config(address)['news_sites'].keys())

def main():
	_create()
	_extract()
	_transform()
	_load()

#Crea el diccionario con los nombres, url y queries de cada sitio de noticias, lo exporta en un archivo .yaml y lo mueve a la carpeta extract
def _create():
	logger.info('Starting create process')
	subprocess.run(['python', 'main.py'], cwd='./create')
	subprocess.run(['mv', 'config.yaml', '../extract/config.yaml'], cwd='./create')
	

#Extrae toda la informacion de sitio de noticias, los exporta por nombre y los mueve a la carpeta transform
def _extract():
	global news_sites_uids
	logger.info('Starting extract process for {}'.format(news_sites_uids))
	subprocess.run(['python', 'main.py'], cwd='./extract')	
	for news_sites_uid in news_sites_uids:
		subprocess.run(['find', '.', '-name', '{}*'.format(news_sites_uid), 	#los envia a la carpeta transform
						'-exec', 'mv', '{}', '../transform/{}_.csv'.format(news_sites_uid), 
						';'], cwd='./extract')


#Limpia todos los archivos uno a uno
def	_transform():
	global news_sites_uids
	logger.info('Starting transform process')
	for news_sites_uid in news_sites_uids:
		dirty_data_filename = '{}_.csv'.format(news_sites_uid)			
		clean_data_filename = 'clean_{}'.format(dirty_data_filename)	#copia y cambia de nombre los DataFrame
		subprocess.run(['python', 'main.py', dirty_data_filename], cwd='./transform') #limpia el DataFrame
		subprocess.run(['rm', dirty_data_filename], cwd='./transform/')					#elimina los DataFrame sucios
		subprocess.run(['mv', clean_data_filename, '../load/{}.csv'.format(news_sites_uid)], cwd='./transform')


#Guarda todos los archivos limpios en una base de datos
def	_load():
	logger.info('Starting load process')
	global news_sites_uids
	for news_sites_uid in news_sites_uids:
		clean_data_filename = '{}.csv'.format(news_sites_uid)
		subprocess.run(['python', 'main.py', clean_data_filename], cwd='./load')
		subprocess.run(['rm', clean_data_filename], cwd='./load')


if __name__=='__main__':
	main()
