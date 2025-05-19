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
                "kana_recognition", 
                "kana_matching", 
                "simple_vocabulary", 
                "word_image_matching",
                "listen_and_choose"  # New listening practice
            ],
            "intermediate": [
                "common_phrases", 
                "vocabulary_categories", 
                "sentence_completion", 
                "speed_challenge", 
                "special_kana_combinations",
                "listening_comprehension"  # New listening comprehension
            ],
            "advanced": [
                "dialogue_comprehension", 
                "grammar_application", 
                "sentence_creation", 
                "verb_conjugation", 
                "reading_comprehension",
                "speech_practice"  # New speaking practice
            ]
        }
        
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
            sentences["beginner"] = [
                {"text": "これはほんです。", "translation": "This is a book.", "tags": ["simple", "object"]},
                {"text": "おはようございます。", "translation": "Good morning.", "tags": ["greeting"]},
                {"text": "ありがとうございます。", "translation": "Thank you.", "tags": ["courtesy"]}
            ]
            
        return sentences
    
    def get_practice_activities(self, difficulty: str) -> List[str]:
        """Get available practice activities for a given difficulty level"""
        return self.practice_types.get(difficulty.lower(), [])
    
    def generate_kana_recognition_exercise(self, syllabary_type: str, syllabary_data: Dict) -> Dict[str, Any]:
        """Generate a kana recognition exercise"""
        # Get all characters from the syllabary
        all_kana = []
        for sound, data in syllabary_data.items():
            all_kana.append({"symbol": data["symbol"], "romaji": data["romaji"]})
        
        # Select a random character as the answer
        answer = random.choice(all_kana)
        
        # Create options (1 correct + 3 random different options)
        options = [answer]
        while len(options) < 4:
            option = random.choice(all_kana)
            if option not in options:
                options.append(option)
        
        # Shuffle options
        random.shuffle(options)
        
        return {
            "type": "kana_recognition",
            "question": f"Select the correct {syllabary_type} for: {answer['romaji']}",
            "options": [opt["symbol"] for opt in options],
            "answer": answer["symbol"],
            "explanation": f"The {syllabary_type} character for '{answer['romaji']}' is '{answer['symbol']}'"
        }
    
    def generate_kana_matching_exercise(self, hiragana_data: Dict, katakana_data: Dict) -> Dict[str, Any]:
        """Generate a hiragana-katakana matching exercise"""
        # Get matching pairs
        matching_pairs = []
        for sound in hiragana_data.keys():
            if sound in katakana_data:
                matching_pairs.append({
                    "hiragana": hiragana_data[sound]["symbol"],
                    "katakana": katakana_data[sound]["symbol"],
                    "romaji": hiragana_data[sound]["romaji"]
                })
        
        # Select a random pair as the question
        question_pair = random.choice(matching_pairs)
        
        # Create options (1 correct + 3 random different options)
        correct_katakana = question_pair["katakana"]
        options = [correct_katakana]
        
        other_katakana = [pair["katakana"] for pair in matching_pairs if pair["katakana"] != correct_katakana]
        random_options = random.sample(other_katakana, min(3, len(other_katakana)))
        options.extend(random_options)
        
        # Fill with more options if needed
        while len(options) < 4 and len(other_katakana) > 0:
            option = random.choice(other_katakana)
            if option not in options:
                options.append(option)
                other_katakana.remove(option)
        
        # Shuffle options
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
            # Choose a random category
            category = random.choice(list(self.vocabulary.keys()))
            # Choose a random word from that category
            word, data = random.choice(list(self.vocabulary[category].items()))
            
            # Create options (1 correct + 3 random different options)
            options = [data["meaning"]]
            other_meanings = [item["meaning"] for item in self.vocabulary[category].values() if item["meaning"] != data["meaning"]]
            
            if len(other_meanings) >= 3:
                options.extend(random.sample(other_meanings, 3))
            else:
                # If not enough options in the same category, get from other categories
                all_meanings = [item["meaning"] for cat in self.vocabulary.values() for item in cat.values() if item["meaning"] != data["meaning"]]
                options.extend(random.sample(all_meanings, min(3, len(all_meanings))))
            
            # Shuffle options
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
            # Create a categorization exercise
            category = random.choice(list(self.vocabulary.keys()))
            words_in_category = list(self.vocabulary[category].keys())
            
            # Get words from other categories for options
            other_words = []
            for other_cat, words in self.vocabulary.items():
                if other_cat != category:
                    other_words.extend(list(words.keys()))
            
            # Select 3 words from the correct category
            selected_correct = random.sample(words_in_category, min(3, len(words_in_category)))
            # Select 3 words from other categories
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
        else:  # advanced
            # Get a sentence and create a fill-in-the-blank exercise
            if len(self.sentences["advanced"]) > 0:
                sentence = random.choice(self.sentences["advanced"])
                # Split sentence into words (simplified approach)
                words = sentence["text"].replace("。", "").replace("、", " ").split()
                
                if len(words) > 3:  # Ensure sentence has enough words
                    # Choose a random word to blank out
                    blank_index = random.randint(1, len(words) - 2)  # Avoid first and last words
                    correct_word = words[blank_index]
                    
                    # Create the question by replacing the word with a blank
                    words[blank_index] = "＿＿＿"
                    question_text = " ".join(words)
                    
                    # Get options (1 correct + 3 distractors)
                    options = [correct_word]
                    
                    # Get other words from sentences for distractors
                    all_words = []
                    for s in self.sentences["advanced"] + self.sentences["intermediate"]:
                        all_words.extend(s["text"].replace("。", "").replace("、", " ").split())
                    
                    # Filter for words of similar length and different from the correct word
                    similar_words = [w for w in all_words if len(w) > 1 and abs(len(w) - len(correct_word)) <= 1 and w != correct_word]
                    
                    if len(similar_words) >= 3:
                        options.extend(random.sample(similar_words, 3))
                    else:
                        # Fallback to any words if not enough similar ones
                        other_words = [w for w in all_words if w != correct_word and len(w) > 1]
                        options.extend(random.sample(other_words, min(3, len(other_words))))
                    
                    random.shuffle(options)
                    
                    return {
                        "type": "sentence_completion",
                        "question": f"Fill in the blank: {question_text}",
                        "options": options,
                        "answer": correct_word,
                        "full_sentence": sentence["text"],
                        "explanation": f"The correct word is '{correct_word}'"
                    }
            
            # Fallback if no suitable sentences
            return self.generate_vocabulary_exercise("intermediate")
    
    def generate_dialogue_comprehension(self) -> Dict[str, Any]:
        """Generate a dialogue comprehension exercise"""
        # Simple dialogues for practice
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
        """Generate a grammar exercise"""
        # Choose a random grammar pattern
        pattern_key = random.choice(list(self.grammar_patterns.keys()))
        pattern_data = self.grammar_patterns[pattern_key]
        
        # Create a sentence completion exercise
        example = random.choice(pattern_data["examples"])
        pattern = pattern_data["pattern"]
        
        # Parse the pattern to create a fill-in-the-blank exercise
        # This is a simplified approach; for production, you'd want more sophisticated parsing
        parts = pattern.split("_")
        if len(parts) == 2:
            # Split the example into words
            example_words = example.replace("。", "").split()
            
            # Find where to put the blank (replace a particle or verb)
            blank_options = []
            for i, word in enumerate(example_words):
                if any(particle in word for particle in ["は", "が", "を", "に", "で"]):
                    blank_options.append((i, word))
            
            if blank_options:
                blank_index, correct_word = random.choice(blank_options)
                
                # Create question by replacing the word with a blank
                example_words[blank_index] = "＿＿＿"
                question_text = " ".join(example_words)
                
                # Options (including the correct particle/word)
                particles = ["は", "が", "を", "に", "で", "も", "と", "から", "まで"]
                options = [correct_word]
                
                # Add some distractors
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
        
        # Fallback: create a simple pattern identification question
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
        
        return random.choice(prompts)
    
    def generate_verb_conjugation_exercise(self) -> Dict[str, Any]:
        """Generate a verb conjugation exercise"""
        # Basic verbs and their conjugations
        verbs = {
            "食べる": {
                "type": "ru-verb",
                "masu": "食べます",
                "masen": "食べません",
                "mashita": "食べました",
                "masendeshita": "食べませんでした",
                "meaning": "to eat"
            },
            "飲む": {
                "type": "u-verb",
                "masu": "飲みます",
                "masen": "飲みません",
                "mashita": "飲みました",
                "masendeshita": "飲みませんでした",
                "meaning": "to drink"
            },
            "行く": {
                "type": "u-verb (irregular)",
                "masu": "行きます",
                "masen": "行きません",
                "mashita": "行きました",
                "masendeshita": "行きませんでした",
                "meaning": "to go"
            },
            "見る": {
                "type": "ru-verb",
                "masu": "見ます",
                "masen": "見ません",
                "mashita": "見ました",
                "masendeshita": "見ませんでした",
                "meaning": "to see/watch"
            },
            "買う": {
                "type": "u-verb",
                "masu": "買います",
                "masen": "買いません",
                "mashita": "買いました",
                "masendeshita": "買いませんでした",
                "meaning": "to buy"
            }
        }
        
        # Choose a random verb
        verb, data = random.choice(list(verbs.items()))
        
        # Choose a random conjugation form
        form = random.choice(["masu", "masen", "mashita", "masendeshita"])
        
        # Create options (1 correct + 3 distractors)
        correct_answer = data[form]
        options = [correct_answer]
        
        # Add conjugations of the same verb in different forms as distractors
        other_forms = [f for f in ["masu", "masen", "mashita", "masendeshita"] if f != form]
        for other_form in other_forms[:2]:  # Add up to 2 other forms of the same verb
            options.append(data[other_form])
        
        # Add conjugations of other verbs in the same form as distractors
        other_verbs = [v for v in verbs.keys() if v != verb]
        for other_verb in random.sample(other_verbs, min(2, len(other_verbs))):
            options.append(verbs[other_verb][form])
        
        # Ensure we have 4 unique options
        while len(set(options)) < 4 and len(options) < 4:
            # Add any other conjugation as a distractor
            random_verb = random.choice(list(verbs.keys()))
            random_form = random.choice(["masu", "masen", "mashita", "masendeshita"])
            options.append(verbs[random_verb][random_form])
        
        # Remove duplicates and ensure we have exactly 4 options
        options = list(set(options))[:4]
        while len(options) < 4:
            options.append(random.choice(list(data.values())))
        
        random.shuffle(options)
        
        form_descriptions = {
            "masu": "present affirmative",
            "masen": "present negative",
            "mashita": "past affirmative",
            "masendeshita": "past negative"
        }
        
        return {
            "type": "verb_conjugation",
            "question": f"Conjugate the verb '{verb}' ({data['meaning']}) into the {form_descriptions[form]} form",
            "options": options,
            "answer": correct_answer,
            "verb_type": data["type"],
            "explanation": f"The {form_descriptions[form]} form of '{verb}' is '{correct_answer}'"
        }
    
    def generate_reading_comprehension_exercise(self) -> Dict[str, Any]:
        """Generate a reading comprehension exercise"""
        # Simple reading passages with questions
        passages = [
            {
                "text": "私の名前は田中です。日本人です。二十歳です。東京に住んでいます。大学生です。日本語と英語を勉強しています。",
                "question": "田中さんは何歳ですか？",
                "options": ["十歳です", "二十歳です", "三十歳です", "四十歳です"],
                "answer": "二十歳です",
                "explanation": "The passage states '二十歳です' which means 'I am 20 years old.'"
            },
            {
                "text": "今日は土曜日です。天気がいいです。私は公園に行きます。友達と会います。一緒に昼ごはんを食べます。それから、映画を見ます。",
                "question": "この人は、誰と会いますか？",
                "options": ["先生と会います", "家族と会います", "友達と会います", "一人です"],
                "answer": "友達と会います",
                "explanation": "The passage states '友達と会います' which means 'I will meet with friends.'"
            }
        ]
        
        return random.choice(passages)
    
    def generate_exercise(self, practice_type: str, difficulty: str, syllabary_data: Dict = None) -> Dict[str, Any]:
        """Generate an exercise based on the practice type and difficulty"""
        if practice_type == "kana_recognition" and syllabary_data:
            syllabary_type = "hiragana" if "あ" in str(syllabary_data.values()) else "katakana"
            return self.generate_kana_recognition_exercise(syllabary_type, syllabary_data)
        
        elif practice_type == "kana_matching" and isinstance(syllabary_data, dict) and len(syllabary_data) == 2:
            return self.generate_kana_matching_exercise(syllabary_data["hiragana"], syllabary_data["katakana"])
        
        elif practice_type in ["simple_vocabulary", "vocabulary_categories"]:
            return self.generate_vocabulary_exercise(difficulty)
        
        elif practice_type == "dialogue_comprehension":
            return self.generate_dialogue_comprehension()
        
        elif practice_type == "grammar_application":
            return self.generate_grammar_exercise()
        
        elif practice_type == "sentence_creation":
            return self.generate_sentence_creation_exercise()
        
        elif practice_type == "verb_conjugation":
            return self.generate_verb_conjugation_exercise()
        
        elif practice_type == "reading_comprehension":
            return self.generate_reading_comprehension_exercise()
        
        elif practice_type == "listen_and_choose":
            return self.generate_listen_and_choose_exercise()
        
        elif practice_type == "listening_comprehension":
            return self.generate_listening_comprehension_exercise()
        
        elif practice_type == "speech_practice":
            return self.generate_speech_practice_exercise()
        
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
        # In a real implementation, this would store data in a database
        print(f"Recording practice result for user {user_id}: {practice_type} - {'Success' if success else 'Failure'}")
        # Additional tracking logic would go here
        
    def get_recommended_practice(self, user_id: str, difficulty: str) -> str:
        """Get a recommended practice type based on user performance"""
        # In a real implementation, this would analyze user data to recommend
        # appropriate practice types. For now, return a random one.
        return random.choice(self.practice_types.get(difficulty.lower(), []))
    
    def generate_listen_and_choose_exercise(self) -> Dict[str, Any]:
        """Generate a listening exercise for beginners where they hear a word and pick its meaning"""
        # Choose a random category
        category = random.choice(list(self.vocabulary.keys()))
        # Choose a random word from that category
        word, data = random.choice(list(self.vocabulary[category].items()))
        
        # Create options (1 correct + 3 random different options)
        options = [data["meaning"]]
        all_meanings = [item["meaning"] for cat in self.vocabulary.values() 
                       for item in cat.values() if item["meaning"] != data["meaning"]]
        options.extend(random.sample(all_meanings, min(3, len(all_meanings))))
        
        # Shuffle options
        random.shuffle(options)
        
        return {
            "type": "listen_and_choose",
            "audio_word": word,  # In real implementation, this would be a path to an audio file
            "question": "Listen and select the meaning of the word",
            "japanese_text": word,  # Show Japanese text for learning purposes
            "options": options,
            "answer": data["meaning"],
            "category": category,
            "explanation": f"The word '{word}' means '{data['meaning']}' in English"
        }
    
    def generate_listening_comprehension_exercise(self) -> Dict[str, Any]:
        """Generate a listening comprehension exercise for intermediate level"""
        # Get a suitable sentence
        if len(self.sentences["intermediate"]) > 0:
            sentence = random.choice(self.sentences["intermediate"])
            text = sentence["text"]
            translation = sentence.get("translation", "")
            
            # Create a question about the sentence
            question = "What is this sentence about?"
            
            # Create options (1 correct + 3 distractors)
            # In a real implementation, these would be more sophisticated
            correct_option = translation if translation else "Basic statement or greeting"
            
            options = [correct_option]
            
            # Create some plausible but incorrect options
            distractors = [
                "Asking for directions",
                "Talking about the weather",
                "Introducing oneself",
                "Making an appointment",
                "Ordering food",
                "Discussing a hobby"
            ]
            
            # Remove the correct answer if it's similar to any distractor
            filtered_distractors = [d for d in distractors if not 
                                   (d.lower() in correct_option.lower() or correct_option.lower() in d.lower())]
            
            options.extend(random.sample(filtered_distractors, min(3, len(filtered_distractors))))
            options = options[:4]  # Ensure we have exactly 4 options
            
            random.shuffle(options)
            
            return {
                "type": "listening_comprehension",
                "audio_sentence": text,  # In real implementation, this would be a path to an audio file
                "japanese_text": text,  # Show Japanese text for learning purposes
                "question": question,
                "options": options,
                "answer": correct_option,
                "translation": translation,
                "explanation": f"The sentence '{text}' means '{translation}'"
            }
        
        # Fallback if no suitable sentences
        return {
            "type": "listening_comprehension",
            "audio_sentence": "こんにちは、元気ですか？",
            "japanese_text": "こんにちは、元気ですか？", 
            "question": "What is this sentence about?",
            "options": ["Greeting and asking how someone is", "Asking for directions", 
                       "Ordering food", "Talking about the weather"],
            "answer": "Greeting and asking how someone is",
            "translation": "Hello, how are you?",
            "explanation": "This is a common greeting asking how someone is feeling."
        }
    
    def generate_speech_practice_exercise(self) -> Dict[str, Any]:
        """Generate a speech practice exercise for advanced level"""
        # For advanced practice, use real sentences from Tatoeba
        if len(self.sentences["advanced"]) > 0:
            # Get a random sentence
            sentence = random.choice(self.sentences["advanced"])
            text = sentence["text"]
            translation = sentence.get("translation", "")
            
            # Generate pronunciation guidance (simplified for demo)
            # In a real implementation, this would be more sophisticated
            pronunciation_guidance = "Pay attention to intonation and rhythm"
            
            return {
                "type": "speech_practice",
                "prompt": "Try to pronounce this sentence:",
                "japanese_text": text,
                "reference_audio": text,  # In real implementation, this would be a path to an audio file
                "translation": translation,
                "pronunciation_guidance": pronunciation_guidance,
                "key_vocabulary": text.replace("。", "").replace("、", " ").split()[:3]  # First few words as key vocab
            }
        
        # Fallback to predefined phrases
        phrases = [
            {
                "text": "日本語を勉強するのは楽しいです。",
                "translation": "Studying Japanese is fun.",
                "pronunciation_guidance": "Focus on the rhythm of 楽しい (tanoshii)"
            },
            {
                "text": "来週、友達と京都に行きます。",
                "translation": "Next week, I will go to Kyoto with my friends.",
                "pronunciation_guidance": "Pay attention to the particles と and に"
            }
        ]
        
        selected = random.choice(phrases)
        return {
            "type": "speech_practice",
            "prompt": "Try to pronounce this sentence:",
            "japanese_text": selected["text"],
            "reference_audio": selected["text"],  # Would be audio file path in real implementation
            "translation": selected["translation"],
            "pronunciation_guidance": selected["pronunciation_guidance"],
            "key_vocabulary": selected["text"].replace("。", "").replace("、", " ").split()[:3]
        }