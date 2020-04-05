# importing libraries 

import requests 
from bs4 import BeautifulSoup 
import os 
import numpy as np 
import matplotlib.pyplot as plt 

extract_contents = lambda row: [x.text.replace('\n', '') for x in row] 
URL = 'https://www.mohfw.gov.in/'
st = []
total = []
response = requests.get(URL).content 
soup = BeautifulSoup(response, 'html.parser') 
header = extract_contents(soup.tr.find_all('th')) 
stats = [] 
all_rows = soup.find_all('tr') 

for row in all_rows: 
	stat = extract_contents(row.find_all('td')) 
	if stat: 
		if len(stat) == 5: 
			stats.append(stat) 
		elif len(stat) == 6: 
			stats.append(stat) 

stats[-1][1] = "Total Cases"
stats.remove(stats[-1]) 

for row in stats:
	st.append(row[1])
	total.append(int(row[2]) + int(row[3]))

y_indexes = np.arange(len(st))

fig, ax = plt.subplots()
plt.style.use('seaborn')
ax.barh(st, total)
ax.set_title("COVID-19 INDIA")
ax.set_xlabel('COVID-19 Confirmed Cases')
ax.set_ylabel('COVID-19 Statwise status')
#ax.set_yticks(y_indexes, st)
for i, v in enumerate(total):
    ax.text(v + 3, i + .25, str(v))
plt.tight_layout()
plt.show()
