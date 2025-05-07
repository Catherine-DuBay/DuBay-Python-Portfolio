# Import necessary functions.
import streamlit as st
import pandas as pd
import datetime

# Load dataset
def load_data():
    return pd.read_csv("StreamlitAppFinal/historical_events.csv", parse_dates=["Start Date", "End Date"])

# Initialize session state variables
if 'app_initialized' not in st.session_state:
    st.session_state.app_initialized = True
    st.session_state.correct_flags = [False] * 5
    st.session_state.correct_answers = [""] * 5
    st.session_state.last_submission_status = None
    st.session_state.correct_order = []
    st.session_state.last_week_number = None
    st.session_state.submitted = False  # Track if submission was made
    st.session_state.events_shuffled = None
    st.session_state.need_rerun = False # Flag to indicate we need to update UI
    st.session_state.scores_reset = False # Flag to track if scores were reset

    # Score tracking variables
    st.session_state.rounds_played = 0
    st.session_state.total_positions_attempted = 0 # Tracks total positions attempted
    st.session_state.total_positions_correct = 0 # Tracks total positions correct
    st.session_state.game_completed = False
    st.session_state.current_round_best_score = 0 # Best score for current round

# Label dataset, loading before callbacks so it is available
df = load_data()

# Function to check answers
def check_answers():
    user_order = [st.session_state.get(f"select_{i}") for i in range(5)]
    
    # Check if any "-" selections remain
    if "-" in user_order:
        st.session_state.warning_message = "Please select an event for each position."
        return
    
    st.session_state.submitted = True

    # Count new correct positions in this attempt (positions that were not correct before)
    new_correct_positions = 0
    positions_attempted = 0

    for i in range(5):
        # Only count positions that were not already correct
        if not st.session_state.correct_flags[i]:
            positions_attempted += 1
            if user_order[i] == st.session_state.correct_order[i]:
                new_correct_positions += 1
    
    # Update total positions attempted and correct
    st.session_state.total_positions_attempted += positions_attempted
    st.session_state.total_positions_correct += new_correct_positions

    # Update the best score for the current round if this attempt is better
    if new_correct_positions > st.session_state.current_round_best_score:
        st.session_state.current_round_best_score = new_correct_positions
    
    if user_order == st.session_state.correct_order:
        st.session_state.correct_flags = [True] * 5
        st.session_state.correct_answers = user_order.copy()
        st.session_state.last_submission_status = "correct"

        # If this is a new game completion (not already marked as completed)
        if not st.session_state.game_completed:
            st.session_state.rounds_played += 1
            st.session_state.game_completed = True

    else:
        # First set status to incorrect
        st.session_state.last_submission_status = "incorrect"
        # Check individual positions
        for i in range(5):
            if user_order[i] == st.session_state.correct_order[i]:
                st.session_state.correct_flags[i] = True
                st.session_state.correct_answers[i] = user_order[i]

        # Check if all positions are now correct (this might happen over multiple submissions)
        if all(st.session_state.correct_flags):
            st.session_state.last_submission_status = "correct"

            # If this is a new game completion (not already marked as completed)
            if not st.session_state.game_completed:
                st.session_state.rounds_played += 1
                st.session_state.game_completed = True

# Function to reset game
def reset_game():
    week_number = st.session_state.last_week_number
    if week_number is not None:
        events_this_week = df[df['Week'] == week_number][['Event', 'Year']]
        st.session_state.events_shuffled = events_this_week.sample(frac=1).reset_index(drop=True)
        st.session_state.correct_flags = [False] * 5
        st.session_state.correct_answers = [""] * 5
        st.session_state.last_submission_status = None
        st.session_state.submitted = False
        st.session_state.game_completed = False # Reset game completion flag
        st.session_state.current_round_best_score = 0 # Reset best score for new round
        # Update correct order when resetting
        st.session_state.correct_order = st.session_state.events_shuffled.sort_values(by='Year')['Event'].tolist()
        for i in range(5):
            st.session_state[f"select_{i}"] = '-'

# Function to reset scores
def reset_scores():
    st.session_state.rounds_played = 0
    st.session_state.total_positions_attempted = 0
    st.session_state.total_positions_correct = 0
    st.session_state.current_round_best_score = 0
    # Add a flag to indicate scores were reset
    st.session_state.scores_reset = True

# Title of the app
st.title("Timeline 🕰️")

# Description of the app
st.markdown("""
🕰️ **Welcome to Timeline: The Historical Event Challenge!**

Ever wish you could travel back in time? Now you can—sort of.  
Choose any week of the year, and we'll drop you into a moment in history with **five real events** that happened during that week... across different years.

Your mission:  
🔍 **Put the events in chronological order** based on the year they occurred.

🎯 Get it right, and you'll reveal the secret year for each event.  
💡 Not quite there? You can keep guessing until you nail the full timeline!

📊 Your accuracy and progress are tracked in the sidebar.  
See how many rounds you can complete—and how sharp your historical instincts really are.
""")

# Display score statistics in a sidebar
st.sidebar.title("Your Overall Score")

# Calculate accuracy based on total positions correct vs. positions attempted
accuracy = 0
if st.session_state.total_positions_attempted > 0:
    accuracy = (st.session_state.total_positions_correct / st.session_state.total_positions_attempted) * 100

# For current round, show progress
current_round_accuracy = 0
if st.session_state.current_round_best_score > 0:
    current_round_accuracy = (st.session_state.current_round_best_score / 5) * 100

st.sidebar.metric("Overall Accuracy", f"{accuracy:.1f}%")
st.sidebar.metric("Current Round Best", f"{current_round_accuracy:.1f}%")
st.sidebar.metric("Total Correct Positions", st.session_state.total_positions_correct)
st.sidebar.metric("Total Positions Attempted", st.session_state.total_positions_attempted)

# Add reset scores button with the dedicated function
if st.sidebar.button("Reset All Scores") or st.session_state.scores_reset:
    reset_scores()
<<<<<<< HEAD
    
# Check if scores were reset and display confirmation message
if hasattr(st.session_state, 'scores_reset') and st.session_state.scores_reset:
    st.sidebar.success("Scores have been reset successfully!")
    # Reset the flag so the message doesn't show again on next rerun
    st.session_state.scores_reset = False
=======
    # If scores were reset, show a confirmation message
    if st.session_state.scores_reset:
        st.sidebar.success("Scores have been reset successfully!")
        # Reset the flag so the message doesn't show again on next rerun
        st.session_state.scores_reset = False
>>>>>>> b3dc71fb524d5f340ab6216cc165ad4747ca961c

# Step 1: Date Input
# Get current date to use as default
today = datetime.date.today()

# Create date input but only care about month and day
selected_date_full = st.date_input("Choose a date! You will travel back in time to that week.")

# Extract just the month and day, then create a date object with a constant year (2000 is a leap year)
month = selected_date_full.month
day = selected_date_full.day
selected_date = datetime.date(2000, month, day) # Using 2000 as it's a leap year (handles Feb 29)

# Step 2: Find the week that matches selected date
# Convert selected date to month-day string for comparison
selected_md = f"{selected_date.month:02d}-{selected_date.day:02d}"

# Find rows where month-day part matches
# First, extract month-day from the Start Date and End Date in the dataframe
df['Start_MD'] = df['Start Date'].dt.strftime('%m-%d')
df['End_MD'] = df['End Date'].dt.strftime('%m-%d')

# Find the week that contains the selected month-day
week_row = df[(df['Start_MD'] <= selected_md) & (df['End_MD'] >= selected_md)]
              
# Special handling for year wrap (e.g., week spans Dec 30 - Jan 5)
if week_row.empty:
    # Check for week spanning year end (Dec) to year start (Jan)
    dec_to_jan_weeks = df[(df['Start_MD'] > df['End_MD'])] # Weeks that cross the year boundary
    for _, row in dec_to_jan_weeks.iterrows():
        # Check if date is after start month-day (e.g., Dec 29) or before end month-day (e.g., Jan 4)
        if selected_md >= row['Start_MD'] or selected_md <= row['End_MD']:
            week_row = pd.DataFrame([row])
            break

if selected_date and not week_row.empty:
    # Step 3: Get the week number 
    week_number = week_row.iloc[0]['Week']
    st.subheader(f"You're looking at Week #{int(week_number)} of the year.")

    # Step 4: Reset session state if new week
    if st.session_state.last_week_number != week_number:
        # Check if previous game was started but not completed - we do not count it
        if st.session_state.last_week_number is not None and not st.session_state.game_completed and st.session_state.submitted:
            # Reset score tracking for incomplete game
            if 'total_attempts' in st.session_state:  # Added safety check
                st.session_state.total_attempts -= sum(1 for flag in st.session_state.correct_flags if flag)

        st.session_state.last_week_number = week_number
        events_this_week = df[df['Week'] == week_number][['Event', 'Year']]
        st.session_state.events_shuffled = events_this_week.sample(frac=1).reset_index(drop=True)
        st.session_state.correct_flags = [False] * 5
        st.session_state.last_submission_status = None
        st.session_state.submitted = False
        st.session_state.game_completed = False # Reset game completion flag
        for i in range(5):
            st.session_state[f"select_{i}"] = '-'
        # Always update the correct order reference
        st.session_state.correct_order = st.session_state.events_shuffled.sort_values(by='Year')['Event'].tolist()

    # Step 5: Prepare data
    events_shuffled = st.session_state.events_shuffled
    if events_shuffled is not None: # Add safety check
        events_list = events_shuffled['Event'].tolist()
    
        st.subheader("Order these events chronologically by year:")

        # Step 6: Display selections
        for i in range(5):
            if st.session_state.correct_flags[i]:
                correct_event = st.session_state.correct_answers[i]

                # Find the corresponding year from the shuffled dataset
                event_match = st.session_state.events_shuffled[
                    st.session_state.events_shuffled['Event'].str.strip() == correct_event.strip()
                ]

                if not event_match.empty:
                    event_year = event_match.iloc[0]['Year']
                else: 
                    event_year = "Unknown"

                st.markdown(
                    f"""
                    <div style="
                        background-color: #d4edda;
                        padding: 10px;
                        border-radius: 8px;
                        border: 1px solid #c3e6cb;
                        color: black;
                        font-weight: bold;
                        box-shadow: 0 0 10px 2px #a4e5af;
                    ">
                        ✅ <strong>Event #{i+1}:</strong> {correct_event} <span style="color: #28a745;">({event_year})</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                # Create a filtered list excluding events that are already correct
                available_events = [event for event in events_list if event not in st.session_state.correct_answers]
                
                current_value = st.session_state.get(f"select_{i}", "-")

                # If current selected value is not in available events (but not "-", add it back temporarily)
                if current_value != "-" and current_value not in available_events:
                    available_events.append(current_value)

                # Sort the available events to maintain consistent order
                available_events.sort(key = lambda x: events_list.index(x) if x in events_list else 999)

                # Add the dash option at the beginning
                options = ["-"] + available_events

                # Calculate the index for the current value
                if current_value == "-":
                    index = 0
                else:
                    index = options.index(current_value)

                st.selectbox(
                    f"Event #{i+1}:",
                    options, # Use the filtered options list we created
                    index=index, # Use the calculated index
                    key=f"select_{i}",
                    disabled=False
                )

        # Step 7: Submit guess and check
        st.button("Submit Guess", on_click=check_answers)
    
        # Display appropriate messages based on submission status
        if 'warning_message' in st.session_state and st.session_state.warning_message:
            st.warning(st.session_state.warning_message)
            st.session_state.warning_message = None # Clear the message after showing
        elif st.session_state.submitted:
            if st.session_state.last_submission_status == "correct":
                st.success("🎉 Correct! You nailed the order!")
            elif st.session_state.last_submission_status == "incorrect":
                st.warning("❌ Not quite. Try again!")

        # Step 8: Reset button
        st.button("Reset Game", on_click=reset_game)

    else: st.error("Error loading events. Please try selecting a different date.")

else:
    st.warning("No events found for that date. Try a different one.")
