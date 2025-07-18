# Import python packages
import streamlit as st
import pandas as pd
#from snowflake.snowpark.context import get_active_session
import requests
cns=st.connection("snowflake")
session=cns.session()
from snowflake.snowpark.functions import col
# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie! :cup_with_straw: ")
st.write(
  "Choose the fruits you want in your custom Smoothie!"
)

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your smoothie will be:", name_on_order)

#option = st.selectbox(
#    "What is your favorite fruit?",
#    ("Banana", "Strawberries", "Peaches"))

#st.write("Your favorite fruit is :", option)

#session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#Convert the Snowpark dataframe to pandas dataframe so that we can use LOC function
#st.dataframe(data=my_dataframe, use_container_width=True)
pd_df=my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()
ingredients_list = st.multiselect('Choose upto 5 ingredients:',my_dataframe,default=None,max_selections=5)
#if ingredients_list:
#    st.write(ingredients_list)
#    st.text(ingredients_list)
if ingredients_list:
    ingredients_string=''
for fruit_chosen in ingredients_list:
    ingredients_string+=fruit_chosen+' '
    search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
    #st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
    st.subheader(fruit_chosen + ' Nutritional Information')
    smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on)
    sf_df=st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)
#st.write(ingredients_string)
time_to_insert=st.button('Submit Order')


if time_to_insert:
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    #st.write(my_insert_stmt)
    #st.stop()
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered!', icon="✅")
    
#st.text(smoothiefroot_response.json())
    
