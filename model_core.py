import torch

class RobotAIEngine:
    def __init__(self, weights_path=None):
        self.weights_path = weights_path
        print("[PyTorch Engine]: Running on base model structure.")

    def generate_response(self, full_context):
        """Context එක කියවා පිරිසිදු පිළිතුරක් ලබා දෙයි"""
        if "[Dataset Answer]:" in full_context:
            # Dataset එකෙන් ආ උත්තරය පිරිසිදුව ලබා දීම
            answer = full_context.split("[Dataset Answer]:")[-1].split("\n")[0].strip()
            return answer

        if "[Web Search Result]:" in full_context:
            # Web Search එකෙන් ආ Raw Text එක Summarize / Format කිරීම
            raw_search = full_context.split("[Web Search Result]:")[-1].strip()
            lines = [line.strip() for line in raw_search.split("\n") if line.strip()]
            summary = " ".join(lines[:3]) # ප්‍රධාන කරුණු 3ක් එකතු කිරීම
            if len(summary) > 300:
                summary = summary[:300] + "..."
            return f"අන්තර්ජාලයේ සෙවුම් තොරතුරු අනුව:\n{summary}"

        return "මම ඒ ගැන අධ්‍යයනය කරමින් සිටිමි."