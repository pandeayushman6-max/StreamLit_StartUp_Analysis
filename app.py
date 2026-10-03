from narwhals import Date
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(layout='wide',page_title='StartUp Analysis')


df = pd.read_csv(r'D:\AI ML\StreamLit\startup_funding.csv')
print(df.shape)


df.drop(columns=['Remarks'],inplace=True)
df.set_index('Sr No',inplace=True,drop=True)
df.rename(columns={
     'Date dd/mm/yyyy':'Date',
     'Startup Name':'Startup',
     'Industry Vertical':'Vertical',
     'SubVertical':'Subvertical',
     'City  Location':'City',
     'Investors Name':'Investors',
     'InvestmentnType':'Round',
     'Amount in USD':'Rupees'
},inplace=True)

##########DATA CLEANING##############

df.dropna(subset=['Date','Startup','Vertical','City','Investors','Round','Rupees'],inplace=True,how='any')


df['Rupees'] = df['Rupees'].fillna(0) 
df['Rupees'] = df['Rupees'].str.replace(',','')
df['Rupees'] = df['Rupees'].str.replace('undisclosed','0')
df['Rupees'] = df['Rupees'].str.replace('unknown','0')
df['Rupees'] = df['Rupees'].str.replace('Undisclosed','0')

df = df[df['Rupees'].str.isdigit()]

df['Rupees'] = df['Rupees'].astype(float)

df['Rupees'] = (df['Rupees'] *82.5)/10000000


df['Date'] = df['Date'].str.replace('05/072018','05/07/2018')
df['Date'] = pd.to_datetime(df['Date'],format=r'%d/%m/%Y',errors='coerce')

df.to_csv(r'startup_funding_cleaned.csv',index=False)

#############DATA CLEANING DONE ##########

cleaned_df = pd.read_csv(r'startup_funding_cleaned.csv',parse_dates=['Date'])

temp_df = st.file_uploader('Upload a file',type=['csv','xlsx','txt'])
if temp_df is not None:
    st.dataframe(cleaned_df)

print(cleaned_df.columns)
print(cleaned_df.index)    
print(cleaned_df.info())
print(cleaned_df.describe())


####FUNCTIONS############

@st.fragment
def render_general_investments(option,cleaned_df):
    st.header('Generally Invests In')

    #Multiselect
    multipleOptions = st.multiselect(
    label='General Selection',
    options=['ByCount','ByRupeesSum','ByCity','YOY Investment Graph'],            
    placeholder='Select mutiple or single'

    )

    if 'ByCount' in multipleOptions:

        st.subheader('Generally Invests In By Count')
        General_Invests_bycount=cleaned_df[cleaned_df['Investors'].str.contains(option)].groupby('Vertical')['Rupees'].count().reset_index().sort_values(by=['Rupees'],ascending=False)
        General_Invests_List = General_Invests_bycount.head(5).index.tolist()
        st.bar_chart(General_Invests_bycount,x='Vertical',y='Rupees',y_label='No.of Investments',x_label='Industry')
        
    if 'ByRupeesSum' in multipleOptions:

        st.subheader('Generally Invests In By Rupees Sum')
        General_Invests_byRupeesSum = cleaned_df[cleaned_df['Investors'].str.contains(option)].groupby('Vertical')['Rupees'].sum().reset_index().sort_values(by=['Rupees'],ascending=False)
        fig1,ax1 = plt.subplots()
        ax1.bar(General_Invests_byRupeesSum['Vertical'],height=General_Invests_byRupeesSum['Rupees'])
        st.pyplot(fig1)

    if 'ByCity' in multipleOptions:

        st.subheader('Generally Invests in By City')
        General_Invests_byCity = cleaned_df[cleaned_df['Investors'].str.contains(option)].groupby('City')['Rupees'].count().reset_index().sort_values(by='Rupees',ascending=False)
        figplot = px.pie(General_Invests_byCity,names=General_Invests_byCity['City'],values=General_Invests_byCity['Rupees'],title='General Investments by City')
        st.plotly_chart(figplot)

    if 'YOY Investment Graph' in multipleOptions:

        st.subheader('Yearly Investments Made')
        Investors_df = cleaned_df[cleaned_df['Investors'].str.contains(option)]    
        Investors_df['Year']=Investors_df['Date'].dt.year
        YOY_df = Investors_df.groupby('Year')['Rupees'].sum().reset_index().sort_values(by='Year',ascending=True)
        figplot = px.line(x=YOY_df['Year'],y=YOY_df['Rupees'])
        st.plotly_chart(figplot)
        #st.line_chart(YOY_df,x=['Year'],y=['Rupees'],x_label='Year',y_label='Rupees')

def load_investor_details(option):

    #Investor Name
    st.header('Investor Name')
    st.subheader(option)

    #Recent Investments
    st.header('Recent Investments')
    Recent_Investments=cleaned_df[cleaned_df['Investors'].str.contains(option)].sort_values(by='Date',ascending=False)
    st.dataframe(Recent_Investments.head(5))


    col1,col2 = st.columns(2)

    with col1:
        #Biggest Investments
        st.header('Biggest Investments')
        Biggest_Investments=cleaned_df[cleaned_df['Investors'].str.contains(option)].groupby('Startup').agg({'Rupees':'sum'}).reset_index().sort_values(by='Rupees',ascending=False,ignore_index=True)

        plot_figure = px.pie(Biggest_Investments,values=Biggest_Investments['Rupees'],names=Biggest_Investments['Startup'],title='Biggest Investments')
        st.plotly_chart(plot_figure)
    
    with col2:
        #Generally Invests In
        render_general_investments(option,cleaned_df)


    #Similiar Investors
    Investors_df = cleaned_df[cleaned_df['Investors'].str.contains(option)]        
    Investors_set = set(Investors_df['Investors_Name_list'].sum())
    l = [i for i in Investors_set if (i != option)]
    st.header('Similiar Investors')
    st.write(l)

@st.fragment
def load_mom_graphs(cleaned_df):

    selected_option = st.selectbox(
            label='Select Type',
            options=['Total','Count'],
            placeholder='Select only one',
            index=None
        )
    
    if selected_option=='Total':
        mom_df=cleaned_df.groupby(['Year','Month'])['Rupees'].sum().reset_index()
        mom_df['MOM'] = mom_df['Month']/12 + mom_df['Year']
        st.dataframe(mom_df)
        st.line_chart(
            data=mom_df,
            x='MOM',
            y='Rupees',
            x_label='month/year',
            y_label='Crores'
            )
    elif selected_option=='Count':
    
        mom_df=cleaned_df.groupby(['Year','Month'])['Rupees'].count().reset_index()
        mom_df['MOM'] = mom_df['Month']/12 + mom_df['Year']
        mom_df.rename(columns={'Rupees':'No.of Investments'},inplace=True)
        
        st.dataframe(mom_df)
        st.line_chart(
            data=mom_df,
            x='MOM',
            y='No.of Investments',
            x_label='month/year',
            y_label='Crores'
            )
        

def load_overall_analysis():

    st.title('Overall Analysis')


    col1,col2,col3,col4 = st.columns(4)

    with col1:
        #Total invested amount
        total = round(cleaned_df['Rupees'].sum())
        st.metric(
            label='Total Funding',
            value= str(total) + 'Cr'
            )
    with col2:
        Max_Rupees_Startup = cleaned_df.groupby('Startup')['Rupees'].max().reset_index().sort_values(by='Rupees',ascending=False)
        st.metric(
            label='Max Funding Received to a Startup',
            value = str(Max_Rupees_Startup.loc[0,'Rupees']) + 'Cr'
            )
    with col3:
        Avg_Rupees_Startup = cleaned_df.groupby('Startup')['Rupees'].sum().reset_index().sort_values(by='Rupees',ascending=False)
        st.metric(
            label='Average Funding Received to a Startup',
            value = str(round(Avg_Rupees_Startup['Rupees'].mean(),ndigits=3)) + 'Cr'
            )    
    with col4:
        st.metric(
            label='Total Funded Startups',
            value= str(len(cleaned_df['Startup'].unique()))
        ) 

    #MOM line chart
    
    st.header('Month by Month Draft')
    cleaned_df['Year'] = cleaned_df['Date'].dt.year   
    cleaned_df['Month'] = cleaned_df['Date'].dt.month

    load_mom_graphs(cleaned_df)



##########FUNTIONS END#########




#####DATA ANALYSIS######
st.sidebar.title('Startup Funding Analysis')
option=st.sidebar.selectbox('Select One',['Overall Analysis','StartUp','Investor'],placeholder='Select a column for analysis',accept_new_options=False,index=None)

if option=='Overall Analysis':
   
    btn0 = st.sidebar.button('Show Overall Analysis')

    if btn0:
        load_overall_analysis()
        
    
elif option=='StartUp':   
    st.title('StartUp Analysis')
    option2 = st.sidebar.selectbox('Select a StartUp',sorted(cleaned_df['Startup'].unique().tolist()),placeholder='Select a StartUp for analysis',accept_new_options=False)

    btn1 = st.sidebar.button('Show StartUp Analysis')
    if btn1:
        st.subheader('StartUp Analysis')
        st.dataframe(cleaned_df[cleaned_df['Startup']==option2])


elif option=='Investor':
    st.title('Investor Analysis')   

    def alag(row):
            row['Investors_Name_list'] = tuple(row['Investors'].split(','))
            return row

      
    cleaned_df=cleaned_df.apply(axis=1,func=alag)

    Inverstor_Name_Set = set(cleaned_df['Investors_Name_list'].sum())
    
    option3 = st.sidebar.selectbox('Select a Investor',sorted(Inverstor_Name_Set),placeholder='Select a Investor for analysis',accept_new_options=False) 

    btn2 = st.sidebar.button('Show Investor Analysis')

    if btn2  and option3:
        
        load_investor_details(option3)        

        st.subheader('Total Investor Analysis')
        st.dataframe(cleaned_df[cleaned_df['Investors'].str.contains(option3)])

    