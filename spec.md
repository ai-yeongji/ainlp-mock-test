# 프로젝트명: AI-NLP 직무 역량 시험 대비 문제은행 웹 서비스

## 1. 프로젝트 개요
* **목표:** 다가오는 AI 자연어처리(NLP) 직무 역량 시험에 대비하기 위한 개인용 웹 기반 문제 풀이 및 학습 도구 개발.
* **대상 사용자:** AI/NLP 엔지니어 직무 면접 및 지필고사를 준비하는 수험생.
* **개발 방향:** 서버 구축 없이 프론트엔드 단에서 모든 기능이 동작하는 가벼운 SPA(Single Page Application). LocalStorage를 활용하여 데이터 저장.

## 2. 주요 기능 요구사항
### 2.1 메인 화면 (카테고리 및 난이도 선택)
* 사용자가 학습할 주제 카테고리와 난이도를 선택할 수 있는 대시보드.
* **카테고리 구성:**
  1. 자연어처리 기초 (NLP Basics)
  2. 모델 학습 (Model Training)
  3. 모델 추론 및 서빙 (Inference & Serving)
  4. 모델 경량화 (Optimization)
* **난이도 선택 기능:**
  * 전체 / 하(개념 확인) / 중(응용 및 원리) / 상(수식 계산 및 심층 아키텍처 분석) 중 택 1

### 2.2 문제 풀이 화면 (Quiz UI)
* 선택한 카테고리와 난이도에 해당하는 문제들만 필터링하여 제공.
* **문제 유형:** 객관식(4지 선다형) 및 단답형(계산 결과 입력 등).
* **기능:** * 이전/다음 문제 이동 버튼.
  * 진행률 표시 (Progress Bar, 예: 3/20).
  * '제출 및 채점' 버튼.

### 2.3 결과 및 오답 노트 화면
* 전체 문항 대비 정답 수 및 점수 표시.
* 사용자가 제출한 답과 실제 정답 비교.
* **핵심 기능:** 각 문제별로 **'상세 해설(Explanation)'**을 반드시 출력하여 오답의 이유를 바로 학습할 수 있도록 구성. 계산 문제의 경우 풀이 과정을 상세히 보여줄 것.
* 틀린 문제만 모아서 다시 풀 수 있는 '오답 노트' 버튼 제공.

## 3. 데이터 구조 (Mock Data Structure)
* 백엔드 API 대신 하드코딩된 JSON 배열을 활용합니다. 각 문제에 `difficulty` 속성을 추가하고, 수식이 들어간 고난도 계산 문제도 포함해 주세요.

```json
[
  {
    "id": 1,
    "category": "Inference & Serving",
    "difficulty": "중",
    "question": "LLM 추론 서버에서 메모리 병목을 줄이고 Throughput을 높이기 위해, 요청의 길이가 다름에도 불구하고 메모리 파편화를 방지하는 메모리 관리 기법은 무엇인가?",
    "type": "multiple-choice",
    "options": [
      "Continuous Batching",
      "PagedAttention",
      "Tensor Parallelism",
      "Speculative Decoding"
    ],
    "answer": "PagedAttention",
    "explanation": "PagedAttention은 OS의 가상 메모리 페이징 기법에서 착안하여 KV Cache를 고정된 크기의 블록으로 나누어 관리함으로써 메모리 파편화를 거의 0에 가깝게 줄이는 vLLM의 핵심 기술입니다."
  },
  {
    "id": 2,
    "category": "NLP Basics",
    "difficulty": "상",
    "question": "임베딩 차원(hidden size)이 768이고 어텐션 헤드(head) 수가 12개인 트랜스포머 모델에서, 단일 어텐션 헤드의 쿼리(Query) 가중치 행렬 W_Q의 파라미터 수는 얼마인가? (단, 바이어스는 무시한다)",
    "type": "multiple-choice",
    "options": [
      "589824",
      "49152",
      "9216",
      "768"
    ],
    "answer": "49152",
    "explanation": "단일 헤드의 차원 $d_k = \\frac{d_{\\text{model}}}{h} = \\frac{768}{12} = 64$ 입니다. 각 헤드의 쿼리 가중치 행렬 $W_Q$의 크기는 $d_{\\text{model}} \\times d_k$이므로, 파라미터 수는 $768 \\times 64 = 49152$개가 됩니다."
  }
]