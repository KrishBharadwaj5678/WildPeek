import streamlit as st
import requests
import re

st.set_page_config(
    page_title="Wild Peek",
    page_icon="icon.png",
    menu_items={
        "About":"Explore Wild Peek, where you can easily access detailed information about animals from around the world. Input any animal name and uncover fascinating  characteristics, behavior, and habitat. Your ultimate source for animal knowledge!"
    }
)

st.write("<h2 style='color:#8cc730;font-size:34px;'>Your Quick Guide to Animal Information</h2>",unsafe_allow_html=True)

name=st.text_input("Enter Animal Name",placeholder="king cobra")

btn=st.button("Search")
if btn:
    api_url = 'https://api.api-ninjas.com/v1/animals?name={}'.format(name)
    response = requests.get(api_url, headers={'X-Api-Key': '2jWCY0dASiPZc7RLybXvXA==R9oC0XPKPWiGJ6k6'})
    if response.status_code == requests.codes.ok:
        data=response.json()
        if(len(data)>=1):
            for i in data:
                animalName=i['name']
                # Extracting Locations
                locations=''
                for j in i['locations']:
                    locations+=j+', '

                st.write(f"<h2 style='color:#FFDE4D;font-size:34px;'>{animalName}</h2>",unsafe_allow_html=True)

                def showFeatures(label,data):
                    st.write(f"<li style='font-size:25.3px;'>{label}: {data}</li>",unsafe_allow_html=True)

                showFeatures('Locations',locations.rstrip(", "))

                # Extracting Characteristics
                characteristics_keys=i['characteristics'].keys()
                for key in characteristics_keys:

                    modified_key=' '.join(i.title() for i in key.split("_"))

                    if(key=='color'):
                        colors=', '.join(re.findall(r'[A-Z][a-z]*',i['characteristics'][key]))
                        showFeatures(modified_key,colors)
                    elif(key=='other_name(s)'):
                        showFeatures('Other Names',i['characteristics'][key])
                    else:
                        showFeatures(modified_key,i['characteristics'][key])
                
                # Extracting Taxonomy
                taxonomy_keys=i['taxonomy'].keys()
                for key in taxonomy_keys:
                        showFeatures(key.title(),i['taxonomy'][key])
        else:
            st.warning("Oops! No Data for This Animal")
