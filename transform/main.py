#newspaper_receipe
"""Limpia el DataSet"""
import argparse
import logging
import hashlib
import nltk 	#permite separar palabras y contar la frecuencia de estas

logging.basicConfig(level = logging.INFO)
from urllib.parse  import urlparse
from nltk.corpus import stopwords #stopwords son palabras que no aportan al analisis (de, a, el, la, etc)

import pandas as pd

logger = logging.getLogger(__name__)
stop_words = set(stopwords.words('spanish')) #el conjunto de los stopwords en español

def main(filename):
	logger.info('Starting cleaning process')
	df = _read_data(filename)							#lee el archivo csv
	newspaper_uid = _extrac_newspaper_uid(filename)		#extrae el nombre del 'news_site' desde el nombre del archivo csv (lo primero que aparece antes del '_')
	df = _add_newspaper_uid_column(df, newspaper_uid)	#agrega la columna con el nombre del 'news_site'
	df = _extract_host(df)								#extrae el host del 'news_site' (el nombre del periodico de la url)
	df = _fill_missing_titles(df)						#rellena titles perdidos (si el articulo no tiene titulo, lo rellena a partir del link)
	df = _generate_uids_for_rows(df)					#genera un id por cada fila
	df = _remove_new_lines_from_body(df)				#elimina saltos de linea ('\n') del body
	df = _tokenize_columns(df, 'body')					#agrega un columna con el numero de tokens del body
	df = _tokenize_columns(df, 'title')					#agrega un columna con el numero de tokens del title
	df = _remove_duplicate_entries(df,'title')			#elimina titles repetidos
	df = _drop_rows_with_missing_values(df)				#eliminar rows con entradas invalidas
	_save_data(df,filename)								#guarda en .csv
	return df


def _read_data(filename):
	logger.info('Readding file {}'.format(filename))
	
	return pd.read_csv(filename)


def _extrac_newspaper_uid(filename):
	logger.info('Extracting newspaper uid')
	newspaper_uid = filename.split('_')[0]
	logger.info('Newspaper uid detected:{}'.format(newspaper_uid))
	
	return newspaper_uid

	
def _add_newspaper_uid_column(df, newspaper_uid):
	logger.info('Filling newspaper_uid column with {}'.format(newspaper_uid))
	df['newspaper_uid'] = newspaper_uid

	return df


def _extract_host(df):
	logger.info('Extracting host from urls')
	df['host'] = df['link'].apply(lambda link: urlparse(link).netloc)

	return df


def _fill_missing_titles(df):
	logger.info('Filling missing titles')
	missing_titles_mask = df['title'].isna()
	missing_titles = (df[missing_titles_mask]['link']
						.str.extract(r'(?P<missing_titles>[^/]+)$')
						.applymap(lambda title: title.split('-'))
						.applymap (lambda title_word_list: ' '.join(title_word_list))
						)
	df.loc[missing_titles_mask, 'title'] = missing_titles.loc[:,'missing_titles']

	return df


def _generate_uids_for_rows(df):
	logger.info('Generating uids for each row')
	uids = (df
			.apply(lambda row: hashlib.md5(bytes(row['link'].encode())),axis = 1)
			.apply(lambda hash_object: hash_object.hexdigest())
			)
	df['uid']=uids

	return df.set_index('uid')


def _remove_new_lines_from_body(df):
	logger.info('Remove new lines from body')

	stripped_body = (df
					.apply (lambda row: row['body'], axis = 1)
					.apply (lambda body: list(body))
					.apply (lambda letters: list(map(lambda letter: letter.replace('\n',' '), letters)))
					.apply (lambda letters: ''.join(letters))
					)
	df['body'] = stripped_body

	return df


def _tokenize_columns(df,column_name):
	global stop_words
	logger.info('Calculing the number of tokens in {}'.format(column_name))

	count_tokens = (df
					.dropna()																				#elimina si existe un na
					.apply (lambda row: nltk.word_tokenize(row[column_name]), axis = 1)						#tokeniza una columna
					.apply (lambda tokens: list(filter(lambda token: token.isalpha(), tokens)))				#filtra las palabras que son alfanumericas y devuelve una lista
					.apply (lambda tokens: list(map(lambda token:token.lower(), tokens)))					#convierte las palabras en minuscula y devuelve una lista
 					.apply (lambda word_list: list(filter(lambda word: word not in stop_words, word_list)))	#filtra las palabras que no son stopwords y devuelve una lista
					.apply (lambda valid_word_list: len(valid_word_list))									#cuenta cuantas palabras hay tokenizadas
					)
	df['n_tokens_{}'.format(column_name)] = count_tokens		
	
	return df


def _remove_duplicate_entries(df,column_name):
	logger.info('Removing duplicates entries')
	df.drop_duplicates(subset=[column_name], keep='first',inplace = True)

	return df


def _drop_rows_with_missing_values(df):
	logger.info('Dropping rows with missing values')
	return df.dropna()


def _save_data(df,filename):
	clean_filename = 'clean_{}'.format(filename)
	logger.info('Saving data at location: {}'.format(clean_filename))
	df.to_csv(clean_filename)


if __name__ == '__main__':
	parser = argparse.ArgumentParser() 	
	parser.add_argument('filename',
						help = 'The path to dirty data',
						type = str)

	args = parser.parse_args()

	df = main(args.filename)
	logger.info('clean process ended')