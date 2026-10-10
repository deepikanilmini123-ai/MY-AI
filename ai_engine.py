import json
import os
from duckduckgo_search import DDGS

class HybridAIEngine:
    def __init__(self, dataset_path="dataset.json"):
        self.dataset_path = dataset_path

    def check_dataset(self, user_input):
        """1. Dataset එක ඇතුළේ ප්‍රශ්නයට අදාළ Keywords තියෙනවාද බලයි"""
        if not os.path.exists(self.dataset_path):
            return None

        try:
            with open(self.dataset_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            user_input_lower = user_input.lower()
            for item in data:
                # Keywords එකක් හෝ prompt එක match වේ නම්
                for key in item.get("keywords", []):
                    if key.lower() in user_input_lower:
                        return item["response"]
        except Exception as e:
            print(f"[Dataset Error]: {e}")
        return None

    def search_web(self, query):
        """2. Internet එකෙන් සෙවීම"""
        try:
            results = DDGS().text(query, max_results=2)
            if results:
                snippet_text = "\n".join([r['body'] for r in results])
                return f"[Web Search Results]:\n{snippet_text}"
        except Exception as e:
            print(f"[Web Search Error]: {e}")
        return None

    def get_response(self, user_input):
        """3. Dataset + Web Search දෙකම ඒකාබද්ධ කර පිළිතුර සැකසීම"""
        # A. මුලින්ම Dataset එකේ තියෙනවාද බලන්න
        local_result = self.check_dataset(user_input)
        
        # B. Internet එකෙන් අලුත් Data සෙවීම
        web_result = self.search_web(user_input)

        # Response එක සකස් කිරීම
        if local_result and web_result:
            return f"{local_result}\n\n📍 **අමතර තොරතුරු (Internet):**\n{web_result}"
        elif local_result:
            return local_result
        elif web_result:
            return web_result
        else:
            return "කණගාටුයි, ඒ පිළිබඳ තොරතුරු Dataset එකේ හෝ Internet එකේ සොයා ගැනීමට නොහැකි විය."