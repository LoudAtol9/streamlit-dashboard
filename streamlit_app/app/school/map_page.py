import streamlit as st
import database.join_csv_geo as jcg

query_lat_lon = jcg.get_table_map_pos()

df_coords = query_lat_lon[['LAT', 'LON']].copy()
df_coords['LAT'] = df_coords['LAT'].astype(float)
df_coords['LON'] = df_coords['LON'].astype(float)

st.map(df_coords)