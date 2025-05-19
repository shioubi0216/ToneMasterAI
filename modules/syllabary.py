import pandas as pd
import random

class JapaneseSyllabary:
    def __init__(self):
        """Initialize the Japanese syllabary data structures"""
        # Initialize hiragana
        self.hiragana = {
            'a': {'symbol': 'あ', 'romaji': 'a'},
            'i': {'symbol': 'い', 'romaji': 'i'},
            'u': {'symbol': 'う', 'romaji': 'u'},
            'e': {'symbol': 'え', 'romaji': 'e'},
            'o': {'symbol': 'お', 'romaji': 'o'},
            'ka': {'symbol': 'か', 'romaji': 'ka'},
            'ki': {'symbol': 'き', 'romaji': 'ki'},
            'ku': {'symbol': 'く', 'romaji': 'ku'},
            'ke': {'symbol': 'け', 'romaji': 'ke'},
            'ko': {'symbol': 'こ', 'romaji': 'ko'},
            'sa': {'symbol': 'さ', 'romaji': 'sa'},
            'shi': {'symbol': 'し', 'romaji': 'shi'},
            'su': {'symbol': 'す', 'romaji': 'su'},
            'se': {'symbol': 'せ', 'romaji': 'se'},
            'so': {'symbol': 'そ', 'romaji': 'so'},
            'ta': {'symbol': 'た', 'romaji': 'ta'},
            'chi': {'symbol': 'ち', 'romaji': 'chi'},
            'tsu': {'symbol': 'つ', 'romaji': 'tsu'},
            'te': {'symbol': 'て', 'romaji': 'te'},
            'to': {'symbol': 'と', 'romaji': 'to'},
            'na': {'symbol': 'な', 'romaji': 'na'},
            'ni': {'symbol': 'に', 'romaji': 'ni'},
            'nu': {'symbol': 'ぬ', 'romaji': 'nu'},
            'ne': {'symbol': 'ね', 'romaji': 'ne'},
            'no': {'symbol': 'の', 'romaji': 'no'},
            'ha': {'symbol': 'は', 'romaji': 'ha'},
            'hi': {'symbol': 'ひ', 'romaji': 'hi'},
            'fu': {'symbol': 'ふ', 'romaji': 'fu'},
            'he': {'symbol': 'へ', 'romaji': 'he'},
            'ho': {'symbol': 'ほ', 'romaji': 'ho'},
            'ma': {'symbol': 'ま', 'romaji': 'ma'},
            'mi': {'symbol': 'み', 'romaji': 'mi'},
            'mu': {'symbol': 'む', 'romaji': 'mu'},
            'me': {'symbol': 'め', 'romaji': 'me'},
            'mo': {'symbol': 'も', 'romaji': 'mo'},
            'ya': {'symbol': 'や', 'romaji': 'ya'},
            'yu': {'symbol': 'ゆ', 'romaji': 'yu'},
            'yo': {'symbol': 'よ', 'romaji': 'yo'},
            'ra': {'symbol': 'ら', 'romaji': 'ra'},
            'ri': {'symbol': 'り', 'romaji': 'ri'},
            'ru': {'symbol': 'る', 'romaji': 'ru'},
            're': {'symbol': 'れ', 'romaji': 're'},
            'ro': {'symbol': 'ろ', 'romaji': 'ro'},
            'wa': {'symbol': 'わ', 'romaji': 'wa'},
            'o': {'symbol': 'を', 'romaji': 'o'},
            'n': {'symbol': 'ん', 'romaji': 'n'},
        }
        
        # Initialize katakana
        self.katakana = {
            'a': {'symbol': 'ア', 'romaji': 'a'},
            'i': {'symbol': 'イ', 'romaji': 'i'},
            'u': {'symbol': 'ウ', 'romaji': 'u'},
            'e': {'symbol': 'エ', 'romaji': 'e'},
            'o': {'symbol': 'オ', 'romaji': 'o'},
            'ka': {'symbol': 'カ', 'romaji': 'ka'},
            'ki': {'symbol': 'キ', 'romaji': 'ki'},
            'ku': {'symbol': 'ク', 'romaji': 'ku'},
            'ke': {'symbol': 'ケ', 'romaji': 'ke'},
            'ko': {'symbol': 'コ', 'romaji': 'ko'},
            'sa': {'symbol': 'サ', 'romaji': 'sa'},
            'shi': {'symbol': 'シ', 'romaji': 'shi'},
            'su': {'symbol': 'ス', 'romaji': 'su'},
            'se': {'symbol': 'セ', 'romaji': 'se'},
            'so': {'symbol': 'ソ', 'romaji': 'so'},
            'ta': {'symbol': 'タ', 'romaji': 'ta'},
            'chi': {'symbol': 'チ', 'romaji': 'chi'},
            'tsu': {'symbol': 'ツ', 'romaji': 'tsu'},
            'te': {'symbol': 'テ', 'romaji': 'te'},
            'to': {'symbol': 'ト', 'romaji': 'to'},
            'na': {'symbol': 'ナ', 'romaji': 'na'},
            'ni': {'symbol': 'ニ', 'romaji': 'ni'},
            'nu': {'symbol': 'ヌ', 'romaji': 'nu'},
            'ne': {'symbol': 'ネ', 'romaji': 'ne'},
            'no': {'symbol': 'ノ', 'romaji': 'no'},
            'ha': {'symbol': 'ハ', 'romaji': 'ha'},
            'hi': {'symbol': 'ヒ', 'romaji': 'hi'},
            'fu': {'symbol': 'フ', 'romaji': 'fu'},
            'he': {'symbol': 'ヘ', 'romaji': 'he'},
            'ho': {'symbol': 'ホ', 'romaji': 'ho'},
            'ma': {'symbol': 'マ', 'romaji': 'ma'},
            'mi': {'symbol': 'ミ', 'romaji': 'mi'},
            'mu': {'symbol': 'ム', 'romaji': 'mu'},
            'me': {'symbol': 'メ', 'romaji': 'me'},
            'mo': {'symbol': 'モ', 'romaji': 'mo'},
            'ya': {'symbol': 'ヤ', 'romaji': 'ya'},
            'yu': {'symbol': 'ユ', 'romaji': 'yu'},
            'yo': {'symbol': 'ヨ', 'romaji': 'yo'},
            'ra': {'symbol': 'ラ', 'romaji': 'ra'},
            'ri': {'symbol': 'リ', 'romaji': 'ri'},
            'ru': {'symbol': 'ル', 'romaji': 'ru'},
            're': {'symbol': 'レ', 'romaji': 're'},
            'ro': {'symbol': 'ロ', 'romaji': 'ro'},
            'wa': {'symbol': 'ワ', 'romaji': 'wa'},
            'wo': {'symbol': 'ヲ', 'romaji': 'wo'},
            'n': {'symbol': 'ン', 'romaji': 'n'},
            # Add more katakana characters as needed
        }
        
        # Define the syllabary structure for display
        self.structure = {
            'vowels': ['a', 'i', 'u', 'e', 'o'],
            'consonants': ['k', 's', 't', 'n', 'h', 'm', 'y', 'r', 'w']
        }
    
    def get_chart(self, syllabary_type):
        """Generate a chart for the specified syllabary type"""
        if syllabary_type not in ['hiragana', 'katakana']:
            raise ValueError("Syllabary type must be 'hiragana' or 'katakana'")
            
        data = self.hiragana if syllabary_type == 'hiragana' else self.katakana
        
        # Create a DataFrame for display
        chart_data = []
        for consonant in [''] + self.structure['consonants']:
            row = [consonant.upper()] if consonant else ['']
            for vowel in self.structure['vowels']:
                key = f"{consonant}{vowel}" if consonant else vowel
                if key in data:
                    row.append(f"{data[key]['symbol']} ({data[key]['romaji']})")
                else:
                    row.append('')
            chart_data.append(row)
            
        return pd.DataFrame(chart_data, columns=[''] + self.structure['vowels'])
        
    def get_random_character(self, syllabary_type):
        """Get a random character from the specified syllabary"""
        data = self.hiragana if syllabary_type == 'hiragana' else self.katakana
        key = random.choice(list(data.keys()))
        return {
            'key': key,
            'symbol': data[key]['symbol'],
            'romaji': data[key]['romaji']
        }
        
    def get_character(self, syllabary_type, key):
        """Get a specific character from the specified syllabary"""
        data = self.hiragana if syllabary_type == 'hiragana' else self.katakana
        if key not in data:
            raise ValueError(f"Character '{key}' not found in {syllabary_type}")
            
        return {
            'key': key,
            'symbol': data[key]['symbol'],
            'romaji': data[key]['romaji']
        }
