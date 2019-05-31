import requests
import bs4 			#analiza gramaticamente los objetos

from common import config #funcion config de create/common.py


class NewsPage:

	def __init__(self, news_site_uid, url):
		#Obtenemos los nombres de cada site
		self._config=config('config.yaml')['news_sites'][news_site_uid]
		#Obtenemos las queries
		self._queries=self._config['queries']
		
		self._html=None
		
		self._visit(url)
		
		self._link=url

	#Rregresa el html de querie
	def	_select(self, query_string):

		return self._html.select(query_string)


	#visitamos la pagina, necesitamos el url
	def _visit(self,url):
		#nos regresa el objeto con el html
		response=requests.get(url)
		#response?
		#response??

		#arroja error si la solicitud no fue concluida correctamente
		response.raise_for_status()

		#analiza el objeto html convirtiendolo un objeto
		self._html=bs4.BeautifulSoup(response.text, 'html.parser')

#representa la pagina principal de la web
class HomePage(NewsPage):

	def __init__(self, news_site_uid, url):
		#extiende la clase NewsPage
		super().__init__(news_site_uid,url)
		
 
	#Enlista en un conjunto los links de los articulos
	@property
	def article_links(self):
		link_list=[]
		for link in self._select(self._queries['homepage_article_links']):
			if link and link.has_attr('href'):
				link_list.append(link)

		return set(link['href'] for link in link_list)

#Accede al cuerpo del articulo y al titulo
class ArticlePage(NewsPage):

	def __init__(self,news_site_uid,url):
		#extiende la clase NewsPage
		super().__init__(news_site_uid,url)
	
	#Regresa el titulo desde el cuerpo de la noticia
	@property
	def title(self):
		result = self._select(self._queries['article_title'])

		return result[0].text if len(result) else ''

	#Regresa el body de la noticia
	@property
	def body(self):
		result = self._select(self._queries['article_body'])

		return result[0].text if len(result) else ''

	#Regresa la url de la noticia
	@property
	def link(self):
		return self._link