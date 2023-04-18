
import openai
from elevenlabslib import *

# this is the max allowed tokens in a request. set by GPT for the gpt-3.5-turbo model
MAX_MODEL_TOKENS = 4096

# ensures GPT can always respond without running out of tokens
PROMPT_TOKEN_BUFFER = 400

# the max tokens to be maintained in the conversation list
MAX_CONVERSATION_TOKENS = MAX_MODEL_TOKENS - PROMPT_TOKEN_BUFFER
conversation = []

def create_setup_prompts():
    """The set up 'system' prompt for GPT-3.5. You can edit this for your own custom scenario
    """
    setup_prompt="""
    We will roleplay- you will act like the narrator from the stanley parable- witty, sarcastic, sardonic. ALWAYS stay in character and speak as the narrator. i am an adventurer in a garden. there is a stone gargoyle in the centre. describe the scene to me, and also describe some other interesting features in the garden. the gargoyle is inanimate you make it seem alive. i am an adventurer attempting to solve the mystery of the gargoyle. wait for my prompts to advance this story. create puzzles/riddles etc for me to solve. the garden and gargoyle are like a mystery box, or an escape room. solving puzzles and using items unlocks secrets in the garden/ causes the gargoyle to change shape/appearance etc. keep your messages concise. When the game is over include 'the end' in your response.
    Here is the conversation so far for context:
    """
    create_prompt('system', setup_prompt)
    
    # This is empty user prompt stops GPT from hallucinating itself as the user AND the narrator and ensures the game begins correctly
    create_prompt("user", "")

def create_prompt(speaker, prompt):
    """Keeps prompts in the conversation list, ensuring GPT does not 'forget' what is being discussed. Removes earlier prompts from the conversation list once the MAX_CONVERSATION_TOKENS has been exceeded."""
    conversation.append({
        'prompt' : {
            'role':speaker,
            'content':prompt,
        },
        'tokens' : _estimate_tokens(prompt)
        }
    )

    while True:
        # checks if old prompts need to be culled so as to not exceed the max tokens
        total_tokens= sum([p_t['tokens'] for p_t in conversation])
        if total_tokens > MAX_CONVERSATION_TOKENS:
            del conversation[2] # < This maintains the original 2 setup prompts
        else:
            break

def narrator_speak_pyttsx3(engine, text):
    """Narrator text to speech using pyttsx3."""
    engine.say(text)
    engine.runAndWait()

def narrator_speak_elevenlabs(voice, text):
    """Narrator text to speech using elevenlabs."""
    voice.generate_and_play_audio(text, playInBackground=False)

def generate_response():
    """Sends the conversation to GPT and returns the text from the response object."""
    prompts = [p_t['prompt'] for p_t in conversation]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages = prompts
    )
    text = response['choices'][0]['message']['content']
    create_prompt('assistant', text)
    return text
    
def _estimate_tokens(text):
    """Estimates the amount of tokens being used. 1 token ~= ¾ words """
    return len(text.split(' '))*1.33