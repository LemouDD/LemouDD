import streamlit as st
import pandas as pd
import plotly.express as px
import qrcode
from io import BytesIO

# Initialize session state for storing results
if "results" not in st.session_state:
    st.session_state["results"] = []

# Define questions and weights for each category
questions = [
    {"question": "Climate change is not a serious issue.",
     "weights": {"denial": 3, "liberal": 1, "left-wing": 0}},
    {"question": "Governments should take moderate steps to combat climate change.",
     "weights": {"denial": 0, "liberal": 3, "left-wing": 1}},
    {"question": "Radical changes are needed to fight climate change.",
     "weights": {"denial": 0, "liberal": 1, "left-wing": 3}},
]

st.title("Environmental Attitude Quiz")
st.write("Answer the following questions to find out your environmental attitude.")

# Get participant's name
name = st.text_input("Enter your name:", key="name")
if name == "":
    st.warning("Please enter your name to proceed.")

# Initialize participant scores
participant_scores = {"denial": 0, "liberal": 0, "left-wing": 0}

# Loop through questions and collect responses
if name != "":
    for question in questions:
        st.write(question["question"])
        response = st.radio(
            "Your choice:",
            ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"],
            key=question["question"]
        )
        
        # Map response to a score (e.g., 0 to 4)
        score = {"Strongly Disagree": 0, "Disagree": 1, "Neutral": 2, "Agree": 3, "Strongly Agree": 4}[response]
        
        # Update scores for each category
        for category, weight in question["weights"].items():
            participant_scores[category] += score * weight

    # Normalize scores to probabilities
    total_score = sum(participant_scores.values())
    if total_score > 0:
        probabilities = {category: round((score / total_score) * 100, 2)
                         for category, score in participant_scores.items()}
    else:
        probabilities = {category: 0 for category in participant_scores}

    # Save results
    if st.button("Submit"):
        st.session_state["results"].append({"name": name, **probabilities})
        st.success("Your responses have been recorded!")

# Show all results if everyone is done
if st.button("Show Results"):
    if st.session_state["results"]:
        st.subheader("All Participants' Results:")
        df = pd.DataFrame(st.session_state["results"])
        st.write(df)

        # Visualize results for each participant
        for _, row in df.iterrows():
            fig = px.bar(
                pd.DataFrame(row[1:]), 
                x=row[1:].index, 
                y=row[1:], 
                title=f"{row['name']}'s Environmental Attitude",
                labels={"index": "Category", "value": "Percentage"},
                color=row[1:].index
            )
            st.plotly_chart(fig)
    else:
        st.warning("No results to show yet!")

# QR Code for Link
st.subheader("Share This Quiz!")
url = "https://your-streamlit-app-link-here"  # Replace with your actual app URL
qr = qrcode.QRCode()
qr.add_data(url)
qr.make()
img = qr.make_image(fill="black", back_color="white")
buffer = BytesIO()
img.save(buffer, format="PNG")
st.image(buffer.getvalue(), caption="Scan the QR code to take the quiz!")
