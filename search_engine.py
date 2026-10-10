import json
import os
import difflib
from ddgs import DDGS

class WebSearchEngine:
    def __init__(self, dataset_path="dataset.json", max_results=2):
        self.dataset_path = dataset_path
        self.max_results = max_results

    def load_dataset(self):
        if not os.path.exists(self.dataset_path):
            return []
        try:
            with open(self.dataset_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[Dataset Load Warning]: {e}")
            return []

    def get_best_dataset_match(self, user_input):
        dataset = self.load_dataset()
        if not dataset:
            return None

        user_input_clean = user_input.lower().strip()
        best_match = None
        highest_score = 0.0

        for item in dataset:
            prompt = item.get("prompt", "").lower().strip()
            if not prompt:
                continue

            similarity_score = difflib.SequenceMatcher(None, user_input_clean, prompt).ratio()

            if prompt in user_input_clean or user_input_clean in prompt:
                similarity_score += 0.25

            if similarity_score > highest_score and similarity_score >= 0.55:
                highest_score = similarity_score
                best_match = item.get("response")

        return best_match

    def check_conversational_intent(self, user_input):
        """සාමාන්‍ය කතාබහ සහ Singlish ප්‍රශ්න Web Search එකට යාම වළක්වයි"""
        text = user_input.lower().strip()
        
        # 1. Identity Queries (කවුද ඔයා / කවුද හදාපු කෙනා)
        identity_keywords = ["kauda oya", "kavuda oya", "oyage nama", "oyage nama mokakda", "who are you", "who r u", "who r you", "mkauda oya"]
        if any(k in text for k in identity_keywords):
            return "මම කවිනු විසින් සාදන ලද Custom Robot AI පද්ධතියක්!"

        # 2. Sinhala Language Capability Check
        if any(w in text for w in ["sinhala", "සිංහල", "sinhala puluwanda", "understand sinhala"]):
            return "ඔවු, මට සිංහල තේරුම් ගන්න සහ සිංහලෙන් පිළිතුරු දෙන්න පුළුවන්!"

        # 3. Greetings & How are you
        if text in ["hi", "hello", "hey", "halo", "haai"]:
            return "Hello! මම ඔයාගේ Custom Robot AI එක. මට ඔයාට උදව් කරන්නේ කොහොමද?"

        return None

    def add_to_dataset(self, new_prompt, new_response):
        dataset = self.load_dataset()
        dataset.append({
            "prompt": new_prompt.strip(),
            "response": new_response.strip()
        })
        try:
            with open(self.dataset_path, "w", encoding="utf-8") as f:
                json.dump(dataset, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"[Dataset Write Error]: {e}")
            return False

    def search_web(self, query):
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=self.max_results))
                if results:
                    cleaned_results = []
                    for r in results:
                        body = r.get('body', '')
                        if body and len(body) > 30:
                            cleaned_results.append(body)
                    return "\n".join(cleaned_results[:2])
        except Exception as e:
            print(f"[Search Warning]: {e}")
        return None

    def get_search_context(self, user_input):
        # 1. Dataset Match (Fuzzy)
        dataset_res = self.get_best_dataset_match(user_input)
        if dataset_res:
            return f"[Dataset Answer]: {dataset_res}"

        # 2. Conversational Intent Check (Identity / Language / Small Talk)
        intent_res = self.check_conversational_intent(user_input)
        if intent_res:
            return f"[Dataset Answer]: {intent_res}"

        # 3. එක වචනයේ Typos සඳහා Web Search යාම වැළැක්වීම
        if len(user_input.strip().split()) == 1 and len(user_input.strip()) < 5:
            return "කරුණාකර ඔබේ ප්‍රශ්නය තව ටිකක් පැහැදිලිව අහන්න."

        # 4. Web Search
        web_res = self.search_web(user_input)
        if web_res:
            return f"[Web Search Result]:\n{web_res}"

        return "කණගාටුයි, ඒ පිළිබඳ තොරතුරු සොයා ගැනීමට නොහැකි විය."