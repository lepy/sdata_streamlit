# -*-coding: utf-8-*-
import streamlit as st
from streamlit_ace import st_ace
import pandas as pd
import numpy as np
import sdata
import uuid

st.set_page_config(
page_title="sdata demo app",
page_icon="🔖",
layout="wide",
initial_sidebar_state="expanded",
)

st.markdown("# sdata v{}".format(sdata.__version__))

st.sidebar.markdown("## sdata demo app")
