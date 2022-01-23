
import io
import os

# Imports the Google Cloud client library
from google.cloud import speech

credential_path = "C:\\Users\\speed\\PycharmProjects\\quizGame\\speechvoice1-42e1023ba8c5.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

class STT():

    def __init__(self):        
        self.config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=44100,
            language_code="en-US",
        )
        self.client = speech.SpeechClient()
        

    def opensoundfile(self, file_name):        
        # Loads the audio into memory
        with io.open(file_name, "rb") as audio_file:
            content = audio_file.read()
            audio = speech.RecognitionAudio(content=content)
        return audio

    def recognize(self,audio):
        response = ''
        # Detects speech in the audio file and return results to caller
        try:
            response = self.client.recognize(config=self.config, audio=audio)
        except:
            print('Something wrong with recognition')
        return response    

if __name__ == '__main__':
    # The name of the audio file to transcribe
    file_name = "C:\\Users\\speed\\PycharmProjects\\quizGame\\output.wav"
    st= STT()
    audio=st.opensoundfile(file_name)
    rz=st.recognize(audio)    
    for result in rz.results:
        print("Transcript: {}".format(result.alternatives[0].transcript))
        print("Transcript: {}".format(result.alternatives[0].confidence))


