from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import streamlit as st
import pandas as pd

url = 'https://randomuser.me/api/'
headers = {
    'dataType': 'json'
}
session = Session()
session.headers.update(headers)
try:
    response = session.get(url)
    dataObj = json.loads(response.text)
    json_formatted_str = json.dumps(dataObj, indent=4)
    print(json_formatted_str)
    print(dataObj['results'][0]['name'])
except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)

st.write("Personal Profile")
nameData = []
nameData.append(
    {
        'First': dataObj['results'][0]['name']['first'],
        'Last': dataObj['results'][0]['name']['last']
    }
)
contactData = []
contactData.append(
    {
        'Email': dataObj['results'][0]['email'],
        'Phone': dataObj['results'][0]['phone'],
        'Cell' : dataObj['results'][0]['cell']
    }
)
# Picture at top
st.image(dataObj['results'][0]['picture']['large'])

# Make Data Frame
df = pd.DataFrame(nameData)
dfContact = pd.DataFrame(contactData)


# Create tabs
tabName, tabContact = st.tabs(["Name", "Contact"])

# Content for name tab
with tabName:
    st.markdown(df.to_html(index=False), unsafe_allow_html=True)

# Content for contact tab
with tabContact:
    st.markdown(dfContact.to_html(index=False), unsafe_allow_html=True)
