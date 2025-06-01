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
                            if st.button("Next Question", key="vocab_next_correct"):
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
                                if st.button("Next Question", key="vocab_next_incorrect"):
                                    new_simple_vocab_question()
                                    st.rerun()
        # --- End of Basic Word Practice ---
        
    # Intermediate tab
    with difficulty_tabs[1]:
        st.header("Intermediate Level Practice")
        st.write("For learners who have mastered the basics and are ready for more complex patterns.")
        
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

        # --- Common Phrases Practice ---
        if intermediate_practice_type == "common_phrases":
            # State management for common phrases
            if 'phrases_exercise' not in st.session_state:
                st.session_state.phrases_exercise = None
            if 'phrases_answered' not in st.session_state:
                st.session_state.phrases_answered = False
            if 'phrases_correct' not in st.session_state:
                st.session_state.phrases_correct = None
            if 'phrases_user_answer' not in st.session_state:
                st.session_state.phrases_user_answer = None
            if 'phrases_wrong_streak' not in st.session_state:
                st.session_state.phrases_wrong_streak = 0
            if 'phrases_right_streak' not in st.session_state:
                st.session_state.phrases_right_streak = 0
            if 'phrases_started' not in st.session_state:
                st.session_state.phrases_started = False

            def new_phrases_question():
                # Choose a random phrase
                phrase, meaning = random.choice(list(practice_manager.common_phrases.items()))
                
                # Create options (1 correct + 3 random)
                options = [meaning]
                other_meanings = [m for m in practice_manager.common_phrases.values() if m != meaning]
                options.extend(random.sample(other_meanings, min(3, len(other_meanings))))
                random.shuffle(options)
                
                st.session_state.phrases_exercise = {
                    "phrase": phrase,
                    "answer": meaning,
                    "options": options
                }
                st.session_state.phrases_answered = False
                st.session_state.phrases_correct = None
                st.session_state.phrases_user_answer = None

            # Show Start button first
            if not st.session_state.phrases_started:
                if st.button("Start Intermediate Practice", key="phrases_start"):
                    st.session_state.phrases_started = True
                    new_phrases_question()
                    st.rerun()
            else:
                # Show the exercise
                if st.session_state.phrases_exercise:
                    exercise = st.session_state.phrases_exercise
                    st.write("## Listen to the phrase and select its meaning")
                    st.write(f"**Phrase:** {exercise['phrase']}")
                    
                    user_answer = st.radio(
                        "Select the meaning:", 
                        exercise['options'],
                        index=exercise['options'].index(st.session_state.phrases_user_answer) if st.session_state.phrases_user_answer in exercise['options'] else 0
                    )

                    # Only show 'Check Answer' if the user hasn't answered yet
                    if not st.session_state.phrases_answered:
                        if st.button("Check Answer", key="phrases_check"):
                            st.session_state.phrases_user_answer = user_answer
                            st.session_state.phrases_answered = True
                            if user_answer == exercise['answer']:
                                st.session_state.phrases_correct = True
                                st.session_state.phrases_right_streak += 1
                                st.session_state.phrases_wrong_streak = 0
                                user_manager.record_practice_result("intermediate", "common_phrases", True, exercise['phrase'])
                            else:
                                st.session_state.phrases_correct = False
                                st.session_state.phrases_wrong_streak += 1
                                st.session_state.phrases_right_streak = 0
                                user_manager.record_practice_result("intermediate", "common_phrases", False, exercise['phrase'])
                    
                    # Show feedback and action buttons after checking the answer
                    if st.session_state.phrases_answered:
                        if st.session_state.phrases_correct:
                            st.success("✅ Correct! 🎉 Great job!")
                            st.info(f"'{exercise['phrase']}' means '{exercise['answer']}'")
                            
                            # Show recommendation if 6 correct in a row
                            if st.session_state.phrases_right_streak >= 6:
                                st.info("🌟 Excellent! You're mastering common phrases. Try the 'Vocabulary by Category' or move to Advanced level!")
                            
                            # Only show Next Question for correct answers
                            if st.button("Next Question", key="phrases_next"):
                                new_phrases_question()
                                st.rerun()
                        else:
                            st.error(f"❌ Not quite. The correct answer is '{exercise['answer']}'")
                            st.info(f"'{exercise['phrase']}' means '{exercise['answer']}'")
                            
                            # Show recommendation if 3 wrong in a row
                            if st.session_state.phrases_wrong_streak >= 3:
                                st.warning("🔎 Having trouble? Consider reviewing basic phrases or try the 'Vocabulary by Category' practice.")
                            
                            # Show both Try Again and Next Question for incorrect answers
                            col1, col2 = st.columns(2)
                            with col1:
                                if st.button("Try Again", key="phrases_retry"):
                                    st.session_state.phrases_answered = False
                                    st.session_state.phrases_user_answer = None
                                    st.rerun()
                            with col2:
                                if st.button("Next Question", key="phrases_next_any"):
                                    new_phrases_question()
                                    st.rerun()
        # --- End of Common Phrases Practice ---

        # --- Vocabulary Categories Practice ---
        elif intermediate_practice_type == "vocabulary_categories":
            # State management for vocabulary categories
            if 'vocab_cat_exercise' not in st.session_state:
                st.session_state.vocab_cat_exercise = None
            if 'vocab_cat_answered' not in st.session_state:
                st.session_state.vocab_cat_answered = False
            if 'vocab_cat_correct' not in st.session_state:
                st.session_state.vocab_cat_correct = None
            if 'vocab_cat_selected' not in st.session_state:
                st.session_state.vocab_cat_selected = []
            if 'vocab_cat_wrong_streak' not in st.session_state:
                st.session_state.vocab_cat_wrong_streak = 0
            if 'vocab_cat_right_streak' not in st.session_state:
                st.session_state.vocab_cat_right_streak = 0
            if 'vocab_cat_started' not in st.session_state:
                st.session_state.vocab_cat_started = False

            def new_vocab_cat_question():
                st.session_state.vocab_cat_exercise = practice_manager.generate_exercise("vocabulary_categories", "intermediate")
                st.session_state.vocab_cat_answered = False
                st.session_state.vocab_cat_correct = None
                st.session_state.vocab_cat_selected = []

            # Show Start button first
            if not st.session_state.vocab_cat_started:
                if st.button("Start Intermediate Practice", key="vocab_cat_start"):
                    st.session_state.vocab_cat_started = True
                    new_vocab_cat_question()
                    st.rerun()
            else:
                # Show the exercise
                if st.session_state.vocab_cat_exercise:
                    exercise = st.session_state.vocab_cat_exercise
                    st.write(f"## {exercise['question']}")
                    
                    # For multiple answer exercises
                    if exercise.get('multiple_answers', False):
                        # Reset selected options if starting fresh
                        if not st.session_state.vocab_cat_answered and not st.session_state.vocab_cat_selected:
                            st.session_state.vocab_cat_selected = []
                        
                        # Show checkboxes for multiple selection
                        selected_options = []
                        for i, option in enumerate(exercise['options']):
                            if st.checkbox(option, key=f"vocab_cat_option_{i}", value=option in st.session_state.vocab_cat_selected):
                                selected_options.append(option)
                        
                        st.session_state.vocab_cat_selected = selected_options

                        # Only show 'Check Answers' if the user hasn't answered yet
                        if not st.session_state.vocab_cat_answered:
                            if st.button("Check Answers", key="vocab_cat_check"):
                                st.session_state.vocab_cat_answered = True
                                if set(selected_options) == set(exercise['answers']):
                                    st.session_state.vocab_cat_correct = True
                                    st.session_state.vocab_cat_right_streak += 1
                                    st.session_state.vocab_cat_wrong_streak = 0
                                    user_manager.record_practice_result("intermediate", "vocabulary_categories", True, exercise['question'])
                                else:
                                    st.session_state.vocab_cat_correct = False
                                    st.session_state.vocab_cat_wrong_streak += 1
                                    st.session_state.vocab_cat_right_streak = 0
                                    user_manager.record_practice_result("intermediate", "vocabulary_categories", False, exercise['question'])
                    
                    # Show feedback and action buttons after checking the answer
                    if st.session_state.vocab_cat_answered:
                        if st.session_state.vocab_cat_correct:
                            st.success("✅ All correct! 🎉 Great job!")
                            st.info(exercise['explanation'])
                            
                            # Show recommendation if 6 correct in a row
                            if st.session_state.vocab_cat_right_streak >= 6:
                                st.info("🌟 Amazing! You're mastering vocabulary categories. Ready for Advanced level practice!")
                            
                            # Only show Next Question for correct answers
                            if st.button("Next Question", key="vocab_cat_next"):
                                new_vocab_cat_question()
                                st.rerun()
                        else:
                            st.error(f"❌ Not quite. The correct answers are: {', '.join(exercise['answers'])}")
                            st.info(exercise['explanation'])
                            
                            # Show recommendation if 3 wrong in a row
                            if st.session_state.vocab_cat_wrong_streak >= 3:
                                st.warning("🔎 Having trouble? Consider reviewing vocabulary categories or try the 'Common Japanese Phrases' practice.")
                            
                            # Show both Try Again and Next Question for incorrect answers
                            col1, col2 = st.columns(2)
                            with col1:
                                if st.button("Try Again", key="vocab_cat_retry"):
                                    st.session_state.vocab_cat_answered = False
                                    st.session_state.vocab_cat_selected = []
                                    st.rerun()
                            with col2:
                                if st.button("Next Question", key="vocab_cat_next_any"):
                                    new_vocab_cat_question()
                                    st.rerun()
        # --- End of Vocabulary Categories Practice ---
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
                "translation_practice": "Translation Practice",
                "grammar_application": "Grammar Usage",
                "dialogue_comprehension": "Dialogue Comprehension"            }.get(x, x.replace("_", " ").title())
        )
          # --- Translation Practice with State Management ---
        if advanced_practice_type == "translation_practice":
            # State management for translation practice
            if 'translation_exercise' not in st.session_state:
                st.session_state.translation_exercise = None
            if 'translation_answered' not in st.session_state:
                st.session_state.translation_answered = False
            if 'translation_correct' not in st.session_state:
                st.session_state.translation_correct = None
            if 'translation_user_answer' not in st.session_state:
                st.session_state.translation_user_answer = ""
            if 'translation_wrong_streak' not in st.session_state:
                st.session_state.translation_wrong_streak = 0
            if 'translation_right_streak' not in st.session_state:
                st.session_state.translation_right_streak = 0
            if 'translation_started' not in st.session_state:
                st.session_state.translation_started = False
            if 'translation_evaluation' not in st.session_state:
                st.session_state.translation_evaluation = None

            def new_translation_question():
                st.session_state.translation_exercise = practice_manager.generate_translation_exercise()
                st.session_state.translation_answered = False
                st.session_state.translation_correct = None
                st.session_state.translation_user_answer = ""
                st.session_state.translation_evaluation = None

            # Show Start button first
            if not st.session_state.translation_started:
                if st.button("Start Translation Practice", key="translation_start"):
                    st.session_state.translation_started = True
                    new_translation_question()
                    st.rerun()
            else:
                # Show the exercise
                if st.session_state.translation_exercise:
                    exercise = st.session_state.translation_exercise
                    st.write(f"### Translate this Japanese sentence to English:")
                    st.write(f"**Japanese:** {exercise['japanese']}")
                    
                    # Use session state for text area value
                    user_translation = st.text_area(
                        "Your English translation:",
                        value=st.session_state.translation_user_answer,
                        key="translation_input"
                    )
                    
                    # Update session state when user types
                    if user_translation != st.session_state.translation_user_answer:
                        st.session_state.translation_user_answer = user_translation

                    # Only show 'Check Translation' if the user hasn't answered yet
                    if not st.session_state.translation_answered:
                        if st.button("Check Translation", key="translation_check"):
                            if user_translation.strip():
                                # Use AI to evaluate the translation
                                evaluation = practice_manager.evaluate_user_translation(
                                    exercise['japanese'], 
                                    exercise['reference_english'], 
                                    user_translation
                                )
                                
                                st.session_state.translation_evaluation = evaluation
                                st.session_state.translation_answered = True
                                
                                if evaluation['is_correct']:
                                    st.session_state.translation_correct = True
                                    st.session_state.translation_right_streak += 1
                                    st.session_state.translation_wrong_streak = 0
                                    user_manager.record_practice_result("advanced", "translation_practice", True, user_translation)
                                else:
                                    st.session_state.translation_correct = False
                                    st.session_state.translation_wrong_streak += 1
                                    st.session_state.translation_right_streak = 0
                                    user_manager.record_practice_result("advanced", "translation_practice", False, user_translation)
                                st.rerun()
                            else:
                                st.error("Please enter a translation.")

                    # Show feedback and action buttons after checking the answer
                    if st.session_state.translation_answered and st.session_state.translation_evaluation:
                        evaluation = st.session_state.translation_evaluation
                        if st.session_state.translation_correct:
                            st.success(f"✅ {evaluation['result']}: {evaluation['explanation']}")
                            st.info(f"**Reference translation:** {exercise['reference_english']}")
                            
                            # Show recommendation if 6 correct in a row - suggest different practice
                            if st.session_state.translation_right_streak >= 6:
                                st.info("🌟 Excellent! You're mastering translation! Try switching to 'Grammar Usage' or 'Dialogue Comprehension' for more challenge!")
                            
                            # Only show Next Question for correct answers
                            if st.button("Next Question", key="translation_next_correct"):
                                new_translation_question()
                                st.rerun()
                        else:
                            st.error(f"❌ {evaluation['result']}: {evaluation['explanation']}")
                            st.info(f"**Reference translation:** {exercise['reference_english']}")
                            
                            # Show recommendation if 3 wrong in a row
                            if st.session_state.translation_wrong_streak >= 3:
                                st.warning("🔎 Having trouble with translations? Consider practicing vocabulary first or try starting with simpler sentences.")
                            
                            # Show both Try Again and Next Question for incorrect answers
                            col1, col2 = st.columns(2)
                            with col1:
                                if st.button("Try Again", key="translation_retry"):
                                    st.session_state.translation_answered = False
                                    st.session_state.translation_evaluation = None
                                    # Keep the user's text in the text area for retry
                                    st.rerun()
                            with col2:
                                if st.button("Next Question", key="translation_next_incorrect"):
                                    new_translation_question()
                                    st.rerun()        # --- End of Translation Practice ---
        elif advanced_practice_type == "grammar_application":
            # State management for grammar practice
            if 'grammar_exercise' not in st.session_state:
                st.session_state.grammar_exercise = None
            if 'grammar_answered' not in st.session_state:
                st.session_state.grammar_answered = False
            if 'grammar_correct' not in st.session_state:
                st.session_state.grammar_correct = None
            if 'grammar_user_answer' not in st.session_state:
                st.session_state.grammar_user_answer = None
            if 'grammar_wrong_streak' not in st.session_state:
                st.session_state.grammar_wrong_streak = 0
            if 'grammar_right_streak' not in st.session_state:
                st.session_state.grammar_right_streak = 0
            if 'grammar_started' not in st.session_state:
                st.session_state.grammar_started = False

            def new_grammar_question():
                st.session_state.grammar_exercise = practice_manager.generate_grammar_exercise()
                st.session_state.grammar_answered = False
                st.session_state.grammar_correct = None
                st.session_state.grammar_user_answer = None

            # Show Start button first
            if not st.session_state.grammar_started:
                if st.button("Start Grammar Practice", key="grammar_start"):
                    st.session_state.grammar_started = True
                    new_grammar_question()
                    st.rerun()
            else:
                # Show the exercise
                if st.session_state.grammar_exercise:
                    exercise = st.session_state.grammar_exercise
                    st.write(f"### {exercise['question']}")
                    
                    user_answer = st.radio(
                        "Select the correct answer:",
                        exercise['options'],
                        index=exercise['options'].index(st.session_state.grammar_user_answer) if st.session_state.grammar_user_answer in exercise['options'] else 0
                    )

                    # Only show 'Check Answer' if the user hasn't answered yet
                    if not st.session_state.grammar_answered:
                        if st.button("Check Answer", key="grammar_check"):
                            st.session_state.grammar_user_answer = user_answer
                            st.session_state.grammar_answered = True
                            if user_answer == exercise['answer']:
                                st.session_state.grammar_correct = True
                                st.session_state.grammar_right_streak += 1
                                st.session_state.grammar_wrong_streak = 0
                                user_manager.record_practice_result("advanced", "grammar_application", True, exercise['question'])
                            else:
                                st.session_state.grammar_correct = False
                                st.session_state.grammar_wrong_streak += 1
                                st.session_state.grammar_right_streak = 0
                                user_manager.record_practice_result("advanced", "grammar_application", False, exercise['question'])
                            st.rerun()

                    # Show feedback and action buttons after checking the answer
                    if st.session_state.grammar_answered:
                        if st.session_state.grammar_correct:
                            st.success("✅ Correct! 🎉 Great job!")
                            st.info(exercise['explanation'])
                            
                            # Show recommendation if 6 correct in a row
                            if st.session_state.grammar_right_streak >= 6:
                                st.info("🌟 Excellent! You're mastering grammar! Try switching to 'Translation Practice' or 'Dialogue Comprehension' for more challenge!")
                            
                            # Only show Next Question for correct answers
                            if st.button("Next Question", key="grammar_next_correct"):
                                new_grammar_question()
                                st.rerun()
                        else:
                            st.error(f"❌ Not quite. The correct answer is '{exercise['answer']}'")
                            st.info(exercise['explanation'])
                            
                            # Show recommendation if 3 wrong in a row
                            if st.session_state.grammar_wrong_streak >= 3:
                                st.warning("🔎 Having trouble with grammar? Consider reviewing basic vocabulary and sentence patterns first.")
                            
                            # Show both Try Again and Next Question for incorrect answers
                            col1, col2 = st.columns(2)
                            with col1:
                                if st.button("Try Again", key="grammar_retry"):
                                    st.session_state.grammar_answered = False
                                    st.session_state.grammar_user_answer = None
                                    st.rerun()
                            with col2:
                                if st.button("Next Question", key="grammar_next_incorrect"):
                                    new_grammar_question()
                                    st.rerun()
        
        elif advanced_practice_type == "dialogue_comprehension":
            # State management for dialogue practice
            if 'dialogue_exercise' not in st.session_state:
                st.session_state.dialogue_exercise = None
            if 'dialogue_answered' not in st.session_state:
                st.session_state.dialogue_answered = False
            if 'dialogue_correct' not in st.session_state:
                st.session_state.dialogue_correct = None
            if 'dialogue_user_answer' not in st.session_state:
                st.session_state.dialogue_user_answer = None
            if 'dialogue_wrong_streak' not in st.session_state:
                st.session_state.dialogue_wrong_streak = 0
            if 'dialogue_right_streak' not in st.session_state:
                st.session_state.dialogue_right_streak = 0
            if 'dialogue_started' not in st.session_state:
                st.session_state.dialogue_started = False

            def new_dialogue_question():
                st.session_state.dialogue_exercise = practice_manager.generate_dialogue_comprehension()
                st.session_state.dialogue_answered = False
                st.session_state.dialogue_correct = None
                st.session_state.dialogue_user_answer = None

            # Show Start button first
            if not st.session_state.dialogue_started:
                if st.button("Start Dialogue Practice", key="dialogue_start"):
                    st.session_state.dialogue_started = True
                    new_dialogue_question()
                    st.rerun()
            else:
                # Show the exercise
                if st.session_state.dialogue_exercise:
                    exercise = st.session_state.dialogue_exercise
                    st.write("### Dialogue:")
                    for line in exercise['dialogue']:
                        st.write(f"**{line['speaker']}:** {line['text']}")
                    st.write(f"**Question:** {exercise['question']}")
                    
                    user_answer = st.radio(
                        "Select the correct answer:",
                        exercise['options'],
                        index=exercise['options'].index(st.session_state.dialogue_user_answer) if st.session_state.dialogue_user_answer in exercise['options'] else 0
                    )

                    # Only show 'Check Answer' if the user hasn't answered yet
                    if not st.session_state.dialogue_answered:
                        if st.button("Check Answer", key="dialogue_check"):
                            st.session_state.dialogue_user_answer = user_answer
                            st.session_state.dialogue_answered = True
                            if user_answer == exercise['answer']:
                                st.session_state.dialogue_correct = True
                                st.session_state.dialogue_right_streak += 1
                                st.session_state.dialogue_wrong_streak = 0
                                user_manager.record_practice_result("advanced", "dialogue_comprehension", True, exercise['question'])
                            else:
                                st.session_state.dialogue_correct = False
                                st.session_state.dialogue_wrong_streak += 1
                                st.session_state.dialogue_right_streak = 0
                                user_manager.record_practice_result("advanced", "dialogue_comprehension", False, exercise['question'])
                            st.rerun()

                    # Show feedback and action buttons after checking the answer
                    if st.session_state.dialogue_answered:
                        if st.session_state.dialogue_correct:
                            st.success("✅ Correct! 🎉 Great job!")
                            st.info(exercise['explanation'])
                            
                            # Special completion message for dialogue comprehension
                            if st.session_state.dialogue_right_streak >= 6:
                                st.balloons()  # Add celebration balloons
                                st.success("🎊 **Congratulations! You have excellently completed the highest difficulty test. You have fully mastered the basics of Japanese! Give yourself some encouragement!** 🎊")
                                st.info("🌟 **Achievement Unlocked:** Japanese Foundation Master! 🌟\n\nYou've conquered the foundational Japanese hiragana learning and can now confidently use other more advanced Japanese learning software. Keep up the excellent work!")
                            
                            # Only show Next Question for correct answers
                            if st.button("Next Question", key="dialogue_next_correct"):
                                new_dialogue_question()
                                st.rerun()
                        else:
                            st.error(f"❌ Not quite. The correct answer is '{exercise['answer']}'")
                            st.info(exercise['explanation'])
                            
                            # Show recommendation if 3 wrong in a row
                            if st.session_state.dialogue_wrong_streak >= 3:
                                st.warning("🔎 Having trouble with dialogue comprehension? Consider practicing more vocabulary and grammar first, or try starting with easier conversations.")
                            
                            # Show both Try Again and Next Question for incorrect answers
                            col1, col2 = st.columns(2)
                            with col1:
                                if st.button("Try Again", key="dialogue_retry"):
                                    st.session_state.dialogue_answered = False
                                    st.session_state.dialogue_user_answer = None
                                    st.rerun()
                            with col2:
                                if st.button("Next Question", key="dialogue_next_incorrect"):
                                    new_dialogue_question()
                                    st.rerun()
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
                        for practice_type, stats in level_stats.items():
                            # Format for display
                            display_name = {
                                "kana_matching": "Match Hiragana & Katakana",
                                "simple_vocabulary": "Basic Word Practice",
                                "common_phrases": "Common Japanese Phrases",
                                "vocabulary_categories": "Vocabulary by Category",
                                "translation_practice": "Translation Practice"
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
                                    "translation_practice": "Translation Practice"
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