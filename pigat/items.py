# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


# whois
class PigatItem_whois(scrapy.Item):
	url = scrapy.Field()
	whois_registrar = scrapy.Field()
	whois_registrarAbuseContactEmail = scrapy.Field()
	whois_registrarAbuseContactPhone = scrapy.Field()
	whois_registrarURL = scrapy.Field()
	whois_registrarWHOISServer = scrapy.Field()
	whois_nameServer = scrapy.Field()
	whois_creationDate = scrapy.Field()
	whois_registryExpiryDate = scrapy.Field()
	whois_updatedDate = scrapy.Field()
	pass


# 备案
class PigatItem_beian(scrapy.Item):
	url = scrapy.Field()
	beian_name = scrapy.Field()
	beian_type = scrapy.Field()
	beian_cpy = scrapy.Field()
	beian_url = scrapy.Field()
	beian_license = scrapy.Field()
	beian_time = scrapy.Field()
	pass


# 子域名
class PigatItem_subdomain(scrapy.Item):
	url = scrapy.Field()
	subdomain_url = scrapy.Field()
	pass


# ip
class PigatItem_ip(scrapy.Item):
	url = scrapy.Field()
	subdomain_url = scrapy.Field()
	sub_ip = scrapy.Field()
	pass


# cms
class PigatItem_cms(scrapy.Item):
	url = scrapy.Field()
	subdomain_url = scrapy.Field()
	cms_title = scrapy.Field()
	cms_CMS = scrapy.Field()
	cms_Font_Scripts = scrapy.Field()
	cms_JavaScript_Frameworks = scrapy.Field()
	cms_JavaScript_Libraries = scrapy.Field()
	cms_Miscellaneous = scrapy.Field()
	cms_Operating_Systems = scrapy.Field()
	cms_Photo_Galleries = scrapy.Field()
	cms_Programming_Languages = scrapy.Field()
	cms_Web_Frameworks = scrapy.Field()
	cms_Web_Servers = scrapy.Field()
	cms_Widgets = scrapy.Field()
	cms_error = scrapy.Field()
	cms_Waf = scrapy.Field()
	cms_CDN = scrapy.Field()
	cms_Marketing_Automation = scrapy.Field()
	pass


# shodan
class PigatItem_shodan(scrapy.Item):
	url = scrapy.Field()
	subdomain_url = scrapy.Field()
	sub_ip = scrapy.Field()
	shodan_ports = scrapy.Field()
	shodan_os = scrapy.Field()
	shodan_vulns = scrapy.Field()
	shodan_country_name = scrapy.Field()
	shodan_isp = scrapy.Field()
	pass


# cve
class PigatItem_cve(scrapy.Item):
	url = scrapy.Field()
	cve_number = scrapy.Field()
	cve_level = scrapy.Field()
	cve_title = scrapy.Field()
	sub_ip = scrapy.Field()
	subdomain_url = scrapy.Field()
	cve_url = scrapy.Field()
	pass
