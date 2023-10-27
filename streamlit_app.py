#Put All the Import Commands Together, At the Top
import streamlit
import pandas
import requests 
import snowflake.connector
# to be used in control of flow changes 
from urllib.error import URLError

#Functions definitions
def get_fruityvice_data(this_fruit_choice):
 fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
 fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
 return fruityvice_normalized

def get_fruit_load_list():
 with my_cnx.cursor() as my_cur:
  my_cur.execute("SELECT * from fruit_load_list")
  return my_cur.fetchall()

def insert_row_snowflake(new_fruit):
 with my_cnx.cursor() as my_cur:
  my_cur.execute("insert into fruit_load_list values('"+new_fruit+"')")
  return "Thanks for adding " + new_fruit

streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

#import pandas
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
# let the customer to choose the fruits by name, by setting and index on Fruit column (fruit name)
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

#  Call the Fruityvice API from Our Streamlit App!
streamlit.header("Fruityvice Fruit Advice!")
try:
 #Add a Text Entry Box and Send the Input to Fruityvice as Part of the API Call
 fruit_choice = streamlit.text_input('What fruit would you like information about?')
 if not fruit_choice:
  streamlit.error("Please select a fruit to get information.")
 else:
  back_from_function = get_fruityvice_data(fruit_choice)
  streamlit.dataframe(back_from_function)
except URLError as e:
 streamlit.error()

streamlit.header("View our fruit list - Add your favorites!")
#import snowflake.connector
# Connect to Snowflake and Query Our Trial Account, Query Some Data, Format the results shown
# Add a button to load the fruit list
if streamlit.button('Get Fruit List'):
 my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
 my_data_rows = get_fruit_load_list()
 my_cnx.close()
 streamlit.dataframe(my_data_rows)

# Allow a user to add a fruit to the list : lab
add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a fruit to the list'):
 my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
 back_fom_function2 = insert_row_snowflake(add_my_fruit)
 my_cnx.close()
 streamlit.write(back_fom_function2)

streamlit.stop()





