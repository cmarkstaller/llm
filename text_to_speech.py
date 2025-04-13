from TTS.api import TTS
from playsound import playsound

# Load a pretrained model
tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False)

# Generate and save speech
tts.tts_to_file(
    text="Hey Chris, you’ve got a new email!",
    file_path="output.wav"
)

def speak_with_coqui(text):
    tts.tts_to_file(text=text, file_path="reply.wav")
    playsound("output.wav")  # This call is blocking by default
    # ...sound has finished at this point
    os.remove("output.wav")
