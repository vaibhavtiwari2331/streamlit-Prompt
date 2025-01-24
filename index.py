# Step 1: Understand the User Context

# System Prompt: Initial Context Gathering
system_prompt = """
You are a travel itinerary planner. Your job is to ask the user specific questions to gather their preferences for a personalized travel itinerary. Focus on:
1. Destination (city or country).
2. Trip duration.
3. Budget (low, moderate, luxury).
4. Purpose (relaxation, adventure, sightseeing, etc.).
5. Preferences (specific activities, interests, or requirements).
Keep your questions simple and adaptable to any location.
"""

# Example User Prompt: Context Gathering
user_prompt_1 = "Hello! I need help planning a trip."

# Model Response Example 1
model_response_1 = "Sure! Let me ask a few questions to customize your itinerary. Where are you planning to travel?"

# Example User Input
user_input_1 = "I want to visit Italy for 5 days on a luxury budget. I enjoy history, wine, and scenic views."

# Step 2: Build Your Prompt System

# Input Refinement Prompt
system_prompt_refinement = """
Based on the user's input, refine additional details:
1. Dietary preferences (vegetarian, non-vegetarian, vegan, etc.).
2. Walking tolerance or mobility concerns.
3. Accommodation type (luxury, budget-friendly, central location, etc.).
4. Any specific attractions or activities they wish to include.
Generate responses dynamically based on the provided destination.
"""

# Example User Prompt for Refinement
user_prompt_2 = "I love history and scenic views. I prefer staying in luxurious accommodations and have no mobility concerns."

# Model Response Example 2
model_response_2 = "Great! Noted your preferences. Let's find top-rated historical landmarks, scenic spots, and luxury accommodations in Italy."

# Activity Suggestions
system_prompt_activities = """
Generate a list of top-rated activities and attractions in the specified destination. Include:
1. Famous landmarks aligned with user preferences.
2. Hidden gems or local experiences.
3. A mix of activities spread across the day, with time suggestions.
4. Group activities based on proximity for efficiency.
"""

# Example Final Prompt
final_prompt = """
Based on the refined inputs, generate a multi-day itinerary for the specified destination. Include:
- Day-by-day breakdown with timings.
- Suggested attractions and activities.
- Recommendations for meals and accommodations.
- Ensure activities align with user preferences and budget.
"""

# Step 3: Deliverables

# Example Input
example_input = {
    "destination": "Italy",
    "trip_duration": 5,
    "budget": "luxury",
    "purpose": "sightseeing",
    "preferences": {
        "interests": ["history", "wine", "scenic views"],
        "accommodation": "luxury",
        "mobility": "no concerns",
    }
}

# Example Output
example_output = """
Day 1: Rome
- Morning: Visit the Colosseum and Roman Forum.
- Afternoon: Lunch near Piazza Navona, then explore the Pantheon.
- Evening: Dinner in Trastevere.

Day 2: Rome to Florence
- Morning: Travel to Florence by train.
- Afternoon: Visit the Uffizi Gallery and Florence Cathedral.
- Evening: Wine tasting in a Tuscan vineyard.

Day 3: Tuscany Day Trip
- Morning: Explore Siena.
- Afternoon: Relax at a vineyard in Chianti.
- Evening: Return to Florence.

Day 4: Venice
- Morning: Travel to Venice. Visit St. Mark’s Basilica.
- Afternoon: Gondola ride and lunch at a canal-side restaurant.
- Evening: Relax in Piazza San Marco.

Day 5: Departure
- Morning: Leisure time in Venice.
- Afternoon: Depart for home.
"""

# Step 4: Hosting (With API Integration in Streamlit)

import openai
import streamlit as st

def call_openai_api(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: {e}"

def travel_itinerary_planner():
    st.title("AI Travel Itinerary Planner")

    st.header("Tell us about your trip")
    destination = st.text_input("Where are you planning to travel? (City or Country)")
    trip_duration = st.number_input("How many days is your trip?", min_value=1, max_value=30)
    budget = st.selectbox("What is your budget?", ["Low", "Moderate", "Luxury"])
    purpose = st.multiselect("What's the purpose of your trip?", ["Relaxation", "Adventure", "Sightseeing", "Cultural", "Food & Drinks"])
    interests = st.text_area("Any specific interests or preferences?")

    if st.button("Generate Itinerary"):
        if destination and trip_duration and budget:
            user_input = f"I want to visit {destination} for {trip_duration} days on a {budget} budget. My purpose is {', '.join(purpose)}. I am interested in {interests}."
            itinerary = call_openai_api(user_input)
            st.subheader(f"Your Personalized Itinerary for {destination}")
            st.write(itinerary)
        else:
            st.error("Please provide all the required details.")

if __name__ == "__main__":
    travel_itinerary_planner()
