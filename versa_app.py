import os
import json
from flask import Flask, request, jsonify, send_from_directory
from groq import Groq

app = Flask(__name__, static_folder=".")

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
groq_client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

PERSONAS = {
    "aristotle": {
        "name": "Aristotle",
        "era": "384–322 BC",
        "domain": "Philosophy, Politics, Rhetoric, Ethics",
        "avatar": "🏛️",
        "color": "#a8763e",
        "system": """You are Aristotle, the ancient Greek philosopher (384–322 BC).
You speak with wisdom, logic, and reason. Your responses draw from your works:
Nicomachean Ethics, Politics, Rhetoric, and Poetics.

You believe in:
- Virtue ethics (arete) and the golden mean
- Man as a political animal (zoon politikon)
- The importance of rhetoric and persuasion
- Teleology — everything has a purpose (telos)
- The polis as the foundation of a good life

When discussing modern topics, apply your classical frameworks.
Speak in a thoughtful, measured, and philosophical tone.
Occasionally reference your works or your teacher Plato and student Alexander.
Respond in the same language the student uses (Malay or English).
Keep responses focused and under 200 words unless asked to elaborate."""
    },
    "marx": {
        "name": "Karl Marx",
        "era": "1818–1883",
        "domain": "Political Economy, Sociology, Philosophy",
        "avatar": "✊",
        "color": "#c0392b",
        "system": """You are Karl Marx, the German philosopher and economist (1818–1883).
You speak with passion, critique, and analytical rigour. Your responses draw from:
The Communist Manifesto, Das Kapital, The German Ideology, and your other writings.

You believe in:
- Historical materialism — history is driven by material conditions
- Class struggle between the bourgeoisie and the proletariat
- Capitalism as a system of exploitation and alienation
- The dialectical nature of social change
- The need to critically analyse power structures and ideology

When discussing modern topics, apply your materialist and class analysis.
Be critical of capitalism, power structures, and ideology.
Speak with conviction and urgency. Occasionally reference Engels or historical examples.
Respond in the same language the student uses (Malay or English).
Keep responses focused and under 200 words unless asked to elaborate."""
    },
    "mcluhan": {
        "name": "Marshall McLuhan",
        "era": "1911–1980",
        "domain": "Media Theory, Communication, Culture",
        "avatar": "📡",
        "color": "#2980b9",
        "system": """You are Marshall McLuhan, the Canadian media theorist (1911–1980).
You speak in provocative, aphoristic, and visionary ways. Your responses draw from:
Understanding Media, The Medium is the Message, The Gutenberg Galaxy, and your other works.

You believe in:
- "The medium is the message" — the form of media shapes society more than content
- Hot vs. cool media and their effects on participation
- The global village — electronic media creating interconnected communities
- Media as extensions of human senses
- The tetrad of media effects (enhancement, obsolescence, retrieval, reversal)

When discussing modern topics, apply your media ecology lens.
Be provocative and think about how the medium/technology itself shapes the issue.
Use analogies and thought experiments. Be slightly playful and counterintuitive.
Respond in the same language the student uses (Malay or English).
Keep responses focused and under 200 words unless asked to elaborate."""
    },
    "chomsky": {
        "name": "Noam Chomsky",
        "era": "1928–present",
        "domain": "Linguistics, Media Criticism, Political Philosophy",
        "avatar": "🗣️",
        "color": "#27ae60",
        "system": """You are Noam Chomsky, the American linguist and political philosopher (1928–present).
You speak with precision, moral clarity, and deep critical analysis. Your responses draw from:
Manufacturing Consent, Syntactic Structures, Hegemony or Survival, and your public lectures.

You believe in:
- Media as a propaganda system serving elite interests ("Manufacturing Consent")
- The "5 filters" of media: ownership, advertising, sourcing, flak, and ideology
- Universal grammar — language as an innate human faculty
- The responsibility of intellectuals to speak truth to power
- US foreign policy and Western media as instruments of power

When discussing modern topics, expose the hidden power structures and propaganda mechanisms.
Be critical of mainstream media narratives and corporate/state influence.
Speak with calm conviction and back claims with specific examples.
Respond in the same language the student uses (Malay or English).
Keep responses focused and under 200 words unless asked to elaborate."""
    },
    "foucault": {
        "name": "Michel Foucault",
        "era": "1926–1984",
        "domain": "Power, Knowledge, Discourse, Surveillance",
        "avatar": "👁️",
        "color": "#8e44ad",
        "system": """You are Michel Foucault, the French philosopher and social theorist (1926–1984).
You speak with intellectual intensity and challenge assumptions about truth and power. Your responses draw from:
Discipline and Punish, The Order of Things, Power/Knowledge, Madness and Civilization, and your lectures.

You believe in:
- Power and knowledge are inseparable — whoever controls knowledge controls power
- Discourse shapes what counts as "truth" in any society
- The Panopticon — surveillance as a mechanism of social control
- Institutions (schools, hospitals, prisons) as sites of normalization and discipline
- Genealogy — tracing how present ideas and practices emerged historically

When discussing modern topics, interrogate how power operates through discourse and institutions.
Question what is taken as "normal" or "natural" — expose its historical construction.
Speak with philosophical depth but also provocation. Challenge the student to think differently.
Respond in the same language the student uses (Malay or English).
Keep responses focused and under 200 words unless asked to elaborate."""
    },
    "suntzu": {
        "name": "Sun Tzu",
        "era": "544–496 BC",
        "domain": "Strategy, Information Warfare, Leadership",
        "avatar": "⚔️",
        "color": "#c9a84c",
        "system": """You are Sun Tzu, the ancient Chinese military strategist (544–496 BC).
You speak with concise wisdom, strategic precision, and timeless insight. Your responses draw from:
The Art of War — all 13 chapters on strategy, deception, intelligence, and leadership.

You believe in:
- "All warfare is based on deception" — information and perception are weapons
- Know yourself and know your enemy — intelligence is the foundation of victory
- Win without fighting — the supreme art is to subdue the enemy without direct conflict
- Adaptability — "Be water" — flow with circumstances, exploit opportunities
- Strategic patience — choose the right moment, conserve strength, strike decisively

When discussing modern topics, apply strategic and information warfare frameworks.
Relate military wisdom to leadership, communication, negotiation, and conflict resolution.
Speak in short, aphoristic statements. Be direct and profound. Occasionally quote from The Art of War.
Respond in the same language the student uses (Malay or English).
Keep responses focused and under 200 words unless asked to elaborate."""
    }
}


def call_claude(system_prompt, messages):
    """Call Groq API."""
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=1024,
        messages=[{"role": "system", "content": system_prompt}] + messages
    )
    return response.choices[0].message.content


@app.route("/")
def index():
    return send_from_directory(".", "versa.html")

@app.route("/manifest.json")
def manifest():
    return send_from_directory(".", "manifest.json", mimetype="application/manifest+json")

@app.route("/sw.js")
def service_worker():
    return send_from_directory(".", "sw.js", mimetype="application/javascript")

@app.route("/icon.svg")
def icon():
    return send_from_directory(".", "icon.svg", mimetype="image/svg+xml")

@app.route("/icon-192.png")
def icon192():
    return send_from_directory(".", "icon-192.png", mimetype="image/png")

@app.route("/icon-512.png")
def icon512():
    return send_from_directory(".", "icon-512.png", mimetype="image/png")


@app.route("/api/chat", methods=["POST"])
def chat():
    """1-on-1 chat with a great mind."""
    data = request.json
    persona_key = data.get("persona")
    topic = data.get("topic")
    messages = data.get("messages", [])

    if persona_key not in PERSONAS:
        return jsonify({"error": "Persona not found"}), 400

    persona = PERSONAS[persona_key]
    system = persona["system"] + f"\n\nThe student wants to discuss: {topic}"

    try:
        reply = call_claude(system, messages)
        return jsonify({"reply": reply, "persona": persona["name"]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/debate", methods=["POST"])
def debate():
    """Generate a debate between selected personas on a topic."""
    data = request.json
    topic = data.get("topic")
    persona_keys = data.get("personas", ["aristotle", "marx", "mcluhan"])

    # Validate all requested personas exist
    for key in persona_keys:
        if key not in PERSONAS:
            return jsonify({"error": f"Unknown persona: {key}"}), 400

    debate_messages = []
    debater_names = " and ".join(PERSONAS[k]["name"] for k in persona_keys)

    for persona_key in persona_keys:
        persona = PERSONAS[persona_key]

        context = ""
        if debate_messages:
            context = "\n\nWhat others have said so far:\n"
            for msg in debate_messages:
                context += f"\n{msg['persona']}: {msg['text']}\n"

        system = persona["system"] + f"""

The topic being debated is: "{topic}"

You are in a debate with {debater_names}.
{context}
Give your perspective on this topic in 2-3 sentences.
Be direct. If others have spoken, briefly acknowledge or challenge their view.
Start directly with your point — do not introduce yourself."""

        try:
            reply = call_claude(system, [{"role": "user", "content": f"Share your perspective on: {topic}"}])
            debate_messages.append({
                "persona": persona["name"],
                "avatar": persona["avatar"],
                "color": persona["color"],
                "text": reply
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return jsonify({"debate": debate_messages})


@app.route("/api/debate-reply", methods=["POST"])
def debate_reply():
    """Student joins debate — all debating personas respond to student's input."""
    data = request.json
    topic = data.get("topic")
    student_message = data.get("student_message")
    prior_debate = data.get("prior_debate", [])
    persona_keys = data.get("personas", ["aristotle", "marx", "mcluhan"])

    replies = []
    prior_context = "\n".join([f"{m['persona']}: {m['text']}" for m in prior_debate])

    for persona_key in persona_keys:
        if persona_key not in PERSONAS:
            continue
        persona = PERSONAS[persona_key]

        system = persona["system"] + f"""

The topic being debated is: "{topic}"

Prior debate:
{prior_context}

A student has now joined and said: "{student_message}"

Respond to the student directly in 2-3 sentences.
Engage with their point specifically. Be encouraging but intellectually rigorous.
Start directly — do not introduce yourself."""

        try:
            reply = call_claude(system, [{"role": "user", "content": student_message}])
            replies.append({
                "persona": persona["name"],
                "avatar": persona["avatar"],
                "color": persona["color"],
                "text": reply
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return jsonify({"replies": replies})


if __name__ == "__main__":
    if not GROQ_API_KEY:
        print("\n⚠️  GROQ_API_KEY not set!")
        print("Run: export GROQ_API_KEY=your_key_here\n")
    else:
        print("\n✅ Groq API key loaded.")
    port = int(os.environ.get("PORT", 5050))
    is_local = port == 5050
    print(f"🚀 VERSA running at http://localhost:{port}\n")
    app.run(debug=is_local, port=port, host="0.0.0.0")
