# Import necessary functions
import streamlit as st
import spacy
from spacy.pipeline import EntityRuler
import pandas as pd
from spacy import displacy

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Session state
if "custom_patterns" not in st.session_state:
    st.session_state.custom_patterns = []

# Create a title for the app
st.title("Named Entity Recognition Program 📱")

# Write a description for the app
st.subheader ("Welcome to the **Named Entity Recognition Program**! ")
st.write ("In this application, you can upload files, text, and datasets, then" \
"add custom entity patterns using our top-of-the-line Entity Ruler and" \
"visualize these entities within the app itself.")

# File upload / text input
st.subheader("Upload Files or Input Text Here:")
input_method = st.radio("", ("Upload file", "Enter text"))

# Create spot to upload / input
text = ""
if input_method == "Upload file":
    uploaded_file = st.file_uploader("Choose a file", type = ["txt"])
    if uploaded_file:
        text = uploaded_file.read().decode("utf-8")
else:
    text = st.text_area("Enter text here:",
                     "Example text: Apple buys a U.K. startup for $1 billion.")

# Create entity rules
st.sidebar.header("Custom Entity Patterns 🧩")
with st.sidebar.form("rule_form"):
    st.write("Create new entity pattern:")
    label = st.text_input("Label (e.g., COMPANY, PRODUCT)", "COMPANY")
    pattern = st.text_input("Pattern (e.g., OpenAI)", "OpenAI")
    submitted = st.form_submit_button("Add Pattern")

# Create condition
if submitted and label and pattern:
    st.session_state.custom_patterns.append({"label": label.upper(), "pattern": pattern})
    st.success(f"New pattern addition successful! Added pattern: {pattern} ({label.upper()})", icon = "✅")

if st.sidebar.button("Clear All Patterns"):
    st.session_state.custom_patterns = []
    st. experimental_rerun()

if st.session_state.custom_patterns:
    st.sidebar.subheader("Current Patterns")
    for i, p in enumerate(st.session_state.custom_patterns, 1):
        st.sidebar.text(F"{i}. {p['label']}: {p['pattern']}")

# NLP Processing
if text.strip():
    with st.spinner("Processing text..."):

        # Add EntityRuler if needed
        if "entity_ruler" not in nlp.pipe_names:
            ruler = nlp.add_pipe("entity_ruler", before = "ner")
        else:
            ruler = nlp.get_pipe("entity_ruler")
        ruler.add_patterns(st.session_state.custom_patterns)

        nlp.max_length = len(text)
        doc = nlp(text)

        # Entity Visualization
        st.subheader("Entity Visualization 🖼️")

        # Define custom colors
        all_labels = list(set(
            [ent["label"] for ent in st.session_state.custom_patterns] +
            [ent.label_ for ent in doc.ents]
        ))

        predefined_colors = [
         "#f94144", "#f3722c", "#f8961e", "#f9844a", "#f9c74f",
        "#90be6d", "#43aa8b", "#577590", "#277da1", "#9d4edd",
        "#7209b7", "#560bad", "#3f37c9", "#4895ef", "#4cc9f0"    
        ]

        colors = {
            label: predefined_colors[i % len(predefined_colors)]
            for i, label in enumerate(all_labels)
        }

        options = {"ents": all_labels, "colors": colors}

        html = displacy.render(doc, style = "ent", options = options, page = False)
        st.markdown(html, unsafe_allow_html = True)

        # Entity table
        st.subheader("Detected Entities 📋")
        if doc.ents:
            data = [{"Entity": ent.text, "Label": ent.label_, "Start": ent.start_char, "End": ent.end_char} for ent in doc.ents]
            df = pd.DataFrame(data)
            st.dataframe(df)
        else:
            st.info("No entities detected in the input.")

# Offer example texts for testing the application
st.subheader("Text Samples:")
st.write("You can test the named entity recognition program with one of the texts below!")

sample_text_1 = """
    Apple Inc. is reportedly acquiring London-based AI startup DeepVision for a staggering $2.3 billion.\
    The deal is expected to finalize by August 2025, with CEO Tim Cook stating it will 'revolutionize on-device intelligence.'\
    Google and Microsoft were also in early talks with DeepVision before Apple made its move."""
st.subheader("**Tech Industry / Business News Example 📉**")
st.code(sample_text_1, language = 'text')

sample_text_2 = """
    According to a study published in The Lancet on March 3rd, 2024,\
    researchers from the University of Oxford and Johns Hopkins University discovered that Remdivir-X,\
    a new antiviral medication, reduces COVID-19 symptoms by 40% in patients over the age of 60.\
    The research was funded by the World Health Organization and the Bill & Melinda Gates Foundation."""
st.subheader("**Medical Research / Academic Example 🩺**")
st.code(sample_text_2, language = 'text')

sample_text_3 = """
    In preparation for the 2026 World Cup, the cities of Toronto, Los Angeles, and Mexico City are undergoing major renovations to their stadiums. \
    FIFA President Gianni Infantino announced the tournament would kick off on June 8th, with opening ceremonies held at SoFi Stadium in California."""
st.subheader("**Travel / Culture / Global Events Example 🛫**")
st.code(sample_text_3, language = 'text')