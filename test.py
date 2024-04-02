import telnetlib
import time

HOST = "170.106.117.254"
PORT = 8081



tn = telnetlib.Telnet(host=HOST, port=PORT, timeout=10)
# tn.interact()
tn.read_until(b"username (guest): ", timeout=0.5)
tn.write(b'a\n\n')
time.sleep(0.1)
tn.read_until(b"password: ", timeout=0.5)
tn.write(b'1\n\n')
time.sleep(0.5)
print(tn.read_very_eager().decode('utf8'))
time.sleep(0.5)
# while(True):
#     info = input()
#     tn.write(info.encode('ascii') + b'\n\n')
#     time.sleep(0.1)
#     print(tn.read_very_eager().decode('utf8'))

tn.write(b"exit\n")
print("exit")

if __name__ == "__main__":
    pass