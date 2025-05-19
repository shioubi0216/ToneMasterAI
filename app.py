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
        
        # Add practice recommendations
        recommended_practice = user_manager.get_recommended_practice("beginner")
        if recommended_practice:
            format_name = {
                "kana_recognition": "Listen & Recognize Kana",
                "kana_matching": "Match Hiragana & Katakana",
                "simple_vocabulary": "Basic Word Practice",
                "word_image_matching": "Match Words with Images",
                "listen_and_choose": "Listen and Choose"
            }.get(recommended_practice, recommended_practice.replace("_", " ").title())
            
            st.info(f"💡 Recommended: Try '{format_name}' to improve your skills!")
        
        # Practice types for beginners
        beginner_activities = practice_manager.get_practice_activities("beginner")
        beginner_practice_type = st.selectbox(
            "Choose practice type:",
            beginner_activities,
            format_func=lambda x: {
                "kana_recognition": "Listen & Recognize Kana",
                "kana_matching": "Match Hiragana & Katakana",
                "simple_vocabulary": "Basic Word Practice",
                "word_image_matching": "Match Words with Images",
                "listen_and_choose": "Listen and Choose"
            }.get(x, x.replace("_", " ").title())
        )
        
        # Start practice session button
        if st.button("Start Beginner Practice"):
            # Create practice exercise based on selected type
            if beginner_practice_type == "kana_recognition":
                # Choose a random syllabary type for this exercise
                target_syllabary = "hiragana" if random.random() > 0.5 else "katakana"
                syllabary_data = syllabary.hiragana if target_syllabary == "hiragana" else syllabary.katakana
                exercise = practice_manager.generate_exercise("kana_recognition", "beginner", syllabary_data)
                
                st.write(f"## {exercise['question']}")
                user_answer = st.radio("Select the correct character:", exercise['options'])
                
                check_col1, check_col2 = st.columns([1, 4])
                with check_col1:
                    if st.button("Check Answer", key="beginner_check"):
                        if user_answer == exercise['answer']:
                            st.success("Correct! 🎉")
                            st.session_state.last_result = True
                            # Record successful practice result
                            user_manager.record_practice_result("beginner", "kana_recognition", True, exercise['answer'])
                        else:
                            st.error(f"Not quite. The correct answer is '{exercise['answer']}'")
                            st.session_state.last_result = False
                            # Record unsuccessful practice result
                            user_manager.record_practice_result("beginner", "kana_recognition", False, exercise['answer'])
                        st.info(exercise['explanation'])
                
            elif beginner_practice_type == "kana_matching":
                exercise = practice_manager.generate_exercise("kana_matching", "beginner", 
                                                            {"hiragana": syllabary.hiragana, "katakana": syllabary.katakana})
                
                st.write(f"## {exercise['question']}")
                user_answer = st.radio("Select the matching katakana:", exercise['options'])
                
                if st.button("Check Answer", key="matching_check"):
                    if user_answer == exercise['answer']:
                        st.success("Correct! 🎉")
                        st.session_state.last_result = True
                        # Record successful practice result
                        user_manager.record_practice_result("beginner", "kana_matching", True, exercise['answer'])
                    else:
                        st.error(f"Not quite. The correct answer is '{exercise['answer']}'")
                        st.session_state.last_result = False
                        # Record unsuccessful practice result
                        user_manager.record_practice_result("beginner", "kana_matching", False, exercise['answer'])
                    st.info(exercise['explanation'])
                
            elif beginner_practice_type == "simple_vocabulary":
                exercise = practice_manager.generate_exercise("simple_vocabulary", "beginner")
                
                st.write(f"## {exercise['question']}")
                
                # Display image if available (in real implementation, you'd have actual images)
                if 'image' in exercise and exercise['image']:
                    st.write("(Image would be displayed here)")
                
                user_answer = st.radio("Select the meaning:", exercise['options'])
                
                if st.button("Check Answer", key="vocab_check"):
                    if user_answer == exercise['answer']:
                        st.success("Correct! 🎉")
                        st.session_state.last_result = True
                        # Track progress
                        user_manager.record_practice_result("beginner", "simple_vocabulary", True, exercise['question'])
                    else:
                        st.error(f"Not quite. The correct answer is '{exercise['answer']}'")
                        st.session_state.last_result = False
                        # Track progress
                        user_manager.record_practice_result("beginner", "simple_vocabulary", False, exercise['question'])
                    st.info(exercise['explanation'])
            
            elif beginner_practice_type == "listen_and_choose":
                exercise = practice_manager.generate_listen_and_choose_exercise()
                
                st.write(f"## {exercise['question']}")
                
                # In a real implementation, this would play actual audio
                st.info(f"Listen to the word: {exercise['japanese_text']}")
                
                user_answer = st.radio("Select the meaning:", exercise['options'])
                
                if st.button("Check Answer", key="listen_check"):
                    if user_answer == exercise['answer']:
                        st.success("Correct! 🎉")
                        st.session_state.last_result = True
                        # Record the successful practice result
                        user_manager.record_practice_result("beginner", "listen_and_choose", True, exercise['japanese_text'])
                    else:
                        st.error(f"Not quite. The correct answer is '{exercise['answer']}'")
                        st.session_state.last_result = False
                        # Record the unsuccessful practice result
                        user_manager.record_practice_result("beginner", "listen_and_choose", False, exercise['japanese_text'])
                    st.info(exercise['explanation'])
    
    # Intermediate tab
    with difficulty_tabs[1]:
        st.header("Intermediate Level Practice")
        st.write("For learners who have mastered the basics and are ready for more complex patterns.")
        
        # Add practice recommendations
        recommended_practice = user_manager.get_recommended_practice("intermediate")
        if recommended_practice:
            format_name = {
                "common_phrases": "Common Japanese Phrases",
                "vocabulary_categories": "Vocabulary by Category",
                "sentence_completion": "Complete the Sentence",
                "speed_challenge": "Speed Recognition Challenge",
                "special_kana_combinations": "Special Kana Combinations",
                "listening_comprehension": "Listening Comprehension"
            }.get(recommended_practice, recommended_practice.replace("_", " ").title())
            
            st.info(f"💡 Recommended: Try '{format_name}' to improve your skills!")
        
        # Practice types for intermediate level
        intermediate_activities = practice_manager.get_practice_activities("intermediate")
        intermediate_practice_type = st.selectbox(
            "Choose practice type:",
            intermediate_activities,
            format_func=lambda x: {
                "common_phrases": "Common Japanese Phrases",
                "vocabulary_categories": "Vocabulary by Category",
                "sentence_completion": "Complete the Sentence",
                "speed_challenge": "Speed Recognition Challenge",
                "special_kana_combinations": "Special Kana Combinations",
                "listening_comprehension": "Listening Comprehension"
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
            
            elif intermediate_practice_type == "sentence_completion":
                # Get a simple sentence from the Tatoeba database
                if practice_manager.sentences["intermediate"]:
                    sentence = random.choice(practice_manager.sentences["intermediate"])
                    
                    # Split sentence into words (simplified approach)
                    words = sentence["text"].replace("。", "").split()
                    
                    if len(words) > 2:  # Ensure sentence has enough words
                        # Choose a random word to blank out
                        blank_index = random.randint(0, len(words) - 1)
                        correct_word = words[blank_index]
                        
                        # Create the question by replacing the word with a blank
                        words[blank_index] = "＿＿＿"
                        question_text = " ".join(words)
                        
                        st.write(f"## Complete the sentence: {question_text}")
                        
                        # Add options (simplified)
                        options = [correct_word]
                        # Add some distractors
                        for _ in range(3):
                            if practice_manager.sentences["beginner"]:
                                distractor_sentence = random.choice(practice_manager.sentences["beginner"])
                                distractor_words = distractor_sentence["text"].replace("。", "").split()
                                if distractor_words:
                                    options.append(random.choice(distractor_words))
                        
                        # Ensure we have 4 options
                        while len(options) < 4:
                            options.append("わたし")  # Add a common word as fallback
                        
                        user_answer = st.radio("Select the missing word:", options)
                        
                        if st.button("Check Answer", key="completion_check"):
                            if user_answer == correct_word:
                                st.success("Correct! 🎉")
                                st.session_state.last_result = True
                            else:
                                st.error(f"Not quite. The correct answer is '{correct_word}'")
                                st.session_state.last_result = False
                                
                            # Show the complete sentence
                            st.info(f"Complete sentence: {sentence['text']}")
    
    # Advanced tab
    with difficulty_tabs[2]:
        st.header("Advanced Level Practice")
        st.write("Challenge yourself with complex grammar, conversations, and reading comprehension.")
        
        # Add practice recommendations for advanced level
        recommended_practice = user_manager.get_recommended_practice("advanced")
        if recommended_practice:
            format_name = {
                "dialogue_comprehension": "Dialogue Comprehension",
                "grammar_application": "Grammar Usage",
                "sentence_creation": "Create Sentences",
                "verb_conjugation": "Verb Conjugation",
                "reading_comprehension": "Reading Comprehension",
                "speech_practice": "Speech Practice"
            }.get(recommended_practice, recommended_practice.replace("_", " ").title())
            
            st.info(f"💡 Recommended: Try '{format_name}' to improve your skills!")
        
        # Practice types for advanced level
        advanced_activities = practice_manager.get_practice_activities("advanced")
        advanced_practice_type = st.selectbox(
            "Choose practice type:",
            advanced_activities,
            format_func=lambda x: {
                "dialogue_comprehension": "Dialogue Comprehension",
                "grammar_application": "Grammar Usage",
                "sentence_creation": "Create Sentences",
                "verb_conjugation": "Verb Conjugation",
                "reading_comprehension": "Reading Comprehension",
                "speech_practice": "Speech Practice"
            }.get(x, x.replace("_", " ").title())
        )
        
        # Start practice session button
        if st.button("Start Advanced Practice"):
            if advanced_practice_type == "dialogue_comprehension":
                exercise = practice_manager.generate_dialogue_comprehension()
                
                st.write("## Read the following dialogue:")
                dialogue_container = st.container()
                with dialogue_container:
                    for line in exercise["dialogue"]:
                        st.write(f"**{line['speaker']}**: {line['text']}")
                
                st.write(f"**Question**: {exercise['question']}")
                user_answer = st.radio("Select your answer:", exercise['options'])
                
                if st.button("Check Answer", key="dialogue_check"):
                    if user_answer == exercise['answer']:
                        st.success("Correct! 🎉")
                        st.session_state.last_result = True
                    else:
                        st.error(f"Not quite. The correct answer is '{exercise['answer']}'")
                        st.session_state.last_result = False
                    st.info(exercise['explanation'])
            
            elif advanced_practice_type == "grammar_application":
                exercise = practice_manager.generate_grammar_exercise()
                
                st.write(f"## {exercise['question']}")
                user_answer = st.radio("Select the correct answer:", exercise['options'])
                
                if st.button("Check Answer", key="grammar_check"):
                    if user_answer == exercise['answer']:
                        st.success("Correct! 🎉")
                        st.session_state.last_result = True
                    else:
                        st.error(f"Not quite. The correct answer is '{exercise['answer']}'")
                        st.session_state.last_result = False
                    st.info(exercise['explanation'])
            
            elif advanced_practice_type == "sentence_creation":
                exercise = practice_manager.generate_sentence_creation_exercise()
                
                st.write(f"## Create a sentence about: {exercise['scenario']}")
                st.write("Use these vocabulary words:")
                for word in exercise['vocabulary']:
                    st.write(f"- {word}")
                
                user_sentence = st.text_input("Your sentence:")
                
                if st.button("Check Sentence", key="creation_check"):
                    # For demonstration purposes, just check if they used some of the vocabulary
                    used_vocab = 0
                    for word in exercise['vocabulary']:
                        if word in user_sentence:
                            used_vocab += 1
                    
                    if used_vocab >= 2:  # If they used at least 2 vocabulary words
                        st.success("Good job! Your sentence uses the vocabulary well.")
                        st.session_state.last_result = True
                    else:
                        st.warning("Try to use more of the provided vocabulary words.")
                        st.session_state.last_result = False
                    
                    st.info(f"Example: {exercise['example']}\nTranslation: {exercise['translation']}")
            
            elif advanced_practice_type == "verb_conjugation":
                exercise = practice_manager.generate_verb_conjugation_exercise()
                
                st.write(f"## {exercise['question']}")
                user_answer = st.radio("Select the correct conjugation:", exercise['options'])
                
                if st.button("Check Answer", key="conjugation_check"):
                    if user_answer == exercise['answer']:
                        st.success("Correct! 🎉")
                        st.session_state.last_result = True
                    else:
                        st.error(f"Not quite. The correct answer is '{exercise['answer']}'")
                        st.session_state.last_result = False
                    st.info(exercise['explanation'])
            
            elif advanced_practice_type == "reading_comprehension":
                exercise = practice_manager.generate_reading_comprehension_exercise()
                
                st.write("## Read the following passage:")
                st.write(exercise['text'])
                
                st.write(f"**Question**: {exercise['question']}")
                user_answer = st.radio("Select your answer:", exercise['options'])
                
                if st.button("Check Answer", key="reading_check"):
                    if user_answer == exercise['answer']:
                        st.success("Correct! 🎉")
                        st.session_state.last_result = True
                    else:
                        st.error(f"Not quite. The correct answer is '{exercise['answer']}'")
                        st.session_state.last_result = False
                    st.info(exercise['explanation'])
            
            elif advanced_practice_type == "speech_practice":
                exercise = practice_manager.generate_speech_practice_exercise()
                
                st.write(f"## {exercise['prompt']}")
                st.write(f"### {exercise['japanese_text']}")
                
                # Display translation and pronunciation guidance
                st.info(f"Translation: {exercise['translation']}")
                st.write(f"**Pronunciation guidance**: {exercise['pronunciation_guidance']}")
                
                # Key vocabulary section
                if exercise['key_vocabulary']:
                    st.write("**Key vocabulary:**")
                    for vocab in exercise['key_vocabulary']:
                        st.write(f"- {vocab}")
                
                # In a real implementation, these would be functional
                st.write("**Practice tools:**")
                col1, col2 = st.columns(2)
                with col1:
                    st.button("🔊 Listen to Reference", key="listen_reference")
                with col2:
                    st.button("🎤 Record Your Attempt", key="record_attempt")
                
                # Simplified assessment for demo
                st.write("### Self-assessment")
                confidence = st.slider("How well do you think you pronounced it?", 1, 5, 3)
                
                if st.button("Submit Practice", key="speech_submit"):
                    if confidence >= 4:
                        st.success("Great job! Keep practicing to perfect your pronunciation.")
                        # Record a successful result for high confidence
                        user_manager.record_practice_result("advanced", "speech_practice", True, exercise['japanese_text'])
                    else:
                        st.info("Practice makes perfect! Try listening to the reference again and repeating.")
                        # Record as a learning opportunity for lower confidence
                        user_manager.record_practice_result("advanced", "speech_practice", False, exercise['japanese_text'])
                        
                    # Provide encouragement regardless of confidence level
                    st.write("**Tips for improving:**")
                    st.write("- Practice individual sounds first, then the full sentence")
                    st.write("- Pay attention to pitch accent and rhythm")
                    st.write("- Record yourself and compare to native speakers")

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
                                # Beginner
                                "kana_recognition": "Listen & Recognize Kana",
                                "kana_matching": "Match Hiragana & Katakana",
                                "simple_vocabulary": "Basic Word Practice",
                                "word_image_matching": "Match Words with Images",
                                "listen_and_choose": "Listen and Choose",
                                # Intermediate
                                "common_phrases": "Common Japanese Phrases",
                                "vocabulary_categories": "Vocabulary by Category",
                                "sentence_completion": "Complete the Sentence",
                                "speed_challenge": "Speed Recognition Challenge",
                                "special_kana_combinations": "Special Kana Combinations",
                                "listening_comprehension": "Listening Comprehension",
                                # Advanced
                                "dialogue_comprehension": "Dialogue Comprehension",
                                "grammar_application": "Grammar Usage",
                                "sentence_creation": "Create Sentences",
                                "verb_conjugation": "Verb Conjugation",
                                "reading_comprehension": "Reading Comprehension",
                                "speech_practice": "Speech Practice"
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
                                    # Format names as above
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

