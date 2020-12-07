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

st.markdown("# sdata")

st.sidebar.markdown("## sdata demo app")

def empty():
    d = sdata.Data(name="N.N", table=pd.DataFrame(columns=[0]), description="This is an empty Data objekt. It has only a `name`, a `uuid` and this `description`.")
    return d

def basic_example():
    description = """# Ein Basisbeispiel

Dieses Beispiel zeigt die Ablage einer Tabelle mit zwei Spalten im sdata-Format. 

Das sdata-Datenformat `Data` besteht aus drei Komponenten: den Daten (hier eine **Tabelle** `table`), den **Metadaten** `metadata` 
(`name`, `uuid`, `Temperatur`) und einer **Beschreibung** der Daten `description`.

Jeder Datensatz `Data` benötigt einen Namen `name`. Die vom User vorgegebene Identifikation des Datensatzes ist aber mit einer hohen 
Wahrscheinlichkeit nicht eindeutig, da i.d.R sehr kurze Bezeichnungen gewählt werden. 

Zur Identifikation eines Datensatzes ist eine möglichst eindeutige Bezeichnung hilfreich. Üblicherweise wird hierzu  
ein sogenannter Universally Unique Identifier [`uuid`](https://de.wikipedia.org/wiki/Universally_Unique_Identifier) 
verwendet. Diese Merkmale eines Datensatzes werden im sdata-Format in den Metadaten gespeichert.

Die Komponente `metadata` hat also mindestenz zwei Attribute `name` und `uuid`. Die einfachste Form eines Attributes 
stellt ein key-value-Tupel dar, d.h. eine Verknüpfung einer Bedeutung mit einer Ausprägung, z.B. `Augenfarbe="blau"` 
oder `name="basic example"`.

Ein Attribut - auch Eigenschaft genannt - stellt demnach ein Merkmal des Datenobjektes dar. Nützlich ist auch eine 
Angabe einer physikalischen Größe, welche i.d.R. Einheiten behaftet ist. Exemplarisch ist hier ein Attribut 
`Temperatur` mit der Ausprägung `25.4°C` aufgeführt. Die physikalische Einheit wird im Attributfeld `unit` abgelegt 
(`unit="degC"`) und der Zahlenwert im Feld `value=25.4`. Da eine physikalische Größe aus dem Produkt einer (reelen) Zahl und 
einer physikalischen Einheit besteht, sieht das sdata-Attribut-Format auch ein Attributfeld `dtype` 
zur Definition des Datentypes für den Attributwert `value` vor.

Ferner kann jedes Attribut im Feld `description` genauer beschrieben werden.

Ein `Attribut` (Eigenschaft) des Datenobjektes hat im sdata-Format hat demnach die Felder

* `name` ... Name des Attributes
* `value` ... Wert des Attributes
* `dtype` ... Datentyp des Attributwertes `values` (default=`str`)
* `unit` ... physikalische Einheit des Attributes (*optional*)
* `description` ... Beschreibung des Attributes (*optional*)

Das eigentliche Datenobjekt `table` ist als `pandas.DataFrame` repräsentiert, d.h. jede Zelle der Tabelle ist durch 
ein Tupel (index, column) indiziert. Jede Spalte (`column`) ist durch den Spaltennamen (hier z.B. `a` oder `b`) indizierbar. 
Jede Zeile (`row`) ist durch den `index` indiziert, wobei der `index` auch alphanumerisch sein kann (z.B. 'max_b').

             a    b
    index          
    0      1.1  2.4
    max_b  2.1  5.2
    2      3.5  2.2

Die Beschreibung `description` ist vom Typ `str`, d.h. es ist u.a. Möglich eine vereinfachte Auszeichnungssprache 
wie [Markdown](https://de.wikipedia.org/wiki/Markdown) zu vewenden.

Beispielhaft ist hier Datenbeschreibung mit Überschriften und Formel aufgeführt.   

    # header
    ## subheader

    a remarkable text

    Bullet list:

    - aaa
        - aaa.b
    - bbb


    Numbered list:

    1. foo
    1. bar

    $f(x) = \\frac{1}{2}\\sin(x)$

    code:

        name="basic example"

    A [Link](https://github.com/lepy/sdata).

# header
## subheader

a remarkable text

Bullet list:

- aaa
    - aaa.b
- bbb


Numbered list:

1. foo
1. bar

$f(x) = \\frac{1}{2}\\sin(x)$

code:

    name="basic example"

A [Link](https://github.com/lepy/sdata).

        """

    df = pd.DataFrame({"a": [1.1, 2.1, 3.5],
                       "b": [2.4, 5.2, 2.2]}, index=[0, 'max_b', 2])
    d = sdata.Data(name="basic example", uuid="38b26864e7794f5182d38459bab85842", table=df, description=description)
    d.metadata.add("Temperatur", value=25.4, dtype="float", unit="degC", description="Temperatur")
    return d

def minimal_example():
    d = sdata.Data(name="Die Antwort",
                      table=pd.DataFrame({"x": [42]}),
                      description="The Answer to the Ultimate Question of Life, The Universe, and Everything")
    return d

examples = {"basic example": basic_example,
            "minimal example": minimal_example,
            "empty":empty}

select_example = st.sidebar.selectbox("Example", list(examples.keys()), index=0, key=None)


@st.cache(persist=False, allow_output_mutation=True)
def get_sdata(name):
    d = examples.get(name, "basic example")()
    return d

data = get_sdata(select_example)

content_metadata = data.metadata.to_csv(sep=";", header=None)
EXAMPLE_DESCRIPTION = 'Example description'
METADATA = "Metadata"
TABLE = "Table"
DESCRIPTION = "Description"
EXPORT = 'Export'

sdatapart = st.sidebar.radio(
    "choose sdata.Data component:",
    (EXAMPLE_DESCRIPTION, METADATA, TABLE, DESCRIPTION, EXPORT))


if sdatapart == EXAMPLE_DESCRIPTION:
    st.markdown(data.description)

# ------------------------- Metadata ----------------------------------------
elif sdatapart == METADATA:
    st.markdown('## Metadata')
    input_name = st.text_input("name", value=data.name)
    if input_name:
        data.name = input_name
        # st.info("changed name to {}".format(data.name))

    gen_uuid = st.button("gen uuid")
    if gen_uuid:
        new_uuid = uuid.uuid4()
        data.uuid = new_uuid
    input_uuid = st.text_input("uuid", value=data.uuid)
    if input_uuid:
        data.uuid = input_uuid
        # todo: textarea update
    # st.markdown("{}".format(data.name))
    # st.markdown("{}".format(data.uuid))


    st.markdown("""### Edit Metadata [name; value; dtype; unit; description]""")
    content_metadata = data.metadata.to_csv(sep=";", header=None)
    content_metadata = content_metadata.replace("\t", " ; ")

    # content_metadata = st_ace(key="Meta", height=100, placeholder=content_metadata, value=content_metadata,
    #                           language="rst")

    content_metadata = st.text_area("metadata", value=content_metadata, height=200, max_chars=None, key="metadata")

    content_metadata = content_metadata.replace("\t", " ; ")
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
            # print([row["name"]])
            if row["name"]:
                data.metadata.add(row["name"], value=row["value"], dtype=str(row["dtype"]), unit=row["unit"],
                              description=row["description"])

    except Exception as exp:
        st.markdown("### error: {}".format(exp))
        st.write(cells)
    st.markdown("### sdata.Data.metadata.df")
    st.dataframe(data.metadata.df)

# ------------------------- Table ----------------------------------------
elif sdatapart == TABLE:
    st.markdown('## Table')
    # content_table = get_content("table")
    content_table = data.df.to_csv(sep=";", index=None)
    content_table = content_table.replace("\t", ";")
    content_table = st.text_area("table", value=content_table, height=200, max_chars=None, key="table")
    # content_table = st_ace(key="table", height=100, placeholder=content_table, value=content_table)
    content_table = content_table.replace("\t", ";")
    cells = []
    for line in content_table.splitlines():
        row = []
        for cell in line.split(";"):
            cell = cell.strip()
            try:
                cell = float(cell.replace(",", "."))
            except:
                pass
            row.append(cell)
        # cells.append(line.split(";"))
        cells.append(row)
    try:
        print(cells[1:10])
        df = pd.DataFrame(cells[1:], columns=cells[0])
        # df.dropna(inplace=True)
        print(df.head())
        # st.write("parsed data")
        # st.dataframe(df)
        data.df = df
    except:
        st.write(cells)

    st.write("sdata.Data.table")
    st.dataframe(data.table)

# ------------------------- Description ----------------------------------------
elif sdatapart == DESCRIPTION:
    st.markdown('## Description')
    content_description = data.description
    content_description = st_ace(key="description", height=100, placeholder=content_description,
                             language="markdown", value=content_description)
    st.write(content_description)
    data.description = content_description

# ------------------------- Export ----------------------------------------
elif sdatapart == EXPORT:
    st.markdown('## Export')

    st.markdown(data.get_download_link(), unsafe_allow_html=True)

    ex = st.button("export data as json")
    if ex:
        st.markdown("## sdata.Data json")
        content_json = data.to_json()
        # content_json = st_ace(key="json", height=100, value=content_json, readonly=True,
        #                       language="json", wrap=True)

        st.json(content_json)

        # data2 = data.from_json(data.to_json())
        st.markdown("## example python code")
        content_python = r"""# python example
import sdata
json_str = r'''{}'''
data = sdata.Data.from_json(json_str)
print(data.describe())
print(data.metadata.df)
print(data.df)
print(data.description)
""".format(data.to_json())

        # st.code(content_python)
        # content_json = st_ace(key="python", height=200, value=content_python, readonly=True,
        #                       language="python", wrap=True)
        st.text_area("python", value=content_python, height=300)
        st.balloons()

else:
    st.write("You didn't select anything.")

st.sidebar.markdown("## sdata.Data Status")
st.sidebar.markdown("{}".format(data.name))
# st.sidebar.markdown("{}".format(data.uuid))
st.sidebar.dataframe(data.describe())


# chart_data = pd.DataFrame(
#     np.random.randn(20, 3),
#     columns=['a', 'b', 'c'])
# button_plot = st.button("plot data")
# if button_plot:
#     chart_data = data.df
#     st.line_chart(chart_data)


st.sidebar.markdown("""© Lepy 2017-2020

* [sdata.git](https://github.com/lepy/sdata)
* [sdata MIT license](https://raw.githubusercontent.com/lepy/sdata/master/LICENSE-MIT)
* [sdata documentation](https://sdata.readthedocs.io/en/latest/index.html)
""")

# * © [sdata demo app GPL license](https://raw.githubusercontent.com/lepy/sdata_streamlit/main/LICENSE)

