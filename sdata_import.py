import streamlit as st
import streamlit.components.v1 as stc
import pandas as pd
import base64
import time

timestr = time.strftime("%Y%m%d-%H%M%S")


def make_downloadable_df_format(data, format_type="csv"):
    if format_type == "csv":
        datafile = data.to_csv(index=False)
    elif format_type == "json":
        datafile = data.to_json()
    b64 = base64.b64encode(datafile.encode()).decode()  # B64 encoding
    st.markdown("### ** Download File  📩 ** ")
    new_filename = "fake_dataset_{}.{}".format(timestr, format_type)
    href = f'<a href="data:file/{format_type};base64,{b64}" download="{new_filename}">Click Here!</a>'
    st.markdown(href, unsafe_allow_html=True)


df = pd.DataFrame([1, 2, 3])

dataformat = st.sidebar.selectbox("Save Data As", ["csv", "json"])

with st.beta_expander("📩: Download"):
    make_downloadable_df_format(df, dataformat)
