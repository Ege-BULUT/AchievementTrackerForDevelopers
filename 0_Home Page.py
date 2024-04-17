import streamlit as st
from datetime import date, datetime
import json

for elem in st.session_state.keys():
    st.session_state[elem] = st.session_state[elem]

st.set_page_config(
    layout="wide",
    initial_sidebar_state="collapsed"
)


def get_date():
    all = str(datetime.now()).split(" ")
    yymmdd = all[0]
    hhmm = all[1].split(".")[0].replace(":", "-")
    return [yymmdd, hhmm]

def import_export_saves():
    with st.expander("Export"):
        st.download_button("Download Current Settings", json.dumps(st.session_state["info"], indent=4),
                           file_name="save_" + get_date()[0] + "_" + get_date()[1] + ".ATFDSave")
    with st.expander("Import"):
        file = st.file_uploader("Drag and Drop your .ATFDSave file here",
                         accept_multiple_files=False,
                         type=[".ATFDSave", ".atfdsave", ".ATFDSAVE"]
                         )
        if file is not None:
            if st.button("import"):
                new_info = json.loads(file.read())
                st.session_state["info"] = new_info


def body():
    st.write("INFO : ")
    st.write(st.session_state["info"])


def get_default_info():
    return json.load(open("data/default_info.ATFDSave", "r"))


def main():
    cols = st.columns([10, 10])

    with cols[1]:
        import_export_saves()
    with cols[0]:
        body()


if "info" not in st.session_state.keys():
    st.session_state["info"] = get_default_info()

main()
