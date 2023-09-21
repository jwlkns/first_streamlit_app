import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

def get_fruityvice_data(fruit: str):
  # Send request
  response = requests.get(f"https://fruityvice.com/api/fruit/{fruit}")
  # Normalize and return api response
  return pandas.json_normalize(response.json())  

def get_fruit_load_list():
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST")
    return my_cur.fetchall()

def insert_row_snowflake(fruit: str):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])

  with my_cnx.cursor() as my_cur:
    my_cur.execute(f"INSERT INTO FRUIT_LOAD_LIST VALUES ('{fruit}')")
  streamlit.text('Thanks for adding ', add_fruit)

streamlit.title("My Parents New Healthy Diner")

streamlit.header("Breakfast Menu")
streamlit.text("🥣 Omega 3 & Blueberry Oatmeal")
streamlit.text("🥗 Kale, Spinach & Rocket Smoothie")
streamlit.text("🐔 Hard-Boiled Free-Range Egg")
streamlit.text("🥑🍞 Avocado Toast")

streamlit.header("🍌🥭 Build Your Own Fruit Smoothie 🥝🍇")
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index("Fruit")

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ["Avocado", "Strawberries"])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table
streamlit.dataframe(fruits_to_show)

streamlit.header("Fruityvice Fruit Advice!")

try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    # Dsiplay api response as table
    streamlit.dataframe(get_fruityvice_data(fruit_choice))
    
except URLError as e:
  streamlit.error()

streamlit.header("The fruit load list contains:")

if streamlit.button("Get Fruit Load List"):
  streamlit.dataframe(get_fruit_load_list())

add_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button("Add a fruit to the list"):
  insert_row_snowflake(add_fruit)
