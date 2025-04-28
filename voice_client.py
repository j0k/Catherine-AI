# Catherine-AI remote client

import argparse
import asyncio
import json
import logging
import os
import queue
import sys
from urllib.parse import urlparse

import requests
import sounddevice as sd
import websockets
import pyttsx3
import vosk

import play_wav

# code based on run_remoteva_voskrem.py (Irina Assistant)

VERSION = "1.4"
ERROR_CONNECTION_FILE = "error_connection.wav"
ERROR_PROCESSING_FILE = "error_processing.wav"
TMP_AUDIO_FILE = "tmpfile.wav"

class VoiceClient:
    def __init__(self):
        self.load_config()
        self.initialize_tts()
        self.audio_queue = None
        self.mic_blocked = False
        self.setup_error_files()

    def load_config(self):
        """Load configuration from JSON file"""
        with open('options.json', 'r', encoding="utf-8") as f:
            config = json.load(f)

        self.tts_formats = config["ttsFormat"].split(",")
        self.base_url = config["baseUrl"]
        self.server_url = urlparse(self.base_url)

    def initialize_tts(self):
        """Initialize text-to-speech engine if needed"""
        if "saytxt" in self.tts_formats:
            self.tts_engine = pyttsx3.init()
            self.tts_engine.setProperty("voice", 0)

    def setup_error_files(self):
        """Download error notification audio files if missing"""
        if not os.path.exists(ERROR_CONNECTION_FILE):
            self.download_error_files()

    def download_error_files(self):
        """Download required error audio files from server"""
        print("Downloading error notification audio files...")

        error_messages = [
            ("Connection error: Lost contact with server", ERROR_CONNECTION_FILE),
            ("Error processing server response", ERROR_PROCESSING_FILE)
        ]

        for text, filename in error_messages:
            response = requests.get(
                f"{self.base_url}ttsWav",
                params={"text": text}
            )
            result = json.loads(response.text)
            play_wav.saywav_to_file(result, filename)

        print("Error audio files downloaded successfully!")

    async def handle_server_response(self, response):
        """Process server response and handle TTS playback"""
        try:
            result = json.loads(response)
            if result == "NO_VA_NAME" or not result:
                return

            if "saytxt" in self.tts_formats and "restxt" in result:
                self.tts_engine.say(result["restxt"])
                self.tts_engine.runAndWait()

            if "saywav" in self.tts_formats:
                play_wav.saywav_to_file(result, TMP_AUDIO_FILE)
                self.mic_blocked = True
                try:
                    play_wav.play_wav(TMP_AUDIO_FILE)
                except Exception as e:
                    print(f"Error playing WAV file: {e}")
                finally:
                    self.mic_blocked = False

        except json.JSONDecodeError:
            play_wav.play_wav(ERROR_PROCESSING_FILE)

    async def process_audio_stream(self, websocket, device):
        """Process audio stream and handle voice commands"""
        await websocket.send(f'{{ "config" : {{ "sample_rate" : {device.samplerate} }} }}')

        while True:
            audio_data = await self.audio_queue.get()
            await websocket.send(audio_data)

            response = await websocket.recv()
            result = json.loads(response)

            if text := result.get("text"):
                print(f"Recognized: {text}")
                await self.process_voice_command(text)

    async def process_voice_command(self, text):
        """Send voice command to server and handle response"""
        try:
            response = requests.get(
                f"{self.base_url}sendRawTxt",
                params={"rawtxt": text, "returnFormat": ",".join(self.tts_formats)}
            )
            await self.handle_server_response(response.text)

        except requests.ConnectionError:
            play_wav.play_wav(ERROR_CONNECTION_FILE)
        except Exception as e:
            print(f"Processing error: {e}")
            play_wav.play_wav(ERROR_PROCESSING_FILE)

    async def run_client(self, args):
        """Main client execution loop"""
        with sd.RawInputStream(
            samplerate=args.samplerate,
            blocksize=4000,
            device=args.device,
            dtype='int16',
            channels=1,
            callback=self.audio_callback
        ) as device:

            async with websockets.connect(args.uri) as websocket:
                await self.process_audio_stream(websocket, device)

    def audio_callback(self, indata, frames, time, status):
        """Audio input callback function"""
        if not self.mic_blocked:
            self.audio_queue.put_nowait(bytes(indata))

def parse_arguments():
    """Configure and parse command line arguments"""
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-l', '--list-devices', action='store_true',
                        help='Show available audio devices')
    args, remaining = parser.parse_known_args()

    if args.list_devices:
        print(sd.query_devices())
        sys.exit(0)

    parser = argparse.ArgumentParser(
        description="Voice Assistant Client",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=[parser]
    )
    parser.add_argument('-u', '--uri', type=str,
                        help='WebSocket server URL',
                        default=f'ws://{client.server_url.hostname}:{client.server_url.port + 1}')
    parser.add_argument('-d', '--device', type=int_or_str,
                        help='Input device ID or name')
    parser.add_argument('-r', '--samplerate', type=int,
                        default=16000, help='Sampling rate')

    return parser.parse_args(remaining)

def int_or_str(value):
    """Helper for device ID parsing"""
    try:
        return int(value)
    except ValueError:
        return value

async def main():
    """Main application entry point"""
    global client
    client = VoiceClient()
    args = parse_arguments()

    logging.basicConfig(level=logging.INFO)
    client.audio_queue = asyncio.Queue()

    print(f"Voice Assistant Client v{VERSION}")
    print(f"TTS Formats: {', '.join(client.tts_formats)}")
    print(f"Server URL: {args.uri}")
    print("Starting voice processing...")

    await client.run_client(args)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nClient terminated by user")
        sys.exit(0)
