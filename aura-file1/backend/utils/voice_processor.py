import speech_recognition as sr
import pyttsx3
import re

class VoiceAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 0.9)
        
        # Hindi support
        try:
            self.engine.setProperty('voice', 'hi')
        except:
            pass
    
    def listen(self):
        with sr.Microphone() as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source, timeout=5)
            
            try:
                text = self.recognizer.recognize_google(audio, language='hi-IN')
                print(f"You said: {text}")
                return text.lower()
            except sr.UnknownValueError:
                return ""
            except sr.RequestError:
                return ""
    
    def speak(self, text):
        print(f"Speaking: {text}")
        self.engine.say(text)
        self.engine.runAndWait()
    
    def process_command(self, command):
        # Hindi/English command processing
        command = command.lower()
        
        if any(word in command for word in ["balance", "शेष", "बैलेंस"]):
            return {"action": "check_balance"}
        
        elif any(word in command for word in ["withdraw", "निकालना", "पैसे निकालो"]):
            amounts = re.findall(r'\d+', command)
            if amounts:
                return {"action": "withdraw", "amount": float(amounts[0])}
        
        elif any(word in command for word in ["deposit", "जमा", "डिपॉजिट"]):
            amounts = re.findall(r'\d+', command)
            if amounts:
                return {"action": "deposit", "amount": float(amounts[0])}
        
        elif any(word in command for word in ["loan", "कर्ज", "लोन"]):
            return {"action": "loan_info"}
        
        return {"action": "unknown"}