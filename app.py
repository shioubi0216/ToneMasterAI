import streamlit as st
import os
import random
from dotenv import load_dotenv
from modules.ai_service import AIService
from modules.syllabary import JapaneseSyllabary
from modules.user_data import UserProgressManager
from modules.content_recommender import ContentRecommender
from modules.practice_manager import PracticeManager  # Import the new module

# Load environment variables
load_dotenv()

# App title and configuration
st.set_page_config(
    page_title="ToneMaster AI - Japanese Syllabary Learning",
    page_icon="🇯🇵",
    layout="wide"
)

# Initialize services
@st.cache_resource
def init_services():
    ai_service = AIService()
    syllabary = JapaneseSyllabary()
    user_manager = UserProgressManager()
    recommender = ContentRecommender(ai_service)
    practice_manager = PracticeManager()  # Initialize the practice manager
    return ai_service, syllabary, user_manager, recommender, practice_manager

ai_service, syllabary, user_manager, recommender, practice_manager = init_services()

# Sidebar menu
st.sidebar.title("ToneMaster AI")
page = st.sidebar.radio(
    "Navigation",
    ["Home", "Learn Hiragana", "Learn Katakana", "Practice", "Settings"]
)

# User interests for personalization
if "interests" not in st.session_state:
    st.session_state.interests = []

# Home page
if page == "Home":
    st.title("Welcome to ToneMaster AI")
    st.write("Learn Japanese syllabary through personalized AI-powered lessons.")
    
    # User interest collection
    if not st.session_state.interests:
        st.subheader("Let's personalize your learning experience")
        interest = st.text_input("What topics interest you? (e.g., anime, travel, food)")
        if st.button("Add Interest"):
            if interest:
                st.session_state.interests.append(interest)
                st.success(f"Added '{interest}' to your interests!")
                
    # Display current interests
    if st.session_state.interests:
        st.subheader("Your interests:")
        for i in st.session_state.interests:
            st.write(f"• {i}")
        
        # Generate personalized recommendation
        if st.button("Generate Personalized Learning Path"):
            with st.spinner("Creating your personalized learning experience..."):
                recommendation = recommender.generate_recommendation(st.session_state.interests)
                st.session_state.recommendation = recommendation
                
        if "recommendation" in st.session_state:
            st.subheader("Your Personalized Learning Path")
            st.write(st.session_state.recommendation)

# Syllabary learning pages
elif page in ["Learn Hiragana", "Learn Katakana"]:
    syllabary_type = "hiragana" if page == "Learn Hiragana" else "katakana"
    st.title(f"Learn {syllabary_type.capitalize()}")
    
    # Display syllabary chart
    st.subheader(f"{syllabary_type.capitalize()} Chart")
    chart = syllabary.get_chart(syllabary_type)
    st.table(chart)
    
    # Interactive learning
    st.subheader("Practice Section")
    character = syllabary.get_random_character(syllabary_type)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"## {character['symbol']}")
    
    with col2:
        user_answer = st.text_input("What is the pronunciation? (romaji)")
        if st.button("Check"):
            if user_answer.lower() == character['romaji'].lower():
                st.success("Correct! 🎉")
                user_manager.record_success(syllabary_type, character['symbol'])
            else:
                st.error(f"Not quite. The correct answer is '{character['romaji']}'")
                user_manager.record_mistake(syllabary_type, character['symbol'])

# Practice page
elif page == "Practice":
    st.title("Practice Your Skills")
      # Tabs for different difficulty levels
    difficulty_tabs = st.tabs(["Beginner", "Intermediate", "Advanced"])
      # Beginner tab
    with difficulty_tabs[0]:
        st.header("Beginner Level Practice")
        st.write("Perfect for those just starting to learn Japanese characters and basic vocabulary.")

        # Practice types for beginners (always available)
        beginner_activities = practice_manager.get_practice_activities("beginner")
        beginner_practice_type = st.selectbox(
            "Choose practice type:",
            beginner_activities,
            format_func=lambda x: {
                "kana_matching": "Match Hiragana & Katakana",
                "simple_vocabulary": "Basic Word Practice"
            }.get(x, x.replace("_", " ").title())
        )

        # --- Kana Matching Practice ---
        if beginner_practice_type == "kana_matching":
            # State management for kana matching
            if 'kana_matching_exercise' not in st.session_state:
                st.session_state.kana_matching_exercise = None
            if 'kana_matching_answered' not in st.session_state:
                st.session_state.kana_matching_answered = False
            if 'kana_matching_correct' not in st.session_state:
                st.session_state.kana_matching_correct = None
            if 'kana_matching_user_answer' not in st.session_state:
                st.session_state.kana_matching_user_answer = None
            if 'kana_matching_wrong_streak' not in st.session_state:
                st.session_state.kana_matching_wrong_streak = 0
            if 'kana_matching_right_streak' not in st.session_state:
                st.session_state.kana_matching_right_streak = 0
            if 'kana_matching_started' not in st.session_state:
                st.session_state.kana_matching_started = False

            def new_kana_matching_question():
                st.session_state.kana_matching_exercise = practice_manager.generate_exercise(
                    "kana_matching", "beginner", {"hiragana": syllabary.hiragana, "katakana": syllabary.katakana})
                st.session_state.kana_matching_answered = False
                st.session_state.kana_matching_correct = None
                st.session_state.kana_matching_user_answer = None

            # Show Start button first
            if not st.session_state.kana_matching_started:
                if st.button("Start Beginner Practice", key="kana_start"):
                    st.session_state.kana_matching_started = True
                    new_kana_matching_question()
                    st.rerun()
            else:
                # Show the exercise
                if st.session_state.kana_matching_exercise:
                    exercise = st.session_state.kana_matching_exercise
                    st.write(f"## {exercise['question']}")
                    
                    user_answer = st.radio(
                        "Select the matching katakana:", 
                        exercise['options'],
                        index=exercise['options'].index(st.session_state.kana_matching_user_answer) if st.session_state.kana_matching_user_answer in exercise['options'] else 0
                    )                    # Only show 'Check Answer' if the user hasn't answered yet
                    if not st.session_state.kana_matching_answered:
                        if st.button("Check Answer", key="matching_check"):
                            st.session_state.kana_matching_user_answer = user_answer
                            st.session_state.kana_matching_answered = True
                            if user_answer == exercise['answer']:
                                st.session_state.kana_matching_correct = True
                                st.session_state.kana_matching_right_streak += 1
                                st.session_state.kana_matching_wrong_streak = 0
                                user_manager.record_practice_result("beginner", "kana_matching", True, exercise['answer'])
                            else:
                                st.session_state.kana_matching_correct = False
                                st.session_state.kana_matching_wrong_streak += 1
                                st.session_state.kana_matching_right_streak = 0
                                user_manager.record_practice_result("beginner", "kana_matching", False, exercise['answer'])
                    
                    # Show feedback and action buttons after checking the answer
                    if st.session_state.kana_matching_answered:
                        if st.session_state.kana_matching_correct:
                            st.success("✅ Correct! 🎉 Great job!")
                            st.info(exercise['explanation'])
                            
                            # Show recommendation if 6 correct in a row
                            if st.session_state.kana_matching_right_streak >= 6:
                                st.info("🌟 You're on a roll! Try the 'Basic Word Practice' section for a new challenge.")
                            
                            # Only show Next Question for correct answers
                            if st.button("Next Question", key="matching_next"):
                                new_kana_matching_question()
                                st.rerun()
                        else:
                            st.error(f"❌ Not quite. The correct answer is '{exercise['answer']}'")
                            st.info(exercise['explanation'])
                            
                            # Show recommendation if 3 wrong in a row
                            if st.session_state.kana_matching_wrong_streak >= 3:
                                st.warning("🔎 Having trouble? Consider reviewing the 'Learn Hiragana' and 'Learn Katakana' pages before practicing again.")
                            
                            # Show both Try Again and Next Question for incorrect answers
                            col1, col2 = st.columns(2)
                            with col1:
                                if st.button("Try Again", key="matching_retry"):
                                    st.session_state.kana_matching_answered = False
                                    st.session_state.kana_matching_user_answer = None
                                    st.rerun()
                            with col2:
                                if st.button("Next Question", key="matching_next_any"):
                                    new_kana_matching_question()
                                    st.rerun()
        # --- End of Kana Matching Practice ---

        # --- Basic Word Practice (Simple Vocabulary) ---
        elif beginner_practice_type == "simple_vocabulary":
            # State management for simple vocabulary
            if 'simple_vocab_exercise' not in st.session_state:
                st.session_state.simple_vocab_exercise = None
            if 'simple_vocab_answered' not in st.session_state:
                st.session_state.simple_vocab_answered = False
            if 'simple_vocab_correct' not in st.session_state:
                st.session_state.simple_vocab_correct = None
            if 'simple_vocab_user_answer' not in st.session_state:
                st.session_state.simple_vocab_user_answer = None
            if 'simple_vocab_wrong_streak' not in st.session_state:
                st.session_state.simple_vocab_wrong_streak = 0
            if 'simple_vocab_right_streak' not in st.session_state:
                st.session_state.simple_vocab_right_streak = 0
            if 'simple_vocab_started' not in st.session_state:
                st.session_state.simple_vocab_started = False

            def new_simple_vocab_question():
                st.session_state.simple_vocab_exercise = practice_manager.generate_exercise("simple_vocabulary", "beginner")
                st.session_state.simple_vocab_answered = False
                st.session_state.simple_vocab_correct = None
                st.session_state.simple_vocab_user_answer = None

            # Show Start button first
            if not st.session_state.simple_vocab_started:
                if st.button("Start Beginner Practice", key="vocab_start"):
                    st.session_state.simple_vocab_started = True
                    new_simple_vocab_question()
                    st.rerun()
            else:
                # Show the exercise
                if st.session_state.simple_vocab_exercise:
                    exercise = st.session_state.simple_vocab_exercise
                    st.write(f"## {exercise['question']}")
                    
                    user_answer = st.radio(
                        "Select the meaning:", 
                        exercise['options'],
                        index=exercise['options'].index(st.session_state.simple_vocab_user_answer) if st.session_state.simple_vocab_user_answer in exercise['options'] else 0
                    )                    # Only show 'Check Answer' if the user hasn't answered yet
                    if not st.session_state.simple_vocab_answered:
                        if st.button("Check Answer", key="simple_vocab_check"):
                            st.session_state.simple_vocab_user_answer = user_answer
                            st.session_state.simple_vocab_answered = True
                            if user_answer == exercise['answer']:
                                st.session_state.simple_vocab_correct = True
                                st.session_state.simple_vocab_right_streak += 1
                                st.session_state.simple_vocab_wrong_streak = 0
                                user_manager.record_practice_result("beginner", "simple_vocabulary", True, exercise['question'])
                            else:
                                st.session_state.simple_vocab_correct = False
                                st.session_state.simple_vocab_wrong_streak += 1
                                st.session_state.simple_vocab_right_streak = 0
                                user_manager.record_practice_result("beginner", "simple_vocabulary", False, exercise['question'])
                    
                    # Show feedback and action buttons after checking the answer
                    if st.session_state.simple_vocab_answered:
                        if st.session_state.simple_vocab_correct:
                            st.success("✅ Correct! 🎉 Great job!")
                            st.info(exercise['explanation'])
                            
                            # Show recommendation if 6 correct in a row - suggest intermediate level
                            if st.session_state.simple_vocab_right_streak >= 6:
                                st.info("🌟 Excellent! You're ready for intermediate level practice. Try switching to the 'Intermediate' tab!")
                            
                            # Only show Next Question for correct answers
                            if st.button("Next Question", key="vocab_next"):
                                new_simple_vocab_question()
                                st.rerun()
                        else:
                            st.error(f"❌ Not quite. The correct answer is '{exercise['answer']}'")
                            st.info(exercise['explanation'])
                            
                            # Show recommendation if 3 wrong in a row
                            if st.session_state.simple_vocab_wrong_streak >= 3:
                                st.warning("🔎 Having trouble? Consider reviewing basic vocabulary or try the 'Match Hiragana & Katakana' practice first.")
                            
                            # Show both Try Again and Next Question for incorrect answers
                            col1, col2 = st.columns(2)
                            with col1:
                                if st.button("Try Again", key="vocab_retry"):
                                    st.session_state.simple_vocab_answered = False
                                    st.session_state.simple_vocab_user_answer = None
                                    st.rerun()
                            with col2:
                                if st.button("Next Question", key="vocab_next_any"):
                                    new_simple_vocab_question()
                                    st.rerun()
        # --- End of Basic Word Practice ---
                    
                    # Show feedback and action buttons after checking the answer
                    if st.session_state.simple_vocab_answered:
                        if st.session_state.simple_vocab_correct:
                            st.success("✅ Correct! 🎉 Great job!")
                            st.info(exercise['explanation'])
                            
                            # Show recommendation if 6 correct in a row
                            if st.session_state.simple_vocab_right_streak >= 6:
                                st.info("🌟 You're doing great! You can try the 'Match Hiragana & Katakana' section for more practice.")
                            
                            # Only show Next Question for correct answers
                            if st.button("Next Question", key="vocab_next"):
                                new_simple_vocab_question()
                                st.rerun()
                        else:
                            st.error(f"❌ Not quite. The correct answer is '{exercise['answer']}'")
                            st.info(exercise['explanation'])
                            
                            # Show recommendation if 3 wrong in a row
                            if st.session_state.simple_vocab_wrong_streak >= 3:
                                st.warning("🔎 Having trouble? Consider reviewing the 'Learn Hiragana' and 'Learn Katakana' pages before practicing again.")
                            
                            # Show both Try Again and Next Question for incorrect answers
                            col1, col2 = st.columns(2)
                            with col1:
                                if st.button("Try Again", key="vocab_retry"):
                                    st.session_state.simple_vocab_answered = False
                                    st.session_state.simple_vocab_user_answer = None
                                    st.rerun()
                            with col2:
                                if st.button("Next Question", key="vocab_next_any"):
                                    new_simple_vocab_question()
                                    st.rerun()
        # --- End of Basic Word Practice ---
    # Intermediate tab
    with difficulty_tabs[1]:
        st.header("Intermediate Level Practice")
        st.write("For learners who have mastered the basics and are ready for more complex patterns.")
          # Add practice recommendations
        recommended_practice = user_manager.get_recommended_practice("intermediate")
        if recommended_practice:
            format_name = {
                "common_phrases": "Common Japanese Phrases",
                "vocabulary_categories": "Vocabulary by Category"
            }.get(recommended_practice, recommended_practice.replace("_", " ").title())
            
            st.info(f"💡 Recommended: Try '{format_name}' to improve your skills!")
        
        # Practice types for intermediate level
        intermediate_activities = practice_manager.get_practice_activities("intermediate")
        intermediate_practice_type = st.selectbox(
            "Choose practice type:",
            intermediate_activities,
            format_func=lambda x: {
                "common_phrases": "Common Japanese Phrases",
                "vocabulary_categories": "Vocabulary by Category"
            }.get(x, x.replace("_", " ").title())
        )
          # Start practice session button
        if st.button("Start Intermediate Practice"):
            if intermediate_practice_type == "vocabulary_categories":
                exercise = practice_manager.generate_exercise("vocabulary_categories", "intermediate")
                
                st.write(f"## {exercise['question']}")
                
                # For multiple answer exercises
                if exercise.get('multiple_answers', False):
                    selected_options = []
                    for option in exercise['options']:
                        if st.checkbox(option, key=f"option_{option}"):
                            selected_options.append(option)
                    
                    if st.button("Check Answers", key="categories_check"):
                        if set(selected_options) == set(exercise['answers']):
                            st.success("All correct! 🎉")
                            st.session_state.last_result = True
                            # Record successful practice result
                            user_manager.record_practice_result("intermediate", "vocabulary_categories", True, exercise['question'])
                        else:
                            st.error(f"Not quite. The correct answers are: {', '.join(exercise['answers'])}")
                            st.session_state.last_result = False
                            # Record unsuccessful practice result
                            user_manager.record_practice_result("intermediate", "vocabulary_categories", False, exercise['question'])
                        st.info(exercise['explanation'])
                        
            elif intermediate_practice_type == "common_phrases":
                # Choose a random phrase
                phrase, meaning = random.choice(list(practice_manager.common_phrases.items()))
                
                # Create a listening exercise (simulated)
                st.write("## Listen to the phrase and select its meaning")
                st.write(f"Phrase: {phrase}")
                
                # Create options (1 correct + 3 random)
                options = [meaning]
                other_meanings = [m for m in practice_manager.common_phrases.values() if m != meaning]
                options.extend(random.sample(other_meanings, min(3, len(other_meanings))))
                random.shuffle(options)
                
                user_answer = st.radio("Select the meaning:", options)
                
                if st.button("Check Answer", key="phrases_check"):
                    if user_answer == meaning:
                        st.success("Correct! 🎉")
                        st.session_state.last_result = True
                        # Record successful practice result
                        user_manager.record_practice_result("intermediate", "common_phrases", True, phrase)
                    else:
                        st.error(f"Not quite. The correct answer is '{meaning}'")
                        st.session_state.last_result = False
                        # Record unsuccessful practice result
                        user_manager.record_practice_result("intermediate", "common_phrases", False, phrase)
      # Advanced tab
    with difficulty_tabs[2]:
        st.header("Advanced Level Practice")
        st.write("Challenge yourself with advanced Japanese exercises.")

        # 取得可用練習類型
        advanced_activities = practice_manager.get_practice_activities("advanced")
        advanced_practice_type = st.selectbox(
            "Choose practice type:",
            advanced_activities,
            format_func=lambda x: {
                "sentence_creation": "Create Sentences",
                "grammar_application": "Grammar Usage",
                "dialogue_comprehension": "Dialogue Comprehension"
            }.get(x, x.replace("_", " ").title())
        )

        if st.button("Start Advanced Practice"):
            if advanced_practice_type == "sentence_creation":
                exercise = practice_manager.generate_sentence_creation_exercise()
                st.write(f"### Scenario: {exercise['scenario']}")
                st.write(f"**Vocabulary to use:** {', '.join(exercise['vocabulary'])}")
                user_sentence = st.text_area("Write your sentence in Japanese:")
                if st.button("Check Sentence", key="sentence_creation_check"):
                    if user_sentence.strip():
                        st.success("Thank you for your answer! Here's an example:")
                        st.info(f"Example: {exercise['example']}")
                        st.info(f"Translation: {exercise['translation']}")
                        st.session_state.last_result = True
                        user_manager.record_practice_result("advanced", "sentence_creation", True, user_sentence)
                    else:
                        st.error("Please enter a sentence.")
                        st.session_state.last_result = False
                        user_manager.record_practice_result("advanced", "sentence_creation", False, user_sentence)
            elif advanced_practice_type == "grammar_application":
                exercise = practice_manager.generate_grammar_exercise()
                st.write(f"### {exercise['question']}")
                user_answer = st.radio("Select the correct answer:", exercise['options'])
                if st.button("Check Answer", key="grammar_check"):
                    if user_answer == exercise['answer']:
                        st.success("Correct! 🎉")
                        st.session_state.last_result = True
                        user_manager.record_practice_result("advanced", "grammar_application", True, exercise['question'])
                    else:
                        st.error(f"Not quite. The correct answer is '{exercise['answer']}'")
                        st.session_state.last_result = False
                        user_manager.record_practice_result("advanced", "grammar_application", False, exercise['question'])
                    st.info(exercise['explanation'])
            elif advanced_practice_type == "dialogue_comprehension":
                exercise = practice_manager.generate_dialogue_comprehension()
                st.write("### Dialogue:")
                for line in exercise['dialogue']:
                    st.write(f"**{line['speaker']}:** {line['text']}")
                st.write(f"**Question:** {exercise['question']}")
                user_answer = st.radio("Select the correct answer:", exercise['options'])
                if st.button("Check Answer", key="dialogue_check"):
                    if user_answer == exercise['answer']:
                        st.success("Correct! 🎉")
                        st.session_state.last_result = True
                        user_manager.record_practice_result("advanced", "dialogue_comprehension", True, exercise['question'])
                    else:
                        st.error(f"Not quite. The correct answer is '{exercise['answer']}'")
                        st.session_state.last_result = False
                        user_manager.record_practice_result("advanced", "dialogue_comprehension", False, exercise['question'])
                    st.info(exercise['explanation'])
# Settings page
elif page == "Settings":
    st.title("Settings")
    
    # Practice Progress Dashboard
    st.subheader("Practice Progress Dashboard")
    practice_stats = user_manager.get_practice_stats()
    
    if practice_stats:
        # Create tabs for each difficulty level
        progress_tabs = st.tabs(["Beginner", "Intermediate", "Advanced"])
        
        # Prepare data for display
        for i, difficulty in enumerate(["beginner", "intermediate", "advanced"]):
            with progress_tabs[i]:
                if difficulty in practice_stats:
                    level_stats = practice_stats[difficulty]
                    if level_stats:
                        # Create a table of practice type statistics
                        data = []
                        for practice_type, stats in level_stats.items():                            # Format for display
                            display_name = {
                                "kana_matching": "Match Hiragana & Katakana",
                                "simple_vocabulary": "Basic Word Practice",
                                "common_phrases": "Common Japanese Phrases",
                                "vocabulary_categories": "Vocabulary by Category",
                                "sentence_creation": "Create Sentences"
                            }.get(practice_type, practice_type.replace("_", " ").title())
                            
                            # Calculate accuracy
                            total = stats["attempts"]
                            correct = stats["correct"]
                            accuracy = f"{int(correct/total * 100)}%" if total > 0 else "N/A"
                            
                            # Format last practiced time
                            last_practiced = "Never" if not stats["last_practiced"] else stats["last_practiced"].split("T")[0]
                            
                            data.append({
                                "Practice Type": display_name,
                                "Attempts": total,
                                "Correct": correct,
                                "Accuracy": accuracy,
                                "Last Practiced": last_practiced
                            })
                        
                        if data:
                            st.table(data)
                            
                            # Show streaks and achievements
                            st.subheader("Practice Suggestions")
                            
                            # Find least practiced activities
                            sorted_by_attempts = sorted(level_stats.items(), key=lambda x: x[1]["attempts"])
                            if sorted_by_attempts:
                                least_practiced = sorted_by_attempts[0][0]
                                display_name = {
                                    "kana_matching": "Match Hiragana & Katakana",
                                    "simple_vocabulary": "Basic Word Practice",
                                    "common_phrases": "Common Japanese Phrases",
                                    "vocabulary_categories": "Vocabulary by Category",
                                    "sentence_creation": "Create Sentences"
                                }.get(least_practiced, least_practiced.replace("_", " ").title())
                                st.info(f"💡 You should try practicing '{display_name}' more often")
                            
                            # Find activities with low accuracy
                            low_accuracy_activities = []
                            for practice_type, stats in level_stats.items():
                                if stats["attempts"] >= 5 and stats["correct"] / stats["attempts"] < 0.7:
                                    low_accuracy_activities.append(practice_type)
                            
                            if low_accuracy_activities:
                                practice_to_improve = random.choice(low_accuracy_activities)
                                display_name = practice_to_improve.replace("_", " ").title()
                                st.warning(f"📝 Focus on improving '{display_name}' - this is challenging for you")
                        else:
                            st.info(f"You haven't practiced any {difficulty} level exercises yet.")
                    else:
                        st.info(f"You haven't practiced any {difficulty} level exercises yet.")
                else:
                    st.info(f"You haven't practiced any {difficulty} level exercises yet.")
    else:
        st.info("Start practicing to see your progress tracked here!")
    
    # App settings
    st.subheader("Application Settings")
    theme = st.selectbox("Theme", ["Light", "Dark"])
    
    # Learning preferences
    st.subheader("Learning Preferences")
    daily_goal = st.slider("Daily learning goal (minutes)", 5, 60, 15)
    
    # Practice settings
    st.subheader("Practice Settings")
    practice_mode = st.selectbox(
        "Default Practice Mode",
        ["Regular", "Spaced Repetition", "Challenge Mode"]
    )
    
    # Audio settings
    st.subheader("Audio Settings")
    enable_audio = st.checkbox("Enable pronunciation audio", value=True)
    audio_volume = st.slider("Audio volume", 0, 100, 75)
    
    # Reset progress option
    st.subheader("Reset Progress")
    if st.button("Reset All Progress"):
        user_confirmation = st.text_input("Type 'reset' to confirm")
        if user_confirmation == "reset":
            user_manager.reset_progress()
            st.success("Progress has been reset!")

# Footer
st.markdown("---")
st.markdown("ToneMaster AI - Personalized Japanese Learning | Powered by Mistral AI")

