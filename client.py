import  google.generativeai as genai


# Yahan apni Gemini API Key paste karein
genai.configure(api_key="AIzaSyDTwg9YvksrISyvNX4ktxHQyP0YHf5vjtE")
print("Available models:")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)

# Model select karein
# Is line ko aise likho:
# Purani line: model = genai.GenerativeModel('gemini-pro')
# Isse badal kar ye karo (aapki list se uthaya hai):
model = genai.GenerativeModel('gemini-3.1-flash-lite-preview')
model = genai.GenerativeModel(
    model_name='gemini-3.1-flash-lite-preview',
    system_instruction="You are Jarvis. Give short and direct answers. Don't ask how you can help every time, just answer the user's question directly."
)
def get_ai_response(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {e}"

# Testing ke liye
if __name__ == "__main__":
    p = "Tell me latest tech news in short"
    print(get_ai_response(p))