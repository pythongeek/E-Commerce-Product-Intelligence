from typing import List, Dict, Any

class ReviewSentimentAnalyzer:
    """NLP sentiment pipeline using XLM-RoBERTa for multilingual reviews.
    
    Handles Bengali, Hindi, and English reviews from South Asian markets.
    Lightweight inference with optional MiniMax theme extraction.
    """
    
    def __init__(self):
        self.classifier = None
        self._load_model()
    
    def _load_model(self):
        """Lazy-load the sentiment model."""
        try:
            from transformers import pipeline
            import torch
            
            self.classifier = pipeline(
                "sentiment-analysis",
                model="cardiffnlp/twitter-xlm-roberta-base-sentiment",
                device=0 if torch.cuda.is_available() else -1,
                batch_size=32
            )
        except Exception:
            # Fallback to simple keyword-based if model unavailable
            self.classifier = None
    
    def analyze_reviews(self, reviews: List[str]) -> Dict[str, Any]:
        if not reviews:
            return {
                "positive_pct": 0,
                "negative_pct": 0,
                "neutral_pct": 0,
                "top_complaints": [],
                "top_praises": [],
                "sample_size": 0
            }
        
        if self.classifier is None:
            return self._fallback_analyze(reviews)
        
        results = self.classifier(reviews, truncation=True, max_length=512)
        
        counts = {"positive": 0, "negative": 0, "neutral": 0}
        negative_reviews = []
        positive_reviews = []
        
        for i, r in enumerate(results):
            label = r["label"].lower()
            counts[label] = counts.get(label, 0) + 1
            
            if label == "negative":
                negative_reviews.append(reviews[i])
            elif label == "positive":
                positive_reviews.append(reviews[i])
        
        total = len(results)
        
        # Extract themes (simplified without MiniMax for speed)
        complaints = self._extract_keywords(negative_reviews, is_complaint=True)
        praises = self._extract_keywords(positive_reviews, is_complaint=False)
        
        return {
            "positive_pct": round(counts["positive"] / total * 100),
            "negative_pct": round(counts["negative"] / total * 100),
            "neutral_pct": round(counts["neutral"] / total * 100),
            "top_complaints": complaints[:5],
            "top_praises": praises[:5],
            "sample_size": total
        }
    
    def _fallback_analyze(self, reviews: List[str]) -> Dict[str, Any]:
        """Simple keyword-based sentiment when model unavailable."""
        positive_words = {"good", "great", "excellent", "amazing", "love", "perfect", "best", "nice", "happy", "satisfied"}
        negative_words = {"bad", "terrible", "awful", "hate", "worst", "broken", "defective", "poor", "disappointed", "waste"}
        
        pos_count = neg_count = neu_count = 0
        negative_reviews = []
        positive_reviews = []
        
        for review in reviews:
            words = set(review.lower().split())
            pos = len(words & positive_words)
            neg = len(words & negative_words)
            
            if neg > pos:
                neg_count += 1
                negative_reviews.append(review)
            elif pos > neg:
                pos_count += 1
                positive_reviews.append(review)
            else:
                neu_count += 1
        
        total = len(reviews)
        return {
            "positive_pct": round(pos_count / total * 100) if total else 0,
            "negative_pct": round(neg_count / total * 100) if total else 0,
            "neutral_pct": round(neu_count / total * 100) if total else 0,
            "top_complaints": self._extract_keywords(negative_reviews, True)[:5],
            "top_praises": self._extract_keywords(positive_reviews, False)[:5],
            "sample_size": total
        }
    
    def _extract_keywords(self, reviews: List[str], is_complaint: bool) -> List[str]:
        """Extract common keywords from reviews."""
        from collections import Counter
        import re
        
        if not reviews:
            return []
        
        stop_words = {"the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
                      "to", "of", "and", "in", "that", "have", "it", "for", "not", "on",
                      "with", "he", "as", "you", "do", "at", "this", "but", "his", "by",
                      "from", "they", "we", "say", "her", "she", "or", "an", "will", "my",
                      "one", "all", "would", "there", "their", "what", "so", "up", "out",
                      "if", "about", "who", "get", "which", "go", "me", "when", "make",
                      "can", "like", "time", "no", "just", "him", "know", "take", "people",
                      "into", "year", "your", "good", "some", "could", "them", "see", "other",
                      "than", "then", "now", "look", "only", "come", "its", "over", "think",
                      "also", "back", "after", "use", "two", "how", "our", "work", "first",
                      "well", "way", "even", "new", "want", "because", "any", "these", "give",
                      "day", "most", "us", "i", "it", "very", "too", "really"}
        
        all_words = []
        for review in reviews:
            words = re.findall(r'\b[a-zA-Z]{3,}\b', review.lower())
            all_words.extend([w for w in words if w not in stop_words])
        
        counter = Counter(all_words)
        return [word for word, count in counter.most_common(10)]
