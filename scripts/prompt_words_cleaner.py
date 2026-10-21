"""
Override the [prompt_words] filename/directory pattern so that the words are taken
from the "meaning" of the prompt rather than its raw text:

- JSON prompts (e.g. MOSS): use the `caption` / `prompt` values instead of the keys
- `<lora:...>` style extra-network tags are dropped
- prompt editing / alternation (`[a:b:0.5]`, `[a|b]`) is resolved to its final state
- emphasis syntax (`(a:1.2)`, `((a))`, `[a]`) is stripped, keeping only the text
"""

import json
import re

from backend.text_processing.parsing import parse_prompt_attention
from modules import images, prompt_parser
from modules.shared import opts

re_extra_network = re.compile(r"<[^<>]+>")


def json_prompt_text(prompt: str) -> str:
    text = prompt.strip()
    if not text.startswith(("{", "[")):
        return prompt
    try:
        data = json.loads(text, strict=False)  # allow raw newlines inside string values
    except ValueError:
        return prompt

    captions, others = [], []

    def walk(node):
        if isinstance(node, dict):
            for key, value in node.items():
                if isinstance(value, str):
                    (captions if key in ("caption", "prompt") else others).append(value)
                else:
                    walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)

    walk(data)
    texts = captions or others
    return " ".join(texts) if texts else prompt


def clean_prompt(prompt: str, steps: int = 20) -> str:
    text = json_prompt_text(prompt or "")
    text = re_extra_network.sub("", text)

    try:
        schedules = prompt_parser.get_learned_conditioning_prompt_schedules([text], steps)[0]
        text = schedules[-1][1]
    except Exception:
        pass

    try:
        parts = parse_prompt_attention(text, getattr(opts, "emphasis", None))
        text = " ".join(part for part, weight in parts if not (part == "BREAK" and weight == -1))
    except Exception:
        pass

    return text


def prompt_words(self: images.FilenameGenerator) -> str:
    steps = getattr(self.p, "steps", None) or 20
    words = [x for x in images.re_nonletters.split(clean_prompt(self.prompt, steps)) if x]
    if not words:
        words = ["empty"]
    return images.sanitize_filename_part(" ".join(words[0 : opts.directories_max_prompt_words]), replace_spaces=False)


images.FilenameGenerator.replacements["prompt_words"] = prompt_words
