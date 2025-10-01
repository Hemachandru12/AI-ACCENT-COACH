from flask import Flask, request, jsonify
from flask_cors import CORS
import speech_recognition as sr
import pronouncing
import difflib
import io
from pydub import AudioSegment
import traceback 

app = Flask(__name__)
CORS(app)

CUSTOM_DICTIONARY = {
    "otorhinolaryngologist": "OW2 T OW0 R AY2 N OW0 L EH2 R IH0 NG G AA1 L AH0 JH IH0 S T"
}

r = sr.Recognizer()

def get_phonemes(word):
    if word in CUSTOM_DICTIONARY:
        print(f"Found '{word}' in the custom dictionary.")
        return [CUSTOM_DICTIONARY[word]]
    else:
        print(f"Checking pronouncing library for '{word}'.")
        return pronouncing.phones_for_word(word)

@app.route('/analyze', methods=['POST'])
def analyze():
    print("\nReceived new analysis request...")

    if 'audio' not in request.files:
        print("ERROR: No audio file in request.")
        return jsonify({"status": "error", "message": "No audio file found"}), 400

    audio_file = request.files['audio']
    target_phrase = request.form.get('phrase', '').lower().strip()

    if not target_phrase:
        print("ERROR: No target phrase in request.")
        return jsonify({"status": "error", "message": "No target phrase provided"}), 400

    print(f"Target phrase: '{target_phrase}'")

    try:
        target_phonemes_list = get_phonemes(target_phrase)
        if not target_phonemes_list:
            print(f"ERROR: No phonemes found for target word '{target_phrase}' in any dictionary.")
            return jsonify({
                "status": "error", 
                "message": f"Sorry, the word '{target_phrase}' is too complex and is not in our pronunciation dictionary. Please try another word."
            }), 400

        print("Loading audio file with pydub...")
        sound = AudioSegment.from_file(audio_file)
        
        wav_io = io.BytesIO()
        sound.export(wav_io, format="wav")
        wav_io.seek(0)
        print("Audio converted to WAV format in memory.")

        with sr.AudioFile(wav_io) as source:
            print("Adjusting for ambient noise...")
            r.adjust_for_ambient_noise(source, duration=0.5)
            print("Recording audio from file...")
            audio_data = r.record(source)

        print("Sending audio to Google Speech API...")
        response = r.recognize_google(audio_data, show_all=True)
        print(f"Google Speech API response: {response}")

        if not response or not isinstance(response, dict) or not response.get("alternative"):
            raise sr.UnknownValueError()

        top_alternative = response["alternative"][0]
        user_text = top_alternative.get("transcript", "").lower().strip()
        print(f"User said: '{user_text}'")

        target_phonemes = target_phonemes_list[0]
        print(f"Target phonemes: '{target_phonemes}'")
        
        phonetic_score = 0.0
        text_score = 0.0
        
        if user_text:
            user_phonemes_list = get_phonemes(user_text)
            if user_phonemes_list:
                user_phonemes = user_phonemes_list[0]
                print(f"User's phonemes: '{user_phonemes}'")
                phonetic_score = difflib.SequenceMatcher(None, user_phonemes, target_phonemes).ratio()
            else:
                print(f"WARNING: No phonemes found for user's word '{user_text}'.")
                phonetic_score = 0.0
            
            # --- FIX: Calculate text similarity score ---
            text_score = difflib.SequenceMatcher(None, user_text, target_phrase).ratio()

        else:
            print("User's speech was empty. All scores are 0.")
        
        print(f"Phonetic Score (raw): {phonetic_score}")
        print(f"Text Similarity Score (raw): {text_score}")

        # --- FIX: Combine scores with weighting ---
        # 70% of the score is for pronunciation, 30% is for getting the word right.
        final_score = (phonetic_score * 0.7) + (text_score * 0.3)
        
        print(f"Final combined score: {final_score}")

        return jsonify({
            "status": "success",
            "score": final_score,
            "user_text": user_text or "(No speech detected)",
            "phonetic_guide": target_phonemes,
        })

    except sr.UnknownValueError:
        print("ERROR: Google Speech Recognition could not understand audio.")
        return jsonify({
            "status": "error", 
            "message": "Could not understand the audio. Please speak more clearly and try again.",
            "score": 0.0
        })
    except sr.RequestError as e:
        print(f"ERROR: Could not request results from Google Speech Recognition service; {e}")
        return jsonify({
            "status": "error", 
            "message": f"Could not request results from the speech recognition service; {e}",
            "score": 0.0
        })
    except Exception as e:
        print("--- An unexpected error occurred ---")
        traceback.print_exc()
        print("------------------------------------")
        return jsonify({
            "status": "error", 
            "message": f"An unexpected error occurred. Please check the server console for details.",
            "score": 0.0
        })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
