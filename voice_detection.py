import speech_recognition as sr
from pydub import AudioSegment
import io
import glob
import os

ffmpeg_paths = glob.glob(r"C:\Users\DELL\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg*\*\bin\ffmpeg.exe")
if ffmpeg_paths:
    ffmpeg_bin_dir = os.path.dirname(ffmpeg_paths[0])
    # Pydub relies heavily on system PATH for both ffmpeg AND ffprobe. We inject it.
    if ffmpeg_bin_dir not in os.environ["PATH"]:
        os.environ["PATH"] = ffmpeg_bin_dir + os.pathsep + os.environ["PATH"]
    AudioSegment.converter = ffmpeg_paths[0]

def extract_text_from_audio(audio_file):
    r = sr.Recognizer()
    
    try:
        audio_file.seek(0)
        
        # Load audio using pydub, which relies on ffmpeg for mp3/mpeg/mp4 processing
        audio_segment = AudioSegment.from_file(audio_file)
        
        # Convert audio natively into in-memory wav stream
        wav_io = io.BytesIO()
        audio_segment.export(wav_io, format="wav")
        wav_io.seek(0)
        
        with sr.AudioFile(wav_io) as source:
            audio_data = r.record(source)
            text = r.recognize_google(audio_data)
            return True, text
            
    except sr.UnknownValueError:
        return False, "Speech Recognition could not understand the audio."
    except sr.RequestError as e:
        return False, f"Could not request results from Speech Recognition service; {e}"
    except Exception as e:
        return False, f"Error processing audio format: {e}. If using an mp3/mp4, ensure ffmpeg is correctly installed and registered."
