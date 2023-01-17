import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pandas import ExcelWriter
from tqdm.auto import tqdm
from webdriver_manager.chrome import ChromeDriverManager

excel_file = 'upu6.csv'
students = pd.read_csv(excel_file, dtype={'No. KP': object})

students = students[students['No. KP'].notna()]

options = Options()
options.headless = True
browser = webdriver.Chrome(ChromeDriverManager().install(), options=options) # Your webdriver path
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

                for node in result.find_all(text=lambda t: t and any(x in t for x in ['TIDAK BERJAYA', 'TAHNIAH', 'HARAP MAAF. TIADA REKOD PERMOHONAN'])):
                    students.at[row['No. KP'], ['UPU']] = node
                break
            except requests.exceptions.RequestException:
                print('Internet problem, cuba lagi lepas 10 second')
                time.sleep(10)  # wait 5 mins before retry

students = students[students['UPU'].notna()]
students = students.drop(columns="No. KP")
students.index.name = 'No. KP'
students.index = students.index.map(str)
students.to_csv('klang_upu.csv')
