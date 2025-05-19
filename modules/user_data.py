import sqlite3
import os
import json
from datetime import datetime
import random

class UserProgressManager:
    def __init__(self, db_path=None):
        """Initialize the user progress manager"""
        # Default to local file-based storage for MVP
        self.db_path = db_path or "user_progress.json"
        
        # Initialize data structure if file doesn't exist
        if not os.path.exists(self.db_path):
            self.progress_data = {
                "hiragana": {
                    "learned": [],
                    "mastered": [],
                    "needs_review": []
                },
                "katakana": {
                    "learned": [],
                    "mastered": [],
                    "needs_review": []
                },
                "statistics": {
                    "correct_answers": 0,
                    "total_attempts": 0,
                    "study_sessions": [],
                    "last_active": None
                },
                "settings": {
                    "daily_goal_minutes": 15,
                    "difficulty": "beginner"
                }
            }
            self.save_progress()
        else:
            self.load_progress()
    
    def load_progress(self):
        """Load user progress from file"""
        try:
            with open(self.db_path, 'r') as f:
                self.progress_data = json.load(f)
        except Exception as e:
            print(f"Error loading progress data: {e}")
            # Initialize with default if loading fails
            self.progress_data = {
                "hiragana": {"learned": [], "mastered": [], "needs_review": []},
                "katakana": {"learned": [], "mastered": [], "needs_review": []},
                "statistics": {"correct_answers": 0, "total_attempts": 0, "study_sessions": [], "last_active": None},
                "settings": {"daily_goal_minutes": 15, "difficulty": "beginner"}
            }
    
    def save_progress(self):
        """Save user progress to file"""
        try:
            with open(self.db_path, 'w') as f:
                json.dump(self.progress_data, f)
        except Exception as e:
            print(f"Error saving progress data: {e}")
    
    def record_success(self, syllabary_type, character):
        """Record a successful answer"""
        self.progress_data["statistics"]["correct_answers"] += 1
        self.progress_data["statistics"]["total_attempts"] += 1
        
        # Update character status
        if character not in self.progress_data[syllabary_type]["learned"]:
            self.progress_data[syllabary_type]["learned"].append(character)
            
        if character in self.progress_data[syllabary_type]["needs_review"]:
            self.progress_data[syllabary_type]["needs_review"].remove(character)
            
        # Check if character should be marked as mastered (simplified logic for MVP)
        if character not in self.progress_data[syllabary_type]["mastered"]:
            self.progress_data[syllabary_type]["mastered"].append(character)
            
        self.progress_data["statistics"]["last_active"] = datetime.now().isoformat()
        self.save_progress()
    
    def record_mistake(self, syllabary_type, character):
        """Record an incorrect answer"""
        self.progress_data["statistics"]["total_attempts"] += 1
        
        # Update character status
        if character not in self.progress_data[syllabary_type]["learned"]:
            self.progress_data[syllabary_type]["learned"].append(character)
            
        if character not in self.progress_data[syllabary_type]["needs_review"]:
            self.progress_data[syllabary_type]["needs_review"].append(character)
            
        # Remove from mastered if previously mastered
        if character in self.progress_data[syllabary_type]["mastered"]:
            self.progress_data[syllabary_type]["mastered"].remove(character)
            
        self.progress_data["statistics"]["last_active"] = datetime.now().isoformat()
        self.save_progress()
    
    def get_next_review_characters(self, syllabary_type, count=5):
        """Get characters that need review"""
        needs_review = self.progress_data[syllabary_type]["needs_review"]
        return needs_review[:count]
    
    def get_progress_summary(self):
        """Get a summary of the user's progress"""
        hiragana_progress = len(self.progress_data["hiragana"]["mastered"])
        katakana_progress = len(self.progress_data["katakana"]["mastered"])
        
        return {
            "hiragana_learned": len(self.progress_data["hiragana"]["learned"]),
            "hiragana_mastered": hiragana_progress,
            "katakana_learned": len(self.progress_data["katakana"]["learned"]),
            "katakana_mastered": katakana_progress,
            "accuracy": self.calculate_accuracy(),
            "last_active": self.progress_data["statistics"]["last_active"]
        }
    
    def calculate_accuracy(self):
        """Calculate the user's overall accuracy"""
        total = self.progress_data["statistics"]["total_attempts"]
        correct = self.progress_data["statistics"]["correct_answers"]
        
        if total == 0:
            return 0
        return round((correct / total) * 100, 2)
    
    def reset_progress(self):
        """Reset all user progress"""
        self.progress_data = {
            "hiragana": {"learned": [], "mastered": [], "needs_review": []},
            "katakana": {"learned": [], "mastered": [], "needs_review": []},
            "statistics": {"correct_answers": 0, "total_attempts": 0, "study_sessions": [], "last_active": None},
            "settings": self.progress_data["settings"]  # Keep settings
        }
        self.save_progress()
    
    def record_practice_result(self, difficulty, practice_type, success, content=None):
        """Record the result of a practice activity"""
        # Update current time for activity tracking
        self.progress_data["statistics"]["last_active"] = datetime.now().isoformat()
        self.progress_data["statistics"]["total_attempts"] += 1
        
        if success:
            self.progress_data["statistics"]["correct_answers"] += 1
        
        # Initialize practice stats if they don't exist
        if "practice_stats" not in self.progress_data:
            self.progress_data["practice_stats"] = {}
            
        if difficulty not in self.progress_data["practice_stats"]:
            self.progress_data["practice_stats"][difficulty] = {}
            
        if practice_type not in self.progress_data["practice_stats"][difficulty]:
            self.progress_data["practice_stats"][difficulty][practice_type] = {
                "attempts": 0,
                "correct": 0,
                "last_practiced": None,
                "content_history": []
            }
        
        # Update practice type statistics
        stats = self.progress_data["practice_stats"][difficulty][practice_type]
        stats["attempts"] += 1
        if success:
            stats["correct"] += 1
        stats["last_practiced"] = datetime.now().isoformat()
        
        # Track content to avoid repeating recent questions too frequently
        if content:
            # Keep a history of recent content (limit to 50 items)
            if len(stats["content_history"]) >= 50:
                stats["content_history"].pop(0)  # Remove oldest
            stats["content_history"].append({
                "content_id": hash(str(content)),
                "timestamp": datetime.now().isoformat(),
                "success": success
            })
        
        self.save_progress()
    
    def get_practice_stats(self):
        """Get statistics about practice activities"""
        if "practice_stats" not in self.progress_data:
            return {}
            
        return self.progress_data["practice_stats"]
    
    def get_recommended_practice(self, difficulty):
        """Get recommended practice activities based on performance"""
        if "practice_stats" not in self.progress_data:
            return None
        
        if difficulty not in self.progress_data["practice_stats"]:
            return None
            
        stats = self.progress_data["practice_stats"][difficulty]
        
        # Find practice types that need improvement (less than 70% correct)
        needs_improvement = []
        for practice_type, data in stats.items():
            if data["attempts"] > 0:
                accuracy = data["correct"] / data["attempts"]
                if accuracy < 0.7:
                    needs_improvement.append(practice_type)
                    
        if needs_improvement:
            return random.choice(needs_improvement)
        
        # Otherwise return a practice type that hasn't been practiced recently
        all_types = list(stats.keys())
        if all_types:
            # Sort by last practiced time (oldest first)
            all_types.sort(key=lambda x: stats[x].get("last_practiced", ""))
            return all_types[0]
            
        return None
