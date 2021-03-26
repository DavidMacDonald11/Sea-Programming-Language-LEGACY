import re

def keyword_pattern(keywords):
    keywords = [re.escape(keyword) for keyword in keywords]
    pattern = "".join(keyword + r"[\W]{1}" for keyword in keywords[:-1])

    return re.compile(r"(^|[\W]{1})" + pattern + keywords[-1] + r"($|[\W]{1})")
