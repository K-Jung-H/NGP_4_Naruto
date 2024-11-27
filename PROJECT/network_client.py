import socket

class NetworkClient:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        # IPv6까지 쓰려면 AF_INET6 로 설정 아직은 테스트 단계니까 일단 이걸로
        # UDP로 설정하려면 SOCK_DGRAM 이걸로
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.is_connected = False

    def connect(self):
        try:
            self.client_socket.connect((self.server_ip, self.server_port))
            self.is_connected = True
            print("서버에 연결되었습니다.")
        except Exception as e:
            print(f"서버 연결 실패: {e}")

    def send_key_data(self, key_data):
        if self.is_connected:
            try:
                # UDP설정이면 self.client_socket.sendto(key_data.encode('utf-8'), (self.server_ip, self.server_port))
                self.client_socket.sendall(key_data.encode('utf-8'))
            except Exception as e:
                print(f"데이터 전송 오류: {e}")
                self.is_connected = False

    def disconnect(self):
        self.client_socket.close()
        self.is_connected = False
        print("서버와의 연결이 종료되었습니다.")

    def __del__(self):
        # 객체 소멸 시 disconnect 호출
        self.disconnect()