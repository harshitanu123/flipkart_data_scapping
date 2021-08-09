import streamlit as st
import pandas as pd
import requests as rq
from bs4 import BeautifulSoup
import os
st.title("WEB SCRAPPING PROJECT")
st.header("EXTRACTING DATASET FROM FLIPKART  ")

data_list=[]

def getpage(link):
    try:
        page=rq.get(link)
        st.success(f'data loaded from=>{link}')
        return BeautifulSoup(page.text,'lxml')
    except Exception as e:
        st.error(e)

def extract(data):
    target = data.find_all('div',{'class':'_1YokD2 _3Mn1Gg'})[1]
    products = target.find_all('div',{'class':'_1xHGtK _373qXS'})
    size = len(products)
    print('products found=>',size)
    if size > 0:
        for item in products:
            brand= item.find('div',{'class':'_2WkVRV'}).text
            name = item.find('a',{'class':'IRpwTa'}).text
            price= item.find('div',{'class':'_30jeq3'}).text[1:]
            try:
                real_price = item.find('div',{'class':'_3I9_wc'}).text[1:]
            except:
                real_price =price
            data_list.append({'name':name ,'brand':brand ,'price':price  ,'real_price':real_price}) 
        return True
    else:
        st.info('no product found') 
        return False                


def save(filepath):
    df=pd.DataFrame(data_list)
    df.to_csv(f'{filepath}.csv')
    print(f'saved file at{filepath}')

#exetution

query =st.text_input('Enter 1 word product')
save_file=st.text_input('name to file to save data')
pos = st.slider('select start page',min_value=1, max_value=10,)
if st.button('start'):
  while True:
      url =f'https://www.flipkart.com/search?q={query}&page={pos}'
      #print(f'extracting data from{url}...')
      soup = getpage(url)
      if soup:
        status = extract(soup)
        if not status:
            st.write('scraping bot finished')
            break
        else:
            pos+=1
        st.success(f'total data collectd =>{len(data_list)}')
      else:
          st.error('some error ,please look carefully')
          break
  if data_list:
    st.write(data_list)
    save(f'data/{save_file}')

if st.checkbox('view dataset'):
    files=os.listdir('data') 
    file= st.sidebar.selectbox('list of data files',files)
    df=pd.read_csv(f'data/{file}',)
    st.write(df)


