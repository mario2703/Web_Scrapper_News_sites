#Cargando datos a SQLite
import argparse
import logging
logging.basicConfig(level=logging.INFO)

import pandas as pd

from article import Article
from base import Base, engine, Session

logger = logging.getLogger(__name__)


def main(filename):
	Base.metadata.create_all(engine)  #genera el schema
	session = Session()					#generamos la sesion
	articles = pd.read_csv(filename)	#leermos el csv

	#iteramos por todos los articulos en los archivos limpios
	for index, row in articles.iterrows():
		logger.info('Loading article uid {} into DB'.format(row['uid']))
		article = Article(row['uid'],
							row['body'],
							row['link'],
							row['title'],
							row['newspaper_uid'],
							row['host'],
							row['n_tokens_body'],
							row['n_tokens_title'])

		session.add(article)

	session.commit()	#genera commit
	session.close()		#cierra la sesion


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('filename', 
						help='The file you want to load into the db',
						type=str)

	args = parser.parse_args()

	main(args.filename)