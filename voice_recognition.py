import uuid
import os
import speech_recognition as sr


class VoiceRecognizer:
    def __init__(self):
        self.language = 'ru_RU'
        self.r = sr.Recognizer()

    def __convert_voice(self, voice_file):
        filename = str(uuid.uuid4())
        self.file_name_full = "./voice/"+filename+".ogg"
        self.file_name_full_converted = "./ready/"+filename+".wav"
        with open(self.file_name_full, 'wb') as new_file:
            new_file.write(voice_file)
        os.system(os.path.abspath("ffmpeg") + " -i " +
                  self.file_name_full+"  "+self.file_name_full_converted)

    def __remove_voice(self):
        os.remove(self.file_name_full)
        os.remove(self.file_name_full_converted)

    def __recognize(self, filename):
        with sr.AudioFile(filename) as source:
            audio_text = self.r.listen(source)
            try:
                text = self.r.recognize_google(
                    audio_text, language=self.language)
                return text
            except:
                return "Не получилось распознать((("

    def get_text(self, voice_file):
        self.__convert_voice(voice_file)
        text = self.__recognize(self.file_name_full_converted)
        self.__remove_voice()
        return text
