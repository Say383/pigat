import time
import json
import zlib
import requests
import scrapy
import pymongo
from bs4 import BeautifulSoup
from pigat.items import PigatItem_cms


class pigat_ip(scrapy.Spider):
	name = 'pigat_cms'

	def start_requests(self):
		headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0'}
		ip_headers = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0',
			'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
		}
		url = self.url  # 待爬取 URL

		client = pymongo.MongoClient('localhost', 27017)  # 连接数据库
		collection = client['pigat']['pigat_subdomain']  # 读取数据
		if list(collection.find({'url': url})) == []:  # 判断数据是否为空
			print(
				'\n\033[1;31m[{}] 数据库中未查询到 {} 的子域信息，无法进行 {} 的 CMS 信息，请先获取 {} 的子域信息\n\033[0m'.format(time.strftime('%Y-%m-%d %H:%M:%S'),
				                                                                    url, url, url))
		else:
			print('\n\033[1;33m[{}] 正在被动收集 {} 的子域 CMS 信息……\033[0m'.format(time.strftime('%Y-%m-%d %H:%M:%S'), url))
			for i in collection.find({'url': url}):
				subdomain_url = i['subdomain_url']
 
				# 子域cms查询
				if 'http' not in subdomain_url:
					sub_url1 = 'http://' + subdomain_url
					yield scrapy.Request(sub_url1, headers=headers, meta={'url': url, 'sub_url': sub_url1},
				                     callback=self.sub_cms)
					sub_url2 = 'https://' + subdomain_url
					yield scrapy.Request(sub_url2, headers=headers, meta={'url': url, 'sub_url': sub_url2},
					                     callback=self.sub_cms)
				else:
					yield scrapy.Request(subdomain_url, headers=headers, meta={'url': url, 'sub_url': subdomain_url},
					                     callback=self.sub_cms)

	def sub_cms(self, response):
		url = response.meta['url']
		subdomain_url = response.meta['sub_url']
		whatweb_dict = {"url": response.url, "text": response.text,
		                "headers": dict(self.convert(response.headers))}
		whatweb_dict = json.dumps(whatweb_dict)
		whatweb_dict = whatweb_dict.encode()
		whatweb_dict = zlib.compress(whatweb_dict)
		data = {"info": whatweb_dict}
		cms_response2 = requests.post(url="http://whatweb.bugscaner.com/api.go", files=data)
		cms_json = json.loads(cms_response2.text)
		cms_soup = BeautifulSoup(response.text, 'html.parser')
		try:
			cms_title = cms_soup.title.text
		except:
			cms_title = ''
			pass

		try:
			cms_CMS = cms_json['CMS'][0]
		except:
			cms_CMS = ''
			pass

		try:
			cms_Font_Scripts = cms_json['Font Scripts'][0]
		except:
			cms_Font_Scripts = ''
			pass

		try:
			cms_JavaScript_Frameworks = cms_json['JavaScript Frameworks'][0]
		except:
			cms_JavaScript_Frameworks = ''
			pass

		try:
			cms_JavaScript_Libraries = cms_json['JavaScript Libraries'][0]
		except:
			cms_JavaScript_Libraries = ''
			pass

		try:
			cms_Miscellaneous = cms_json['Miscellaneous'][0]
		except:
			cms_Miscellaneous = ''
			pass

		try:
			cms_Operating_Systems = cms_json['Operating Systems'][0]
		except:
			cms_Operating_Systems = ''
			pass

		try:
			cms_Photo_Galleries = cms_json['Photo Galleries'][0]
		except:
			cms_Photo_Galleries = ''
			pass

		try:
			cms_Programming_Languages = cms_json['Programming Languages'][0]
		except:
			cms_Programming_Languages = ''
			pass

		try:
			cms_Web_Frameworks = cms_json['Web_Frameworks'][0]
		except:
			cms_Web_Frameworks = ''
			pass

		try:
			cms_Web_Servers = cms_json['Web Servers'][0]
		except:
			cms_Web_Servers = ''
			pass

		try:
			cms_Widgets = cms_json['Widgets'][0]
		except:
			cms_Widgets = ''
			pass

		try:
			cms_error = cms_json['error'][0]
		except:
			cms_error = ''
			pass

		try:
			cms_Waf = cms_json['Waf'][0]
		except:
			cms_Waf = ''
			pass

		try:
			cms_CDN = cms_json['CDN'][0]
		except:
			cms_CDN = ''
			pass

		try:
			cms_Marketing_Automation = cms_json['Marketing Automation'][0]
		except:
			cms_Marketing_Automation = ''
			pass

		item = PigatItem_cms(
			url=url,
			subdomain_url=subdomain_url,
			cms_title=cms_title,
			cms_CMS=cms_CMS,
			cms_Font_Scripts=cms_Font_Scripts,
			cms_JavaScript_Frameworks=cms_JavaScript_Frameworks,
			cms_JavaScript_Libraries=cms_JavaScript_Libraries,
			cms_Miscellaneous=cms_Miscellaneous,
			cms_Operating_Systems=cms_Operating_Systems,
			cms_Photo_Galleries=cms_Photo_Galleries,
			cms_Programming_Languages=cms_Programming_Languages,
			cms_Web_Frameworks=cms_Web_Frameworks,
			cms_Web_Servers=cms_Web_Servers,
			cms_Widgets=cms_Widgets,
			cms_error=cms_error,
			cms_Waf=cms_Waf,
			cms_CDN=cms_CDN,
			cms_Marketing_Automation=cms_Marketing_Automation
		)
		yield item

		cms_info = ''
		for i in cms_json:
			cms_info = cms_info + '\t' + cms_json[i][0]
		print('\033[1;32m[{}] {}\t{}\t{}\t{}\033[0m'.format(time.strftime('%Y-%m-%d %H:%M:%S'), url, subdomain_url,
		                                                       cms_title, cms_info))

		if cms_response2.headers['X-RateLimit-Remaining'] == '今日识别 cms 剩余次数：0':
			print('\033[1;33m[{}] 每天有 1500 次免费识别次数，今日剩余次数已为 0，挂代理可继续使用\n\033[0m'.format(
				time.strftime('%Y-%m-%d %H:%M:%S')))

	def convert(self, data):
		if isinstance(data, bytes):  return data.decode('ascii')
		if isinstance(data, list):   return data.pop().decode('ascii')
		if isinstance(data, dict):   return dict(map(self.convert, data.items()))
		if isinstance(data, tuple):  return map(self.convert, data)
		return data
