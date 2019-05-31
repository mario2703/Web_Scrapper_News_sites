"""
Crea un diccionario con los nombres de los sitios, la url, y los queries.
Guarda el diccionario en un archivo .yaml
"""

import yaml

config=None

#clases a donde pertenecen las queries
def class_names():
	tags_names=['homepage_article_links','article_title','article_body']
	tags=[str(input('add class for '+name+': ')) for name in tags_names]
	dict_tags=dict(zip(tags_names,tags))
	
	return dict_tags


#Url and queries
def url_and_queries(uid):
	uaq=dict()
	uaq['url']=str(input('add {}\'s url: '.format(uid)))
	uaq['queries']=class_names()
	
	return uaq


#Agrega las Url and queries a cada sitio
def names_news_sites():
	global news_sites_uids
	names=dict()
	for uid in news_sites_uids:
		names[uid]=url_and_queries(uid)
	
	return names


#Diccionario
news_sites_uids=None
def dict_news_sites():
	global news_sites_uids
	number_of_new_sites=int(input('Number of new sites '))
	news_sites_uids=[str(input('Name of the {}° news site '.format(i+1))) for i in range(number_of_new_sites)]
	dict_news_sites = {'news_sites':names_news_sites()}
	
	return dict_news_sites


#Convierte el diccionario en texto comprendido por yaml
def config():
	config=yaml.dump(dict_news_sites())
	return config


#Guarda el diccionario en un archivo .yaml
def _save():
	archivo=open('config.yaml', mode='w+')
	archivo.write(config())
	archivo.close()

if __name__ == '__main__':
	if not config:
		config()
	_save()


