# LLMTheBox

LLMTheBox is a project that leverages HackTheBox writeups as educational material, incorporating Language Model Machines (LLMs) and Retrieval Augmented Generation (RAG) to create an interactive and intelligent learning experience.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction

LLMTheBox aims to enhance cybersecurity education by utilizing advanced AI techniques. By integrating HackTheBox writeups with LLMs and RAG, the project provides an engaging and interactive platform for learning cybersecurity concepts and practices.

## Features

- **Interactive Learning:** Engage with HackTheBox writeups using conversational AI.
- **Retrieval Augmented Generation:** Combine LLMs with a retrieval mechanism to provide contextually relevant information.
- **Open Source:** Contribute to the project and improve the learning experience for everyone.
- **Powered by GPT4-Turbo** A fast and relatively affordable model

## Installation

To install LLMTheBox, follow these steps:

Clone the repository:
   ```bash
   git clone https://github.com/robsware/LLMTheBox.git
   cd LLMTheBox
   pip install -r requirements.txt

   ```
Set up a .env file with your openAI API Key in the format OPENAI_API_KEY = "sk-xxxxx"

During the first run, the chromaDB will need to be built and populated which may take a few minutes depending on your internet speed. 
Once the setup is complete, you can interact with the DB using:
```bash
python askquestion.py
```
This will prompt up a user input field where you can ask questions. Just keep an eye on your openAI bill.
