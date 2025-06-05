import hashlib

def track_prompt_version(prompt):
    # Return first 8 chars of SHA256 hash as version
    return hashlib.sha256(prompt.encode()).hexdigest()[:8]

def count_tokens(text):
    # Rough estimate: 1 token ≈ 4 characters
    return len(text) // 4
