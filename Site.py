import streamlit as st
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials, storage
import pandas as pd
import json
import datetime
import plotly.express as px


key_dict = json.loads(st.secrets["textkey"])

Data = pd.read_csv('AS East Greed.csv')
date = '2022-7-30'

cred = credentials.Certificate(key_dict)
try:
    ASUapp = firebase_admin.initialize_app(cred, {'storageBucket':'asudata.appspot.com'})
except:
    pass

bucket = storage.bucket()
db = firestore.client()


def getImage(image):
    imageblob = bucket.blob(image)
    imageurl = imageblob.generate_signed_url(datetime.timedelta(seconds=300), method="GET")
    return imageurl

def DownloadDf(Df):
    return Df.to_csv().encode('utf-8')

membersCollection = list(db.collection(u'members').stream())


members_dict = list(map(lambda x: x.to_dict(), membersCollection))
membersDF = pd.DataFrame(members_dict)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.title('AfterShock East Greed Data Hub')

col2.metric("Prime", f'{Data.loc[Data["Clan"] == "AftershockUnitedPrime", "Name"].count()} members', "Max 300", delta_color='off')
col3.metric("Gold", f'{Data.loc[Data["Clan"] == "AftershockUnitedGold", "Name"].nunique()} members', "Max 300", delta_color='off')
col4.metric("Silver", f'{Data.loc[Data["Clan"] == "AftershockUnitedSilver", "Name"].nunique()} members', "Max 300", delta_color='off')

ClanFilter ={
    'All':'All',
    'Prime':'AftershockUnitedPrime',
    'Gold':'AftershockUnitedGold',
    'Silver':'AftershockUnitedSilver'}



tab1, tab2, tab3 = st.tabs(["Dashboard", "Member Search", 'Raw'])


with tab1:
    Clans = st.selectbox('Clan Filter',options=ClanFilter, key='ClanSelect')
    if Clans == 'All':
        DashDf = Data
    else:
        DashDf = Data.loc[Data['Clan']==ClanFilter.get(Clans)]

    fig = px.pie(DashDf,values=DashDf.value_counts('Class').values, names=DashDf.value_counts('Class').index)
    fig.update_traces(title='Clan by Class',showlegend=False,textinfo='label+value')

    st.plotly_chart(fig,use_container_width=True)


with tab2:
    search = st.text_input('Press "Enter" to Search Name ',value='KeLP',)
    st.table(Data[Data["Name"].str.contains(search,case=False)])
    #st.table(Data.loc[Data['Name']== search],)


with tab3:
    col1, col2 = st.columns(2,gap="small")
    with col1:
        st.download_button('Download Raw Data', DownloadDf(Data), 'ASURaw.csv')
    with col2:
        st.write(f'Last Updated: {date}')
    st.dataframe(Data)



