def remove_markdown_tags(text: str) -> str:
    if text.startswith("```"):
        lines = text.split("\n")
        lines = lines[1:-1]
        return "\n".join(lines)
    return text
