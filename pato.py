from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Firefox()
driver.get("http://gshow.globo.com/RPC/Estudio-C/interatividade/enquete/2017/7/22/qual-cidade-voce-quer-ver-no-descubra-o-parana-francisco-beltrao-ou-pato-branco-6898d3e0-6f01-11e7-918b-0242ac110003.html")
votar = driver.find_element_by_link_text('Pato Branco').click()
imprime = "Votou de novo! Total = "
contador = 0
while contador <= 1000:
	if driver.find_element_by_link_text('Pato Branco'):
		driver.find_element_by_link_text('Pato Branco').click()
		contador = contador +1
		print ("Votou de novo! Total = " + str(contador))
	time.sleep(1)
	driver.find_element_by_class_name('glb-poll-btn-close').click()
	time.sleep(1)
	driver.find_element_by_link_text('Vote de novo').click()