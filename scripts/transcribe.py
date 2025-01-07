import assemblyai as aai
import os
import time
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set your API key from environment variable
aai.settings.api_key = os.getenv('ASSEMBLYAI_API_KEY')

# Get the current working directory
cwd = os.getcwd()
print(f"Current Working Directory: {cwd}")

# List all files in the @audio folder
audio_folder_path = os.path.join(cwd, 'audio')
audio_files = os.listdir(audio_folder_path)  # Store files in a list
print("Files in the @audio directory:")
for index, filename in enumerate(audio_files):
    print(f"{index + 1}: {filename}")  # Display files with index

# Specify the audio file name by allowing user to select
audio_file_index = int(input("Enter the number of the audio file you want to use: ")) - 1
if 0 <= audio_file_index < len(audio_files):
    audio_file_name = audio_files[audio_file_index]  # Select file based on user input
else:
    print("Error: Invalid selection.")
    sys.exit(1)  # Exit if the selection is invalid

# Construct the full path to the audio file in the @audio folder
audio_file_path = os.path.join(audio_folder_path, audio_file_name)

# Check if the audio file exists
if not os.path.isfile(audio_file_path):
    print(f"Error: The specified audio file '{audio_file_name}' does not exist in the @audio directory.")
else:
    # Initialize the transcriber
    transcriber = aai.Transcriber()

    # Transcribe the file - this returns a Transcript object
    transcript = transcriber.transcribe(audio_file_path)

    # Access the transcribed text through the text attribute of the transcript object
    print(transcript.text)

    # Ask user if they want speaker diarization
    diarization_choice = input("Do you want to enable speaker diarization? (yes/no): ").strip().lower()

    # If user wants speaker diarization, ask for speaker names
    speaker_names = []
    if diarization_choice == 'yes':
        num_speakers = int(input("How many speakers are there in the audio? "))
        for i in range(num_speakers):
            speaker_name = input(f"Enter the name of speaker {i + 1} (or press Enter to use default 'Speaker {i + 1}'): ")
            if speaker_name.strip() == "":
                speaker_names.append(f"Speaker {i + 1}")
            else:
                speaker_names.append(speaker_name)

    # Transcribe the audio file
    try:
        config = aai.TranscriptionConfig(speaker_labels=True)
        
        # Start transcription and show loading animation
        print("Transcribing... Please wait.")
        transcript = transcriber.transcribe(audio_file_path, config=config)

        # Animation while waiting for transcription
        for _ in range(10):  # Adjust the range for longer or shorter animation
            for char in "|/-\\":
                sys.stdout.write(f"\r{char} Waiting for transcription...")
                sys.stdout.flush()
                time.sleep(0.2)  # Adjust speed of animation

        # Only proceed with speaker diarization if user chose it
        if diarization_choice == 'yes':
            print("\nTranscription with Speaker Diarization:")
            for utterance in transcript.utterances:
                speaker = utterance.speaker
                text = utterance.text
                speaker_index = int(speaker) - 1 if speaker.isdigit() else -1
                speaker_name = speaker_names[speaker_index] if speaker_index >= 0 and speaker_index < len(speaker_names) else f"Speaker {speaker}"
                print(f"{speaker_name}: {text}")
        else:
            print("\nTranscription:")
            print(transcript.text)

    except TypeError as e:
        print(f"TypeError: {e}. Please check the parameters passed to the transcribe method.")
    except Exception as e:
        print(f"An error occurred: {e}")

    if transcript:
        # Ask user for the desired output filename
        output_filename = input("Enter the desired name for the transcription file (without extension): ") + ".txt"

        # Construct the full path to save the transcription in the @txtOutputs folder
        output_file_path = os.path.join(cwd, 'txtOutputs', output_filename)

        # Save the transcription based on whether diarization was used
        with open(output_file_path, 'w', encoding='utf-8') as f:
            if diarization_choice == 'yes':
                for utterance in transcript.utterances:
                    speaker = utterance.speaker
                    text = utterance.text
                    speaker_index = int(speaker) - 1 if speaker.isdigit() else -1
                    speaker_name = speaker_names[speaker_index] if speaker_index >= 0 and speaker_index < len(speaker_names) else f"Speaker {speaker}"
                    f.write(f"{speaker_name}: {text}\n")
            else:
                f.write(transcript.text)

        print(f"Transcription saved to {output_file_path}")
    else:
        print("Transcription was not created.")