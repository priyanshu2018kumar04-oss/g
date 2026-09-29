# Import necessary modules
import ollama
import json
import os
from datetime import datetime
from gtts import gTTS
from playsound import playsound

# File to save excuse history
HISTORY_FILE = "excuse_history.json"
# Load history from file
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f) 
    return []

# Save a new excuse to history
def save_excuse(excuse, scenario, urgency):
    history = load_history()
    history.append({
        "excuse": excuse,
        "scenario": scenario,
        "urgency": urgency,
        "timestamp": str(datetime.now())
    })
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

# Speak the excuse out loud
def speak_excuse(text, language="en"):
    tts = gTTS(text=text, lang=language)
    tts.save("excuse.mp3")
    playsound("excuse.mp3")
    os.remove("excuse.mp3")

# Generating excuse
def generate_excuse(scenario, urgency="normal", proof=False):
    prompt = f"""
    Generate a believable excuse for the following situation.
    Scenario: {scenario}
    Urgency: {urgency}
    Include proof: {"yes" if proof else "no"}
    Make it guilt-tripping and realistic. If proof is required, include a line about screenshots, documents, or GPS logs.
    """

    response = ollama.chat(model="llama3", messages=[
        {"role": "user", "content": prompt}
    ])
    excuse = response["message"]["content"]
    save_excuse(excuse, scenario, urgency)
    return excuse

# Generate a formal apology
def generate_apology(scenario):
    prompt = f"Write a heartfelt apology for this situation: {scenario}"
    response = ollama.chat(model="llama3", messages=[
        {"role": "user", "content": prompt}
    ])
    return response["message"]["content"]

# Simulate emergency alert
def simulate_emergency():
    print(" Simulating fake emergency message... (This is just a demo)")
    print(" Text sent: 'URGENT: Family emergency. Please call back ASAP!'")

# Show all saved excuses
def show_history():
    history = load_history()
    if not history:
        print("No excuses saved yet.")
    else:
        print("\n📚 Saved Excuse History:")
        for item in history:
            print(f"[{item['timestamp']}] ({item['scenario']}, {item['urgency']}):")
            print(item['excuse'])
            print("-" * 60)
            
# Main program
def main():
    print("Welcome to the Intelligent Excuse Generator")

    while True:
        print("\nMenu:")
        print("1. Generate Excuse")
        print("2. Generate Apology")
        print("3. Simulate Emergency Alert")
        print("4. View Excuse History")
        print("5. Exit")
        choice = input("Choose an option (1-5): ")

        if choice == "1":
            scenario = input("Enter the situation (e.g., missed class, late to work): ")
            urgency = input("Enter urgency (low / normal / high): ").lower()
            proof = input("Do you want proof included? (yes / no): ").lower() == "yes"
            language = input("Choose language for voice (en for English, hi for Hindi, etc.): ").lower()

            print("\nGenerating your excuse... Please wait.")
            excuse = generate_excuse(scenario, urgency, proof)
            print("\n Excuse:\n", excuse)

            speak = input("Do you want to hear it? (yes / no): ").lower()
            if speak == "yes":
                speak_excuse(excuse, language)

        elif choice == "2":
            scenario = input("Enter what you want to apologize for: ")
            apology = generate_apology(scenario)
            print("\n Apology:\n", apology)

        elif choice == "3":
            simulate_emergency()

        elif choice == "4":
            show_history()

        elif choice == "5":
            print("bye! Thanks for using the Intelligent Excuse Generator!")
            break

        else:
            print("Invalid choice. Please try again.")

# Start the program
if __name__ == "__main__":
    main()
