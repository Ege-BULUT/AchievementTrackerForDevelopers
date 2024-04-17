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
    platform = st.selectbox("PLATFORM", options=["GITHUB", "LEETCODE", "HACKERRANK"])
    options = []
    if platform == "GITHUB":
        options = ["Finished Project", "Ongoing Project", "Planned Project", "Abandoned Project"]
    else:
        options = ["Solved Question", "Ongoing Question"]
    cols = st.columns([1,2])
    with cols[0]:
        amount = st.number_input("AMOUNT", min_value=1, max_value=100000)
    with cols[1]:
        status = st.selectbox("STATUS", options=options)

    cols = st.columns([2,7,1,2,16,16])
    with cols[0]:
        st.write("On ")
    with cols[1]:
        st.write(platform)
    with cols[2]:
        st.write(amount)
    with cols[3]:
        st.write("x")
    with cols[4]:
        st.write(status)

    if st.button("Add"):
        if platform in st.session_state["info"].keys():
            if status in st.session_state["info"][platform].keys():
                st.session_state["info"][platform][status] += amount
            else:
                st.session_state["info"][platform].update({status: amount})
        else:
            st.session_state["info"].update({platform: {status: amount}})

    st.write(" ")
    st.write(" ")
    with st.expander("INFO : ", expanded=True   ):
        st.write(st.session_state["info"])


def get_default_info():
    return json.load(open("data/default_info.ATFDSave", "r"))


def main():
    cols = st.columns([10, 10])

    with cols[1]:
        st.write(" ")
        import_export_saves()
    with cols[0]:
        body()


if "info" not in st.session_state.keys():
    st.session_state["info"] = get_default_info()

main()
