from sqlalchemy import Column, String, Integer

from base import Base

class Article(Base):
	__tablename__ = 'articles'

	id = Column(String, primary_key=True)
	body = Column(String)
	link = Column(String, unique=True)
	title = Column(String)
	newspaper_uid = Column(String)
	host = Column(String)
	n_tokens_body = Column(Integer)
	n_tokens_title = Column(Integer)
	

	def __init__(self,
				uid,
				body,
				link,
				title,
				newspaper_uid,
				host,
				n_tokens_body,
				n_tokens_title,
				):
		self.id = uid
		self.body = body
		self.link = link
		self.title = title
		self.newspaper_uid = newspaper_uid
		self.host = host
		self.n_tokens_body = n_tokens_body
		self.n_tokens_title = n_tokens_title
		
		