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
            # 基礎助詞 (Basic Particles)
            "は_です": {
                "pattern": "XはYです",
                "description": "X is Y",
                "examples": ["わたしは学生です", "これは本です"]
            },
            "は_じゃない": {
                "pattern": "XはYじゃない",
                "description": "X is not Y",
                "examples": ["これはペンじゃない", "これペンじゃない"]
            },
            "の_名詞": {
                "pattern": "XのY",
                "description": "X's Y / Y of X",
                "examples": ["わたしの本", "わたし本"]
            },
            "も_particle": {
                "pattern": "Xも",
                "description": "X too/also",
                "examples": ["わたしも学生です", "わたしは学生もです"]
            },
            
            # 存在動詞 (Existence Verbs)
            "に_あります": {
                "pattern": "XにYがあります",
                "description": "Y is in/at X (non-living)",
                "examples": ["部屋にテレビがあります", "部屋でテレビがあります"]
            },
            "に_います": {
                "pattern": "XにYがいます",
                "description": "Y is in/at X (living)",
                "examples": ["公園に人がいます", "公園で人がいます"]
            },
            
            # 動作動詞 (Action Verbs)
            "を_します": {
                "pattern": "Xをします",
                "description": "Do X",
                "examples": ["勉強をします", "勉強がします"]
            },
            "を_食べます": {
                "pattern": "Xを食べます",
                "description": "Eat X",
                "examples": ["パンを食べます", "パンが食べます"]
            },
            "を_飲みます": {
                "pattern": "Xを飲みます",
                "description": "Drink X",
                "examples": ["水を飲みます", "水に飲みます"]
            },
            "を_見ます": {
                "pattern": "Xを見ます",
                "description": "Look at/Watch X",
                "examples": ["テレビを見ます", "テレビが見ます"]
            },
            "を_聞きます": {
                "pattern": "Xを聞きます",
                "description": "Listen to X",
                "examples": ["音楽を聞きます", "音楽が聞きます"]
            },
            "を_読みます": {
                "pattern": "Xを読みます",
                "description": "Read X",
                "examples": ["本を読みます", "本が読みます"]
            },
            "を_書きます": {
                "pattern": "Xを書きます",
                "description": "Write X",
                "examples": ["手紙を書きます", "手紙が書きます"]
            },
            "を_買います": {
                "pattern": "Xを買います",
                "description": "Buy X",
                "examples": ["服を買います", "服が買います"]
            },
            
            # 移動動詞 (Movement Verbs)
            "に_行きます": {
                "pattern": "Xに行きます",
                "description": "Go to X",
                "examples": ["学校に行きます", "学校を行きます"]
            },
            "に_来ます": {
                "pattern": "Xに来ます",
                "description": "Come to X",
                "examples": ["家に来ます", "家を来ます"]
            },
            "に_帰ります": {
                "pattern": "Xに帰ります",
                "description": "Return to X",
                "examples": ["国に帰ります", "国を帰ります"]
            },
            "から_来ました": {
                "pattern": "Xから来ました",
                "description": "Came from X",
                "examples": ["日本から来ました", "日本に来ました"]
            },
            "まで_行きます": {
                "pattern": "Xまで行きます",
                "description": "Go as far as X",
                "examples": ["駅まで行きます", "駅から行きます"]
            },
            
            # 時間表現 (Time Expressions)
            "に_時間": {
                "pattern": "X時に",
                "description": "At X o'clock",
                "examples": ["三時に会います", "三時で会います"]
            },
            "から_まで": {
                "pattern": "XからYまで",
                "description": "From X to Y",
                "examples": ["九時から五時まで", "九時に五時まで"]
            },
            "前に": {
                "pattern": "Xの前に",
                "description": "Before X",
                "examples": ["昼ご飯の前に", "昼ご飯の後に"]
            },
            "後で": {
                "pattern": "Xの後で",
                "description": "After X",
                "examples": ["授業の後で", "授業の前で"]
            },
            
            # 場所の助詞 (Location Particles)
            "で_action": {
                "pattern": "Xで〜します",
                "description": "Do ~ at X",
                "examples": ["図書館で勉強します", "図書館に勉強します"]
            },
            "へ_direction": {
                "pattern": "Xへ行きます",
                "description": "Go towards X",
                "examples": ["東京へ行きます", "東京を行きます"]
            },
            
            # 形容詞 (Adjectives)
            "い_adjective": {
                "pattern": "Xは〜い",
                "description": "X is ~",
                "examples": ["今日は暑い", "今日は暑いです"]
            },
            "くない_negative": {
                "pattern": "〜くない",
                "description": "Not ~ (i-adjective)",
                "examples": ["高くない", "高いくない"]
            },
            "な_adjective": {
                "pattern": "Xは〜な",
                "description": "X is ~ (na-adjective)",
                "examples": ["彼は元気な人です", "彼は元気い人です"]
            },
            "じゃない_na_neg": {
                "pattern": "〜じゃない",
                "description": "Not ~ (na-adjective)",
                "examples": ["静かじゃない", "静かくない"]
            },
            
            # 疑問詞 (Question Words)
            "何_what": {
                "pattern": "Xは何ですか",
                "description": "What is X?",
                "examples": ["これは何ですか", "これ何ですか"]
            },
            "誰_who": {
                "pattern": "Xは誰ですか",
                "description": "Who is X?",
                "examples": ["あの人は誰ですか", "あの人誰ですか"]
            },
            "どこ_where": {
                "pattern": "Xはどこですか",
                "description": "Where is X?",
                "examples": ["トイレはどこですか", "トイレどこですか"]
            },
            "いつ_when": {
                "pattern": "いつXしますか",
                "description": "When do you X?",
                "examples": ["いつ来ますか", "いつに来ますか"]
            },
            "どう_how": {
                "pattern": "Xはどうですか",
                "description": "How is X?",
                "examples": ["日本はどうですか", "日本がどうですか"]
            },
            "いくら_how_much": {
                "pattern": "Xはいくらですか",
                "description": "How much is X?",
                "examples": ["これはいくらですか", "これがいくらですか"]
            },
            
            # 数量詞 (Counters)
            "つ_counter": {
                "pattern": "〜つ",
                "description": "General counter",
                "examples": ["りんごを三つください", "りんごを三ください"]
            },
            "人_counter": {
                "pattern": "〜人",
                "description": "People counter",
                "examples": ["学生が五人います", "学生が五ついます"]
            },
            "枚_counter": {
                "pattern": "〜枚",
                "description": "Flat objects counter",
                "examples": ["紙を二枚ください", "紙を二つください"]
            },
            "本_counter": {
                "pattern": "〜本",
                "description": "Long objects counter",
                "examples": ["ペンが三本あります", "ペンが三つあります"]
            },
            
            # 願望表現 (Desire Expressions)
            "たい_want": {
                "pattern": "〜たい",
                "description": "Want to ~",
                "examples": ["食べたいです", "食べるたいです"]
            },
            "ほしい_want_thing": {
                "pattern": "Xがほしい",
                "description": "Want X",
                "examples": ["新しい車がほしい", "新しい車をほしい"]
            },
            
            # 接続詞 (Conjunctions)
            "と_and": {
                "pattern": "XとY",
                "description": "X and Y",
                "examples": ["犬と猫", "犬も猫"]
            },
            "や_and_etc": {
                "pattern": "XやY",
                "description": "X and Y (etc.)",
                "examples": ["本や雑誌", "本と雑誌と"]
            },
            "から_because": {
                "pattern": "Xから、Y",
                "description": "Because X, Y",
                "examples": ["雨だから、行きません", "雨ので、行きません"]
            },
            "でも_but": {
                "pattern": "でも",
                "description": "But/However",
                "examples": ["でも、高いです", "しかし、高いです"]
            },
            
            # 過去形 (Past Tense)
            "ました_past": {
                "pattern": "〜ました",
                "description": "Past tense",
                "examples": ["食べました", "食べます"]
            },
            "でした_past_copula": {
                "pattern": "〜でした",
                "description": "Was/Were",
                "examples": ["学生でした", "学生だった"]
            },
            "かった_past_adj": {
                "pattern": "〜かった",
                "description": "Was ~ (i-adjective)",
                "examples": ["暑かった", "暑いかった"]
            },
            
            # 否定形 (Negative Forms)
            "ません_negative": {
                "pattern": "〜ません",
                "description": "Don't/Doesn't ~",
                "examples": ["行きません", "行かません"]
            },
            "ない_plain_neg": {
                "pattern": "〜ない",
                "description": "Don't ~ (plain)",
                "examples": ["食べない", "食べません"]
            },
            
            # 丁寧な表現 (Polite Expressions)
            "ください_please": {
                "pattern": "〜てください",
                "description": "Please ~",
                "examples": ["待ってください", "待つください"]
            },
            "ましょう_let's": {
                "pattern": "〜ましょう",
                "description": "Let's ~",
                "examples": ["行きましょう", "行こうましょう"]
            },
            "ませんか_invitation": {
                "pattern": "〜ませんか",
                "description": "Won't you ~?",
                "examples": ["一緒に行きませんか", "一緒に行きましょうか"]
            },
            
            # 能力・可能 (Ability/Possibility)
            "できる_can": {
                "pattern": "Xができる",
                "description": "Can do X",
                "examples": ["日本語ができる", "日本語をできる"]
            },
            "ことができる": {
                "pattern": "〜ことができる",
                "description": "Can/Be able to ~",
                "examples": ["泳ぐことができる", "泳ぐのができる"]
            },
            
            # 経験 (Experience)
            "たことがある": {
                "pattern": "〜たことがある",
                "description": "Have done ~",
                "examples": ["日本に行ったことがある", "日本に行くことがある"]
            },
            
            # 比較 (Comparison)
            "より_comparison": {
                "pattern": "XよりY",
                "description": "Y more than X",
                "examples": ["これよりあれが好き", "これからあれが好き"]
            },
            "のほうが": {
                "pattern": "Xのほうが〜",
                "description": "X is more ~",
                "examples": ["夏のほうが暑い", "夏ほうが暑い"]
            },
            "いちばん": {
                "pattern": "いちばん〜",
                "description": "The most ~",
                "examples": ["いちばん好きな食べ物", "一番に好きな食べ物"]
            },
            
            # 理由・説明 (Reason/Explanation)
            "んです_explanation": {
                "pattern": "〜んです",
                "description": "It's that ~",
                "examples": ["忙しいんです", "忙しいです"]
            },
            "ので_because": {
                "pattern": "〜ので",
                "description": "Because ~",
                "examples": ["雨なので", "雨から"]
            },
            
            # 推量・予定 (Conjecture/Plans)
            "でしょう_probably": {
                "pattern": "〜でしょう",
                "description": "Probably ~",
                "examples": ["明日は晴れでしょう", "明日は晴れましょう"]
            },
            "つもり_intend": {
                "pattern": "〜つもり",
                "description": "Intend to ~",
                "examples": ["旅行に行くつもり", "旅行に行きたいつもり"]
            },
            "予定_plan": {
                "pattern": "〜予定です",
                "description": "Plan to ~",
                "examples": ["明日会う予定です", "明日会うの予定です"]
            },
            
            # 授受表現 (Giving/Receiving)
            "あげる_give": {
                "pattern": "XにYをあげる",
                "description": "Give Y to X",
                "examples": ["友達にプレゼントをあげる", "友達がプレゼントをあげる"]
            },
            "もらう_receive": {
                "pattern": "XからYをもらう",
                "description": "Receive Y from X",
                "examples": ["先生から本をもらう", "先生に本をもらう"]
            },
            "くれる_give_me": {
                "pattern": "XがYをくれる",
                "description": "X gives Y (to me)",
                "examples": ["母が手紙をくれる", "母に手紙をくれる"]
            },
            
            # 同時動作 (Simultaneous Actions)
            "ながら_while": {
                "pattern": "〜ながら",
                "description": "While doing ~",
                "examples": ["音楽を聞きながら勉強する", "音楽を聞いてながら勉強する"]
            },
            
            # 提案・意見 (Suggestions/Opinions)
            "たらどう": {
                "pattern": "〜たらどう",
                "description": "How about ~?",
                "examples": ["休んだらどう", "休むたらどう"]
            },
            "ばいい": {
                "pattern": "〜ばいい",
                "description": "Should ~",
                "examples": ["早く寝ればいい", "早く寝るばいい"]
            },
            
            # 禁止 (Prohibition)
            "てはいけない": {
                "pattern": "〜てはいけない",
                "description": "Must not ~",
                "examples": ["触ってはいけない", "触るてはいけない"]
            },
            "ないでください": {
                "pattern": "〜ないでください",
                "description": "Please don't ~",
                "examples": ["行かないでください", "行くないでください"]
            },
            
            # 義務 (Obligation)
            "なければならない": {
                "pattern": "〜なければならない",
                "description": "Must ~",
                "examples": ["勉強しなければならない", "勉強するなければならない"]
            },
            "なくちゃ": {
                "pattern": "〜なくちゃ",
                "description": "Have to ~ (casual)",
                "examples": ["行かなくちゃ", "行くなくちゃ"]
            },
            
            # 様態 (Manner)
            "そう_seems": {
                "pattern": "〜そう",
                "description": "Seems/Looks ~",
                "examples": ["おいしそう", "おいしいそう"]
            },
            "みたい_like": {
                "pattern": "〜みたい",
                "description": "Like/Seems like",
                "examples": ["学生みたい", "学生のみたい"]
            },
            "よう_like": {
                "pattern": "〜よう",
                "description": "Like/As if",
                "examples": ["子供のよう", "子供よう"]
            },
            
            # 条件 (Conditionals)
            "たら_if": {
                "pattern": "〜たら",
                "description": "If/When ~",
                "examples": ["雨が降ったら", "雨が降るたら"]
            },
            "ば_conditional": {
                "pattern": "〜ば",
                "description": "If ~ (conditional)",
                "examples": ["安ければ買う", "安いければ買う"]
            },
            
            # 時間関係 (Time Relations)
            "とき_when": {
                "pattern": "〜とき",
                "description": "When ~",
                "examples": ["暇なとき", "暇のとき"]
            },
            "前_before": {
                "pattern": "〜前",
                "description": "Before ~",
                "examples": ["食べる前", "食べた前"]
            },
            
            # その他 (Others)
            "ことがある_sometimes": {
                "pattern": "〜ことがある",
                "description": "Sometimes ~",
                "examples": ["忘れることがある", "忘れたことがある"]
            },
            "ために_for": {
                "pattern": "〜ために",
                "description": "For/In order to",
                "examples": ["健康のために", "健康にために"]
            },
            "について_about": {
                "pattern": "〜について",
                "description": "About ~",
                "examples": ["日本について話す", "日本において話す"]
            },
            "まだ_still": {
                "pattern": "まだ〜",
                "description": "Still/Not yet",
                "examples": ["まだ食べていない", "もう食べていない"]
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
        # Dialogue Comprehension Database (50 dialogues)
        dialogues = [
            # 1. 天気の会話
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
            
            # 2. 道案内
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
            },
            
            # 3. レストランでの注文
            {
                "dialogue": [
                    {"speaker": "店員", "text": "いらっしゃいませ。何名様ですか？"},
                    {"speaker": "客", "text": "二人です。"},
                    {"speaker": "店員", "text": "こちらへどうぞ。メニューです。"},
                    {"speaker": "客", "text": "ラーメンとギョーザをください。"}
                ],
                "question": "お客さんは何を注文しましたか？",
                "options": ["ラーメンだけ", "ギョーザだけ", "ラーメンとギョーザ", "まだ注文していない"],
                "answer": "ラーメンとギョーザ",
                "explanation": "お客さんは「ラーメンとギョーザをください」と言っています。"
            },
            
            # 4. 時間について
            {
                "dialogue": [
                    {"speaker": "A", "text": "今、何時ですか？"},
                    {"speaker": "B", "text": "三時半です。"},
                    {"speaker": "A", "text": "映画は何時からですか？"},
                    {"speaker": "B", "text": "四時からです。急ぎましょう。"}
                ],
                "question": "映画まであと何分ありますか？",
                "options": ["15分", "30分", "45分", "1時間"],
                "answer": "30分",
                "explanation": "今は3時半で、映画は4時からなので、あと30分です。"
            },
            
            # 5. 買い物
            {
                "dialogue": [
                    {"speaker": "客", "text": "このシャツはいくらですか？"},
                    {"speaker": "店員", "text": "それは三千円です。"},
                    {"speaker": "客", "text": "ちょっと高いですね。"},
                    {"speaker": "店員", "text": "今日はセールで、二千円になります。"}
                ],
                "question": "シャツの値段はいくらですか？",
                "options": ["千円", "二千円", "三千円", "四千円"],
                "answer": "二千円",
                "explanation": "店員さんは「今日はセールで、二千円になります」と言っています。"
            },
            
            # 6. 自己紹介
            {
                "dialogue": [
                    {"speaker": "A", "text": "はじめまして。田中です。"},
                    {"speaker": "B", "text": "はじめまして。スミスです。アメリカから来ました。"},
                    {"speaker": "A", "text": "日本語がお上手ですね。"},
                    {"speaker": "B", "text": "ありがとうございます。大学で二年間勉強しました。"}
                ],
                "question": "スミスさんはどのくらい日本語を勉強しましたか？",
                "options": ["半年", "一年", "二年", "三年"],
                "answer": "二年",
                "explanation": "スミスさんは「大学で二年間勉強しました」と言っています。"
            },
            
            # 7. 趣味について
            {
                "dialogue": [
                    {"speaker": "A", "text": "週末は何をしますか？"},
                    {"speaker": "B", "text": "たいてい本を読みます。"},
                    {"speaker": "A", "text": "どんな本が好きですか？"},
                    {"speaker": "B", "text": "ミステリー小説が一番好きです。"}
                ],
                "question": "Bさんの好きな本のジャンルは何ですか？",
                "options": ["恋愛小説", "ミステリー小説", "歴史小説", "SF小説"],
                "answer": "ミステリー小説",
                "explanation": "Bさんは「ミステリー小説が一番好きです」と言っています。"
            },
            
            # 8. 交通手段
            {
                "dialogue": [
                    {"speaker": "A", "text": "会社まで何で行きますか？"},
                    {"speaker": "B", "text": "電車で行きます。"},
                    {"speaker": "A", "text": "時間はどのくらいかかりますか？"},
                    {"speaker": "B", "text": "だいたい四十分ぐらいです。"}
                ],
                "question": "Bさんの通勤時間はどのくらいですか？",
                "options": ["20分", "30分", "40分", "50分"],
                "answer": "40分",
                "explanation": "Bさんは「だいたい四十分ぐらいです」と言っています。"
            },
            
            # 9. 家族について
            {
                "dialogue": [
                    {"speaker": "A", "text": "ご家族は何人ですか？"},
                    {"speaker": "B", "text": "五人家族です。"},
                    {"speaker": "A", "text": "お子さんはいらっしゃいますか？"},
                    {"speaker": "B", "text": "はい、息子が一人と娘が二人います。"}
                ],
                "question": "Bさんには子供が何人いますか？",
                "options": ["一人", "二人", "三人", "四人"],
                "answer": "三人",
                "explanation": "Bさんは「息子が一人と娘が二人います」と言っているので、合計三人です。"
            },
            
            # 10. 病院での会話
            {
                "dialogue": [
                    {"speaker": "医者", "text": "どうしましたか？"},
                    {"speaker": "患者", "text": "昨日から頭が痛いです。"},
                    {"speaker": "医者", "text": "熱はありますか？"},
                    {"speaker": "患者", "text": "はい、少しあります。"}
                ],
                "question": "患者さんの症状は何ですか？",
                "options": ["お腹が痛い", "頭が痛い", "歯が痛い", "足が痛い"],
                "answer": "頭が痛い",
                "explanation": "患者さんは「昨日から頭が痛いです」と言っています。"
            },
            
            # 11. 電話での約束
            {
                "dialogue": [
                    {"speaker": "A", "text": "もしもし、山田さんですか？"},
                    {"speaker": "B", "text": "はい、山田です。"},
                    {"speaker": "A", "text": "明日の会議は何時からですか？"},
                    {"speaker": "B", "text": "午前十時からです。場所は会議室Aです。"}
                ],
                "question": "会議はいつですか？",
                "options": ["今日の午前", "今日の午後", "明日の午前", "明日の午後"],
                "answer": "明日の午前",
                "explanation": "Bさんは「午前十時からです」と言い、Aさんが「明日の会議」と言っています。"
            },
            
            # 12. ホテルのチェックイン
            {
                "dialogue": [
                    {"speaker": "フロント", "text": "いらっしゃいませ。"},
                    {"speaker": "客", "text": "予約した田中です。"},
                    {"speaker": "フロント", "text": "確認いたします。シングルルームで二泊ですね。"},
                    {"speaker": "客", "text": "はい、そうです。"}
                ],
                "question": "田中さんは何泊しますか？",
                "options": ["一泊", "二泊", "三泊", "四泊"],
                "answer": "二泊",
                "explanation": "フロントの人は「シングルルームで二泊ですね」と確認しています。"
            },
            
            # 13. 学校での会話
            {
                "dialogue": [
                    {"speaker": "先生", "text": "宿題はやりましたか？"},
                    {"speaker": "学生", "text": "すみません、忘れました。"},
                    {"speaker": "先生", "text": "明日必ず持って来てください。"},
                    {"speaker": "学生", "text": "はい、わかりました。"}
                ],
                "question": "学生は何を忘れましたか？",
                "options": ["教科書", "ノート", "宿題", "ペン"],
                "answer": "宿題",
                "explanation": "先生が「宿題はやりましたか？」と聞き、学生は「忘れました」と答えています。"
            },
            
            # 14. スポーツについて
            {
                "dialogue": [
                    {"speaker": "A", "text": "スポーツは好きですか？"},
                    {"speaker": "B", "text": "はい、大好きです。"},
                    {"speaker": "A", "text": "何のスポーツをしますか？"},
                    {"speaker": "B", "text": "テニスと水泳をします。"}
                ],
                "question": "Bさんがするスポーツは何ですか？",
                "options": ["サッカーと野球", "テニスと水泳", "バスケとテニス", "水泳だけ"],
                "answer": "テニスと水泳",
                "explanation": "Bさんは「テニスと水泳をします」と言っています。"
            },
            
            # 15. 誕生日について
            {
                "dialogue": [
                    {"speaker": "A", "text": "誕生日はいつですか？"},
                    {"speaker": "B", "text": "四月十日です。"},
                    {"speaker": "A", "text": "もうすぐですね。"},
                    {"speaker": "B", "text": "はい、来週です。"}
                ],
                "question": "Bさんの誕生日はいつですか？",
                "options": ["三月十日", "四月十日", "五月十日", "六月十日"],
                "answer": "四月十日",
                "explanation": "Bさんは「四月十日です」と言っています。"
            },
            
            # 16. 週末の予定
            {
                "dialogue": [
                    {"speaker": "A", "text": "週末は何か予定がありますか？"},
                    {"speaker": "B", "text": "土曜日は友達と映画を見ます。"},
                    {"speaker": "A", "text": "日曜日は？"},
                    {"speaker": "B", "text": "日曜日は家でゆっくり休みます。"}
                ],
                "question": "Bさんは土曜日に何をしますか？",
                "options": ["買い物に行く", "映画を見る", "家で休む", "仕事をする"],
                "answer": "映画を見る",
                "explanation": "Bさんは「土曜日は友達と映画を見ます」と言っています。"
            },
            
            # 17. 仕事について
            {
                "dialogue": [
                    {"speaker": "A", "text": "お仕事は何ですか？"},
                    {"speaker": "B", "text": "会社員です。"},
                    {"speaker": "A", "text": "どんな会社ですか？"},
                    {"speaker": "B", "text": "コンピューター会社です。"}
                ],
                "question": "Bさんはどんな会社で働いていますか？",
                "options": ["銀行", "病院", "コンピューター会社", "学校"],
                "answer": "コンピューター会社",
                "explanation": "Bさんは「コンピューター会社です」と言っています。"
            },
            
            # 18. 食事の好み
            {
                "dialogue": [
                    {"speaker": "A", "text": "日本料理は好きですか？"},
                    {"speaker": "B", "text": "はい、とても好きです。"},
                    {"speaker": "A", "text": "何が一番好きですか？"},
                    {"speaker": "B", "text": "寿司が一番好きです。でも、納豆は苦手です。"}
                ],
                "question": "Bさんが苦手な食べ物は何ですか？",
                "options": ["寿司", "天ぷら", "納豆", "ラーメン"],
                "answer": "納豆",
                "explanation": "Bさんは「納豆は苦手です」と言っています。"
            },
            
            # 19. 季節について
            {
                "dialogue": [
                    {"speaker": "A", "text": "日本の季節で何が一番好きですか？"},
                    {"speaker": "B", "text": "春が一番好きです。"},
                    {"speaker": "A", "text": "どうしてですか？"},
                    {"speaker": "B", "text": "桜がとてもきれいだからです。"}
                ],
                "question": "Bさんが春を好きな理由は何ですか？",
                "options": ["暖かいから", "桜がきれいだから", "雪が降るから", "紅葉がきれいだから"],
                "answer": "桜がきれいだから",
                "explanation": "Bさんは「桜がとてもきれいだからです」と言っています。"
            },
            
            # 20. 旅行について
            {
                "dialogue": [
                    {"speaker": "A", "text": "夏休みはどこか行きましたか？"},
                    {"speaker": "B", "text": "はい、京都に行きました。"},
                    {"speaker": "A", "text": "どうでしたか？"},
                    {"speaker": "B", "text": "お寺がたくさんあって、とても良かったです。"}
                ],
                "question": "Bさんは京都で何を見ましたか？",
                "options": ["海", "山", "お寺", "城"],
                "answer": "お寺",
                "explanation": "Bさんは「お寺がたくさんあって」と言っています。"
            },
            
            # 21. 勉強について
            {
                "dialogue": [
                    {"speaker": "A", "text": "日本語の勉強はどうですか？"},
                    {"speaker": "B", "text": "楽しいですが、漢字が難しいです。"},
                    {"speaker": "A", "text": "毎日勉強していますか？"},
                    {"speaker": "B", "text": "はい、一日二時間ぐらい勉強しています。"}
                ],
                "question": "Bさんは一日何時間日本語を勉強していますか？",
                "options": ["一時間", "二時間", "三時間", "四時間"],
                "answer": "二時間",
                "explanation": "Bさんは「一日二時間ぐらい勉強しています」と言っています。"
            },
            
            # 22. ペットについて
            {
                "dialogue": [
                    {"speaker": "A", "text": "ペットを飼っていますか？"},
                    {"speaker": "B", "text": "はい、犬を飼っています。"},
                    {"speaker": "A", "text": "何という名前ですか？"},
                    {"speaker": "B", "text": "ポチです。もう五歳になりました。"}
                ],
                "question": "Bさんのペットは何歳ですか？",
                "options": ["三歳", "四歳", "五歳", "六歳"],
                "answer": "五歳",
                "explanation": "Bさんは「もう五歳になりました」と言っています。"
            },
            
            # 23. 住まいについて
            {
                "dialogue": [
                    {"speaker": "A", "text": "どこに住んでいますか？"},
                    {"speaker": "B", "text": "東京に住んでいます。"},
                    {"speaker": "A", "text": "アパートですか、家ですか？"},
                    {"speaker": "B", "text": "小さいアパートです。駅から歩いて十分です。"}
                ],
                "question": "Bさんの家から駅まで何分かかりますか？",
                "options": ["五分", "十分", "十五分", "二十分"],
                "answer": "十分",
                "explanation": "Bさんは「駅から歩いて十分です」と言っています。"
            },
            
            # 24. 服装について
            {
                "dialogue": [
                    {"speaker": "A", "text": "素敵なコートですね。"},
                    {"speaker": "B", "text": "ありがとうございます。"},
                    {"speaker": "A", "text": "どこで買いましたか？"},
                    {"speaker": "B", "text": "デパートのセールで買いました。半額でした。"}
                ],
                "question": "Bさんはコートをどこで買いましたか？",
                "options": ["オンライン", "専門店", "デパート", "アウトレット"],
                "answer": "デパート",
                "explanation": "Bさんは「デパートのセールで買いました」と言っています。"
            },
            
            # 25. 音楽について
            {
                "dialogue": [
                    {"speaker": "A", "text": "音楽は聞きますか？"},
                    {"speaker": "B", "text": "はい、よく聞きます。"},
                    {"speaker": "A", "text": "どんな音楽が好きですか？"},
                    {"speaker": "B", "text": "J-POPとクラシックが好きです。"}
                ],
                "question": "Bさんの好きな音楽は何ですか？",
                "options": ["ロックとジャズ", "J-POPとクラシック", "演歌とロック", "ジャズとクラシック"],
                "answer": "J-POPとクラシック",
                "explanation": "Bさんは「J-POPとクラシックが好きです」と言っています。"
            },
            
            # 26. 休日の過ごし方
            {
                "dialogue": [
                    {"speaker": "A", "text": "休みの日は何をしていますか？"},
                    {"speaker": "B", "text": "朝はジョギングをします。"},
                    {"speaker": "A", "text": "午後は？"},
                    {"speaker": "B", "text": "午後は友達とカフェでおしゃべりします。"}
                ],
                "question": "Bさんは朝何をしますか？",
                "options": ["カフェに行く", "ジョギングする", "友達に会う", "家で寝る"],
                "answer": "ジョギングする",
                "explanation": "Bさんは「朝はジョギングをします」と言っています。"
            },
            
            # 27. 飲み物について
            {
                "dialogue": [
                    {"speaker": "A", "text": "何か飲みますか？"},
                    {"speaker": "B", "text": "お茶をお願いします。"},
                    {"speaker": "A", "text": "緑茶と紅茶、どちらがいいですか？"},
                    {"speaker": "B", "text": "緑茶がいいです。"}
                ],
                "question": "Bさんは何を飲みますか？",
                "options": ["コーヒー", "紅茶", "緑茶", "ジュース"],
                "answer": "緑茶",
                "explanation": "Bさんは「緑茶がいいです」と言っています。"
            },
            
            # 28. 料理について
            {
                "dialogue": [
                    {"speaker": "A", "text": "料理はできますか？"},
                    {"speaker": "B", "text": "少しできます。"},
                    {"speaker": "A", "text": "何が作れますか？"},
                    {"speaker": "B", "text": "カレーとパスタなら作れます。"}
                ],
                "question": "Bさんが作れる料理は何ですか？",
                "options": ["寿司とラーメン", "カレーとパスタ", "天ぷらとそば", "おにぎりと味噌汁"],
                "answer": "カレーとパスタ",
                "explanation": "Bさんは「カレーとパスタなら作れます」と言っています。"
            },
            
            # 29. 映画について
            {
                "dialogue": [
                    {"speaker": "A", "text": "昨日、映画を見ましたか？"},
                    {"speaker": "B", "text": "はい、見ました。"},
                    {"speaker": "A", "text": "何を見ましたか？"},
                    {"speaker": "B", "text": "新しいアクション映画を見ました。とても面白かったです。"}
                ],
                "question": "Bさんが見た映画のジャンルは何ですか？",
                "options": ["ホラー", "コメディー", "アクション", "ロマンス"],
                "answer": "アクション",
                "explanation": "Bさんは「新しいアクション映画を見ました」と言っています。"
            },
            
            # 30. 郵便局で
            {
                "dialogue": [
                    {"speaker": "客", "text": "この手紙をアメリカに送りたいです。"},
                    {"speaker": "局員", "text": "航空便ですか、船便ですか？"},
                    {"speaker": "客", "text": "早く着く方がいいです。"},
                    {"speaker": "局員", "text": "では、航空便ですね。五百円です。"}
                ],
                "question": "手紙の送料はいくらですか？",
                "options": ["三百円", "四百円", "五百円", "六百円"],
                "answer": "五百円",
                "explanation": "局員さんは「五百円です」と言っています。"
            },
            
            # 31. 図書館で
            {
                "dialogue": [
                    {"speaker": "A", "text": "図書館は何時に開きますか？"},
                    {"speaker": "B", "text": "朝九時に開きます。"},
                    {"speaker": "A", "text": "何時まで開いていますか？"},
                    {"speaker": "B", "text": "夜八時まで開いています。"}
                ],
                "question": "図書館は何時間開いていますか？",
                "options": ["九時間", "十時間", "十一時間", "十二時間"],
                "answer": "十一時間",
                "explanation": "朝九時から夜八時まで、十一時間開いています。"
            },
            
            # 32. タクシーで
            {
                "dialogue": [
                    {"speaker": "運転手", "text": "どちらまで？"},
                    {"speaker": "客", "text": "東京駅までお願いします。"},
                    {"speaker": "運転手", "text": "はい、わかりました。"},
                    {"speaker": "客", "text": "急いでいるんですが、何分ぐらいかかりますか？"},
                    {"speaker": "運転手", "text": "二十分ぐらいですね。"}
                ],
                "question": "東京駅まで何分かかりますか？",
                "options": ["十分", "十五分", "二十分", "二十五分"],
                "answer": "二十分",
                "explanation": "運転手さんは「二十分ぐらいですね」と言っています。"
            },
            
            # 33. 銀行で
            {
                "dialogue": [
                    {"speaker": "客", "text": "お金を引き出したいです。"},
                    {"speaker": "行員", "text": "カードをお持ちですか？"},
                    {"speaker": "客", "text": "はい、これです。"},
                    {"speaker": "行員", "text": "ATMは右側にあります。"}
                ],
                "question": "ATMはどこにありますか？",
                "options": ["左側", "右側", "二階", "外"],
                "answer": "右側",
                "explanation": "行員さんは「ATMは右側にあります」と言っています。"
            },
            
            # 34. 美容院で
            {
                "dialogue": [
                    {"speaker": "美容師", "text": "今日はどうしますか？"},
                    {"speaker": "客", "text": "髪を短く切ってください。"},
                    {"speaker": "美容師", "text": "どのくらい短くしますか？"},
                    {"speaker": "客", "text": "五センチぐらい切ってください。"}
                ],
                "question": "お客さんは髪をどのくらい切りますか？",
                "options": ["三センチ", "四センチ", "五センチ", "六センチ"],
                "answer": "五センチ",
                "explanation": "お客さんは「五センチぐらい切ってください」と言っています。"
            },
            
            # 35. コンビニで
            {
                "dialogue": [
                    {"speaker": "店員", "text": "いらっしゃいませ。"},
                    {"speaker": "客", "text": "お弁当を温めてください。"},
                    {"speaker": "店員", "text": "はい、かしこまりました。"},
                    {"speaker": "客", "text": "お箸もください。"},
                    {"speaker": "店員", "text": "お箸は一膳でよろしいですか？"}
                ],
                "question": "お客さんは何を頼みましたか？",
                "options": ["お弁当を買う", "お弁当を温める", "お箸を買う", "袋をもらう"],
                "answer": "お弁当を温める",
                "explanation": "お客さんは「お弁当を温めてください」と言っています。"
            },
            
            # 36. 空港で
            {
                "dialogue": [
                    {"speaker": "係員", "text": "パスポートを見せてください。"},
                    {"speaker": "旅行者", "text": "はい、どうぞ。"},
                    {"speaker": "係員", "text": "お荷物はいくつですか？"},
                    {"speaker": "旅行者", "text": "スーツケース一つと手荷物です。"}
                ],
                "question": "旅行者の荷物は全部でいくつですか？",
                "options": ["一つ", "二つ", "三つ", "四つ"],
                "answer": "二つ",
                "explanation": "旅行者は「スーツケース一つと手荷物」と言っているので、二つです。"
            },
            
            # 37. 写真について
            {
                "dialogue": [
                    {"speaker": "A", "text": "きれいな写真ですね。どこですか？"},
                    {"speaker": "B", "text": "富士山です。"},
                    {"speaker": "A", "text": "いつ撮りましたか？"},
                    {"speaker": "B", "text": "去年の夏に撮りました。"}
                ],
                "question": "写真はいつ撮られましたか？",
                "options": ["今年の春", "今年の夏", "去年の春", "去年の夏"],
                "answer": "去年の夏",
                "explanation": "Bさんは「去年の夏に撮りました」と言っています。"
            },
            
            # 38. パーティーの準備
            {
                "dialogue": [
                    {"speaker": "A", "text": "パーティーは何人来ますか？"},
                    {"speaker": "B", "text": "十五人ぐらい来ると思います。"},
                    {"speaker": "A", "text": "飲み物は足りますか？"},
                    {"speaker": "B", "text": "もう少し買った方がいいですね。"}
                ],
                "question": "パーティーには何人来ますか？",
                "options": ["十人", "十五人", "二十人", "二十五人"],
                "answer": "十五人",
                "explanation": "Bさんは「十五人ぐらい来ると思います」と言っています。"
            },
            
            # 39. 引っ越しについて
            {
                "dialogue": [
                    {"speaker": "A", "text": "新しい家はどうですか？"},
                    {"speaker": "B", "text": "とても広くて明るいです。"},
                    {"speaker": "A", "text": "駅から近いですか？"},
                    {"speaker": "B", "text": "はい、歩いて五分です。"}
                ],
                "question": "新しい家の特徴は何ですか？",
                "options": ["狭くて暗い", "広くて明るい", "古くて小さい", "新しくて高い"],
                "answer": "広くて明るい",
                "explanation": "Bさんは「とても広くて明るいです」と言っています。"
            },
            
            # 40. 試験について
            {
                "dialogue": [
                    {"speaker": "A", "text": "日本語の試験はどうでしたか？"},
                    {"speaker": "B", "text": "聞き取りは簡単でしたが、文法が難しかったです。"},
                    {"speaker": "A", "text": "結果はいつ分かりますか？"},
                    {"speaker": "B", "text": "来月の初めに分かります。"}
                ],
                "question": "試験で難しかった部分は何ですか？",
                "options": ["聞き取り", "文法", "読解", "作文"],
                "answer": "文法",
                "explanation": "Bさんは「文法が難しかったです」と言っています。"
            },
            
            # 41. 友達との待ち合わせ
            {
                "dialogue": [
                    {"speaker": "A", "text": "明日、どこで会いましょうか？"},
                    {"speaker": "B", "text": "駅の改札口はどうですか？"},
                    {"speaker": "A", "text": "いいですね。何時にしましょうか？"},
                    {"speaker": "B", "text": "二時はどうですか？"}
                ],
                "question": "待ち合わせ場所はどこですか？",
                "options": ["カフェ", "公園", "駅の改札口", "図書館"],
                "answer": "駅の改札口",
                "explanation": "Bさんは「駅の改札口はどうですか？」と提案し、Aさんが同意しています。"
            },
            
            # 42. 忘れ物
            {
                "dialogue": [
                    {"speaker": "A", "text": "すみません、傘を忘れました。"},
                    {"speaker": "B", "text": "どこに忘れましたか？"},
                    {"speaker": "A", "text": "電車の中だと思います。"},
                    {"speaker": "B", "text": "駅の忘れ物センターに聞いてみてください。"}
                ],
                "question": "Aさんは何を忘れましたか？",
                "options": ["財布", "携帯", "傘", "鍵"],
                "answer": "傘",
                "explanation": "Aさんは「傘を忘れました」と言っています。"
            },
            
            # 43. スーパーでの会話
            {
                "dialogue": [
                    {"speaker": "A", "text": "今日は野菜が安いですね。"},
                    {"speaker": "B", "text": "本当ですね。トマトが特に安いです。"},
                    {"speaker": "A", "text": "一個いくらですか？"},
                    {"speaker": "B", "text": "百円です。普段は百五十円ぐらいです。"}
                ],
                "question": "トマトの今日の値段はいくらですか？",
                "options": ["五十円", "百円", "百五十円", "二百円"],
                "answer": "百円",
                "explanation": "Bさんは「百円です」と言っています。"
            },
            
            # 44. 薬局で
            {
                "dialogue": [
                    {"speaker": "薬剤師", "text": "どうされましたか？"},
                    {"speaker": "客", "text": "風邪薬をください。"},
                    {"speaker": "薬剤師", "text": "熱はありますか？"},
                    {"speaker": "客", "text": "いいえ、咳と鼻水だけです。"}
                ],
                "question": "お客さんの症状は何ですか？",
                "options": ["熱と頭痛", "咳と鼻水", "腹痛と吐き気", "めまいと疲れ"],
                "answer": "咳と鼻水",
                "explanation": "お客さんは「咳と鼻水だけです」と言っています。"
            },
            
            # 45. 観光案内所で
            {
                "dialogue": [
                    {"speaker": "観光客", "text": "この近くに有名な観光地はありますか？"},
                    {"speaker": "案内員", "text": "はい、お城と美術館があります。"},
                    {"speaker": "観光客", "text": "お城までどのくらいかかりますか？"},
                    {"speaker": "案内員", "text": "バスで十五分ぐらいです。"}
                ],
                "question": "お城まで何で行きますか？",
                "options": ["電車", "バス", "タクシー", "歩いて"],
                "answer": "バス",
                "explanation": "案内員さんは「バスで十五分ぐらいです」と言っています。"
            },
            
            # 46. 天気予報
            {
                "dialogue": [
                    {"speaker": "A", "text": "明日の天気予報を見ましたか？"},
                    {"speaker": "B", "text": "はい、見ました。"},
                    {"speaker": "A", "text": "どんな天気ですか？"},
                    {"speaker": "B", "text": "午前中は晴れですが、午後から雨が降るそうです。"}
                ],
                "question": "明日の午後の天気は？",
                "options": ["晴れ", "曇り", "雨", "雪"],
                "answer": "雨",
                "explanation": "Bさんは「午後から雨が降るそうです」と言っています。"
            },
            
            # 47. カラオケで
            {
                "dialogue": [
                    {"speaker": "A", "text": "カラオケは好きですか？"},
                    {"speaker": "B", "text": "はい、月に一回ぐらい行きます。"},
                    {"speaker": "A", "text": "何時間ぐらい歌いますか？"},
                    {"speaker": "B", "text": "だいたい二時間ぐらいです。"}
                ],
                "question": "Bさんはカラオケでどのくらい歌いますか？",
                "options": ["一時間", "二時間", "三時間", "四時間"],
                "answer": "二時間",
                "explanation": "Bさんは「だいたい二時間ぐらいです」と言っています。"
            },
            
            # 48. 新年の挨拶
            {
                "dialogue": [
                    {"speaker": "A", "text": "あけましておめでとうございます。"},
                    {"speaker": "B", "text": "おめでとうございます。今年もよろしくお願いします。"},
                    {"speaker": "A", "text": "お正月はどう過ごしましたか？"},
                    {"speaker": "B", "text": "家族と一緒におせち料理を食べました。"}
                ],
                "question": "Bさんはお正月に何をしましたか？",
                "options": ["旅行に行った", "友達と会った", "おせち料理を食べた", "初詣に行った"],
                "answer": "おせち料理を食べた",
                "explanation": "Bさんは「家族と一緒におせち料理を食べました」と言っています。"
            },
            
            # 49. 遅刻の連絡
            {
                "dialogue": [
                    {"speaker": "A", "text": "もしもし、田中です。"},
                    {"speaker": "B", "text": "すみません、電車が遅れています。"},
                    {"speaker": "A", "text": "何分ぐらい遅れそうですか？"},
                    {"speaker": "B", "text": "十五分ぐらい遅れます。申し訳ありません。"}
                ],
                "question": "Bさんはなぜ遅れていますか？",
                "options": ["寝坊した", "電車が遅れている", "道に迷った", "忘れ物をした"],
                "answer": "電車が遅れている",
                "explanation": "Bさんは「電車が遅れています」と言っています。"
            },
            
            # 50. コンサートについて
            {
                "dialogue": [
                    {"speaker": "A", "text": "昨日のコンサートはどうでしたか？"},
                    {"speaker": "B", "text": "とても良かったです。"},
                    {"speaker": "A", "text": "何時に終わりましたか？"},
                    {"speaker": "B", "text": "九時半に終わりました。二時間半のコンサートでした。"}
                ],
                "question": "コンサートは何時間でしたか？",
                "options": ["一時間半", "二時間", "二時間半", "三時間"],
                "answer": "二時間半",
                "explanation": "Bさんは「二時間半のコンサートでした」と言っています。"
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
