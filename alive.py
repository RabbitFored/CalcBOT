from threading import Thread
from flask import Flask


app = Flask("")

@app.route("/")
def main():
  return'hello_world'
  
  
def run():
  app.run(host="0.0.0.0",port=8080)

def keep_alive():
  server = Thread(target=run)
  server.start()
