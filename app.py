import streamlit as st
from analyzer import analyze_abstract

st.set_page_config(page_title="Research Innovation Interpreter", layout="centered")

st.title("AI-Based Research Innovation Interpreter")
st.write("Paste a research abstract below to get a structured interpretation of its problem, approach, and probable innovation.")

abstract_text = st.text_area("Paste your research abstract here:", height=200)

if st.button("Analyze Abstract"):
    if abstract_text.strip() == "":
        st.warning("Please paste an abstract first.")
    else:
        with st.spinner("Analyzing abstract..."):
            try:
                result = analyze_abstract(abstract_text)
            except Exception as e:
                st.error(f"Something went wrong: {e}")
                result = None

        if result:
            st.header("Research Problem")
            st.write(result["problem"])

            st.header("Existing Gap")
            st.write(result["gap"])

            st.header("Proposed Approach")
            st.write(result["approach"])

            st.header("Probable Innovation")
            st.write(result["probable_innovation"])

            st.header("Why It May Work")
            st.write(result["why_it_may_work"])

            st.header("Technical Terms")
            for term in result["technical_terms"]:
                st.subheader(term["term"])
                st.write(f"**Meaning:** {term['simple_meaning']}")
                st.write(f"**Role in this research:** {term['role_in_research']}")

            st.header("Explain Like I'm New to the Topic")
            st.write(result["simple_explanation"])

            st.header("Researcher's Main Message")
            st.write(result["researchers_message"])

            st.header("Evidence")
            for e in result["evidence"]:
                st.write(f"- {e}")

            st.header("Confidence")
            st.write(result["confidence"])