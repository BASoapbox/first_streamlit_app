import streamlit
import pandas
import requests


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
# # Let's put a pick list here so they can pick the fruit they want to include 
# streamlit.multiselect("Pick some fruits 1:", list(my_fruit_list.index))
# streamlit.multiselect("Pick some fruits 2:", list(my_fruit_list.Fruit))

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


#  Call the Fruityvice API from Streamlit App!

# # Testing API call
# fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
# streamlit.text(fruityvice_response)

### New Section to display fruityvice api response

streamlit.header ('Fruityvice Fruit Advice!')

# API call and assigning response to a variable
# fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + "kiwi")

# Display response in Json format
streamlit.text(fruityvice_response.json())

## Let's Get the Fruityvice Data Looking a Little Nicer

# Use Pandas to normalize Json respomse
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())

# asking streamlit library to display it on the page as DataFrame/table
streamlit.dataframe(fruityvice_normalized)


## Add a Text Entry Box and Send the Input to Fruityvice as Part of the API Call
fruit_choice = streamlit.text_input('What fruit would you like information about?', 'kiwi')

fruityvice_response2 = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)

streamlit.write('The user entered:', fruityvice_response2)