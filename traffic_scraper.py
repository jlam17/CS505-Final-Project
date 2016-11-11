import requests 
from bs4 import BeautifulSoup
import selenium
import json
import time
import os
import sys

url = 'https://www4.honolulu.gov/hpdtraffic/MainPrograms/frmMain.asp?sSearch=All+Incidents&sSort=I_tTimeCreate'
counter = 0
last_seen = ''

while(True):
	try:
	    response = requests.get(url)
	    if response.status_code == 200:
	        soup = BeautifulSoup(response.text, 'html.parser')
	        data = soup.find_all('tr', {'align':'left'})
	        data = data[1:]

	        keys = ['date','time','type','address','location','area']
	        top = list(filter(None,data[0].text.splitlines()))[1]# latest incident data
	        df_data = [] 
	        
	        print('Last seen incident: ' + last_seen)
	        print('Latest incident: ' + top)
	        for incident in data:
	            
	            values = list(filter(None,incident.text.splitlines()))
	            dict_values = dict(zip(keys,values))
	            if dict_values['time'] == last_seen:
	                break
	            else:
	                df_data.append(dict_values)
	        
	        last_seen = top
	        print('Scrapped {} datapoints'.format(len(df_data)))
	        with open('data_' + str(counter) + '.txt', 'w+') as f:
	            f.write(json.dumps(df_data))

	        counter += 1
	        time.sleep(3600)
	except KeyboardInterrupt:
		print('Exiting...')
		try:
			sys.exit(0)
		except SystemExit:
			os._exit(0)
	except:
		print('Error')
		pass