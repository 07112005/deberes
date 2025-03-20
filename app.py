import streamlit as st
import pandas as pd
import numpy as np


st.set_page_config(page_title="Apartment Dashboard")


np.random.seed(0)


data = {
    'listing_type': ['Entire home/apt', 'Private room', 'Entire home/apt', 'Shared room', 'Private room', 'Entire home/apt'] * 50,
    'neighborhood': ['Downtown', 'Uptown', 'Midtown', 'Downtown', 'Uptown', 'Midtown'] * 50,
    'price': np.random.randint(50, 500, 300),
    'num_people': np.random.randint(1, 5, 300),
    'reviews_per_month': np.random.randint(0, 15, 300),
}

df = pd.DataFrame(data)


st.sidebar.title('Apartment Dashboard Filters')
listing_type_filter = st.sidebar.multiselect('Select Listing Type', df['listing_type'].unique(), default=df['listing_type'].unique())
neighborhood_filter = st.sidebar.multiselect('Select Neighborhood', df['neighborhood'].unique(), default=df['neighborhood'].unique())


filtered_df = df[df['listing_type'].isin(listing_type_filter) & df['neighborhood'].isin(neighborhood_filter)]


tab1, tab2 = st.tabs(['Overview', 'Price Simulator'])

with tab1:
    st.header('Overview of Listings')

    
    st.subheader('Listing Type vs Number of People')
    st.bar_chart(filtered_df.groupby('listing_type')['num_people'].mean())

   
    st.subheader('Price Distribution by Listing Type')
    st.bar_chart(filtered_df.groupby('listing_type')['price'].mean())

    
    st.subheader('Top Apartments with Highest Reviews per Month by Neighborhood')
    top_reviews_df = filtered_df.groupby(['neighborhood', 'price']).agg({'reviews_per_month': 'sum'}).reset_index()
    top_reviews_df = top_reviews_df.sort_values('reviews_per_month', ascending=False).head(10)
    st.bar_chart(top_reviews_df.set_index('neighborhood')['reviews_per_month'])

   
    st.subheader('Price vs Number of Reviews')
    st.line_chart(filtered_df[['price', 'reviews_per_month']].groupby('price').mean())


with tab2:
    st.header('Price Simulator')

   
    neighborhood_input = st.selectbox('Select Neighborhood', df['neighborhood'].unique())
    listing_type_input = st.selectbox('Select Listing Type', df['listing_type'].unique())
    num_people_input = st.slider('Number of People', 1, 5, 2)

    st.write(f"Based on your input, here are the price recommendations:")


    selected_data = df[(df['neighborhood'] == neighborhood_input) & 
                       (df['listing_type'] == listing_type_input) & 
                       (df['num_people'] == num_people_input)]
    
  
    min_price = selected_data['price'].min()
    max_price = selected_data['price'].max()
    
    st.write(f"The recommended price range for your selected apartment is: **${min_price} - ${max_price}**")


