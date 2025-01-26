import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import qrcode
from io import BytesIO

# Set up session state to store participant results
if "participants" not in st.session_state:
    st.session_state.participants = []

# QR code to reach the app
st.title("Interactive Quiz Game")
st.markdown("**Scan the QR code below to access the quiz on your phone:**")
qr_link = "https://your-app-url.streamlit.app/"  # Replace with your actual Streamlit app URL
qr_img = qrcode.make(qr_link)
buffer = BytesIO()
qr_img.save(buffer)
st.image(buffer.getvalue(), caption="Scan this QR Code")

# Participant Information
name = st.text_input("Enter your name to start:", "")

if name:
    st.subheader(f"Hello, {name}! Answer the questions below:")

    # Questions with Likert scale
    st.markdown("### Questions:")
    q1 = st.slider("Question 1: Your opinion on X?", 1, 5, 3)
    q2 = st.slider("Question 2: Your stance on Y?", 1, 5, 3)
    q3 = st.slider("Question 3: How do you feel about Z?", 1, 5, 3)

    # Calculate attitude scores
    denial_score = (6 - q1) * 0.5 + q2 * 0.3
    liberal_score = q1 * 0.4 + (6 - q3) * 0.6
    leftist_score = q3 * 0.8 + q2 * 0.2
    total = denial_score + liberal_score + leftist_score

    # Normalize to percentages
    denial_percent = (denial_score / total) * 100
    liberal_percent = (liberal_score / total) * 100
    leftist_percent = (leftist_score / total) * 100

    if st.button("Submit"):
        # Save this participant's results
        st.session_state.participants.append({
            "name": name,
            "denial": denial_percent,
            "liberal": liberal_percent,
            "leftist": leftist_percent
        })

# Display all results (only after at least one participant has completed)
if st.session_state.participants:
    st.subheader("Results for All Participants:")
    for participant in st.session_state.participants:
        st.markdown(f"### {participant['name']}'s Results:")
        
        # Create bar chart
        categories = ["Denial", "Liberal", "Leftist"]
        percentages = [participant["denial"], participant["liberal"], participant["leftist"]]

        fig, ax = plt.subplots()
        ax.bar(categories, percentages, color=["red", "blue", "green"])
        ax.set_ylabel("Percentage")
        ax.set_title(f"{participant['name']}'s Attitude Breakdown")
        st.pyplot(fig)

        # Show percentages in a table
        df = pd.DataFrame({
            "Category": categories,
            "Percentage": percentages
        })
        st.table(df)
