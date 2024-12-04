#pragma once
#include "Object.h"
#define MAX_ROOMS 4


struct Room 
{
	int room_id;         // �� ��ȣ
	int player_count;    // ���� �濡 ���� �÷��̾� ��
	SOCKET players[2];   // �濡 ���� �÷��̾��� ����
};

class Room_Server 
{
private:
	Room rooms[MAX_ROOMS];  // �� �迭

public:
	Room_Server();
	bool JoinRoom(int room_id, SOCKET client_n, int& player_number);
	void LeaveRoom(int room_id, SOCKET client_n);
	void BroadcastRoomStatus(); // ��� �� ���¸� ����
};

class Timer {
public:
	Timer() : target_fps(60), last_time(std::chrono::high_resolution_clock::now()) {}

	void start(int fps) {
		target_fps = fps;
		last_time = std::chrono::high_resolution_clock::now();
	}

	float getElapsedTime() {
		auto current_time = std::chrono::high_resolution_clock::now();
		std::chrono::duration<float> elapsed = current_time - last_time;
		last_time = current_time; // ���� �ð��� ���� �������� ���� �ð����� ����
		return elapsed.count();   // �� ������ ��� �ð� ��ȯ
	}

	void Wait() {
		auto start_time = std::chrono::high_resolution_clock::now();

		// ������ ó�� �� ��� �ð� ���
		auto end_time = std::chrono::high_resolution_clock::now();
		std::chrono::duration<float> frame_duration = end_time - start_time;
		float frame_time = frame_duration.count(); // �� ������ ������ �ð� ���

		// ��ǥ FPS�� ���߱� ���� ��� �ð� ���
		float sleep_time = (1.0f / target_fps) - frame_time;
		if (sleep_time > 0.0f) {
			std::this_thread::sleep_for(std::chrono::duration<float>(sleep_time));
		}
		else {
			// sleep_time�� ������ ��� �α׸� ����ϰų�, ��� ó��
			std::cout << "Frame processing too slow for target FPS: " << target_fps << "\n";
		}
	}

private:
	int target_fps;
	std::chrono::time_point<std::chrono::high_resolution_clock> last_time;
};

class Server
{
private:
	// ������ - ȣ�� Ƚ�� ī���� �� Ÿ�̸� �ʱ�ȭ
	std::atomic<int> call_count = 0; // Thread-safe
	std::chrono::steady_clock::time_point last_time = std::chrono::steady_clock::now();

private:
	std::queue<std::pair<int, Key_Info>> keyQueue;
	Timer timer;

	CRITICAL_SECTION cs_key_queue; // Ű �Է� ���� ť�� ���� �Ӱ� ����

	std::array<Attack*, MAX_ATTACKS> Stage_Attack_Object_List; 

	SOCKET client1_socket = INVALID_SOCKET;
    SOCKET client2_socket = INVALID_SOCKET;

	Player* p1_ptr = NULL;
	Player* p2_ptr = NULL;

	float game_time = 0.0f;
public:
	Server() 
	{ 
		InitializeCriticalSection(&cs_key_queue); 
		Stage_Attack_Object_List.fill(nullptr);
	}
	~Server() { DeleteCriticalSection(&cs_key_queue); }

	void EnqueueKeyInput(int client_n, const Key_Info& keyInfo);
	bool DequeueKeyInput(std::pair<int, Key_Info>& keyInfo);

	bool Add_Client_Socket(SOCKET clientSocket, int playerNum);
	void Remove_Client_Socket(int playerNum);

	void Add_P1(Object* p_ptr, int n);
	void Add_P2(Object* p_ptr, int n);

	void Add_Skill_Object(Object* skill_ptr);

	void Decoding(std::pair<int, Key_Info>* key_info);
	Game_Data* Encoding();

	void Update_Server(float Elapsed_time);
	void Update_Collision() {};
	void Broadcast_GameData_All(Game_Data* data);
	
	int Get_Key_Input_Buffer_size() { return keyQueue.size(); }
	void Set_FrameRate(int n) { timer.start(n); }
	float Get_ElapsedTime() { return timer.getElapsedTime(); }
	void Wait() { timer.Wait(); }
	Player* Get_Player(int Client);
	void Remove_Player(int Client);


};

