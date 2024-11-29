from pandas import DataFrame
import streamlit as st
import database.mysql_operations as op


def get_table_map_pos():
    query = '''

    SELECT * FROM escola_geo;

    '''

    return  op.load_table_custom(query, ())
