# Import necessary modules
import ollama
import json
import os
from datetime import datetime
from gtts import gTTS
from playsound import playsound
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
import textwrap
from reportlab.lib.units import inch

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
    print("🚨 Simulating fake emergency message... (This is just a demo)")
    print("📱 Text sent: 'URGENT: Family emergency. Please call back ASAP!'")

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

def generate_fake_whatsapp_image(messages, filename="chat_proof.png"):
    width, height = 720, 1280
    image = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except:
        font = ImageFont.load_default()

    y = 50
    for msg in messages:
        sender = msg["sender"]
        text = msg["text"]
        wrapped = textwrap.fill(text, width=40)
        text_size = draw.textbbox((0, 0), wrapped, font=font)
        bubble_w = text_size[2] + 30
        bubble_h = text_size[3] + 20
        x = width - bubble_w - 40 if sender == "You" else 40
        color = (220, 248, 198) if sender == "You" else (240, 240, 240)

        draw.rectangle([x, y, x + bubble_w, y + bubble_h], fill=color, outline=(180, 180, 180))
        draw.text((x + 15, y + 10), wrapped, font=font, fill=(0, 0, 0))
        y += bubble_h + 20

    image.save(filename)
    return filename

def export_excuse_pdf(excuse_text, chat_img_path, scenario, filename="final_excuse_proof.pdf"):
    c = canvas.Canvas(filename, pagesize=A4)
    page_width, page_height = A4

    margin = 50
    current_y = page_height - margin

    # Header
    c.setFont("Helvetica-Bold", 16)
    c.drawString(margin, current_y, "AI-Generated Excuse and Proof")
    current_y -= 30

    # Scenario + Date
    c.setFont("Helvetica", 12)
    c.drawString(margin, current_y, f"Scenario: {scenario}")
    current_y -= 20
    c.drawString(margin, current_y, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    current_y -= 30

    # Excuse Text (wrapped)
    c.setFont("Helvetica", 11)
    wrapped_text = textwrap.wrap(excuse_text, width=100)
    for line in wrapped_text:
        if current_y < 100:
            c.showPage()  # move to next page
            current_y = page_height - margin
        c.drawString(margin, current_y, line)
        current_y -= 15

    # Add space before image
    current_y -= 20

    # Add chat image
    if os.path.exists(chat_img_path):
        img = ImageReader(chat_img_path)
        img_width = 4.5 * inch
        img_height = 7 * inch  # fixed height
        img_x = margin
        img_y = current_y - img_height

        if img_y < 0:
            c.showPage()
            img_y = page_height - img_height - margin

        c.drawImage(img, img_x, img_y, width=img_width, height=img_height)

    c.showPage()
    c.save()
    print(f"✅ PDF saved as: {filename}")



    
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
            
            print("\n📲 Creating WhatsApp chat proof...")
            sample_chat = [
            {"sender": "Mom", "text": "Where are you? Grandma fainted!"},
            {"sender": "You", "text": "I'm on the way! I just left class."}
            ]
            chat_img = generate_fake_whatsapp_image(sample_chat)

                # 3. Combine Everything into a PDF
            print("\n📦 Exporting everything to final PDF...")
            export_excuse_pdf(excuse, chat_img, scenario)

            print("\n✅ Done! Your excuse and proof PDF is ready.\n")

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
