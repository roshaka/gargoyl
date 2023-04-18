
import openai
import dotenv
import os
import pyttsx3
from elevenlabslib import *
from pydub import AudioSegment, playback
import speech_recognition as sr
from prompt_handling import (
    create_setup_prompts,
    create_prompt,
    narrator_speak_pyttsx3,
    narrator_speak_elevenlabs,
    generate_response
)
from game_text import (
    print_titles,
    print_start_msg
)

# choose the text to speech engine for the narrators voice. fast_tts = True will use a local install of pyttsx3- quicker, but inferior. fast_tts = False will use elevenlabs AI using their API
def main(fast_tts : bool):
    """The game engine"""
    # game initialisation
    dotenv.load_dotenv()
    openai.api_key = os.getenv('OPENAI_KEY')

    if fast_tts:
        engine = pyttsx3.init()
        narrator_speak = narrator_speak_pyttsx3
    else:
        user = ElevenLabsUser(os.getenv('ELEVENLABS_KEY'))
        # The voice name can be customised. See docs
        engine = user.get_voices_by_name('Josh')[0]
        narrator_speak = narrator_speak_elevenlabs

    # game title screen
    print_titles()
    song = AudioSegment.from_mp3('assets/load_music.mp3')
    playback.play(song)
    print_start_msg()

    # AI setup
    create_setup_prompts()

    # game begins
    text= generate_response()
    narrator_speak(engine, text)
    print(f'"{text}"')

    while True:
        # prints '.' each time the microphone begins recording audio, listening for the player's voice
        print(f'\u001B[30m.\u001B[0m')
        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            source.pause_threshold = 1
            audio = recognizer.listen(
                source, 
                phrase_time_limit = None,
                timeout = None
            )
            try:
                # attempts to transcribe recorded audio
                transcription = recognizer.recognize_google(audio)

                # if successfully transcribed 
                if transcription:
                    print(f'\u001B[30m~ {transcription}\u001B[0m')
                    # prompt GPT using the player's spoken text
                    create_prompt('user',transcription)

                    # speak the narrator's response from GPT
                    text = generate_response()
                    narrator_speak(engine, text)
                    print(text)

                    # breaks loop if the end game response from GPT is detected
                    if 'the end' in text:
                        break
            except Exception as e:
                pass

    print('Well played! The end')

if __name__ == "__main__":
    main(False)