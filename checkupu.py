import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pandas import ExcelWriter
from tqdm.auto import tqdm


excel_file = 'upu6.csv'
students = pd.read_csv(excel_file, dtype={'No. KP': object})
# print (students.head())
# writer = pd.ExcelWriter('outputUpu.xlsx')
students = students[students['No. KP'].notna()]

options = Options()
	# options.add_argument("user-data-dir=C:\\Users\\Administrator\\AppData\\Local\\Google\\Chrome\\User Data\\")
options.headless = True
browser = webdriver.Chrome(executable_path=r'C:\chromedriver.exe', options=options) # Your webdriver path
total_rows = len(students.index)

with tqdm(total=int(total_rows)) as progress_bar:
	for index,row in students.iterrows():
		progress_bar.update(1)
		while True:
			try:
				nokp = (row["No. KP"])

				
				browser.get("https://jpt.unimas.my/semakKeputusanSPM.jsp")
				ic = browser.find_element_by_id('vNOKP')
				ic.send_keys(nokp)


				browser.find_element_by_id('bMASUK').click()

				result = BeautifulSoup(browser.page_source, "html.parser")
				
				# students.set_index('No. KP')
				for node in result.find_all(text=lambda t: t and any(x in t for x in ['TIDAK BERJAYA', 'TAHNIAH', 'HARAP MAAF. TIADA REKOD PERMOHONAN'])):
					students.at[row['No. KP'], ['UPU']] = node
					# print(row['No. KP'] +" "+node)
				break
			except requests.exceptions.RequestException:
				print('Internet problem, cuba lagi lepas 10 second')
				time.sleep(10)  # wait 5 mins before retry

		

students = students[students['UPU'].notna()]
# students.drop(['No. KP'], axis = 1)
students = students.drop(columns="No. KP")
# students.columns = ['No. KP']
students.index.name = 'No. KP'
students.index = students.index.map(str)

students.to_csv('klang_upu.csv')



	






# nokp = '030127100672'
# 030818100524
# result
# 1. HARAP MAAF. TIADA REKOD PERMOHONAN
# 2. TAHNIAH
# 3. TIDAK BERJAYA


# response = requests.post(url = 'https://jpt.unimas.my/Authenticate', data=post_params)
# soup = BeautifulSoup(response.text, 'html.parser')
# print (soup.prettify())

# options = Options()
# # options.add_argument("user-data-dir=C:\\Users\\Administrator\\AppData\\Local\\Google\\Chrome\\User Data\\")
# options.headless = False
# browser = webdriver.Chrome(executable_path=r'C:\chromedriver.exe', options=options) # Your webdriver path
# browser.get("https://jpt.unimas.my/semakKeputusanSPM.jsp")
# ic = browser.find_element_by_id('vNOKP')
# ic.send_keys("030127100672")

# browser.find_element_by_id('bMASUK').click()

# result = BeautifulSoup(browser.page_source, "html.parser")

# for node in result.find_all(text=lambda t: t and any(x in t for x in ['TIDAK BERJAYA', 'TAHNIAH', 'HARAP MAAF. TIADA REKOD PERMOHONAN'])):
#     print(node)
