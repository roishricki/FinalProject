"""Synthesizes speech from the input string of text or ssml.
pip install --upgrade google-cloud-texttospeech
Note: ssml must be well-formed according to:
    https://www.w3.org/TR/speech-synthesis/
"""
import os
from google.cloud import texttospeech

def toSound(array):
    credential_path = "C:\\Users\\speed\\PycharmProjects\\quizGame\\.json"

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

    # Instantiates a client
    client = texttospeech.TextToSpeechClient()
    for i in range(len(array)):
        # Set the text input to be synthesized
        synthesis_input = texttospeech.SynthesisInput(text=array[i])
        # Build the voice request, select the language code ("en-US") and the ssml
        # voice gender ("neutral")
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
        )
        # Select the type of audio file you want returned
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.LINEAR16
        )

        # Perform the text-to-speech request on the text input with the selected
        # voice parameters and audio file type
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        # The response's audio_content is binary.
        with open(array[i] + ".wav", "wb") as out:
            # Write the response to the output file.
            out.write(response.audio_content)
            print('Audio content written to file "output.wav"')
