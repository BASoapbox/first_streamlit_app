import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError


streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Broiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# pulling the data into a pandas dataframe called my_fruit_list
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

# # We'll add a user interactive widget called a Multi-select that will allow users to pick the fruits they want in their smoothies.

# Choose the Fruit Name Column as the Index
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))

# asking streamlit library to display it on the page
streamlit.dataframe(my_fruit_list)


# Filter the Table Data

# We'll ask our app to put the list of selected fruits into a variable called fruits_selected. 
# Then, we'll ask our app to use the fruits in our fruits_selected list to pull rows from the 
# full data set (and assign that data to a variable called fruits_to_show). 
# Finally, we'll ask the app to use the data in fruits_to_show in the dataframe it displays on the page. 
fruit_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])

# https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.loc.html
fruits_to_show = my_fruit_list.loc[fruit_selected]

# asking streamlit library to display it on the page as DataFrame
streamlit.dataframe(fruits_to_show)


### Call the Fruityvice API from Streamlit App!
### New Section to display fruityvice api response

streamlit.header('Fruityvice Fruit Advice!')

## Add a Text Entry Box and Send the Input to Fruityvice as Part of the API Call
fruit_choice = streamlit.text_input('What fruit would you like information about?', 'kiwi')

# API call and assigning response to a variable
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)

# Use Pandas to normalize Json respomse
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())

streamlit.write('The user entered:', fruit_choice)

# asking streamlit library to display it on the page as DataFrame/table
streamlit.dataframe(fruityvice_normalized)


# Add a STOP Command to Focus Our Attention
# don't run anything past here while we troubleshoot
streamlit.stop()

# Let's Query Some Data, Instead
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")
my_data_row = my_cur.fetchone()
streamlit.text("The fruit load list contains:")
streamlit.text(my_data_row)


# Let's Change the Streamlit Components to Make Things Look a Little Nicer
my_data_row = my_cur.fetchone()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_row)


# Let's Get All the Rows, Not Just One
my_cur.execute("select * from fruit_load_list")
my_data_rows = my_cur.fetchall() 
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)
                                                     
                                                     
# Allow the use to add a fruit to the list
add_my_fruit = streamlit.text_input('What fruit would you like to?', 'jackfruit')
streamlit.write('Thanks for adding ', add_my_fruit)

# Write Code to Add Rows to Our Fruit List in Snowflake

#This will not work correctly, but just go with it for now
my_cur.execute("insert into fruit_load_list values ('from streamlit')")
