## Connect to the "Underground chat"

### https://github.com/Michael-Zapivahin/underground_chat
 
## How install:

Python3 should already be installed. 
Use pip or pip3, if there is a conflict with Python2) to install dependencies:

Copy repository to bots' catalog:
```bash
 git clone https://github.com/Michael-Zapivahin/underground_chat
```
Create and activate a virtual environment:
```bash

 python3 -m venv example_environment 
 source example_environment/bin/activate 
```
Install external libraries
```
pip install -r requirements.txt
```

## Program uses an environment variable

#### Variables:

```  
CHAT_TOKEN: chat's token for write messages.
```  

# Start

Arguments for running scripts can be replaced with settings in environment variables.

In this case, priority is given to the launch arguments.

```bash
python chat_reader.py [--host HOST] [--port READE_PORT] [--history HISTORY_FILE]

python chat_writer.py [--host HOST] [--port WRITE_PORT] ([--token CHAT_TOKEN] or [--name USER_NAME])
```

## The aim of the project 
The code is written for educational purposes on the online course for web developers [Devman практика Python](https://dvmn.org/)