import streamlit as st
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
import pandas as pd

cred = credentials.Certificate("asukey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

membersCollection = db.collection(u'members').stream()
membersDF = pd.DataFrame.from_dict(membersCollection)

st.title('AfterShock East Greed Data Hub')

st.text_input('SearchText',value='Search Greed')
st.table(membersDF)

