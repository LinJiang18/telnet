import telnetlib
import time

HOST = "170.106.117.254"
PORT = 8081

tn = telnetlib.Telnet(host=HOST, port=PORT, timeout=10)
tn.read_until(b"username (guest): ", timeout=2)
tn.write(b'a')
time.sleep(0.1)
tn.read_until(b"password: ", timeout=2)
tn.write(b'1')
time.sleep(0.1)
a = tn.read_very_eager().decode('utf8')
print(a)

# number = a.find("\n")
# print(a[:number])

# print(tn.read_until(b"You have 0 unread message.", timeout=2).decode('utf8'))
# time.sleep(0.5)
# tn.write(b'help\n\n')
# time.sleep(0.5)
# tn.write(b'shout hello world1234 dwdaw daw\n\n')
# time.sleep(0.5)
# print(tn.read_very_eager().decode('utf8'))


# tn.write("a".encode('ascii') + b'\n')
# # time.sleep(1)
# tn.read_until(b"password: ", timeout=2)
# tn.write("1".encode('ascii') + b'\n')
# # time.sleep(1)
# command_result = tn.read_very_eager().decode('ascii')
# print(command_result)

# tn.interact()


# account = input()  # 从键盘读取输入
# tn.write(account.encode('utf-8') + b"\r\n")
#
# tn.read_eager()
# passward = input()  # 从键盘读取输入
# tn.write(passward.encode('utf-8') + b"\r\n")
#
# tn.read_very_eager()

tn.write(b"exit\n")
# print("exit")

if __name__ == "__main__":
    pass