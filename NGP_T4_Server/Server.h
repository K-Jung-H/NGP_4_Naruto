#pragma once
#include "Object.h"

#include <chrono>
#include <thread>
#include <iostream>

class Timer {
public:
	Timer() : target_fps(60), last_time(std::chrono::high_resolution_clock::now()) {}

	// 목표 FPS 설정 및 초기화
	void Start(int fps) {
		target_fps = fps;
		last_time = std::chrono::high_resolution_clock::now();
	}

	// 프레임 경과 시간 계산
	float GetElapsedTime() {
		auto current_time = std::chrono::high_resolution_clock::now();
		std::chrono::duration<float> elapsed = current_time - last_time;
		last_time = current_time; // 현재 시간을 다음 프레임의 시작 시간으로 설정
		return elapsed.count();   // 초 단위로 경과 시간 반환
	}

	// 목표 FPS에 맞춰 대기
	void Wait() {
		auto frame_start = std::chrono::high_resolution_clock::now();  // 프레임 시작 시간
		auto frame_end = std::chrono::high_resolution_clock::now();  // 프레임 처리 끝난 시간
		std::chrono::duration<float> frame_duration = frame_end - frame_start;
		float frame_time = frame_duration.count(); // 초 단위로 프레임 시간 계산

		// 목표 FPS에 맞추기 위한 대기 시간 계산
		float target_frame_time = 1.0f / target_fps; // 목표 프레임 시간
		float sleep_time = target_frame_time - frame_time; // 남은 대기 시간

		if (sleep_time > 0.0f) {
			std::this_thread::sleep_for(std::chrono::duration<float>(sleep_time));  // 대기
		}
		else {
			// 프레임 처리 속도가 목표 FPS를 초과하는 경우 경고 출력
			std::cout << "Frame processing too slow for target FPS: " << target_fps << "\n";
		}
	}

private:
	int target_fps; // 목표 FPS
	std::chrono::time_point<std::chrono::high_resolution_clock> last_time; // 마지막 프레임 시간
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
	// 디버깅용 - 호출 횟수 카운터 및 타이머 초기화
	std::atomic<int> call_count = 0; // Thread-safe
	std::chrono::steady_clock::time_point last_time = std::chrono::steady_clock::now();

	
private:
	std::queue<std::pair<int, Key_Info>> keyQueue;
	Timer timer;

	CRITICAL_SECTION cs_key_queue; // 키 입력 저장 큐에 대한 임계 영역

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

