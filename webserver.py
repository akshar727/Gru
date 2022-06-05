from flask import Flask

from threading import Thread



app = Flask('')



@app.route('/')

def home():

    return "Discord bot is OK and running\nWebserver is OK and ready to be pinged!"


@app.route('/files/1')

def jobs():
    with open('databases/jobs.json','r') as f:
        text = f.read()
    return text

@app.route('/files/2')

def levels():
    with open('databases/levels.json','r') as f:
        text = f.read()
    return text


@app.route('/files/3')

def lootboxes():
    with open('databases/lootboxes.json','r') as f:
        text = f.read()
    return text

@app.route('/files/4')

def bank():
    with open('databases/mainbank.json','r') as f:
        text = f.read()
    return text


@app.route('/files/5')

def prefixes():
    with open('databases/prefixes.json','r') as f:
        text = f.read()
    return text

@app.route('/files/6')

def role():
    with open('databases/reactrole.json','r') as f:
        text = f.read()
    return text



@app.route('/files/7')

def conf():
    with open('databases/server_configs.json','r') as f:
        text = f.read()
    return text



def run():
  app.run(host='0.0.0.0',port=8080)


def keep_alive():  

    t = Thread(target=run)

    t.start()