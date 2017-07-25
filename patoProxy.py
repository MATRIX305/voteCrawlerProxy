from selenium import webdriver
import urllib2, socket
import time

socket.setdefaulttimeout(60)

ProxyHost = []
URL = "http://gshow.globo.com/RPC/Estudio-C/interatividade/enquete/2017/7/22/qual-cidade-voce-quer-ver-no-descubra-o-parana-francisco-beltrao-ou-pato-branco-6898d3e0-6f01-11e7-918b-0242ac110003.html"

def ChangeProxy(ipproxy):
	ipproxy = ipproxy.split(":")
	profile = webdriver.FirefoxProfile()
	profile.set_preference("network.proxy.type", 1)
	profile.set_preference("network.proxy.http", ipproxy[0] )
	profile.set_preference("network.proxy.http_port", int(ipproxy[1]))
	profile.update_preferences()
	return webdriver.Firefox(firefox_profile=profile)

def FixProxy():
	profile = webdriver.FirefoxProfile()
	profile.set_preference("network.proxy.type", 0)
	return webdriver.Firefox(firefox_profile=profile)

def is_bad_proxy(pip):
	try:        
		proxy_handler = urllib2.ProxyHandler({'http': pip})        
		opener = urllib2.build_opener(proxy_handler)
		opener.addheaders = [('User-agent', 'Mozilla/5.0')]
		urllib2.install_opener(opener)        
		req=urllib2.Request('http://www.google.com')
		sock=urllib2.urlopen(req)
	except urllib2.HTTPError, e:        
		print 'Error code: ', e.code
		return e.code
	except Exception, detail:
		print "ERROR:", detail
		return 1
	return 0

# Pega mais proxy automaticamente!
def pegaProxyList():
	global ProxyHost
	print("Vamos procurar alguns proxys...")
	driver = webdriver.Firefox()
	driver.get("https://free-proxy-list.net/")
	data = []
	ipList = []
	for tr in driver.find_elements_by_xpath('//table[@id="proxylisttable"]//tr'):
			tds = tr.find_elements_by_tag_name('td')
			if tds:
				data.append([td.text for td in tds])
	for row in data:
		ip = (row[0] + ":" + row[1])
		ProxyHost.append(ip)
	driver.quit()
	print(str(len(ProxyHost)) + " Novos proxys adicionados!")

def vaiRobo():
	global ProxyHost
	for host in ProxyHost:
		print("Testando seu proxy...")
		if is_bad_proxy(host):
			print "Bad Proxy", host
			ProxyHost.remove(host)
		else:
			print("Proxy: "+ host + " parece funcionar, vamos tentar!")
			driver = ChangeProxy(host)
			try: 
				driver.get(URL)
				contador = 0
				while contador <= 15:
					# Vota
					try:
						driver.find_element_by_link_text('Pato Branco').click()
					except Exception as e:
						print(e)
						driver.quit()
					else:
						pass
					finally:
						time.sleep(3)
					# Vota no Pato
					try:
						driver.find_element_by_class_name('glb-poll-btn-close').click()		
						contador += 1
						print (str(host)+" Total = " + str(contador))
					except Exception as e:
						print(e)
						driver.quit()
					else:
						pass
					finally:
						driver.find_element_by_link_text('Vote de novo').click()
						time.sleep(2)
						
				ProxyHost.remove(host)
				driver.quit()
			except Exception as e:
				print("Caiu na exception")
				print(e)
				driver.quit()
				ProxyHost.remove(host)
			else:
				print("Nao consegui acessar a URL")
# Executa
repeticao = 0
while repeticao < 10:
	if len(ProxyHost) > 1:
		vaiRobo()
	else:
		pegaProxyList()
		vaiRobo()
	repeticao + 1