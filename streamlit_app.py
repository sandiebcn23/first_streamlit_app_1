import snowflake.connector
import streamlit
import pandas
import requests
from urllib.error import URLError

streamlit.title ('My parents new healthy diner');

streamlit.header('Breakfast Favourites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
streamlit.dataframe(my_fruit_list)
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Strawberries','Banana'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show);

try:
fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
  if not fruit_choice:
    streamlit.error('Please select a fruit to get info');
  else:
  streamlit.write('The user entered ', fruit_choice);
  streamlit.header("Fruityvice Fruit Advice!");
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice);
  streamlit.text(fruityvice_response);
  # write your own comment - Normzlize response?
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json());
  # write your own comment - write response to dataframe?
  streamlit.dataframe(fruityvice_normalized);

except URLError as e:
   streamlit.error()
    
streamlit.stop();
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
# my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_cur.execute("SELECT * FROM pc_rivery_db.public.fruit_load_list")
# my_data_row = my_cur.fetchone()
my_data_row = my_cur.fetchall()
# streamlit.text("Hello from Snowflake:")
streamlit.text("The fruit load list contains: ");
# streamlit.text(my_data_row);

add_my_fruit = streamlit.text_input('What fruit would you like to add?','Jackfruit')
streamlit.write('Thanks for adding ', add_my_fruit);

my_cur.execute("insert into pc_rivery_db.public.fruit_load_list values ('from streamlit')");
