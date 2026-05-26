from services.openai_service import extract_user_intent

prompt = """
I already own male white sneakers and a black hoodie.
I need something for travelling during winter that still
looks fashionable and comfortable. I don't want bright colours.
"""

intent = extract_user_intent(prompt)

print(intent)