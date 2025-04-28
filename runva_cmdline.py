import traceback

from vacore import VACore
import time

# ------------------- main loop ------------------
if __name__ == "__main__":
    cmd_core = VACore()
    cmd_core.init_with_plugins()
    print("Command-line interface for VoiceAssistantCore.")

    # here you can debug any command
    time.sleep(0.5) # timeout
    cmd = "hello"
    try:
        cmd_core.execute_next(cmd,cmd_core.context)
    except:
        if cmd == "hello":
            print("Error running 'hello' command. Most likely a problem with TTS.")
        import traceback
        traceback.print_exc()


    exit(0) # comment fo you want to work in command-line mode

    print("Enter command (user text like 'hello') or 'exit'")
    while True:
        cmd = input("> ")
        if cmd == "exit":
            break

        cmd_core.execute_next(cmd,cmd_core.context)
