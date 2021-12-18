import sys
from commandclient import CommandClient

host = sys.argv[1]
port = sys.argv[2]

print("Connecting to "+str(host)+":"+str(port))
while True:
    text = input("CMD to send:")
    if (text == "q"):
        sys.exit()

    client = CommandClient(host, port)

    response = client.send(str(text.rstrip()))
    print(">"+str(response))

