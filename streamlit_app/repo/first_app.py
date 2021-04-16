import streamlit as st
import numpy as np
import pandas as pd
import time


def get_textfile_content(filepath):
    with open(filepath, mode='r') as f:
        content = f.read()
    return content

def side_by_side():
    a,b,c = st.beta_columns(3)
    a.button('I am A')
    b.button('I am B')
    c.write(' I am C')

def expand_bar():
    expander = st.beta_expander("FAQ")
    expander.write("Here you could put in some really, really long explanations...")

def show_progress():
    latest_iteration = st.empty()
    bar = st.progress(0)

    for i in range(100):
        # Update the progress bar with each iteration.
        latest_iteration.text(f'Iteration {i+1}')
        bar.progress(i + 1)
        time.sleep(0.1)

def side_description():
    content = get_textfile_content('temp.md')
    st.sidebar.markdown(content)

def description():
    st.title('First App chhìgiām')

def data_table():
    st.write("Use data to create a table:")
    st.write(pd.DataFrame({
        '1st col': [1,2,3,4],
        '2nd col': [10,20,30,40],
        }))

def chart_data():
    chart_data = pd.DataFrame(
         np.random.randn(20, 3),
         columns=['a', 'b', 'c'])
    
    st.line_chart(chart_data)

def show_map():
    map_data = pd.DataFrame(
        np.random.randn(1000, 2) / [50, 50] + [22.962396,120.2505378],
        columns=['lat', 'lon'])
    
    st.map(map_data)
    
def sidebar_controller():
    option = st.sidebar.selectbox(
        'Which model do you like best?',
         ('SSD', 'YOLO', 'oops', '測試'))
    
    st.sidebar.write(f'You selected: {option}')

def init_settings():
    st.set_page_config(
            page_title="Aqua test",
            page_icon="🐠",
            )

def main():
    init_settings()
    description()
    side_description()

    data_table()
    chart_data()

    if st.checkbox('Show map'):
        show_map()

    sidebar_controller()
    side_by_side()
    expand_bar()

    if st.checkbox('Show progress'):
        show_progress()


if __name__=='__main__':
    main()
