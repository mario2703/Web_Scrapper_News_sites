import yaml
sites=yaml.dump({'news_sites':
		{'eluniversal':
			{'url':'http://www.eluniversal.com.mx',
			'queries':
				{'homepage_article_links':'.field-content a',
				'article_title':'pane-content h1','article_body': '.field-name-body'}},
		'elnacional':
			{'url':'http://www.el-nacional.com',
			'queries':
				{'homepage_article_links':'.title a',
				'article_title':'.title','article_body': '.detail-body p'}}}})

archivo=open('config1.yaml', mode='w+')
archivo.write(sites)
archivo.close()