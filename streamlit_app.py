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

#create the repeatable code block (called a function)
def get_fruityvice_data(this_fruit_choice):
    # API call and assigning response to a variable
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)    
    
    # Use Pandas to normalize json respomse
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    
    return fruityvice_normalized 

streamlit.header('Fruityvice Fruit Advice!')
try:
    ## Add a Text Entry Box and Send the Input to Fruityvice as Part of the API Call
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice:
        streamlit.error("Please select a fruit to get information.")
    else:
        back_from_function = get_fruityvice_data(fruit_choice)
        streamlit.dataframe (back_from_function)

except URLError as e:
    streamlit.error()


# Let's Query Some Data
streamlit.header("View Our Fruit List - Add Your Favorites!") 

#Snowflake-related function
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("select * from fruit_load_list")
        return my_cur.fetchall()

# Add a button to load the fruit
if streamlit.button('Get Fruit List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    my_cnx.close()
    streamlit.dataframe(my_data_rows)

# Allow the end user to add a fruit to the list
def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur: 
        my_cur.execute("insert into fruit_load_list values ('" + new_fruit +"')")
        return "Thanks for adding " + new_fruit

add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a Fruit to the List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function = insert_row_snowflake(add_my_fruit)
    streamlit.text(back_from_function)


# Add a STOP Command to Focus Our Attention
# don't run anything past here while we troubleshoot
# streamlit.stop()                                                 

