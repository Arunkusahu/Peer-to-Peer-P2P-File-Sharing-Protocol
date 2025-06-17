# Peer-to-Peer (P2P) File Sharing Protocol

## 🧠 Project Description

This project implements a simple decentralized Peer-to-Peer (P2P) file sharing system in Python.  
Peers can share files and send text messages directly with each other using TCP sockets.  
A central **tracker server** is used only for peer discovery (keeping track of online peers), but all file transfers and messages happen directly between peers.

---

## 🚀 Features

- Register peers and discover active peers using a tracker server.
- Share files stored in a local `shared/` folder.
- Download files directly from other peers.
- Send text messages between peers.
- Files are transferred in chunks for reliability.
- Simple console-based user interface.

---

## 🛠 Tech Stack

- Python 3.6 or higher
- TCP socket programming
- Multithreading for handling multiple connections

---

## ✅ Prerequisites

- Python 3.6+ installed on your system  
- Basic understanding of command line / terminal

---


## 📂 Project Structure

### 1. Clone or Download the Project

Download the project folder to your local machine.

### 2. Create the Required Folders

Before running the peer script, create the following folders inside the project directory:

- `shared/` — Place files here that you want to share with other peers.
- `downloads/` — Files downloaded from other peers will be saved here automatically (created by the script if it doesn't exist).

You can create them via command line:

```bash
mkdir shared
mkdir downloads

How to Run
Step 1: Start the Tracker Server
Open a terminal and run:

Step 2: Start One or More Peers
Open a new terminal for each peer you want to start.

Run the peer program:
Copy code
python peer.py
You will be prompted to enter a unique peer name (e.g., Alice).

Step 3: Interact Between Peers
Use the menu options in each peer terminal:

---

### 👨‍💻 About Developer ✈️

Made with ❤️ by ARUN KUMAR SAHU 😎

- 📧 Email: aurnkumarsahu634@gmail.com

- 📷 Instagram: @arunsahu_98

- 💼 LinkedIn: Arun Kumar Sahu

- 💻 GitHub: github.com/Arunkusahu
