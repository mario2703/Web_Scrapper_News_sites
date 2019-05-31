import logging 
import datetime
import csv
import re #importa expresiones regulares

from common import config #funcion config de create/common.py
from requests.exceptions import HTTPError
from urllib3.exceptions import MaxRetryError

import news_page_objects as news #traemos los objetos


logging.basicConfig(level=logging.INFO)
logger=logging.getLogger(__name__)
#Expresiones regulares
is_well_formed_link = re.compile(r'^https?://.+/.+$')	# https://example.com/hello
is_root_path = re.compile (r'^/.+$')					#/some-text


#Hace scraper por cada site
def _news_scraper(news_site_uid):
	#obtenemos la direccion url
	host=config('config.yaml')['news_sites'][news_site_uid]['url']
	logging.info('Beginning scraper for {}'.format(host))

	#Envia el nombre del site y la url a la clase HomePage
	homepage = news.HomePage(news_site_uid, host)
	articles=[]
	for link in homepage.article_links:
		article = _fetch_article(news_site_uid, host, link) #Rectifica el link de cada articulo
		if article:
			logger.info('Article fetched!!')
			#Enlista los articulos encontrados
			articles.append(article)
			#print(article.title)
		#if len(articles)==3:
		#	break
	#Guarda el articulo
	_save_articles(news_site_uid, articles)


def _save_articles(news_site_uid, articles):
	#formatea la fecha con año, mes y dia
	now = datetime.datetime.now().strftime('%Y_%m_%d')
	#obtiene el nombre del articulo
	out_file_name = '{}_{}_articles.csv'.format(news_site_uid,now)
	#filtra que los articulos no comiencen por _
	csv_headers = list(filter(lambda property: not property.startswith('_'),dir(articles[0])))

	#Guarda el archivo csv
	with open (out_file_name, mode='w+') as f:
		writer = csv.writer(f)
		writer.writerow(csv_headers)

		#cada articulo lo escribimos en el archivo csv
		for article in articles:
			#guarda las propiedades aunque modifiquemos el codigo en un futuro
			row = [str(getattr(article,prop)) for prop in csv_headers]
			writer.writerow(row)

#Rectifica los enlaces de cada articulo
def _fetch_article(news_site_uid, host, link):
	logger.info('Start fetching article at {}'.format(link))

	article = None
	try:
		#Envia cada articulo a la clase ArticlePage
		article = news.ArticlePage(news_site_uid, _build_link(host, link)) #revisa que los vinculos esten bien construidos
	except (HTTPError, MaxRetryError) as e:
		#si ocurre un error, invalida el articulo
		logger.warning('Error while fechting the article', exc_info=False)

	#si el articulo no tiene cuerpo, queda invalidado
	if article and not article.body:
		logger.warning('Invalid article. There is no body')
		return None

	return article

#Revisa los links y valida los principales con las expresiones regulares
def _build_link(host,link):
	if is_well_formed_link.match(link): #si es de tipo  https://example.com/hello
		return link
	elif is_root_path.match(link):		#si es de tipo /some-text
		return '{}{}'.format(host,link)
	else:
		return '{}/{}'.format(host,link)


if __name__ == '__main__':

	#enlista los nombres de los sites
	news_site_choices=list(config('config.yaml')['news_sites'].keys())
	for choices in news_site_choices:
		_news_scraper(choices) 