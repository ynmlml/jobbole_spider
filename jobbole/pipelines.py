# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from jobbole.items import JobboleItem

class JobbolePipeline(object):
	path='/usr/jobbole/'
  	def process_item(self, item, spider):
    	title=item['title']
    	for it in ['/',':','?','<','>']:
        	title=title.replace(it,' ')
    		f=open(self.path+title+'.html','w')
    		f.write(item['content'])
    		f.close()
			return item
