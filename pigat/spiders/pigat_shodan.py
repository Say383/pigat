import time
import json
import scrapy
import pymongo
from pigat.items import PigatItem_shodan


class pigat_shodan(scrapy.Spider):
	name = 'pigat_shodan'

	def start_requests(self):
		headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0'}
		url = self.url  # 待爬取 URL
		client = pymongo.MongoClient('localhost', 27017)  # 连接数据库
		collection = client['pigat']['pigat_ip']  # 读取数据
		if list(collection.find({'url': url})) == []:  # 判断数据是否为空
			print(
				'\n\033[1;31;40m[{}] 数据库中未查询到 {} 的 IP 信息，无法进行 {} 的 shodan 信息查询，请先获取 {} 的子域名 IP 信息\n\033[0m'.format(time.strftime('%Y-%m-%d %H:%M:%S'),
				                                                                    url, url, url))
		else:
			print('\n\033[1;33;40m[{}] 正在被动收集 {} 的子域 shodan 信息……\033[0m'.format(time.strftime('%Y-%m-%d %H:%M:%S'), url))
			print(
				'\033[1;33;40m[{}] 如果您的 api 输入错误，可到数据库中修改\033[0m'.format(time.strftime('%Y-%m-%d %H:%M:%S'), url))
			# 判断是否存在api
			collection_api = client['pigat']['shodan_api']  # 读取数据
			if list(collection_api.find()) == []:  # 判断数据是否为空
				shodan_api = input(
					"\033[1;31;40m[{}] 请输入你的shodan api : \033[0m".format(time.strftime('%Y-%m-%d %H:%M:%S')))
				collection_api.insert({'shodan_api': shodan_api})
			else:
				shodan_api = collection_api.find_one()['shodan_api']
			ip_temp = []
			for i in collection.find({'url': url}):
				sub_ip = i['sub_ip']
				if sub_ip not in ip_temp:  # 判断ip是否重复
					ip_temp.append(sub_ip)  # 如果不重复就添加到数组里
					subdomain_url = []
					for i in collection.find({'sub_ip': sub_ip}):
						subdomain_url.append(i['subdomain_url'])  # 将相同IP的子域url放到一起

					shodan_url = 'https://api.shodan.io/shodan/host/{}?key={}'.format(sub_ip, shodan_api)
					yield scrapy.Request(url=shodan_url, headers=headers,
					                     meta={'url': url, 'sub_ip': sub_ip, 'subdomain_url': subdomain_url},
					                     callback=self.sub_shodan)

	def sub_shodan(self, response):
		url = response.meta['url']
		sub_ip = response.meta['sub_ip']
		subdomain_url = response.meta['subdomain_url']
		if 'No information available for that IP' in response.text:
			print('\033[1;31;40m[{}] 未查询到 {} 的shodan信息\033[0m'.format(time.strftime('%Y-%m-%d %H:%M:%S'), sub_ip))
		else:
			shodan_json = json.loads(response.text)
			shodan_ports = shodan_json['ports']
			shodan_os = shodan_json['os']
			shodan_country_name = shodan_json['country_name']
			shodan_isp = shodan_json['isp']
			try:
				shodan_vulns = shodan_json['vulns']
			except:
				shodan_vulns = ''

			print(
				'\033[1;32;40m[{}] {}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n\033[0m'.format(time.strftime('%Y-%m-%d %H:%M:%S'),
				                                                                   url, sub_ip,
				                                                                   subdomain_url,
				                                                                   shodan_country_name,
				                                                                   shodan_isp, shodan_os, shodan_ports,
				                                                                   shodan_vulns))
			item = PigatItem_shodan(
				url=url,
				subdomain_url=subdomain_url,
				sub_ip=sub_ip,
				shodan_ports=shodan_ports,
				shodan_os=shodan_os,
				shodan_vulns=shodan_vulns,
				shodan_country_name=shodan_country_name,
				shodan_isp=shodan_isp
			)
			yield item
