import streamlit as st
from streamlit_ace import st_ace
import pandas as pd
import numpy as np
import sdata
import uuid

st.set_page_config(
page_title="sdata demo app",
page_icon="!",
layout="wide",
initial_sidebar_state="expanded",
)


st.markdown("# sdata example")
st.sidebar.markdown("## sdata")


@st.cache(persist=False, allow_output_mutation=True)
def get_sdata(name):
    df = pd.DataFrame({"a": [1.1, 2.1, 3.5],
                       "b": [2.4, 1.2, 2.2]})
    d = sdata.Data(name=name, uuid="38b26864e7794f5182d38459bab85842", table=df)
    d.metadata.add("Temp", value=25.4, dtype="float", unit="degC", description="Temperatur")
    d.comment = """# header
## subheader

a remarkable text



$f(x) = \\frac{1}{2}\\sin(x)$


"""
    return d

# print(help(st_ace))
# Spawn a new Ace editor
# st_ace(value='', placeholder='', height=500, language='plain_text', theme='chrome',
# keybinding='vscode', min_lines=None, max_lines=None, font_size=12,
# tab_size=4, wrap=False, show_gutter=True, show_print_margin=False,
# readonly=False, annotations=None, markers=None, auto_update=True, key=None)

data = get_sdata("my_first_sdata")



content_metadata = data.metadata.to_csv(sep=";", header=None)


sdatapart = st.sidebar.radio(
    "choose sdata.Data component:",
    ('Metadata', 'Table', 'Comment'))



if sdatapart == 'Metadata':
    st.markdown('## Metadata')
    gen_uuid = st.button("gen uuid")
    if gen_uuid:
        new_uuid = uuid.uuid4()
        data.uuid = new_uuid
    # content_metadata = get_content("metadata")
    content_metadata = data.metadata.to_csv(sep=";", header=None)

    content_metadata = content_metadata.replace("\t", ";")

    st.write("name; value; dtype; unit; description")
    content_metadata = st_ace(key="Meta", height=100, placeholder=content_metadata, value=content_metadata,
                              language="rst")
    content_metadata = content_metadata.replace("\t", ";")
    # st.write(content_metadata)
    cells = []
    for line in content_metadata.splitlines():
        cells.append(line.split(";"))
    try:
        df = pd.DataFrame(cells, columns=['name', 'value', 'dtype', 'unit', 'description'])
        # st.write("parsed data")
        # st.dataframe(df)
        data.metadata._attributes = {}
        for i, row in df.iterrows():
            # print(row)
            # print(row["name"], row.value, str(row.dtype), row.unit, row.description)
            data.metadata.add(row["name"], value=row["value"], dtype=str(row["dtype"]), unit=row["unit"],
                              description=row["description"])

    except Exception as exp:
        st.markdown("### error: {}".format(exp))
        st.write(cells)
    st.write("sdata.Data.metadata")
    st.dataframe(data.metadata.df)

elif sdatapart == 'Table':
    st.markdown('## Table')
    # content_table = get_content("table")
    content_table = data.df.to_csv(sep=";", index=None)
    content_table = content_table.replace("\t", ";")
    content_table = st_ace(key="table", height=100, placeholder=content_table, value=content_table)
    content_table = content_table.replace("\t", ";")
    cells = []
    for line in content_table.splitlines():
        row = []
        for cell in line.split(";"):
            try:
                cell = float(cell.replace(",", "."))
            except:
                pass
            row.append(cell)
        # cells.append(line.split(";"))
        cells.append(row)
    try:
        df = pd.DataFrame(cells[1:], columns=cells[0])
        # st.write("parsed data")
        # st.dataframe(df)
        data.df = df
    except:
        st.write(cells)

    st.write("sdata.Data.table")
    st.dataframe(data.table)


elif sdatapart == 'Comment':
    st.markdown('## Comment')
    content_comment = data.comment
    content_comment = st_ace(key="comment", height=100, placeholder=content_comment,
                             language="markdown", value=content_comment)
    st.write(content_comment)
    data.comment = content_comment

else:
    st.write("You didn't select anything.")



st.sidebar.markdown("## sdata.Data Status")
st.sidebar.markdown("{}".format(data.name))
st.sidebar.markdown("{}".format(data.uuid))
st.sidebar.dataframe(data.describe())

ex = st.button("export data")
if ex:
    st.markdown("## sdata.Data json")
    content_json = st_ace(key="json", height=100, value=data.to_json(), readonly=True,
                          language="json", wrap=True)

    # data2 = data.from_json(data.to_json())
    st.markdown("## example python code")
    content_python = r"""# python example
import sdata
json_str = r'''{}'''
data = sdata.Data.from_json(json_str)
print(data.describe())
print(data.metadata.df)
print(data.df)
print(data.comment)
""".format(data.to_json())
    content_json = st_ace(key="python", height=200, value=content_python, readonly=True,
                          language="python", wrap=True)
    st.balloons()

st.sidebar.markdown("""© Lepy 2017-2020

* [sdata.git](https://github.com/lepy/sdata)
* [sdata MIT license](https://raw.githubusercontent.com/lepy/sdata/master/LICENSE-MIT)
* [sdata documentation](https://sdata.readthedocs.io/en/latest/index.html)
""")

# * © [sdata demo app GPL license](https://raw.githubusercontent.com/lepy/sdata_streamlit/main/LICENSE)

st.markdown(data.get_download_link(), unsafe_allow_html=True)
st.write(data.df.dtypes)
st.write(data.df.iloc[0].dtype)