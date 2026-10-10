from config import SYSTEM_PROMPT, MODEL_WEIGHTS_PATH
from search_engine import WebSearchEngine
from firebase_manager import FirebaseManager
from model_core import RobotAIEngine

def main():
    search = WebSearchEngine(max_results=3)
    firebase = FirebaseManager()
    ai = RobotAIEngine(weights_path=MODEL_WEIGHTS_PATH)

    # Conversation Memory එක තබා ගන්නා List එක
    chat_history = []

    print("🤖 Custom Robot AI System Online (Pro Engine).")
    print("💡 AI එක Train කිරීමට: train: [ප්‍රශ්නය] | [උත්තරය]")
    print("Type 'exit' to stop the execution.\n")

    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue

        # "You:" කොටසක් Copy-Paste වුවහොත් එය ඉවත් කිරීම
        if user_input.lower().startswith("you:"):
            user_input = user_input[4:].strip()

        if user_input.lower() in ["exit", "quit"]:
            break

        # 1. Training Mode Routing
        if user_input.lower().startswith("train:"):
            raw_data = user_input[6:].strip()
            if "|" in raw_data:
                prompt, response = raw_data.split("|", 1)
                prompt = prompt.strip()
                response = response.strip()

                if prompt and response:
                    json_success = search.add_to_dataset(prompt, response)
                    fb_success = firebase.add_to_dataset(prompt, response)

                    if json_success or fb_success:
                        print(f"Robot AI: ✅ සාර්ථකයි! dataset.json එකට සහ Firebase එකට සේව් කරගත්තා.\n   📌 Prompt: {prompt}\n   📌 Response: {response}\n")
                    else:
                        print("Robot AI: ❌ Save කිරීමේදී දෝෂයක් සිදුවුණා.\n")
                else:
                    print("Robot AI: ⚠️ කරුණාකර 'train: ප්‍රශ්නය | උත්තරය' ආකෘතියට ටයිප් කරන්න.\n")
            else:
                print("Robot AI: ⚠️ ප්‍රශ්නය සහ උත්තරය වෙන් කිරීමට '|' සංකේතය යොදන්න.\n")
            continue

        # 2. Regular Query Search Context
        search_context = search.get_search_context(user_input)
        full_context = f"{SYSTEM_PROMPT}\n\nSearch Context:\n{search_context}\n\nUser Question: {user_input}"
        
        response = ai.generate_response(full_context)

        # 3. Save Context to Memory (Last 5 Interactions)
        chat_history.append({"user": user_input, "ai": response})
        if len(chat_history) > 5:
            chat_history.pop(0)

        print(f"Robot AI: {response}\n")
        firebase.log_interaction(user_input, response)

if __name__ == "__main__":
    main()