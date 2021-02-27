import socket
import re
from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash


class User(db.Model):
    """
    User Model Class
    """

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def set_password(self, password):
        self.password = generate_password_hash(password, method="sha512")


class RCON:
    def __init__(
        self,
        host: str,
        port: int,
        password: str,
        packet_prefix: bytes = b"\xff\xff\xff\xff",
    ):

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # dgram is udp
        self.packet_prefix = packet_prefix
        self.host = host
        self.port = port
        self.password = password

    # def recv_timeout(self, the_socket, timeout=2):
    #     # make socket non blocking
    #     the_socket.setblocking(1)

    #     # total data partwise in an array
    #     total_data = None;

    #     # beginning time
    #     begin=time.time()
    #     while 1:
    #         # if you got some data, then break after timeout
    #         if total_data and time.time()-begin > timeout:
    #             break

    #         # if you got no data at all, wait a little longer, twice the timeout
    #         elif time.time()-begin > timeout*2:
    #             break

    #         # recv something
    #         try:
    #             data = the_socket.recv(8192)
    #             if data:
    #                 print('Data from socket as string: ' + str(data))
    #                 data_str = data.decode("utf-8", errors="ignore")
    #                 total_data = total_data + data_str
    #                 print('Got this from udp socket: ' + data_str)

    #                 if data_str.contains('\n\n'):
    #                     print('Reached end of reply...')
    #                     break

    #                 # change the beginning time for measurement
    #                 begin = time.time()
    #             else:
    #                 # sleep for sometime to indicate a gap
    #                 time.sleep(0.1)
    #         except:
    #             pass

    #     # join all parts to make final string
    #     return total_data

    def strip_colors(self, some_name):
        some_name = some_name.replace("^^", "^")
        some_name = some_name.replace("^0", "")
        some_name = some_name.replace("^1", "")
        some_name = some_name.replace("^2", "")
        some_name = some_name.replace("^3", "")
        some_name = some_name.replace("^4", "")
        some_name = some_name.replace("^5", "")
        some_name = some_name.replace("^6", "")
        some_name = some_name.replace("^7", "")
        some_name = some_name.replace("^8", "")
        some_name = some_name.replace("^9", "")

        return some_name

    def replace_multi_occurences(self, string, char):
        pattern = char + "{2,}"
        string = re.sub(pattern, char, string)
        return string

    def send(self, cmd):
        cmd = f"rcon {self.password} {cmd}"
        cmd = self.packet_prefix + cmd.encode()
        self.socket.sendto(cmd, (self.host, self.port))
        data, addr = self.socket.recvfrom(8192)
        print("Data from socket as string:", str(data[10:]))
        data_str = data[10:].decode("utf-8", errors="ignore")
        print("Data after decode:", data_str)

        return data_str

    def kick(self, player_num):
        response = self.send(f"clientkick {player_num}")
        return "EXE_PLAYERKICKED" in response

    def status(self):
        status_str = self.send("status")
        status_str = self.strip_colors(status_str)

        # for char in status_str:
        #     print(f"{char} {ord(char)}")

        player_objects = []

        i = 0
        for some_str in status_str.split("\n"):
            # print('Line %d - String: %s' % (i, some_str))
            if "map: " in some_str:
                continue
            elif "num score" in some_str:
                continue
            elif (
                some_str == ""
                or some_str == "\r"
                or some_str == " "
                or some_str == "\t"
            ):
                continue
            elif "--- ----- ---- ------ ---------------" in some_str:
                continue

            some_str = some_str.strip()
            some_str = self.replace_multi_occurences(some_str, " ")
            player_parts = some_str.split(" ")
            res_len = len(player_parts)
            if res_len < 9:
                print("Error response is incomplete - HANDLE THIS!!!")
                raise Exception("Error response is incomplete - HANDLE THIS!!!")

            player = {}

            player["num"] = player_parts[0]
            player["score"] = player_parts[1]
            player["ping"] = player_parts[2]
            guid = player_parts[3]
            player["rate"] = player_parts[res_len - 1]
            qport = player_parts[res_len - 2]
            player["address"] = player_parts[res_len - 3]
            lastmsg = player_parts[res_len - 4]

            player["name"] = ""
            for j in range(4, res_len - 4):
                if j == res_len - 5:
                    player["name"] = player["name"] + player_parts[j]
                else:
                    player["name"] = player["name"] + player_parts[j] + " "

            print("Located player line: |" + some_str + "|")

            # i = i + 1
            player_objects.append(player)

        return player_objects
