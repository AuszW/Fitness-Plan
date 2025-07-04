import streamlit as st
import openai
import re

# Hide Streamlit's default menu and header
hide_streamlit_style = """
    <style>
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Set page config with minimal menu
st.set_page_config(
    page_title="FitnessApp",
    layout="centered",
    initial_sidebar_state="collapsed",
    menu_items={
        'About': None,
        'Get help': None,
        'Report a bug': None,
    }
)

# Load API key from Streamlit Secrets
try:
    openai.api_key = st.secrets["OPENAI_API_KEY"]
except KeyError:
    st.error("OpenAI API key not found in Streamlit secrets. Please add it in the Secrets manager.")
    st.stop()

st.title("💪 FitnessApp")
st.write("Get a custom workout plan in seconds. Just tell me what you need:")

# User Inputs
goal = st.selectbox("What's your goal?", ["Bulk", "Cut", "Recomposition"])
experience = st.selectbox("Your experience level:", ["Beginner", "Intermediate", "Advanced"])
days = st.slider("How many days per week can you train?", 1, 7, 4)
workout_type = st.selectbox("Preferred workout type:", ["Weights only", "Cardio focus", "Mixed", "Home workouts"])
injuries = st.text_input("Any injuries or limitations? (Leave blank if none)")
style = st.selectbox("Trainer style?", ["Motivational", "No BS", "Friendly coach"])

st.markdown("✅ **Screenshot your plan once it's generated to keep it!**")

if st.button("Generate My Plan"):
    with st.spinner("Creating your plan..."):
        prompt = f"""
        You are a personal trainer. Create a {days}-day gym workout plan for a {experience.lower()} lifter.
        The goal is to {goal.lower()}.
        The preferred workout type is {workout_type.lower()}.
        """

        if injuries:
            prompt += f" Avoid exercises that affect: {injuries}."
        if style == "Motivational":
            prompt += " Speak in an encouraging and uplifting tone."
        elif style == "No BS":
            prompt += " Be straight to the point and intense."
        else:
            prompt += " Use a friendly, informative tone."

        prompt += " Include exercises, sets, reps, and rest time. Format clearly by day."

        try:
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a skilled personal trainer who builds custom fitness plans."},
                    {"role": "user", "content": prompt}
                ]
            )
            plan = response.choices[0].message.content

            # Clean up formatting
            plan = plan.replace('<br>', '\n')
            clean_plan = re.sub(r'<[^>]+>', '', plan)

            st.subheader("📋 Your Custom Plan:")
            st.text_area("", clean_plan, height=700)
        except Exception as e:
            st.error(f"Something went wrong: {e}")
