import re
class EditorAgent:
    def run(self, text):
        if isinstance(text, dict): return text
        return re.sub(r"\n{3,}", "\n\n", text).strip()
