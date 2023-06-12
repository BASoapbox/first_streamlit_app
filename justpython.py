import pandas as pd
import requests

# pulling the data into a pandas dataframe called my_fruit_list
my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

# myfruit = pd.DataFrame(my_fruit_list)
# print(myfruit.index)

# print(my_fruit_list)

# print(list(my_fruit_list.index))

# print(list(my_fruit_list.Fruit))

# print(my_fruit_list.set_index('Fruit'))


fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")

# print(fruityvice_response.json())

fruityvice_normalized = pd.json_normalize(fruityvice_response.json())

print(fruityvice_normalized)
