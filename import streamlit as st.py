import streamlit as st

# Define your questions
questions = [
    "Question 1: I am concerned about climate change.",
    "Question 2: Renewable energy should be prioritized over fossil fuels.",
    "Question 3: Governments should invest more in sustainability programs.",
    "Question 4: I actively take steps to reduce my environmental impact.",
    "Question 5: Plastic pollution is a serious issue that needs to be addressed.",
]

# Define response options
options = ["1 - Strongly Disagree", "2 - Disagree", "3 - Neutral", "4 - Agree", "5 - Strongly Agree"]

# Title of the app
st.title("Environmental Attitude Quiz")

# Collect responses
st.subheader("Please rate each statement on a scale from 1 to 5:")
responses = []
for i, question in enumerate(questions):
    response = st.radio(question, options, key=f"q{i}")
    responses.append(int(response[0]))  # Get numeric value (1-5)

# Submit button
if st.button("Submit"):
    total_score = sum(responses)
    avg_score = total_score / len(questions)

    # Classify attitude based on average score
    if avg_score >= 4:
        attitude = "Positive"
    elif avg_score >= 3:
        attitude = "Neutral"
    else:
        attitude = "Negative"

    st.success(f"Thank you for participating! Your overall attitude is: **{attitude}**.")

