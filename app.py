from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__)

CRISIS_PATTERNS = [
    "suicide", "kill myself", "end my life", "self harm", "self-harm",
    "hurt myself", "want to die", "i want to die", "die"
]

RESPONSES = {
    "greeting": [
        "Hey! I'm MindMate 🌿 I'm here to listen without judgment. How are you feeling right now?",
        "Hi there 💚 You can talk to me about what's on your mind. What's been going on?"
    ],
    "stress": [
        "That sounds stressful. Let's make the next few minutes easier: relax your shoulders, take one slow breath in, and breathe out longer than you breathed in. What is causing the most pressure right now?",
        "When everything feels like too much, try focusing on just one small thing you can control today. You don't have to solve everything at once."
    ],
    "sad": [
        "I'm sorry you're having a difficult moment. You don't have to force yourself to feel okay immediately. If you want, tell me what happened—I can listen.",
        "It sounds like you're carrying something heavy. Be gentle with yourself today. What's making you feel this way?"
    ],
    "anxiety": [
        "Anxiety can make the present feel more dangerous than it is. Try the 5-4-3-2-1 grounding exercise: name 5 things you see, 4 you can touch, 3 you hear, 2 you smell, and 1 you taste.",
        "Let's slow things down. Put both feet on the floor and take five gentle breaths. You can tell me what you're worried about."
    ],
    "angry": [
        "It's okay to feel angry. Before reacting, give yourself a little space—step away, breathe slowly, or write down what you want to say. What triggered the anger?",
        "Strong emotions need somewhere safe to go. Try a short walk, some water, or writing everything down without sending it to anyone."
    ],
    "lonely": [
        "Feeling lonely can be really painful. Even one small connection can help—message someone you trust or spend a few minutes around people you feel comfortable with. I'm here to listen too.",
        "You deserve connection and support. If talking feels difficult, you could start with a simple 'Hey, can we talk for a bit?'"
    ],
    "sleep": [
        "For tonight, try a simple wind-down: reduce screen brightness, keep the room comfortable, and do slow breathing for a few minutes. If sleep problems keep happening, consider talking with a qualified professional.",
        "A racing mind can make sleep difficult. Try writing down tomorrow's tasks so your brain doesn't have to keep holding them."
    ],
    "study": [
        "Academic pressure can feel overwhelming. Try a 25-minute focus session followed by a 5-minute break, and choose only one task to start with.",
        "You don't need to finish everything right now. Pick the smallest useful step—one page, one question, or ten minutes of revision."
    ],
    "confidence": [
        "Confidence grows through small actions, not perfection. Pick one tiny thing you can do today and give yourself credit for doing it.",
        "Try speaking to yourself like you would speak to a close friend. You can improve without putting yourself down."
    ],
    "thanks": [
        "You're welcome 💚 Take things one step at a time.",
        "Anytime. Be kind to yourself today 🌱"
    ],
    "default": [
        "I'm listening. Tell me a little more about what you're experiencing.",
        "That sounds important. You can take your time—what part of it is bothering you the most?",
        "I hear you. Would you like to talk about what happened, how you're feeling, or what you need right now?"
    ]
}

def detect_intent(message):
    text = message.lower()
    if any(x in text for x in ["hello", "hi", "hey", "vanakkam", "good morning", "good evening"]):
        return "greeting"
    if any(x in text for x in ["stress", "stressed", "pressure", "overwhelmed", "tension"]):
        return "stress"
    if any(x in text for x in ["sad", "cry", "crying", "upset", "depressed", "hurt", "heartbroken"]):
        return "sad"
    if any(x in text for x in ["anxiety", "anxious", "panic", "worried", "fear", "nervous"]):
        return "anxiety"
    if any(x in text for x in ["angry", "anger", "mad", "frustrated", "irritated"]):
        return "angry"
    if any(x in text for x in ["lonely", "alone", "no friends", "isolated"]):
        return "lonely"
    if any(x in text for x in ["sleep", "insomnia", "can't sleep", "cannot sleep"]):
        return "sleep"
    if any(x in text for x in ["exam", "study", "college", "assignment", "marks", "placement"]):
        return "study"
    if any(x in text for x in ["confidence", "insecure", "not good enough", "self esteem"]):
        return "confidence"
    if any(x in text for x in ["thanks", "thank you", "tq"]):
        return "thanks"
    return "default"

def is_crisis(message):
    text = message.lower()
    return any(re.search(r"\b" + re.escape(p) + r"\b", text) for p in CRISIS_PATTERNS)

@app.route("/")
def home():
    return render_template("index.html")

@app.post("/chat")
def chat():
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()

    if not message:
        return jsonify({"reply": "I'm here whenever you're ready to talk 💚", "crisis": False})

    if is_crisis(message):
        reply = (
            "I'm really sorry you're going through this. I can't provide emergency care, "
            "but your safety matters right now. Please move away from anything you could use "
            "to hurt yourself and stay with someone you trust. If you may act on these thoughts "
            "or are in immediate danger, contact your local emergency service or go to the nearest "
            "emergency department now. In India, you can also call Tele-MANAS at 14416 for mental-health support."
        )
        return jsonify({"reply": reply, "crisis": True})

    import random
    return jsonify({"reply": random.choice(RESPONSES[detect_intent(message)]), "crisis": False})

if __name__ == "__main__":
    app.run(debug=True)
