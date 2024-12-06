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
		return elapsed.count(); // 초 단위로 경과 시간 반환
	}

	// 목표 FPS에 맞춰 대기
	void Wait() {
		auto current_time = std::chrono::high_resolution_clock::now();
		std::chrono::duration<float> frame_duration = current_time - last_time;

		// 목표 FPS에 따라 프레임 간격 계산
		float target_frame_time = 1.0f / target_fps;

		// 목표 시간까지 남은 대기 시간 계산
		float sleep_time = target_frame_time - frame_duration.count();

		// 대기 시간 적용
		if (sleep_time > 0.0f) {
			std::this_thread::sleep_for(std::chrono::duration<float>(sleep_time));
		}

		// 현재 시간을 `last_time`으로 갱신
		last_time = std::chrono::high_resolution_clock::now();
	}

private:
	int target_fps; // 목표 FPS
	std::chrono::time_point<std::chrono::high_resolution_clock> last_time; // 마지막 프레임 시간
};

//class Timer {
//public:
//    Timer()
//        : target_fps(100), // 기본 목표 FPS 설정
//        m_bStopped(false),
//        m_fTimeScale(1.0),
//        m_nPerformanceFrequencyPerSec(0),
//        m_nBasePerformanceCounter(0),
//        m_nLastPerformanceCounter(0),
//        m_nCurrentPerformanceCounter(0),
//        m_nStopPerformanceCounter(0),
//        m_nPausedPerformanceCounter(0) {
//
//        // 성능 카운터 주파수 확인
//        QueryPerformanceFrequency((LARGE_INTEGER*)&m_nPerformanceFrequencyPerSec);
//        QueryPerformanceCounter((LARGE_INTEGER*)&m_nLastPerformanceCounter);
//        m_fTimeScale = 1.0 / (double)m_nPerformanceFrequencyPerSec;
//
//        m_nBasePerformanceCounter = m_nLastPerformanceCounter;
//        m_nStopPerformanceCounter = 0;
//        m_nPausedPerformanceCounter = 0;
//    }
//
//    // 타이머 시작
//    void Start(int fps = -1) {
//        if (fps != -1) {
//            target_fps = fps;  // 목표 FPS 설정
//        }
//
//        if (m_bStopped) {
//            // 정지된 타이머가 있을 경우, 멈춘 시간을 조정하여 다시 시작
//            QueryPerformanceCounter((LARGE_INTEGER*)&m_nCurrentPerformanceCounter);
//            m_nPausedPerformanceCounter += m_nCurrentPerformanceCounter - m_nStopPerformanceCounter;
//            m_nLastPerformanceCounter = m_nCurrentPerformanceCounter;
//            m_nStopPerformanceCounter = 0;
//            m_bStopped = false;
//        }
//    }
//
//    // 타이머 멈추기
//    void Stop() {
//        if (!m_bStopped) {
//            QueryPerformanceCounter((LARGE_INTEGER*)&m_nStopPerformanceCounter);
//            m_bStopped = true;
//        }
//    }
//
//    // 경과 시간 반환
//    float GetElapsedTime() {
//        if (m_bStopped) {
//            return 0.0f;
//        }
//
//        QueryPerformanceCounter((LARGE_INTEGER*)&m_nCurrentPerformanceCounter);
//        float fTimeElapsed = (float)((m_nCurrentPerformanceCounter - m_nLastPerformanceCounter) * m_fTimeScale);
//        return fTimeElapsed;
//    }
//
//    // 목표 FPS에 맞춰 대기
//    void Wait() {
//        if (m_bStopped) {
//            return;
//        }
//
//        QueryPerformanceCounter((LARGE_INTEGER*)&m_nCurrentPerformanceCounter);
//        float elapsedTime = (float)((m_nCurrentPerformanceCounter - m_nLastPerformanceCounter) * m_fTimeScale);
//
//        // 목표 FPS에 맞는 대기 시간 계산
//        float targetFrameTime = 1.0f / target_fps;
//        float sleepTime = targetFrameTime - elapsedTime;
//
//        if (sleepTime > 0.0f) {
//            std::this_thread::sleep_for(std::chrono::duration<float>(sleepTime));
//        }
//
//        // 현재 시간을 `last_time`으로 갱신
//        m_nLastPerformanceCounter = m_nCurrentPerformanceCounter;
//    }
//
//    // 전체 시간 반환
//    float GetTotalTime() {
//        if (m_bStopped) {
//            return (float)((m_nStopPerformanceCounter - m_nPausedPerformanceCounter - m_nBasePerformanceCounter) * m_fTimeScale);
//        }
//        return (float)((m_nCurrentPerformanceCounter - m_nPausedPerformanceCounter - m_nBasePerformanceCounter) * m_fTimeScale);
//    }
//
//private:
//    int target_fps;                          // 목표 FPS
//    double m_fTimeScale;                     // 시간 스케일
//    __int64 m_nPerformanceFrequencyPerSec;   // 성능 카운터 주파수
//    __int64 m_nBasePerformanceCounter;       // 시작 카운터
//    __int64 m_nLastPerformanceCounter;       // 마지막 카운터
//    __int64 m_nCurrentPerformanceCounter;    // 현재 카운터
//    __int64 m_nStopPerformanceCounter;       // 정지 카운터
//    __int64 m_nPausedPerformanceCounter;     // 일시정지 카운터
//    bool m_bStopped;                         // 타이머 정지 여부
//};

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
	void Select_Mode_Decoding(std::pair<int, Key_Info>* key_info);
	void Game_Mode_Decoding(std::pair<int, Key_Info>* key_info);
	Game_Data* Encoding();

	void Update_Character_Select(float Elapsed_time);
	void Update_Game_World(float Elapsed_time);
	void Update_Collision(float Elapsed_time);
	void Broadcast_GameData_All(Game_Data* data);
	
	int Get_Key_Input_Buffer_size() { return keyQueue.size(); }
	void Set_FrameRate(int n) { timer.Start(n); }
	float Get_ElapsedTime() { return timer.GetElapsedTime(); }
	void Wait() { timer.Wait(); }
	Player* Get_Player(int Client);
	void Remove_Player(int Client);


};

