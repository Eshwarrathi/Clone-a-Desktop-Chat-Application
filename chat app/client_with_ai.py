import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
import random

# Client setup
HOST = '127.0.0.1'
PORT = 12345

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

nickname = input("Choose your nickname: ")
ai_nickname = "AI_Assistant"

# Predefined responses for the AI Assistant
ai_responses = [
    "Hello! How can I help you today?",
    "I'm here to assist you with any questions.",
    "Can you please elaborate on that?",
    "That's interesting! Tell me more.",
    "I'm not sure about that. Let me find out for you.",
    "Thank you for reaching out!"
]

def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK':
                client.send(nickname.encode('utf-8'))
            else:
                display_message(message)
                if nickname not in message:
                    ai_response(message)
        except:
            print("An error occurred!")
            client.close()
            break

def write():
    message = f'{nickname}: {message_entry.get()}'
    client.send(message.encode('utf-8'))
    message_entry.delete(0, tk.END)

def display_message(message):
    chat_window.config(state=tk.NORMAL)
    chat_window.insert(tk.END, message + '\n')
    chat_window.yview(tk.END)
    chat_window.config(state=tk.DISABLED)

def ai_response(user_message):
    # Simple rule-based response
    response = random.choice(ai_responses)
    ai_message = f'{ai_nickname}: {response}'
    client.send(ai_message.encode('utf-8'))

# GUI setup
root = tk.Tk()
root.title("Chat Application")

chat_window = scrolledtext.ScrolledText(root)
chat_window.pack(padx=20, pady=5)
chat_window.config(state=tk.DISABLED)

message_entry = tk.Entry(root, width=50)
message_entry.pack(padx=20, pady=5)

send_button = tk.Button(root, text="Send", command=write, borderwidth=2, relief="solid")
send_button.pack(padx=20, pady=5)

thread = threading.Thread(target=receive)
thread.start()

root.mainloop()
