import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

# Define questions and weights for each category
questions = [
    {"question": "Climate change is not a serious issue.",
     "weights": {"denial": 3, "liberal": 1, "left-wing": 0}},
    {"question": "Governments should take moderate steps to combat climate change.",
     "weights": {"denial": 0, "liberal": 3, "left-wing": 1}},
    {"question": "Radical changes are needed to fight climate change.",
     "weights": {"denial": 0, "liberal": 1, "left-wing": 3}},
]

# Initialize participant scores
participant_scores = {"denial": 0, "liberal": 0, "left-wing": 0}

st.title("Environmental Attitude Quiz")
st.write("Answer the following questions to find out your environmental attitude.")

# Loop through questions and collect responses
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

# Display results
st.subheader("Your Results:")
df = pd.DataFrame.from_dict(probabilities, orient="index", columns=["Probability"])
st.write(df)

# Visualize results
fig = px.bar(df, x=df.index, y="Probability", color=df.index,
             labels={"x": "Category", "Probability": "Percentage"},
             title="Environmental Attitude Distribution")
st.plotly_chart(fig)
