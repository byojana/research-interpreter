import streamlit as st
from analyzer import analyze_abstract
from datetime import datetime

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

            # Build a nicely styled HTML version of the analysis for download
            terms_html = ""
            for term in result["technical_terms"]:
                terms_html += f"""
                <div class="term-box">
                    <h3>{term['term']}</h3>
                    <p><strong>Meaning:</strong> {term['simple_meaning']}</p>
                    <p><strong>Role in this research:</strong> {term['role_in_research']}</p>
                </div>
                """

            evidence_html = "".join(f"<li>{e}</li>" for e in result["evidence"])

            analysis_html = f"""
            <html>
            <head>
                <meta charset="UTF-8">
                <style>
                    body {{ font-family: Georgia, serif; max-width: 750px; margin: 40px auto; color: #222; line-height: 1.6; }}
                    h1 {{ color: #1a1a2e; border-bottom: 3px solid #1a1a2e; padding-bottom: 10px; }}
                    h2 {{ color: #16213e; margin-top: 30px; border-left: 4px solid #0f4c81; padding-left: 10px; }}
                    h3 {{ color: #0f4c81; margin-bottom: 5px; }}
                    .meta {{ color: #666; font-size: 0.9em; margin-bottom: 30px; }}
                    .abstract-box {{ background: #f5f5f5; padding: 15px; border-radius: 6px; font-style: italic; }}
                    .term-box {{ background: #f9f9f9; padding: 12px; margin: 10px 0; border-radius: 6px; border-left: 3px solid #0f4c81; }}
                    li {{ margin-bottom: 6px; }}
                </style>
            </head>
            <body>
                <h1>Research Abstract Analysis</h1>
                <p class="meta">Generated on {datetime.now().strftime("%Y-%m-%d %H:%M")}</p>

                <h2>Original Research Abstract</h2>
                <div class="abstract-box">{abstract_text}</div>

                <h2>Research Problem</h2>
                <p>{result["problem"]}</p>

                <h2>Existing Gap</h2>
                <p>{result["gap"]}</p>

                <h2>Proposed Approach</h2>
                <p>{result["approach"]}</p>

                <h2>Probable Innovation</h2>
                <p>{result["probable_innovation"]}</p>

                <h2>Why It May Work</h2>
                <p>{result["why_it_may_work"]}</p>

                <h2>Technical Terms</h2>
                {terms_html}

                <h2>Explain Like I'm New to the Topic</h2>
                <p>{result["simple_explanation"]}</p>

                <h2>Researcher's Main Message</h2>
                <p>{result["researchers_message"]}</p>

                <h2>Evidence</h2>
                <ul>{evidence_html}</ul>

                <h2>Confidence</h2>
                <p>{result["confidence"]}</p>
            </body>
            </html>
            """

            st.download_button(
                label="📥 Download Analysis (HTML)",
                data=analysis_html,
                file_name="research_analysis.html",
                mime="text/html"
            )