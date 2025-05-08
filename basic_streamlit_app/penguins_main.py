import streamlit as st
import pandas as pd

# Title of the app
st.title("My First App: Penguins!")

# Description of the app
st.write("This app allows the user to filter the dataset based on penguin island, body mass, and species.")
st.write("First, the user selects an island. This prompts the app to display all penguins on that island, including a total number.")
st.write("""
         Next, the user uses a slider to choose the maximum weight of the penguins they want to examine. 
         Then,  the app displays all penguins who from that island and below that weight, along with a total number.
         """)
st.write("""
         Finally, the user selects a species. 
         This prompts the app to display all penguins of that species who are below the desired weight on the desired island.
         """)
st.write("This app allows users to examine smaller penguins from various islands and species.")

# Dataset I am working with
df = pd.read_csv("basic_streamlit_app/data/penguins.csv")
st.write("Here is the penguins dataset loaded from a CSV file:")
st.dataframe(df)

# Use a selectbox to filter penguins by island.
island = st.selectbox("Select a island", df["island"].unique())

# Filter DataFrame based on user selection.
filtered_df = df[df["island"] == island]

# Display the number of results with those filters applied.
st.write (f"Number of penguins on {island}: {len(filtered_df)}")
st.dataframe(filtered_df)

# Use a slider to display number of penguins under certain body mass on that island.
min_val, max_val = df["body_mass_g"].min(), df["body_mass_g"].max()
selected_value = st.slider('Select a maximum body mass value:', min_value=min_val, max_value=max_val)

# Filter DataFrame based on user selection.
extra_filtered_df = filtered_df[(filtered_df["body_mass_g"] <= selected_value)]

# Display number of results with those filters applied.
st.write(f"Number of penguins on {island} below {selected_value} g: {len(extra_filtered_df)}")
st.dataframe(extra_filtered_df)

# Based on the values below that body mass, let user choose a species.
species = st.selectbox("Select a species", df["species"].unique())

# Filter DataFrame based on user selection.
extremely_filtered_df = extra_filtered_df[(extra_filtered_df["species"] == species)]

# Display number of results with those filters applied.
st.write(f"Number of {species} penguins on {island} below {selected_value} g: {len(extremely_filtered_df)}")
st.dataframe(extremely_filtered_df)
