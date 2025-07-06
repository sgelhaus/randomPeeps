from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import streamlit as st
import pandas as pd
from pandas import json_normalize

url = 'https://randomuser.me/api/'
headers = {
    'dataType': 'json'
}
session = Session()
session.headers.update(headers)
responseList = []
try:
    response = session.get(url, params={'results': 5})
    dataObj = json.loads(response.text)
    json_formatted_str = json.dumps(dataObj, indent=4)
    responseList.append(dataObj)
    print(json_formatted_str)
    print(dataObj['results'][0]['name'])
except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)


prefix = dataObj['results']

df = json_normalize(prefix)

# Create a column to identify users by name
df['fullName'] = df['name.first'] + ' ' + df['name.last']

# Dropdown list
selected_name = st.selectbox("Select a user to view details:", df['fullName'])

# Find the row for the selected user
selected_user = df[df['fullName'] == selected_name].iloc[0]


firstEntry = lastEntry = None


# Convert list to Data Frame
df = pd.DataFrame(responseList)

startData = []
for num in range(5): 
    firstEntry = prefix[num]['name']['first']
    lastEntry = prefix[num]['name']['last']
    listUser = {
        'First': firstEntry,
        'Last': lastEntry
    }
    startData.append(listUser)


st.write("Personal Profile")
nameData = []
nameData.append(
    {
        'First': firstEntry,
        'Last': lastEntry
    }
)
contactData = []
contactData.append(
    {
        'Email': prefix[0]['email'],
        'Phone': prefix[0]['phone'],
        'Cell' : prefix[0]['cell']
    }
)

# Profile picture 
st.image(prefix[0]['picture']['large'])

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
