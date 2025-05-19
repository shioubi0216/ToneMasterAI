class ContentRecommender:
    def __init__(self, ai_service):
        """Initialize the content recommender with AI service"""
        self.ai_service = ai_service
        
    def generate_recommendation(self, interests):
        """Generate personalized learning recommendations based on user interests"""
        if not interests:
            return "Please add some interests to get personalized recommendations."
            
        # Use the AI service to create a personalized learning path
        recommendation = self.ai_service.create_personalized_learning_path(interests)
        return recommendation
        
    def get_themed_vocabulary(self, theme, count=10):
        """Get vocabulary words related to a specific theme"""
        # This would use the AI service to generate themed vocabulary
        # For MVP, we'll just return sample data
        themes = {
            "anime": ["まんが (manga)", "アニメ (anime)", "キャラクター (character)"],
            "food": ["すし (sushi)", "ラーメン (ramen)", "おちゃ (tea)"],
            "travel": ["でんしゃ (train)", "ホテル (hotel)", "りょこう (trip)"]
        }
        
        return themes.get(theme.lower(), ["No vocabulary found for this theme"])
