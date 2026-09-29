from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__)

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL = "llama3.2:3b"


def generate_comic(
    story_prompt,
    character_name,
    setting,
    tone,
    art_style
):

    prompt = f"""
You are a professional comic book writer.

Create a 4-panel comic.

Story:
{story_prompt}

Main Character:
{character_name}

Setting:
{setting}

Tone:
{tone}

Art Style:
{art_style}

Return ONLY valid JSON.

Use exactly this structure:

{{
  "title": "Comic title",
  "genre": "Mystery",
  "panels": [
    {{
      "title": "Panel title",
      "scene": "What is happening visually in this panel.",
      "narration": "Narrator text.",
      "dialogue": {{
        "speaker": "Character name",
        "text": "Character dialogue."
      }},
      "image_prompt": "Comic artwork description."
    }}
  ]
}}

Create exactly 4 panels.

Every panel must contain:
title
scene
narration
dialogue
image_prompt

Return JSON only.
"""

    try:

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False,
                "format": "json"
            },
            timeout=180
        )

        response.raise_for_status()

        result = response.json()

        raw_text = result.get("response", "")

        comic = json.loads(raw_text)

        panels = comic.get("panels", [])

        fixed_panels = []

        for i, panel in enumerate(panels):

            dialogue = panel.get("dialogue", {})

            if isinstance(dialogue, str):

                dialogue = {
                    "speaker": character_name,
                    "text": dialogue
                }

            if not isinstance(dialogue, dict):

                dialogue = {}

            fixed_panels.append({

                "title": panel.get(
                    "title",
                    f"Panel {i + 1}"
                ),

                "scene": panel.get(
                    "scene",
                    "The scene continues the story."
                ),

                "narration": panel.get(
                    "narration",
                    "The mystery continues."
                ),

                "dialogue": {

                    "speaker": dialogue.get(
                        "speaker",
                        character_name
                    ),

                    "text": dialogue.get(
                        "text",
                        "Something strange is happening."
                    )
                },

                "image_prompt": panel.get(
                    "image_prompt",
                    f"{character_name} in {setting}, {art_style} style."
                )

            })

        if not fixed_panels:

            raise ValueError(
                "Ollama returned no panels."
            )

        comic["panels"] = fixed_panels

        return comic

    except Exception as error:

        print("OLLAMA ERROR:", error)

        return {

            "title": "The Mysterious Clock Tower",

            "genre": "Mystery",

            "panels": [

                {
                    "title": "The Clock Tower",

                    "scene":
                    "Maya stands outside the old clock tower at midnight.",

                    "narration":
                    "Every night at exactly midnight, the old clock tower rings thirteen times.",

                    "dialogue": {
                        "speaker": "Maya",
                        "text":
                        "Why does this happen every night?"
                    },

                    "image_prompt":
                    "Maya standing in front of an old clock tower at midnight, dramatic comic book style."
                },

                {
                    "title": "Inside the Tower",

                    "scene":
                    "Maya enters the dusty clock tower and discovers a hidden room.",

                    "narration":
                    "Inside the tower, she discovers a hidden room containing mysterious photographs.",

                    "dialogue": {
                        "speaker": "Maya",
                        "text":
                        "What is this place?"
                    },

                    "image_prompt":
                    "Maya discovering a hidden room filled with mysterious photographs, comic book style."
                },

                {
                    "title": "The Photograph From Tomorrow",

                    "scene":
                    "Maya finds a photograph showing herself inside the tower tomorrow.",

                    "narration":
                    "The photograph is dated tomorrow, and Maya realizes she has very little time.",

                    "dialogue": {
                        "speaker": "Maya",
                        "text":
                        "That's me... but this photograph was taken tomorrow!"
                    },

                    "image_prompt":
                    "Maya holding a mysterious photograph from the future, dramatic comic book style."
                },

                {
                    "title": "Before Midnight",

                    "scene":
                    "Maya looks at the clock as midnight approaches again.",

                    "narration":
                    "Maya must solve the mystery before the clock strikes thirteen again.",

                    "dialogue": {
                        "speaker": "Maya",
                        "text":
                        "I have to find the truth before midnight."
                    },

                    "image_prompt":
                    "Maya facing the mysterious clock tower as midnight approaches, dramatic comic book style."
                }

            ]
        }


@app.route("/")
def home():

    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():

    story_prompt = request.form.get(
        "story_prompt",
        ""
    )

    character_name = request.form.get(
        "character_name",
        "Maya"
    )

    setting = request.form.get(
        "setting",
        "Old Clock Tower"
    )

    tone = request.form.get(
        "tone",
        "Mystery"
    )

    art_style = request.form.get(
        "art_style",
        "Comic Book"
    )

    comic = generate_comic(
        story_prompt,
        character_name,
        setting,
        tone,
        art_style
    )

    return jsonify(comic)


@app.route("/comic-preview")
def comic_preview():

    return render_template(
        "Comic_preview.html"
    )


@app.route("/export-success")
def export_success():

    return render_template(
        "export-success.html"
    )


if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )