def generate_comic(payload):
    return {
        "story_prompt": payload.story_prompt,
        "character_name": payload.character_name,
        "setting": payload.setting,
        "tone": payload.tone,
        "art_style": payload.art_style,
    }