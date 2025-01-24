import openai
import streamlit as st

# Access your OpenAI API key securely from Streamlit's Secrets
openai_api_key = st.secrets["openai_api_key"]

# Set the OpenAI API key
openai.api_key = openai_api_key

# Function to handle user input and make API requests
def generate_itinerary(user_input):
    # Initial system message to provide context to GPT-3 about the task
    system_prompt = """
    You are an AI travel planner. Your task is to generate a personalized travel itinerary based on user input. 
    The user provides their destination, budget, preferences, and trip duration. Generate a 7-day detailed itinerary considering the following:
    1. The user's budget (low, moderate, high).
    2. Their interests (e.g., culture, sightseeing, relaxation, local experiences).
    3. Dietary preferences (e.g., vegetarian, vegan, gluten-free).
    4. Trip duration and mobility concerns (e.g., moderate walking).
    5. Suggest a mix of famous and off-the-beaten-path locations.
    """

    # Constructing the prompt for OpenAI API
    prompt = f"""
    User input: {user_input}
    Based on the provided details, generate a detailed 7-day itinerary. Ensure to:
    - Keep the budget in mind: moderate budget.
    - Focus on cultural exploration, sightseeing, and local experiences.
    - Include vegetarian-friendly options.
    - Provide a mix of well-known and hidden spots for each day.
    """

    # Making a request to the OpenAI API to generate the itinerary
    response = openai.Completion.create(
        engine="text-davinci-003",  # You can use other engines depending on your needs
        prompt=system_prompt + prompt,
        max_tokens=1000,  # Adjust the number of tokens based on expected response length
        temperature=0.7,  # Adjust temperature for creativity and variability
        n=1,  # Only one response
        stop=None  # Stop sequence for controlling output
    )

    # Extract the generated itinerary
    itinerary = response.choices[0].text.strip()
    return itinerary

# Streamlit UI for user input
st.title("AI Travel Itinerary Generator")
st.write("Welcome to the personalized AI travel planner. Please provide your travel details below:")

# Input fields for user preferences
destination = st.text_input("Enter your destination (e.g., Paris):")
budget = st.selectbox("Select your budget", ["Low", "Moderate", "High"])
duration = st.slider("Select your trip duration (days)", 1, 14, 7)  # Default 7 days
preferences = st.text_area("Tell us about your travel preferences (e.g., sightseeing, cultural, relaxing, vegetarian, etc.):")

# Button to generate the itinerary
if st.button("Generate Itinerary"):
    if not destination or not preferences:
        st.error("Please provide both destination and preferences.")
    else:
        # Forming user input based on fields
        user_input = f"Destination: {destination}, Budget: {budget}, Duration: {duration} days, Preferences: {preferences}"

        # Generating the itinerary
        itinerary = generate_itinerary(user_input)

        # Displaying the generated itinerary
        st.write("Here is your personalized travel itinerary:")
        st.write(itinerary)
