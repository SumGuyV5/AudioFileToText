import os
import sys
import speech_recognition as sr
from pydub import AudioSegment


# a function that splits the audio file into chunks
# and applies speech recognition
def stt_conversion(file_name):
    # open the audio file that was pass to the function.
    song = AudioSegment.from_wav(file_name)

    # opens two files that we will add the text too
    fh_google = open(f"{os.path.splitext(file_name)[0]}_google.txt", "w+")
    fh_sphinx = open(f"{os.path.splitext(file_name)[0]}_sphinx.txt", "w+")

    # split into 5 second chunks
    chunks = song[::5000]

    # create a directory to store the audio chunks.
    try:
        os.mkdir('audio_chunks')
    except FileExistsError:
        pass

    # change to the audio_chunks directory to store the audio chunks.
    os.chdir('audio_chunks')

    # create a chunk of audio that is just silent
    chunk_silent = AudioSegment.silent()

    # process each chunk
    for i, chunk in enumerate(chunks):

        # lets add silent to the beginning and end of the audio chunk
        audio_chunk = chunk_silent + chunk + chunk_silent

        # filename for the chunk
        filename = f'chunk{i}.wav'

        # export the audio chunk and save it in the directory.
        print(f"saving {filename}")
        audio_chunk.export(f"./{filename}", bitrate='192k', format="wav")

        print(f"Processing chunk {i}")

        # create a speech recognition object
        r = sr.Recognizer()

        # recognize the chunk
        with sr.AudioFile(filename) as source:
            r.adjust_for_ambient_noise(source)
            audio_listened = r.listen(source)

        try:
            # try converting it to text
            rec = r.recognize_google(audio_listened)
            # write the output to the file.
            fh_google.write(f"{rec}. ")
        except sr.UnknownValueError:
            print("Could not understand audio. google")
        except sr.RequestError:
            print(f"Could not request results. check your internet connection.")

        try:
            # try converting it to text
            rec = r.recognize_sphinx(audio_listened)
            # write the output to the file.
            fh_sphinx.write(f"{rec}. ")
        except sr.UnknownValueError:
            print("Could not understand audio. sphinx")
        # no internet is required for sphinx
        except sr.RequestError:
            print("Could not request results. check your internet connection.")

    os.chdir('..')


if __name__ == '__main__':
    stt_conversion(sys.argv[1])
