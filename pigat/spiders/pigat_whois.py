import timeimport jsonimport scrapyfrom pigat.items import PigatItem_whoisclass pigat_whois(scrapy.Spider):	name = 'pigat_whois'	def start_requests(self):		headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0'}		url = self.url  # 待爬取 URL		# Whois 查询		whois_url = 'https://api.devopsclub.cn/api/whoisquery?domain={}&type=json'.format(url)		yield scrapy.Request(whois_url, headers=headers, meta={'url': url, 'handle_httpstatus_list': [400]},		                     callback=self.sub_whois)	def sub_whois(self, response):		url = response.meta['url']		print('\n\033[1;33m[{}] 正在被动收集 {} 的 Whois 信息……\033[0m'.format(time.strftime('%Y-%m-%d %H:%M:%S'), url))		if 'query fail' in response.text:			print('\033[1;31m[{}] 未查询到 {} 的 Whois 信息\n\033[0m'.format(time.strftime('%Y-%m-%d %H:%M:%S'), url))		else:			whois_json = json.loads(response.text)			whois_registrar = whois_json['data']['data']['registrar']  # 注册商			whois_registrarAbuseContactEmail = whois_json['data']['data']['registrarAbuseContactEmail']  # 注册邮箱			whois_registrarAbuseContactPhone = whois_json['data']['data']['registrarAbuseContactPhone']  # 注册电话			whois_registrarURL = whois_json['data']['data']['registrarURL']  # 注册网址			whois_registrarWHOISServer = whois_json['data']['data']['registrarWHOISServer']  # 注册商whois服务器			whois_nameServer = whois_json['data']['data']['nameServer']  # DNS 解析服务器			whois_creationDate = whois_json['data']['data']['creationDate']  # 注册日期			whois_registryExpiryDate = whois_json['data']['data']['registryExpiryDate']  # 到期日期			whois_updatedDate = whois_json['data']['data']['updatedDate']  # 更新日期			print('\033[1;32m'			      '[{}] 注册商：{}\n'			      '[{}] 注册邮箱：{}\n'			      '[{}] 注册电话：{}\n'			      '[{}] 注册网址：{}\n'			      '[{}] 注册商 Whois 服务器：{}\n'			      '[{}] DNS 解析服务器：{} \n'			      '[{}] 注册日期：{}\n'			      '[{}] 到期日期：{}\n'			      '[{}] 更新日期：{}'			      '\033[0m'.format(				time.strftime('%Y-%m-%d %H:%M:%S'), whois_registrar,				time.strftime('%Y-%m-%d %H:%M:%S'), whois_registrarAbuseContactEmail,				time.strftime('%Y-%m-%d %H:%M:%S'), whois_registrarAbuseContactPhone,				time.strftime('%Y-%m-%d %H:%M:%S'), whois_registrarURL,				time.strftime('%Y-%m-%d %H:%M:%S'), whois_registrarWHOISServer,				time.strftime('%Y-%m-%d %H:%M:%S'), whois_nameServer,				time.strftime('%Y-%m-%d %H:%M:%S'), whois_creationDate,				time.strftime('%Y-%m-%d %H:%M:%S'), whois_registryExpiryDate,				time.strftime('%Y-%m-%d %H:%M:%S'), whois_updatedDate			))			item = PigatItem_whois(				url=url,				whois_registrar=whois_registrar,				whois_registrarAbuseContactEmail=whois_registrarAbuseContactEmail,				whois_registrarAbuseContactPhone=whois_registrarAbuseContactPhone,				whois_registrarURL=whois_registrarURL,				whois_registrarWHOISServer=whois_registrarWHOISServer,				whois_nameServer=whois_nameServer,				whois_creationDate=whois_creationDate,				whois_registryExpiryDate=whois_registryExpiryDate,				whois_updatedDate=whois_updatedDate			)			yield item