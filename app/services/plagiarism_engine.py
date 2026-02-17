from difflib import SequenceMatcher


def analyze_plagiarism(new_code: str, existing_codes: list):
    highest_similarity = 0

    for code in existing_codes:
        similarity = SequenceMatcher(None, new_code, code).ratio()
        if similarity > highest_similarity:
            highest_similarity = similarity

    plagiarism_percentage = round(highest_similarity * 100, 2)

    return {
        "plagiarism_score": 100 - plagiarism_percentage,
        "similarity_percentage": plagiarism_percentage
    }
