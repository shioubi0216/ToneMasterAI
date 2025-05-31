import random
import os
import pandas as pd
import csv
from typing import List, Dict, Any, Tuple
from modules.ai_service import AIService

class PracticeManager:
    """Manages practice activities for Japanese language learning"""
    
    def __init__(self):
        """Initialize practice data and resources"""
        self.practice_types = {
            "beginner": [
                "kana_matching",
                "simple_vocabulary"
            ],
            "intermediate": [
                "common_phrases",
                "vocabulary_categories"
            ],
            "advanced": [
                "translation_practice",
                "grammar_application", 
                "dialogue_comprehension"
            ]
        }

        # Basic vocabulary with categories for beginner and intermediate practice
        self.vocabulary = {
            "animals": {
                "いぬ": {"meaning": "dog", "image": "dog.jpg"},
                "ねこ": {"meaning": "cat", "image": "cat.jpg"},
                "とり": {"meaning": "bird", "image": "bird.jpg"},
                "うま": {"meaning": "horse", "image": "horse.jpg"},
                "さかな": {"meaning": "fish", "image": "fish.jpg"}
            },
            "colors": {
                "あか": {"meaning": "red", "image": "red.jpg"},
                "あお": {"meaning": "blue", "image": "blue.jpg"},
                "きいろ": {"meaning": "yellow", "image": "yellow.jpg"},
                "みどり": {"meaning": "green", "image": "green.jpg"},
                "しろ": {"meaning": "white", "image": "white.jpg"},
                "くろ": {"meaning": "black", "image": "black.jpg"}
            },
            "food": {
                "ごはん": {"meaning": "rice", "image": "rice.jpg"},
                "みず": {"meaning": "water", "image": "water.jpg"},
                "パン": {"meaning": "bread", "image": "bread.jpg"},
                "りんご": {"meaning": "apple", "image": "apple.jpg"},
                "おちゃ": {"meaning": "tea", "image": "tea.jpg"}
            },
            "numbers": {
                "いち": {"meaning": "one", "image": "one.jpg"},
                "に": {"meaning": "two", "image": "two.jpg"},
                "さん": {"meaning": "three", "image": "three.jpg"},
                "よん": {"meaning": "four", "image": "four.jpg"},
                "ご": {"meaning": "five", "image": "five.jpg"}
            }
        }

        # Common phrases for intermediate practice
        self.common_phrases = {
            "おはようございます": "Good morning",
            "こんにちは": "Hello",
            "こんばんは": "Good evening",
            "ありがとうございます": "Thank you",
            "すみません": "Excuse me/I'm sorry",
            "いただきます": "Thanks for the food (before eating)",
            "ごちそうさまでした": "Thanks for the meal (after eating)",
            "はじめまして": "Nice to meet you",
            "よろしくおねがいします": "Please treat me well",
            "さようなら": "Goodbye"
        }

        # Basic grammar patterns for advanced practice
        self.grammar_patterns = {
            "は_です": {
                "pattern": "XはYです",
                "description": "X is Y",
                "examples": ["わたしは学生です", "これはほんです"]
            },
            "に_あります": {
                "pattern": "XにYがあります",
                "description": "Y is in/at X",
                "examples": ["部屋にテレビがあります", "公園に木があります"]
            },
            "を_します": {
                "pattern": "Xをします",
                "description": "Do X",
                "examples": ["勉強をします", "料理をします"]
            },
            "に_います": {
                "pattern": "XにYがいます",
                "description": "Y (living thing) is in/at X",
                "examples": ["家に猫がいます", "公園に人がいます"]
            }
        }

        # Initialize AI service for translation evaluation
        try:
            self.ai_service = AIService()
        except Exception as e:
            print(f"Warning: Could not initialize AI service: {e}")
            self.ai_service = None

        # Load translation practice data
        self.translation_data = self._load_translation_data()

    def _load_translation_data(self) -> List[Dict[str, str]]:
        """Load translation practice data from TSV files"""
        translation_pairs = []
        
        try:
            # Load Japanese to English translations (jp-en file)
            jp_en_path = os.path.join(os.getcwd(), "jpn_sentences", "jp-en - 2025-05-18.tsv")
            if os.path.exists(jp_en_path):
                with open(jp_en_path, 'r', encoding='utf-8') as file:
                    reader = csv.reader(file, delimiter='\t')
                    count = 0
                    for row in reader:
                        if len(row) >= 4 and count < 200:  # Limit to 200 sentences
                            japanese_text = row[1].strip()
                            english_text = row[3].strip()
                            
                            # Filter for reasonable length sentences (not too short or too long)
                            if 3 <= len(japanese_text) <= 50 and 3 <= len(english_text) <= 100:
                                translation_pairs.append({
                                    "japanese": japanese_text,
                                    "english": english_text,
                                    "jp_id": row[0],
                                    "en_id": row[2]
                                })
                                count += 1
                
                print(f"Loaded {len(translation_pairs)} translation pairs from jp-en file")
            else:
                print(f"Warning: Translation file not found at {jp_en_path}")
                # Fallback data
                translation_pairs = [
                    {"japanese": "こんにちは。", "english": "Hello.", "jp_id": "1", "en_id": "1"},
                    {"japanese": "ありがとうございます。", "english": "Thank you.", "jp_id": "2", "en_id": "2"},
                    {"japanese": "すみません。", "english": "Excuse me.", "jp_id": "3", "en_id": "3"},
                    {"japanese": "さようなら。", "english": "Goodbye.", "jp_id": "4", "en_id": "4"},
                    {"japanese": "おはようございます。", "english": "Good morning.", "jp_id": "5", "en_id": "5"}
                ]
                        
        except Exception as e:
            print(f"Error loading translation data: {e}")
            # Minimal fallback data
            translation_pairs = [
                {"japanese": "こんにちは。", "english": "Hello.", "jp_id": "1", "en_id": "1"},
                {"japanese": "ありがとうございます。", "english": "Thank you.", "jp_id": "2", "en_id": "2"}
            ]
        
        return translation_pairs

    def generate_translation_exercise(self) -> Dict[str, Any]:
        """Generate a translation practice exercise"""
        if not self.translation_data:
            return {
                "type": "translation_practice",
                "japanese": "こんにちは。",
                "reference_english": "Hello.",
                "user_translation": "",
                "explanation": "Translate the Japanese sentence to English."
            }
        
        # Select a random translation pair
        selected_pair = random.choice(self.translation_data)
        
        return {
            "type": "translation_practice",
            "japanese": selected_pair["japanese"],
            "reference_english": selected_pair["english"],
            "user_translation": "",
            "explanation": "Translate the Japanese sentence to English. Similar meanings and synonyms are acceptable."
        }

    def evaluate_user_translation(self, japanese_text: str, reference_english: str, user_translation: str) -> Dict[str, Any]:
        """Evaluate user's translation using AI service with improved fallback"""
        # Try AI service first if available
        if self.ai_service:
            try:
                # Use AI service to evaluate translation
                ai_response = self.ai_service.evaluate_translation(
                    japanese_text, reference_english, user_translation
                )
                
                # Parse the simple true/false response
                is_correct = ai_response.strip().lower() == "true"
                
                if is_correct:
                    return {
                        "result": "CORRECT",
                        "explanation": "Great translation! You captured the meaning correctly.",
                        "is_correct": True,
                        "reference": reference_english
                    }
                else:
                    return {
                        "result": "INCORRECT", 
                        "explanation": f"Not quite right. The correct translation is: {reference_english}",
                        "is_correct": False,
                        "reference": reference_english
                    }
                
            except Exception as e:
                print(f"Error in AI translation evaluation: {e}")
                # Fall through to manual evaluation
        
        # Enhanced fallback evaluation when AI service is not available
        return self._manual_translation_evaluation(reference_english, user_translation)
    
    def _manual_translation_evaluation(self, reference_english: str, user_translation: str) -> Dict[str, Any]:
        """Manual translation evaluation with flexible matching"""
        ref_clean = reference_english.lower().strip().rstrip('.,!?;')
        user_clean = user_translation.lower().strip().rstrip('.,!?;')
        
        # Exact match
        if ref_clean == user_clean:
            return {
                "result": "CORRECT",
                "explanation": "Perfect match!",
                "is_correct": True,
                "reference": reference_english
            }
        
        # Common word substitutions that should be accepted
        synonyms = {
            'hello': ['hi', 'hey', 'greetings'],
            'thank you': ['thanks', 'thank you very much', 'many thanks'],
            'goodbye': ['bye', 'farewell', 'see you later', 'see you'],
            'excuse me': ['sorry', 'pardon me', 'pardon'],
            'good morning': ['morning'],
            'good evening': ['evening'],
            'good night': ['night'],
            'please': ['pls'],
            'yes': ['yeah', 'yep', 'sure'],
            'no': ['nope', 'nah'],
            'i am': ['im', 'i\'m'],
            'you are': ['youre', 'you\'re'],
            'it is': ['its', 'it\'s'],
            'do not': ['dont', 'don\'t'],
            'will not': ['wont', 'won\'t'],
            'cannot': ['cant', 'can\'t']
        }
        
        # Check if user translation is a valid synonym
        for standard, alternatives in synonyms.items():
            if standard in ref_clean:
                for alt in alternatives:
                    if alt in user_clean:
                        modified_ref = ref_clean.replace(standard, alt)
                        if modified_ref == user_clean:
                            return {
                                "result": "CORRECT",
                                "explanation": f"Synonym accepted: '{alt}' for '{standard}'",
                                "is_correct": True,
                                "reference": reference_english
                            }
        
        # Check word overlap (if most words match, consider it partial)
        ref_words = set(ref_clean.split())
        user_words = set(user_clean.split())
        
        # Remove common particles and articles that can be omitted
        ignore_words = {'a', 'an', 'the', 'is', 'are', 'am', 'was', 'were', 'be', 'been', 'being'}
        ref_words_filtered = ref_words - ignore_words
        user_words_filtered = user_words - ignore_words
        
        if ref_words_filtered and user_words_filtered:
            overlap = len(ref_words_filtered & user_words_filtered)
            total_ref = len(ref_words_filtered)
            
            if overlap / total_ref >= 0.8:  # 80% word overlap
                return {
                    "result": "CORRECT",
                    "explanation": "Good translation with minor differences",
                    "is_correct": True,
                    "reference": reference_english
                }
            elif overlap / total_ref >= 0.6:  # 60% word overlap
                return {
                    "result": "PARTIAL",
                    "explanation": "Mostly correct, but missing some key words",
                    "is_correct": True,
                    "reference": reference_english
                }
        
        # If no good match found
        return {
            "result": "INCORRECT",
            "explanation": f"Try again. Reference: {reference_english}",
            "is_correct": False,
            "reference": reference_english
        }

    def generate_dialogue_comprehension(self) -> Dict[str, Any]:
        """Generate a dialogue comprehension exercise for advanced level"""
        dialogues = [
            {
                "dialogue": [
                    {"speaker": "A", "text": "こんにちは。お元気ですか？"},
                    {"speaker": "B", "text": "はい、元気です。ありがとう。"},
                    {"speaker": "A", "text": "今日は天気がいいですね。"},
                    {"speaker": "B", "text": "そうですね。とても暖かいです。"}
                ],
                "question": "この会話で、天気はどうですか？",
                "options": ["雨です", "暖かいです", "寒いです", "曇りです"],
                "answer": "暖かいです",
                "explanation": "Bさんは「とても暖かいです」と言っています。"
            },
            {
                "dialogue": [
                    {"speaker": "A", "text": "すみません、駅はどこですか？"},
                    {"speaker": "B", "text": "駅は右に行って、二つ目の角を左に曲がってください。"},
                    {"speaker": "A", "text": "ありがとうございます。"},
                    {"speaker": "B", "text": "いいえ、どういたしまして。"}
                ],
                "question": "駅に行くには、どうすればいいですか？",
                "options": ["左に行って、右に曲がる", "右に行って、左に曲がる", "まっすぐ行く", "バスに乗る"],
                "answer": "右に行って、左に曲がる",
                "explanation": "Bさんは「駅は右に行って、二つ目の角を左に曲がってください」と言っています。"
            }
        ]
        
        return random.choice(dialogues)
    
    def get_practice_activities(self, difficulty: str) -> List[str]:
        """Get available practice activities for a given difficulty level"""
        return self.practice_types.get(difficulty.lower(), [])
    
    def generate_kana_matching_exercise(self, hiragana_data: Dict, katakana_data: Dict) -> Dict[str, Any]:
        """Generate a hiragana-katakana matching exercise"""
        matching_pairs = []
        for sound in hiragana_data.keys():
            if sound in katakana_data:
                matching_pairs.append({
                    "hiragana": hiragana_data[sound]["symbol"],
                    "katakana": katakana_data[sound]["symbol"],
                    "romaji": hiragana_data[sound]["romaji"]
                })
        
        question_pair = random.choice(matching_pairs)
        correct_katakana = question_pair["katakana"]
        options = [correct_katakana]
        
        other_katakana = [pair["katakana"] for pair in matching_pairs if pair["katakana"] != correct_katakana]
        random_options = random.sample(other_katakana, min(3, len(other_katakana)))
        options.extend(random_options)
        
        while len(options) < 4 and len(other_katakana) > 0:
            option = random.choice(other_katakana)
            if option not in options:
                options.append(option)
                other_katakana.remove(option)
        
        random.shuffle(options)
        
        return {
            "type": "kana_matching",
            "question": f"Match the hiragana '{question_pair['hiragana']}' with its katakana equivalent",
            "options": options,
            "answer": correct_katakana,
            "explanation": f"The hiragana '{question_pair['hiragana']}' and katakana '{correct_katakana}' both represent '{question_pair['romaji']}'"
        }
    
    def generate_vocabulary_exercise(self, difficulty: str) -> Dict[str, Any]:
        """Generate a vocabulary exercise based on difficulty"""
        if difficulty == "beginner":
            category = random.choice(list(self.vocabulary.keys()))
            word, data = random.choice(list(self.vocabulary[category].items()))
            options = [data["meaning"]]
            
            other_meanings = [item["meaning"] for item in self.vocabulary[category].values() if item["meaning"] != data["meaning"]]
            if len(other_meanings) >= 3:
                options.extend(random.sample(other_meanings, 3))
            else:
                all_meanings = [item["meaning"] for cat in self.vocabulary.values() for item in cat.values() if item["meaning"] != data["meaning"]]
                options.extend(random.sample(all_meanings, min(3, len(all_meanings))))
            
            random.shuffle(options)
            
            return {
                "type": "simple_vocabulary",
                "question": f"What does '{word}' mean?",
                "options": options,
                "answer": data["meaning"],
                "image": data.get("image", ""),
                "category": category,
                "explanation": f"'{word}' means '{data['meaning']}' in English"
            }
        elif difficulty == "intermediate":
            category = random.choice(list(self.vocabulary.keys()))
            words_in_category = list(self.vocabulary[category].keys())
            other_words = []
            for other_cat, words in self.vocabulary.items():
                if other_cat != category:
                    other_words.extend(list(words.keys()))
            
            selected_correct = random.sample(words_in_category, min(3, len(words_in_category)))
            selected_incorrect = random.sample(other_words, min(3, len(other_words)))
            all_words = selected_correct + selected_incorrect
            random.shuffle(all_words)
            
            return {
                "type": "vocabulary_categories",
                "question": f"Select all words that belong to the category: {category}",
                "options": all_words,
                "multiple_answers": True,
                "answers": selected_correct,
                "explanation": f"The words in the '{category}' category are: {', '.join(words_in_category)}"
            }
        else:
            return self.generate_vocabulary_exercise("intermediate")
    
    def generate_grammar_exercise(self) -> Dict[str, Any]:
        """Generate a grammar usage exercise for advanced level"""
        pattern_key = random.choice(list(self.grammar_patterns.keys()))
        pattern_data = self.grammar_patterns[pattern_key]
        example = random.choice(pattern_data["examples"])
        pattern = pattern_data["pattern"]
        
        parts = pattern.split("_")
        if len(parts) == 2:
            example_words = example.replace("。", "").split()
            blank_options = []
            for i, word in enumerate(example_words):
                if any(particle in word for particle in ["は", "が", "を", "に", "で"]):
                    blank_options.append((i, word))
            
            if blank_options:
                blank_index, correct_word = random.choice(blank_options)
                example_words[blank_index] = "＿＿＿"
                question_text = " ".join(example_words)
                
                particles = ["は", "が", "を", "に", "で", "も", "と", "から", "まで"]
                options = [correct_word]
                for _ in range(3):
                    distractor = random.choice(particles)
                    if distractor not in options:
                        options.append(distractor)
                
                while len(options) < 4:
                    options.append(random.choice(particles))
                
                random.shuffle(options)
                
                return {
                    "type": "grammar_application",
                    "question": f"Fill in the blank: {question_text}",
                    "options": options,
                    "answer": correct_word,
                    "pattern": pattern,
                    "explanation": f"The pattern '{pattern}' requires '{correct_word}' in this context. {pattern_data['description']}"
                }
        
        return {
            "type": "grammar_application",
            "question": f"Which of these examples uses the pattern: {pattern}?",
            "options": [ex for ex in pattern_data["examples"]],
            "answer": pattern_data["examples"][0],
            "explanation": f"The pattern '{pattern}' means: {pattern_data['description']}"
        }
    
    def generate_exercise(self, practice_type: str, difficulty: str, syllabary_data: Dict = None) -> Dict[str, Any]:
        """Generate an exercise based on the practice type and difficulty"""
        if practice_type == "kana_matching" and isinstance(syllabary_data, dict) and len(syllabary_data) == 2:
            return self.generate_kana_matching_exercise(syllabary_data["hiragana"], syllabary_data["katakana"])
        elif practice_type == "simple_vocabulary":
            return self.generate_vocabulary_exercise("beginner")
        elif practice_type == "common_phrases":
            # This is handled directly in app.py
            return {}
        elif practice_type == "vocabulary_categories":
            return self.generate_vocabulary_exercise("intermediate")
        elif practice_type == "translation_practice":
            return self.generate_translation_exercise()
        elif practice_type == "grammar_application":
            return self.generate_grammar_exercise()
        elif practice_type == "dialogue_comprehension":
            return self.generate_dialogue_comprehension()
        
        # Default fallback
        return {
            "type": "simple_vocabulary",
            "question": "What does 'こんにちは' mean?",
            "options": ["Good morning", "Hello", "Good evening", "Goodbye"],
            "answer": "Hello",
            "explanation": "'こんにちは' means 'Hello' in English"
        }

    def record_practice_result(self, user_id: str, practice_type: str, success: bool, details: Dict[str, Any] = None) -> None:
        """Record the result of a practice session for tracking user progress"""
        print(f"Recording practice result for user {user_id}: {practice_type} - {'Success' if success else 'Failure'}")

    def get_recommended_practice(self, user_id: str, difficulty: str) -> str:
        """Get a recommended practice type based on user performance"""
        return random.choice(self.practice_types.get(difficulty.lower(), []))
