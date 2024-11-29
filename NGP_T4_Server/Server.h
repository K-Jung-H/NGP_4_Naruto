#pragma once
#include "Object.h"



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
		last_time = current_time; // 현재 시간을 다음 프레임의 시작 시간으로 설정
		return elapsed.count();   // 초 단위로 경과 시간 반환
	}

	void Wait() {
		auto start_time = std::chrono::high_resolution_clock::now();

		// 프레임 처리 후 경과 시간 계산
		auto end_time = std::chrono::high_resolution_clock::now();
		std::chrono::duration<float> frame_duration = end_time - start_time;
		float frame_time = frame_duration.count(); // 초 단위로 프레임 시간 계산

		// 목표 FPS에 맞추기 위해 대기 시간 계산
		float sleep_time = (1.0f / target_fps) - frame_time;
		if (sleep_time > 0.0f) {
			std::this_thread::sleep_for(std::chrono::duration<float>(sleep_time));
		}
		else {
			// sleep_time이 음수인 경우 로그를 출력하거나, 경고 처리
			std::cout << "Frame processing too slow for target FPS: " << target_fps << "\n";
		}
	}

private:
	int target_fps;
	std::chrono::time_point<std::chrono::high_resolution_clock> last_time;
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

	Server_Mode sever_mode = Server_Mode::ETC;

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

	void Update_Character_Select(float Elapsed_time);
	void Update_Game_World(float Elapsed_time);
	void Update_Collision() {};
	void Broadcast_GameData_All(Game_Data* data);
	
	int Get_Key_Input_Buffer_size() { return keyQueue.size(); }
	void Set_FrameRate(int n) { timer.start(n); }
	float Get_ElapsedTime() { return timer.getElapsedTime(); }
	void Wait() { timer.Wait(); }
	Player* Get_Player(int Client);
	void Remove_Player(int Client);


};

