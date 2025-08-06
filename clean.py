import re

def clean_scraped_text(input_file="visionq_scraped.txt", output_file="visionq_cleaned.txt"):
    with open(input_file, "r", encoding="utf-8") as file:
        text = file.read()

    # Remove page markers like "--- PAGE: https://... ---"
    text = re.sub(r"--- PAGE:.*?---", "", text)

    # Remove repeated menu/navigation items
    keywords_to_remove = [
        "Home", "About", "Service", "Career", "Contact", "Read More", "Subscribe",
        "Phone:", "Email:", "Useful Links", "Terms of Service", "Privacy Policy",
        "Join our newsletter", "Stay Connected", "VisionQ Technologies"
    ]
    for keyword in keywords_to_remove:
        text = re.sub(rf"\b{re.escape(keyword)}\b", "", text)

    # Remove duplicate empty lines
    text = re.sub(r"\n\s*\n", "\n\n", text)

    # Strip leading/trailing whitespace
    cleaned = text.strip()

    with open(output_file, "w", encoding="utf-8") as file:
        file.write(cleaned)

    print(f"✅ Cleaned content written to {output_file}")


if __name__ == "__main__":
    clean_scraped_text()
