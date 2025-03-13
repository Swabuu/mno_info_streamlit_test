import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

MCCMNC_FILE = '1741865932mccmnc.xlsx'
MNO_INFO_FILE = '1741863539_List_of_mobile_network_operators.csv'

# Config
st.set_page_config(
	page_title = 'MCCMNC',
	page_icon =  ':calling:',
	layout = 'wide'
)
# Remove whitespace from the top of the page and sidebar
st.markdown("""
        <style>
               .css-18e3th9 {
                    padding-top: 0rem;
                    padding-bottom: 10rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
               .css-1d391kg {
                    padding-top: 3.5rem;
                    padding-right: 1rem;
                    padding-bottom: 3.5rem;
                    padding-left: 1rem;
                }
        </style>
        """, unsafe_allow_html=True)


@st.cache
def read_excel(file):
	df = pd.read_excel(
		io = '1669897178mccmnc.xlsx',
		engine = 'openpyxl',
		sheet_name = 'Sheet1'
		)
	return df

def not_number(p):
	if p[0].isnumeric() and not '%' in p:
		return p.split()[0]
	else:
		return 0

def extract_subs_pattern():
	r = '[0-9]+\.[0-9]+'

	return r 

def extract_quarter_pattern():
	r = 'Q[0-9]\s[0-9]{2,4}'

	return r

@st.cache
def read_csv():
	col_names = ['Country',	'Rank',	'Operator',	'Subscribers']
	df = pd.read_csv(MNO_INFO_FILE, dtype={'Country': str,'Rank': str,'Operator': str,'Subscribers': str,'Owner': str}, delimiter=';', skiprows=0, usecols=col_names, low_memory=False)
	df['Subs'] = df['Subscribers'].astype({'Subscribers':'str'})
	df['Subs'] = df['Subs'].apply(lambda x: not_number(x))
	df['Subs'] = df['Subs'].replace('nan', '0')

	df['Rank'] = df['Rank'].astype({'Rank':'str'})
	df['Rank'] = df['Rank'].replace('nan', '0')
	df['Rank'] = df['Rank'].apply(lambda x: x.split('.')[0])
	df['Rank'] = df['Rank'].astype({'Rank':'str'}) 
 
	
	df['Subs'] = df['Subs'].replace('nan', '0')
	
	df['Subs'] = df['Subs'].replace('%', '')
	df['Subs'] = df['Subs'].astype({'Subs':'float'})

	return df



df = read_excel(MCCMNC_FILE)
mno_info_df = read_csv()

df = df[['Country', 'MCC', 'MNC', 'Operator', 'Status', 'References and notes']]

selected_countries = st.sidebar.selectbox(
	"Select country",
	options = df['Country'].unique(),
	#default = df['Country'].unique()[1],
	index = 3,
	key = 1
)

selected_country = selected_countries

URLS = [
'https://en.wikipedia.org/wiki/Mobile_Network_Codes_in_ITU_region_2xx_(Europe)', 
'https://en.wikipedia.org/wiki/Mobile_Network_Codes_in_ITU_region_3xx_(North_America)', 
'https://en.wikipedia.org/wiki/Mobile_Network_Codes_in_ITU_region_4xx_(Asia)', 
'https://en.wikipedia.org/wiki/Mobile_Network_Codes_in_ITU_region_5xx_(Oceania)', 
'https://en.wikipedia.org/wiki/Mobile_Network_Codes_in_ITU_region_6xx_(Africa)', 
'https://en.wikipedia.org/wiki/Mobile_Network_Codes_in_ITU_region_7xx_(South_America)'
]

df_selection = df.query(
	'Country == @selected_countries'
)
st.title('Mobile operator information')
# Add social media tags and links to the web page.
"""
[![Follow](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/anton-ivarsson)
[![Follow](https://img.shields.io/badge/Twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)](#)
"""

mno_info = mno_info_df.query(
	'Country == @selected_countries'
)

grouped_mno = mno_info.groupby(['Operator']).aggregate({'Subs':'sum'}).reset_index()

chart_data = grouped_mno

import plotly.express as px

fig = px.bar(chart_data, x='Operator', y=['Subs'])

country_info_df = pd.read_excel('Operator_Info.xlsx')
country_info_df = country_info_df.drop_duplicates(subset='Info')
country_info = country_info_df.query(
	"Country == @selected_countries"
)

# Sidebar Configuration
st.sidebar.write(country_info['Info'].iloc[0])
st.sidebar.image('CAT2.png', width=200)

st.sidebar.markdown('---')
st.sidebar.write('Developed by Anton Ivarsson')
st.sidebar.write('Contact @ mccmnc.se/LinkedIn')



st.subheader(selected_country)
st.write("List of MCCs, MNCs, the status and technology used for the countries selected in the left navbar.")
st.dataframe(df_selection, use_container_width=True)


st.write("If subscriber count is available, you'll find the data + graph here below.")
st.dataframe(mno_info, use_container_width=True)
st.plotly_chart(fig, use_container_width=True)
