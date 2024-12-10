#pragma once
#include "Object.h"

#include <chrono>
#include <thread>
#include <iostream>

class Timer {
public:
	Timer() : target_fps(60), last_time(std::chrono::high_resolution_clock::now()) {}

	// ��ǥ FPS ���� �� �ʱ�ȭ
	void Start(int fps) {
		target_fps = fps;
		last_time = std::chrono::high_resolution_clock::now();
	}

	// ������ ��� �ð� ���
	float GetElapsedTime() {
		auto current_time = std::chrono::high_resolution_clock::now();
		std::chrono::duration<float> elapsed = current_time - last_time;
		last_time = current_time; // ���� �ð��� ���� �������� ���� �ð����� ����
		return elapsed.count();   // �� ������ ��� �ð� ��ȯ
	}

	// ��ǥ FPS�� ���� ���
	void Wait() {
		auto frame_start = std::chrono::high_resolution_clock::now();  // ������ ���� �ð�
		auto frame_end = std::chrono::high_resolution_clock::now();  // ������ ó�� ���� �ð�
		std::chrono::duration<float> frame_duration = frame_end - frame_start;
		float frame_time = frame_duration.count(); // �� ������ ������ �ð� ���

		// ��ǥ FPS�� ���߱� ���� ��� �ð� ���
		float target_frame_time = 1.0f / target_fps; // ��ǥ ������ �ð�
		float sleep_time = target_frame_time - frame_time; // ���� ��� �ð�

		if (sleep_time > 0.0f) {
			std::this_thread::sleep_for(std::chrono::duration<float>(sleep_time));  // ���
		}
		else {
			// ������ ó�� �ӵ��� ��ǥ FPS�� �ʰ��ϴ� ��� ��� ���
			std::cout << "Frame processing too slow for target FPS: " << target_fps << "\n";
		}
	}

private:
	int target_fps; // ��ǥ FPS
	std::chrono::time_point<std::chrono::high_resolution_clock> last_time; // ������ ������ �ð�
};


enum class Server_Mode
{
	Character_Select,
	Game_Play,
	ETC
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

	Server_Mode server_mode = Server_Mode::ETC;

	Player* p1_ptr = NULL;
	Player* p2_ptr = NULL;

	float game_time = 0.0f;
public:
	Server() 
	{ 
		server_mode = Server_Mode::Character_Select;
		InitializeCriticalSection(&cs_key_queue); 
		Stage_Attack_Object_List.fill(nullptr);
	}
	~Server() { DeleteCriticalSection(&cs_key_queue); }

	void EnqueueKeyInput(int client_n, const Key_Info& keyInfo);
	bool DequeueKeyInput(std::pair<int, Key_Info>& keyInfo);

	bool Add_Client_Socket(SOCKET clientSocket, int playerNum);
	void Remove_Client_Socket(int playerNum);

	void Add_P1(Player* p_ptr);
	void Add_P2(Player* p_ptr);

	void Add_Skill_Object(Object* skill_ptr);

	void Decoding(std::pair<int, Key_Info>* key_info);
	void Select_Mode_Decoding(std::pair<int, Key_Info>* key_info);
	void Game_Mode_Decoding(std::pair<int, Key_Info>* key_info);
	Game_Data* Encoding();

	void Update_Character_Select(float Elapsed_time);
	void Update_Game_World(float Elapsed_time);
	void Update_Collision(float Elapsed_time);
	void Check_Overlap();
	void Broadcast_GameData_All(Game_Data* data);
	
	int Get_Key_Input_Buffer_size() { return keyQueue.size(); }
	void Set_FrameRate(int n) { timer.Start(n); }
	float Get_ElapsedTime() { return timer.GetElapsedTime(); }
	void Wait() { timer.Wait(); }
	Player* Get_Player(int Client);
	void Remove_Player(int Client);

	Server_Mode Get_Server_Mode() { return server_mode; };
	void Set_Server_Mode(Server_Mode mode) { server_mode = mode; };
};

