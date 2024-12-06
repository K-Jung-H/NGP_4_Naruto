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
		return elapsed.count(); // �� ������ ��� �ð� ��ȯ
	}

	// ��ǥ FPS�� ���� ���
	void Wait() {
		auto current_time = std::chrono::high_resolution_clock::now();
		std::chrono::duration<float> frame_duration = current_time - last_time;

		// ��ǥ FPS�� ���� ������ ���� ���
		float target_frame_time = 1.0f / target_fps;

		// ��ǥ �ð����� ���� ��� �ð� ���
		float sleep_time = target_frame_time - frame_duration.count();

		// ��� �ð� ����
		if (sleep_time > 0.0f) {
			std::this_thread::sleep_for(std::chrono::duration<float>(sleep_time));
		}

		// ���� �ð��� `last_time`���� ����
		last_time = std::chrono::high_resolution_clock::now();
	}

private:
	int target_fps; // ��ǥ FPS
	std::chrono::time_point<std::chrono::high_resolution_clock> last_time; // ������ ������ �ð�
};

//class Timer {
//public:
//    Timer()
//        : target_fps(100), // �⺻ ��ǥ FPS ����
//        m_bStopped(false),
//        m_fTimeScale(1.0),
//        m_nPerformanceFrequencyPerSec(0),
//        m_nBasePerformanceCounter(0),
//        m_nLastPerformanceCounter(0),
//        m_nCurrentPerformanceCounter(0),
//        m_nStopPerformanceCounter(0),
//        m_nPausedPerformanceCounter(0) {
//
//        // ���� ī���� ���ļ� Ȯ��
//        QueryPerformanceFrequency((LARGE_INTEGER*)&m_nPerformanceFrequencyPerSec);
//        QueryPerformanceCounter((LARGE_INTEGER*)&m_nLastPerformanceCounter);
//        m_fTimeScale = 1.0 / (double)m_nPerformanceFrequencyPerSec;
//
//        m_nBasePerformanceCounter = m_nLastPerformanceCounter;
//        m_nStopPerformanceCounter = 0;
//        m_nPausedPerformanceCounter = 0;
//    }
//
//    // Ÿ�̸� ����
//    void Start(int fps = -1) {
//        if (fps != -1) {
//            target_fps = fps;  // ��ǥ FPS ����
//        }
//
//        if (m_bStopped) {
//            // ������ Ÿ�̸Ӱ� ���� ���, ���� �ð��� �����Ͽ� �ٽ� ����
//            QueryPerformanceCounter((LARGE_INTEGER*)&m_nCurrentPerformanceCounter);
//            m_nPausedPerformanceCounter += m_nCurrentPerformanceCounter - m_nStopPerformanceCounter;
//            m_nLastPerformanceCounter = m_nCurrentPerformanceCounter;
//            m_nStopPerformanceCounter = 0;
//            m_bStopped = false;
//        }
//    }
//
//    // Ÿ�̸� ���߱�
//    void Stop() {
//        if (!m_bStopped) {
//            QueryPerformanceCounter((LARGE_INTEGER*)&m_nStopPerformanceCounter);
//            m_bStopped = true;
//        }
//    }
//
//    // ��� �ð� ��ȯ
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
//    // ��ǥ FPS�� ���� ���
//    void Wait() {
//        if (m_bStopped) {
//            return;
//        }
//
//        QueryPerformanceCounter((LARGE_INTEGER*)&m_nCurrentPerformanceCounter);
//        float elapsedTime = (float)((m_nCurrentPerformanceCounter - m_nLastPerformanceCounter) * m_fTimeScale);
//
//        // ��ǥ FPS�� �´� ��� �ð� ���
//        float targetFrameTime = 1.0f / target_fps;
//        float sleepTime = targetFrameTime - elapsedTime;
//
//        if (sleepTime > 0.0f) {
//            std::this_thread::sleep_for(std::chrono::duration<float>(sleepTime));
//        }
//
//        // ���� �ð��� `last_time`���� ����
//        m_nLastPerformanceCounter = m_nCurrentPerformanceCounter;
//    }
//
//    // ��ü �ð� ��ȯ
//    float GetTotalTime() {
//        if (m_bStopped) {
//            return (float)((m_nStopPerformanceCounter - m_nPausedPerformanceCounter - m_nBasePerformanceCounter) * m_fTimeScale);
//        }
//        return (float)((m_nCurrentPerformanceCounter - m_nPausedPerformanceCounter - m_nBasePerformanceCounter) * m_fTimeScale);
//    }
//
//private:
//    int target_fps;                          // ��ǥ FPS
//    double m_fTimeScale;                     // �ð� ������
//    __int64 m_nPerformanceFrequencyPerSec;   // ���� ī���� ���ļ�
//    __int64 m_nBasePerformanceCounter;       // ���� ī����
//    __int64 m_nLastPerformanceCounter;       // ������ ī����
//    __int64 m_nCurrentPerformanceCounter;    // ���� ī����
//    __int64 m_nStopPerformanceCounter;       // ���� ī����
//    __int64 m_nPausedPerformanceCounter;     // �Ͻ����� ī����
//    bool m_bStopped;                         // Ÿ�̸� ���� ����
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

