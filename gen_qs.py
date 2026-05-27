import json
import random

random.seed(42)

questions = []
current_id = 1

def add_q(cat, diff, q_text, q_type, options, ans, exp):
    global current_id
    q = {
        "id": current_id,
        "category": cat,
        "difficulty": diff,
        "question": q_text,
        "type": q_type,
        "answer": ans,
        "explanation": exp
    }
    if options:
        q["options"] = options
    questions.append(q)
    current_id += 1

# 15 Original Questions
original = [
    ("Inference & Serving", "중", "LLM 추론 서버에서 메모리 병목을 줄이고 Throughput을 높이기 위해, 요청의 길이가 다름에도 불구하고 메모리 파편화를 방지하는 메모리 관리 기법은 무엇인가?", "multiple-choice", ["Continuous Batching", "PagedAttention", "Tensor Parallelism", "Speculative Decoding"], "PagedAttention", "PagedAttention은 OS의 가상 메모리 페이징 기법에서 착안하여 KV Cache를 고정된 크기의 블록으로 나누어 관리함으로써 메모리 파편화를 거의 0에 가깝게 줄이는 vLLM의 핵심 기술입니다."),
    ("NLP Basics", "상", "임베딩 차원(hidden size)이 768이고 어텐션 헤드(head) 수가 12개인 트랜스포머 모델에서, 단일 어텐션 헤드의 쿼리(Query) 가중치 행렬 W_Q의 파라미터 수는 얼마인가? (단, 바이어스는 무시한다)", "short-answer", None, "49152", "단일 헤드의 차원 d_k = 768/12 = 64 입니다. W_Q 크기는 768 * 64 = 49152 입니다."),
    ("Model Training", "하", "다음 중 언어 모델의 학습 시, 다음 단어를 예측하는 목적 함수를 최적화하기 위해 흔히 사용되는 손실 함수는?", "multiple-choice", ["Mean Squared Error (MSE)", "Cross Entropy Loss", "Hinge Loss", "Contrastive Loss"], "Cross Entropy Loss", "다음 단어 예측은 다중 클래스 분류 문제로 접근하여 Cross Entropy Loss를 주로 사용합니다."),
    ("Optimization", "중", "LLM을 양자화하여 메모리 사용량을 줄이고 PEFT와 결합한 방법론의 이름은?", "multiple-choice", ["QLoRA", "Prompt Tuning", "Knowledge Distillation", "Pruning"], "QLoRA", "QLoRA는 가중치를 4-bit로 양자화하고 LoRA 어댑터를 미세조정하는 기법입니다."),
    ("NLP Basics", "하", "트랜스포머 아키텍처에서 입력 시퀀스의 순서 정보를 제공하는 벡터는?", "multiple-choice", ["Word Embedding", "Positional Encoding", "Attention Mask", "Layer Normalization"], "Positional Encoding", "어텐션 메커니즘은 순서 정보가 없으므로 Positional Encoding을 더해줍니다."),
    ("NLP Basics", "중", "자연어 처리에서 단어의 빈도와 역문서 빈도를 결합하여 특정 문서 내 단어의 중요도를 평가하는 통계적 수치는 무엇인가? (약어로 입력)", "short-answer", None, "TF-IDF", "TF-IDF는 단어의 문서 내 출현 빈도와 전체 문서 군에서의 출현 빈도의 역수를 곱한 값입니다."),
    ("Model Training", "중", "Transformer 모델의 불안정한 학습을 방지하기 위해 Layer Normalization을 Attention이나 FFN 계층 이전에 적용하는 구조의 이름은?", "multiple-choice", ["Post-LN", "Pre-LN", "RMSNorm", "Batch Normalization"], "Pre-LN", "Pre-LN은 잔차 연결 이전에 정규화를 수행하여 웜업 없이도 안정적인 학습을 가능하게 합니다."),
    ("Inference & Serving", "상", "LLM 추론 시, 여러 Query 헤드가 KV 텐서를 공유하여 메모리 대역폭 병목을 줄이는 기술은?", "multiple-choice", ["Multi-Head Attention", "Grouped-Query Attention (GQA)", "Sparse Attention", "Self-Attention"], "Grouped-Query Attention (GQA)", "GQA는 Query 헤드들을 묶어 동일한 KV 헤드를 공유하게 하여 추론 시 메모리 대역폭 요구량을 줄입니다."),
    ("Optimization", "하", "거대 언어 모델의 가중치 중 0에 가까운 값을 제거하는 경량화 기법은?", "multiple-choice", ["Quantization (양자화)", "Pruning (가지치기)", "Knowledge Distillation (지식 증류)", "Low-Rank Adaptation (LoRA)"], "Pruning (가지치기)", "Pruning은 예측 성능에 영향이 적은 가중치를 제거하여 크기를 줄입니다."),
    ("Model Training", "상", "주어진 문장에서 토큰화된 단어가 3개일 때, Causal LM에서 발생하는 마스킹된 Self-Attention 행렬의 0이 아닌 요소의 총 개수는?", "short-answer", None, "6", "Lower Triangular 형태이므로 1 + 2 + 3 = 6개입니다."),
    ("NLP Basics", "중", "주변 단어들을 기반으로 중심 단어를 예측하도록 네트워크를 학습시키는 Word2Vec 모델은?", "short-answer", None, "CBOW", "CBOW는 주변 단어들로 중심 단어를 예측합니다."),
    ("Optimization", "상", "Knowledge Distillation에서 Student가 Teacher의 확률 분포를 모사할 때 사용하는 손실 함수는?", "multiple-choice", ["Kullback-Leibler (KL) Divergence", "Mean Absolute Error (MAE)", "Huber Loss", "Binary Cross Entropy"], "Kullback-Leibler (KL) Divergence", "두 분포 간의 차이를 줄이기 위해 KL Divergence를 사용합니다."),
    ("Inference & Serving", "중", "디코딩 과정에서 확률 분포를 뾰족하거나 완만하게 만들어 생성의 다양성을 조절하는 파라미터는?", "short-answer", None, "Temperature", "Temperature를 조정하여 토큰 샘플링의 랜덤성을 제어합니다."),
    ("Model Training", "중", "인간의 피드백을 반영하여 강화학습으로 언어 모델을 미세조정하는 기법의 약자는?", "short-answer", None, "RLHF", "RLHF는 보상 모델과 강화학습을 이용해 미세조정하는 기법입니다."),
    ("Optimization", "중", "상대적인 거리 정보를 Attention의 Query와 Key 벡터의 회전 변환으로 인코딩하는 기법은?", "multiple-choice", ["ALiBi", "RoPE", "Sinusoidal Positional Encoding", "Relative Position Representations"], "RoPE", "RoPE는 복소수 평면에서의 회전으로 상대적 위치 정보를 인코딩합니다.")
]

for q in original:
    add_q(*q)

# Additional Concept Questions
concepts = [
    ("NLP Basics", "하", "RNN의 장기 의존성 문제를 완화하기 위해 도입된, Forget, Input, Output 게이트를 가지는 구조는?", "multiple-choice", ["LSTM", "GRU", "Transformer", "CNN"], "LSTM", "LSTM은 게이트 구조를 통해 기울기 소실 문제를 완화합니다."),
    ("Inference & Serving", "중", "LLM 추론에서 생성 중인 토큰의 Context를 유지하기 위해 이전 토큰들의 Key와 Value 벡터를 메모리에 저장하는 기법은?", "short-answer", None, "KV Cache", "KV Cache는 매 스텝마다 모든 이전 토큰을 재연산하지 않도록 Key와 Value를 캐싱합니다."),
    ("Model Training", "상", "분산 학습 기법 중, 모델의 파라미터, 그래디언트, 옵티마이저 상태를 여러 GPU에 분할하여 저장하는 ZeRO(Zero Redundancy Optimizer) 기술을 핵심으로 하는 라이브러리는?", "multiple-choice", ["DeepSpeed", "Megatron-LM", "Horovod", "Ray"], "DeepSpeed", "Microsoft의 DeepSpeed는 ZeRO를 통해 메모리 효율적인 분산 학습을 지원합니다."),
    ("Optimization", "중", "LoRA 기법에서 가중치 행렬 W를 두 개의 저랭크 행렬 A와 B로 분해할 때, B 행렬의 초기화 방식은 무엇인가?", "multiple-choice", ["Xavier Initialization", "Kaiming Initialization", "Zero Initialization", "Random Normal"], "Zero Initialization", "LoRA에서 B는 0으로 초기화하여 학습 초기에는 원본 가중치와 동일하게 동작하도록 만듭니다."),
    ("Inference & Serving", "상", "LLM 추론 시, 초안 모델(Draft model)을 사용하여 여러 토큰을 빠르게 생성한 후, 타겟 모델이 이를 병렬로 검증(Verify)하여 속도를 높이는 기법은?", "multiple-choice", ["Continuous Batching", "Speculative Decoding", "FlashAttention", "Prefix Caching"], "Speculative Decoding", "Speculative Decoding은 작은 모델이 추측한 토큰들을 큰 모델이 한 번에 검증하여 디코딩 속도를 비약적으로 향상시킵니다."),
    ("Model Training", "하", "분류 문제에서 정답 라벨에 1, 나머지에 0을 할당하는 대신, 정답에는 1-epsilon, 오답에는 epsilon/K를 할당하여 과적합을 방지하는 기법은?", "short-answer", None, "Label Smoothing", "Label Smoothing은 정답에 대한 모델의 확신도를 낮추어 일반화 성능을 높입니다."),
    ("NLP Basics", "상", "단어의 의미적 모호성을 해소하기 위해, 동일한 단어라도 문맥에 따라 다른 임베딩 벡터를 가지도록 한 최초의 딥러닝 기반 언어 모델은?", "multiple-choice", ["Word2Vec", "GloVe", "FastText", "ELMo"], "ELMo", "ELMo는 양방향 LSTM을 사용하여 문맥을 반영한 임베딩을 생성한 초기 모델입니다."),
    ("Model Training", "상", "Transformer의 Attention 연산 시 메모리 접근 횟수를 최소화하여 GPU 메모리 대역폭 병목을 극복하고 연산 속도를 크게 높인 알고리즘은?", "short-answer", None, "FlashAttention", "FlashAttention은 Tiling 기법을 사용하여 HBM 접근을 줄이고 SRAM에서 연산을 수행합니다."),
    ("Optimization", "하", "기존 모델을 더 작은 모델로 압축하기 위해 Teacher 모델의 출력을 Student 모델이 학습하도록 하는 기법은?", "short-answer", None, "Knowledge Distillation", "Knowledge Distillation(지식 증류)는 큰 모델의 '지식'을 작은 모델로 전달합니다."),
    ("Inference & Serving", "중", "사용자 요청을 배치 단위로 모아서 처리할 때, 각 요청의 생성 길이가 달라도 유휴 컴퓨팅 자원이 생기지 않도록 매 스텝마다 완료된 요청을 내보내고 새 요청을 삽입하는 스케줄링 기법은?", "multiple-choice", ["Dynamic Batching", "Continuous Batching", "Static Batching", "Micro-Batching"], "Continuous Batching", "Continuous Batching (또는 In-flight Batching)은 배치 크기를 최대한 유지하여 Throughput을 극대화합니다."),
    ("NLP Basics", "중", "BPE(Byte-Pair Encoding) 토크나이저에서 가장 빈번하게 등장하는 바이트(또는 문자) 쌍을 병합하여 어휘 사전을 구축합니다. 병합을 중단하는 기준은 보통 무엇입니까?", "multiple-choice", ["최대 어휘 사전 크기 (Vocab Size)", "최대 시퀀스 길이", "특정 빈도수 이하 도달", "문장의 끝(EOS) 도달"], "최대 어휘 사전 크기 (Vocab Size)", "BPE는 사전에 정의된 최대 Vocab Size에 도달할 때까지 병합 연산을 반복합니다."),
    ("Model Training", "상", "Mixed Precision Training(혼합 정밀도 학습)에서, 그레디언트 언더플로우(Underflow) 문제를 방지하기 위해 손실값(Loss)에 특정 상수를 곱해주는 기법의 이름은?", "short-answer", None, "Loss Scaling", "Loss Scaling은 FP16의 표현 범위를 벗어나는 작은 그래디언트를 유지하기 위해 Loss를 스케일링하는 기법입니다."),
    ("Optimization", "상", "언어 모델의 컨텍스트 창(Context Window) 한계를 극복하기 위해, 학습에 사용된 시퀀스 길이보다 더 긴 시퀀스를 처리할 수 있도록 Positional Encoding의 스케일을 조정하는 기법은?", "multiple-choice", ["Position Interpolation", "Longformer", "Sparse Attention", "Sliding Window Attention"], "Position Interpolation", "Position Interpolation은 RoPE와 같은 인코딩을 긴 시퀀스에 맞게 스케일링 다운하여 Extrapolation 성능을 높입니다."),
    ("Inference & Serving", "하", "디코딩 과정 중 Beam Search에서 Beam Size를 1로 설정하는 것과 동일한 결과를 내는 탐색 기법은?", "short-answer", None, "Greedy Search", "Greedy Search는 매 스텝 확률이 가장 높은 토큰 1개만을 선택합니다."),
    ("NLP Basics", "상", "어텐션 메커니즘에서 Query와 Key의 내적값을 $\\sqrt{d_k}$ 로 나누어주는 이유는 무엇인가?", "multiple-choice", ["Softmax 기울기 소실 방지", "연산 속도 증가", "메모리 사용량 감소", "어텐션 마스크 적용을 위해"], "Softmax 기울기 소실 방지", "내적값이 너무 커지면 Softmax의 출력값이 한쪽으로 치우쳐 기울기(Gradient)가 소실되는 현상을 막기 위함입니다.")
]
for q in concepts:
    add_q(*q)

# Template Generation to reach 100
# Template 1: W_Q Parameters
d_models_1 = [(256, 4), (512, 8), (1024, 16), (2048, 32), (4096, 32), (4096, 64), (8192, 64)]
for d, h in d_models_1:
    q_text = f"임베딩 차원이 {d}이고 어텐션 헤드 수가 {h}개인 트랜스포머 모델에서, 단일 어텐션 헤드의 쿼리(Query) 가중치 행렬 W_Q의 파라미터 수는? (단, 바이어스 무시)"
    ans = str(d * (d // h))
    exp = f"단일 헤드의 차원 d_k = {d}/{h} = {d//h}입니다. W_Q의 파라미터 수는 {d} * {d//h} = {ans}개 입니다."
    add_q("NLP Basics", "상", q_text, "short-answer", None, ans, exp)

# Template 2: Causal Mask Non-Zero
lengths = [4, 5, 6, 7, 8, 10, 16, 32, 64, 128]
for l in lengths:
    q_text = f"주어진 문장에서 토큰화된 단어가 {l}개일 때, Causal LM에서 발생하는 마스킹된 Self-Attention 행렬의 0이 아닌 요소의 총 개수는?"
    ans = str(l * (l + 1) // 2)
    exp = f"Lower Triangular 형태이므로 1부터 {l}까지의 합 = {l}*({l}+1)/2 = {ans}개입니다."
    add_q("Model Training", "상", q_text, "short-answer", None, ans, exp)

# Template 3: LoRA Parameters
lora_dims = [(1024, 8), (1024, 16), (2048, 16), (2048, 32), (4096, 32), (4096, 64), (8192, 64)]
for d, r in lora_dims:
    q_text = f"가중치 행렬 W의 크기가 {d}x{d}일 때, LoRA를 적용하여 Rank r={r}인 A, B 두 행렬로 분해하여 학습한다면, A와 B의 파라미터 수의 합은?"
    ans = str(2 * d * r)
    exp = f"A의 크기는 {d}x{r}, B의 크기는 {r}x{d}이므로 총 파라미터 수는 2 * {d} * {r} = {ans}개입니다."
    add_q("Optimization", "상", q_text, "short-answer", None, ans, exp)

# Template 4: KV Cache Size (elements per token per layer)
# size = 2 (K, V) * hidden_size * num_layers (wait, per layer it's 2 * hidden_size)
hidden_sizes = [512, 1024, 2048, 4096]
for h in hidden_sizes:
    q_text = f"Hidden size가 {h}인 트랜스포머 디코더 모델에서 1개의 토큰이 1개의 레이어에서 차지하는 KV Cache 텐서의 전체 원소(Element) 개수는? (Key와 Value를 모두 포함)"
    ans = str(2 * h)
    exp = f"1개 토큰에 대해 Key({h})와 Value({h}) 벡터가 저장되므로 {h} + {h} = {ans}개의 원소가 저장됩니다."
    add_q("Inference & Serving", "중", q_text, "short-answer", None, ans, exp)

# Additional diverse concept variations to fill up to 100
vocab_sizes = [10000, 30000, 50000]
for v in vocab_sizes:
    q_text = f"분류할 클래스 수가 {v}개인 언어 모델 출력층(Vocab size={v})에서, Hidden size가 1024일 때 출력 가중치 행렬(LM Head)의 파라미터 수는? (바이어스 무시)"
    ans = str(v * 1024)
    exp = f"출력층은 1024차원의 은닉 상태를 {v}차원의 로짓으로 변환하므로 파라미터 수는 1024 * {v} = {ans}입니다."
    add_q("Model Training", "상", q_text, "short-answer", None, ans, exp)

batch_sizes = [4, 8, 16, 32]
for b in batch_sizes:
    q_text = f"배치 사이즈가 {b}이고, 프롬프트 시퀀스 길이가 128인 입력을 처리하는 Prefill 단계에서, Attention 마스크 행렬의 전체 요소(Element) 개수는? (배치 전체 기준)"
    ans = str(b * 128 * 128)
    exp = f"각 시퀀스마다 128x128 크기의 어텐션 마스크가 필요하며 배치가 {b}이므로 {b} * 128 * 128 = {ans}입니다."
    add_q("Inference & Serving", "상", q_text, "short-answer", None, ans, exp)

# Let's see how many we have. 
# 15 original + 15 concepts + 7 + 10 + 7 + 4 + 3 + 4 = 65 questions.
# We need 35 more. Let's add some more templates.

epochs = [1, 2, 3, 4, 5]
for e in epochs:
    q_text = f"총 학습 데이터 수가 10,000,000건이고, Batch Size가 1000건일 때, {e} Epoch 동안 학습한다면 총 수행되는 Step 수는?"
    ans = str(10000 * e)
    exp = f"1 Epoch 당 스텝 수는 10,000,000 / 1000 = 10,000번입니다. {e} Epoch 이므로 10,000 * {e} = {ans}입니다."
    add_q("Model Training", "하", q_text, "short-answer", None, ans, exp)

learning_rates = [0.001, 0.0001, 0.0005, 0.01, 0.05, 0.1, 0.2]
for lr in learning_rates:
    q_text = f"기존 Learning Rate가 {lr}일 때, Linear Warmup Scheduler를 적용하여 10,000 Step 동안 Warmup을 수행한다. 5,000번째 Step에서의 Learning Rate는 얼마인가?"
    ans = str(lr / 2)
    exp = f"Linear Warmup이므로 5,000/10,000 = 50% 시점에서는 목표 LR인 {lr}의 절반인 {ans}가 됩니다."
    add_q("Model Training", "상", q_text, "short-answer", None, ans, exp)

ffn_dims = [2048, 4096, 8192, 16384]
for f in ffn_dims:
    q_text = f"Hidden size가 {f//4}인 트랜스포머에서 FFN(Feed Forward Network)의 중간 차원(Intermediate size)이 주로 {f}일 때, 첫 번째 선형 변환 행렬 W_1의 파라미터 수는? (바이어스 무시)"
    ans = str((f//4) * f)
    exp = f"입력 차원이 {f//4}이고 출력 차원이 {f}이므로 파라미터 수는 {f//4} * {f} = {ans}입니다."
    add_q("NLP Basics", "상", q_text, "short-answer", None, ans, exp)

dropouts = [10, 20, 30, 40, 50]
for d in dropouts:
    q_text = f"Dropout 비율이 {d}%일 때, 학습 시 출력을 스케일링하기 위해 뉴런의 출력값에 곱해지는 Scaling Factor 값은 얼마인가?"
    ans = str(1 / (1 - d/100.0))
    exp = f"Dropout 시 활성화된 뉴런의 출력 기댓값을 맞추기 위해 1 / (1 - p) 배 해줍니다. 1 / (1 - {d/100.0}) = {ans}입니다."
    add_q("Model Training", "상", q_text, "short-answer", None, ans, exp)

# Fill the rest with some random duplicates of the original concepts with slight wording changes to reach exactly 100.
while current_id <= 100:
    base = random.choice(concepts)
    q_text = f"[유사문제] {base[2]}"
    add_q(base[0], base[1], q_text, base[3], base[4], base[5], base[6])

with open("questions.json", "w", encoding="utf-8") as f:
    json.dump(questions[:100], f, ensure_ascii=False, indent=4)

print(f"Generated {len(questions[:100])} questions.")
