import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclibrary
import requests
import google.generativeai as genai

# Gemini Configuration
genai.configure(api_key="")
# Model name ko explicitly aise likho
# Is line ko aise likho:
# Purani line: model = genai.GenerativeModel('gemini-pro')
# Isse badal kar ye karo (aapki list se uthaya hai):
model = genai.GenerativeModel('gemini-3.1-flash-lite-preview')
model = genai.GenerativeModel(
    model_name='gemini-3.1-flash-lite-preview',
    system_instruction="You are Jarvis. Give short and direct answers. Don't ask how you can help every time, just answer the user's question directly."
)

news_api = "YOUR API_KEY"

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def processcommand(c):
    if "open google" in c.lower():
        speak("opening google")
        webbrowser.open("https://google.com")
    elif "open youtube" in c.lower():
        speak("opening youtube")
        webbrowser.open("https://youtube.com")
    elif c.lower().startswith("play"):
        speak("playing music")
        song = c.lower().split(" ")[1]
        link = musiclibrary.music[song]
        webbrowser.open(link)
    elif "open news" in c.lower():
        speak("fetching latest news")
        url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={news_api}"
        response = requests.get(url)
        data = response.json()
        if data["status"] != "ok":
            speak("failed to fetch news")
            return
        articles = data["articles"]
        for article in articles[:3]:
            title = article["title"]
            print(title)
            speak(title)
            webbrowser.open(article["url"])
    else:
        # Gemini AI Integration with proper indentation
        try:
            print("Thinking...")
            response = model.generate_content(c)
            # Response text nikalne ke liye
            answer = response.text
            print(f"Jarvis: {answer}")
            speak(answer)
        except Exception as e:
            print(f"AI Error: {e}")
            speak("Sorry, I am facing an issue connecting to the brain.")

if __name__ == "__main__":
    speak("hello jarvis")
    r = sr.Recognizer()

    while True:
        try:
            with sr.Microphone() as source:
                print("Listening for wake word...")
                # Ambient noise ke liye adjust karna achha hota hai
                r.adjust_for_ambient_noise(source, duration=0.5)
                audio = r.listen(source, timeout=5, phrase_time_limit=10)

            command = r.recognize_google(audio)
            print(f"Detected: {command}")

            if command.lower() == "jarvis":
                print("Jarvis Active...")
                speak("yes i am listening mr. sambhav")
                with sr.Microphone() as source:
                    print("Listening for command...")
                    audio = r.listen(source, timeout=3, phrase_time_limit=5)
                
                final_command = r.recognize_google(audio)
                print(f"User Command: {final_command}")
                processcommand(final_command)

        except sr.WaitTimeoutError:
            pass # Silent raho jab tak koi na bole
        except sr.UnknownValueError:
            print("Could not understand audio")
        except Exception as e:
            print(f"System Error: {e}")
