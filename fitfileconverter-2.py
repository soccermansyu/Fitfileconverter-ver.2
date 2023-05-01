#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import datetime
import os
import shutil
import csv
from pathlib import Path

import fitdecode
import pandas as pd
import plotly.express as px
import streamlit as st

current_dir = os.path.dirname(__file__)


def load_fit_tmp(path):
    """
    this is an only sample function
    load fit file and convert to dataframe
    you should change codes below for fit file structure that you expect
    """

    datas = []
    with fitdecode.FitReader(path) as fit:
        for frame in fit:
            if isinstance(frame, fitdecode.FitDataMessage):
                if frame.name == 'record':
                    data = {}
                    for field in frame.fields:
                        data[field.name] = field.value
                    datas.append(data)

    # データクレンジング
    df = pd.DataFrame(datas)
    for col_name in df.columns:
        if 'unknown' in col_name:
            df = df.drop(col_name, axis=1)

    return df


@st.cache
def convert_df(df):
    """
    convert df to csv
    """
    return df.to_csv(index=False).encode('cp932')


def calc_tmp(df):
    """
    this is an only sample function
    you should define process for your purpose
    """
    df = df.loc[0:, :]
    return df

# upload .fit file
uploaded_file = st.file_uploader("あなたの .fit fileをアップロードしてください")
if uploaded_file is not None:
    # set path
    data_directory_path = Path(current_dir, "data")
    file_path = Path(data_directory_path, uploaded_file.name)

    # make data directory
    if data_directory_path.exists():
        shutil.rmtree(data_directory_path)
    os.makedirs(data_directory_path)

    # export .file to data directory
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # load fit file and convert to dataframe
    df = load_fit_tmp(file_path)

    # data processing
    df = calc_tmp(df)


    # convert df to csv
    csv = convert_df(df)

    # download
    st.download_button(
        label="Download",
        data=csv,
        file_name='activity_converted.csv',
        mime='text/csv',
    )

