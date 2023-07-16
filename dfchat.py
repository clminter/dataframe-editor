import streamlit as st
import pandas as pd
import numpy as np

def load_data(file):
    data = pd.read_csv(file)
    return data

def rename_column(df, old_name, new_name):
    df = df.rename(columns={old_name: new_name})
    return df

st.title('Data Editor')

file = st.file_uploader('Upload CSV', type=['csv'])

if file is not None:
    if 'df' not in st.session_state:
        data = load_data(file)
        st.session_state.df = data
        st.session_state.edited_df = st.session_state.df.copy()

    def save_edits():
        st.session_state.df = st.session_state.edited_df.copy()

    if 'df' in st.session_state:

        with st.expander("Instructions"):
            st.write("""
            1. Upload a CSV file.
            2. Edit the dataframe by adding or deleting rows.
            3. Change column name.
            4. Download the edited dataframe.
            """)

        new_row = st.button('Add New Row')
        delete_row = st.button('Delete Row')

        if new_row:
            st.session_state.edited_df = st.session_state.edited_df.append(pd.Series(), ignore_index=True)

        if delete_row:
            row_index = st.number_input('Enter the row index to delete', min_value=0, max_value=len(st.session_state.edited_df)-1, value=0, step=1)
            if st.button('Confirm Delete'):
                st.session_state.edited_df = st.session_state.edited_df.drop(row_index)
                st.session_state.edited_df = st.session_state.edited_df.reset_index(drop=True)

        old_name = st.selectbox('Select Column to Rename', st.session_state.edited_df.columns)
        rename_placeholder = st.empty()
        new_name = rename_placeholder.text_input('Enter New Column Name')

        if st.button('Rename Column'):
            st.session_state.edited_df = rename_column(st.session_state.edited_df, old_name, new_name)
            rename_placeholder.text_input('Enter New Column Name', value='', key=123)

        st.session_state.edited_df = st.data_editor(st.session_state.edited_df)

        st.download_button('Download data as CSV', data=st.session_state.edited_df.to_csv(index=False), file_name='data.csv', mime='text/csv')

        # Call save_edits at the end of script
        save_edits()
