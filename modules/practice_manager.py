import random
import os
import pandas as pd
from typing import List, Dict, Any, Tuple

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
                "sentence_creation",
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
        
        # Load sentences from Tatoeba for practice activities
        self.sentences = self._load_sentences()
        
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
        
    def _load_sentences(self) -> Dict[str, List[Dict[str, Any]]]:
        """Load Japanese sentences from Tatoeba corpus with improved translation handling"""
        sentences = {
            "beginner": [],
            "intermediate": [],
            "advanced": []
        }
        
        try:
            # Look for the tsv directory
            tsv_dir = os.path.join(os.getcwd(), "jpn_sentences.tsv")
            
            # First try to load from the jpn_sentences.tsv directly (Japanese sentences only)
            jpn_path = os.path.join(tsv_dir, "jpn_sentences.tsv")
            if os.path.exists(jpn_path):
                # Read Japanese sentences (limit to 5000 for efficiency)
                df = pd.read_csv(jpn_path, sep='\t', header=None, names=['id', 'lang', 'text'], nrows=5000)
                japanese_sentences = df[df['lang'] == 'jpn'][['id', 'text']].to_dict('records')
                
                # Categorize sentences by complexity
                for sentence_data in japanese_sentences:
                    sentence = sentence_data['text']
                    sentence_id = sentence_data['id']
                    
                    # Simple categorization based on length and complexity
                    entry = {"text": sentence, "id": sentence_id, "translation": "", "tags": []}
                    
                    if len(sentence) < 10 and all(char not in sentence for char in "。、"):
                        sentences["beginner"].append(entry)
                    elif len(sentence) < 20:
                        sentences["intermediate"].append(entry)
                    else:
                        sentences["advanced"].append(entry)
                
                # Try to load translations from jp-en
                en_path = os.path.join(tsv_dir, "jp-en - 2025-05-18.tsv")
                if os.path.exists(en_path):
                    try:
                        # Load english translations
                        trans_df = pd.read_csv(en_path, sep='\t', header=None, names=['jp_id', 'en_id', 'en_text'])
                        translations = {row['jp_id']: row['en_text'] for _, row in trans_df.iterrows()}
                        
                        # Add translations to sentences
                        for category in sentences.keys():
                            for entry in sentences[category]:
                                if entry["id"] in translations:
                                    entry["translation"] = translations[entry["id"]]
                    except Exception as e:
                        print(f"Error loading translations: {e}")
            else:
                print(f"Warning: Tatoeba sentences file not found at {jpn_path}")
                # Fallback to a few hardcoded sentences for each level
                sentences["beginner"] = [
                    {"text": "これはほんです。", "translation": "This is a book.", "tags": ["simple", "object"]},
                    {"text": "おはようございます。", "translation": "Good morning.", "tags": ["greeting"]},
                    {"text": "ありがとうございます。", "translation": "Thank you.", "tags": ["courtesy"]},
                    {"text": "わたしはがくせいです。", "translation": "I am a student.", "tags": ["introduction"]},
                    {"text": "あのひとはせんせいです。", "translation": "That person is a teacher.", "tags": ["occupation"]}
                ]
                
                sentences["intermediate"] = [
                    {"text": "あしたはあめがふるでしょう。", "translation": "It will probably rain tomorrow.", "tags": ["weather"]},
                    {"text": "このほんはとてもおもしろいです。", "translation": "This book is very interesting.", "tags": ["opinion"]},
                    {"text": "わたしはまいにちにほんごをべんきょうします。", "translation": "I study Japanese every day.", "tags": ["routine"]},
                    {"text": "このレストランのりょうりはおいしいです。", "translation": "The food at this restaurant is delicious.", "tags": ["food"]}
                ]
                
                sentences["advanced"] = [
                    {"text": "日本の伝統文化について詳しく説明してください。", "translation": "Please explain Japanese traditional culture in detail.", "tags": ["culture"]},
                    {"text": "環境問題の解決策について話し合いましょう。", "translation": "Let's discuss solutions for environmental issues.", "tags": ["environment"]},
                    {"text": "自分の将来の目標を達成するために、毎日努力することが大切です。", "translation": "It's important to make efforts every day to achieve your future goals.", "tags": ["motivation"]},
                    {"text": "東京は世界で最も人口が多い都市の一つです。", "translation": "Tokyo is one of the most populous cities in the world.", "tags": ["facts"]}
                ]
        except Exception as e:
            print(f"Error loading sentences: {e}")
            # Fallback to a few hardcoded sentences
            sentences["beginner"] = [                {"text": "これはほんです。", "translation": "This is a book.", "tags": ["simple", "object"]},
                {"text": "おはようございます。", "translation": "Good morning.", "tags": ["greeting"]},
                {"text": "ありがとうございます。", "translation": "Thank you.", "tags": ["courtesy"]}
            ]
            
        return sentences
    
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
    
    def generate_sentence_creation_exercise(self) -> Dict[str, Any]:
        """Generate a sentence creation exercise"""
        # Simple sentence creation prompts
        prompts = [
            {
                "scenario": "Introduce yourself (name, age, nationality)",
                "vocabulary": ["わたし", "なまえ", "さい", "にほんじん", "です"],
                "example": "わたしのなまえはたろうです。にじゅうさいです。にほんじんです。",
                "translation": "My name is Taro. I am 20 years old. I am Japanese."
            },
            {
                "scenario": "Describe what you like to eat",
                "vocabulary": ["たべもの", "すし", "ラーメン", "が", "すき", "です"],
                "example": "わたしはすしがすきです。ラーメンもすきです。",
                "translation": "I like sushi. I also like ramen."
            },
            {
                "scenario": "Ask where something is",
                "vocabulary": ["トイレ", "えき", "どこ", "ですか"],
                "example": "トイレはどこですか。えきはどこですか。",
                "translation": "Where is the toilet? Where is the station?"
            }
        ]


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
        elif practice_type == "sentence_creation":
            return self.generate_sentence_creation_exercise()
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
    
