import re

html_path = '/Users/yeongji/Documents/LLM/ss/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

new_questions = """
                ["Foundations", "중", "다중공선성(Multicollinearity) 문제가 심할 때 가장 적절한 해결책은?", "multiple-choice", ["표준화(Standardization) 수행", "PCA로 차원 축소", "학습률 감소", "데이터 크기 확대"], "PCA로 차원 축소", "높은 상관변수는 VIF↑ → PCA 또는 변수제거로 해결합니다."],
                ["Foundations", "상", "가설검정에서 p-value가 0.03이라는 의미로 올바른 것은?", "multiple-choice", ["귀무가설이 참일 확률이 3%이다.", "귀무가설 하에서 관측값 이상이 나올 확률이 3%이다.", "대립가설이 참일 확률이다.", "유의수준을 초과했으므로 기각한다."], "귀무가설 하에서 관측값 이상이 나올 확률이 3%이다.", "p-value는 '귀무가설(H₀)이 참이라고 가정할 때 현재의 관측 데이터나 그보다 극단적인 결과가 나올 확률'을 의미합니다."],
                ["Foundations", "중", "PCA에서 고유값(Eigenvalue)이 크다는 것은 어떤 의미인가?", "multiple-choice", ["해당 주성분이 데이터의 분산을 많이 설명한다.", "잡음이 많다.", "변수 개수가 많다.", "다중공선성이 크다."], "해당 주성분이 데이터의 분산을 많이 설명한다.", "주성분이 설명하는 정보량(분산)은 해당 주성분의 고유값에 비례합니다."],
                ["Foundations", "중", "공분산은 단위에 의존적이지만, 이를 단위에 독립적이도록 표준화하여 -1에서 1 사이의 값으로 변수 간의 선형 관계를 나타내는 지표는?", "short-answer", null, "상관계수 (Correlation)", "상관계수는 공분산을 각 변수의 표준편차로 나누어 정규화한 값입니다."],
                ["Foundations", "중", "결측치(Missing Value) 처리 시 모델 평가에서의 데이터 누출(Leakage)을 방지하는 올바른 방식은?", "multiple-choice", ["train/test 전체에 Imputer fit 후 transform", "train에만 fit 후 test는 transform", "test에만 fit", "랜덤 대치"], "train에만 fit 후 test는 transform", "모델 검증 시 test 데이터의 정보(평균, 분산 등)가 train 단계에 반영되면 안 됩니다."],
                ["Foundations", "하", "정규화(Normalization)와 표준화(Standardization)의 차이로 옳은 것은?", "multiple-choice", ["Normalization은 평균0 분산1로 맞춘다.", "Standardization은 [0,1] 범위로 조정한다.", "Normalization은 [0,1] 스케일링, Standardization은 평균0·분산1", "둘 다 동일한 의미"], "Normalization은 [0,1] 스케일링, Standardization은 평균0·분산1", "일반적으로 Normalization(MinMax)은 0~1 사이로, Standardization은 표준정규분포로 변환합니다."],
                ["Foundations", "중", "Oversampling과 SMOTE 기법의 차이로 옳은 것은?", "multiple-choice", ["Oversampling은 단순 복제, SMOTE는 인접 샘플을 기반으로 합성 데이터 생성", "SMOTE는 단순 복제, Oversampling은 합성 데이터 생성", "둘 다 단순 복제", "둘 다 데이터를 제거하는 방식"], "Oversampling은 단순 복제, SMOTE는 인접 샘플을 기반으로 합성 데이터 생성", "SMOTE는 K-NN을 이용하여 소수 클래스의 새로운 샘플을 보간(Interpolation)하여 생성합니다."],
                ["Foundations", "상", "OLS 회귀에서 다중공선성 문제가 심하면 어떤 현상이 나타나는가?", "multiple-choice", ["결정계수(R²)가 감소한다.", "가중치 분산이 커지고 불안정한 추정치가 된다.", "Loss가 0으로 수렴한다.", "Gradient 폭발"], "가중치 분산이 커지고 불안정한 추정치가 된다.", "다중공선성이 높으면 회귀계수의 분산이 크게 팽창(VIF)하여 모델 해석이 불안정해집니다."],
                ["Foundations", "상", "Bias-Variance Trade-off에서 정규화(Regularization) 강도를 높이면 어떤 효과가 나타나는가?", "multiple-choice", ["편향↑ 분산↓", "편향↓ 분산↑", "둘 다 감소", "둘 다 증가"], "편향↑ 분산↓", "규제가 강해지면 모델이 단순해져 분산(Variance)은 줄어들지만, 데이터를 충분히 모사하지 못해 편향(Bias)이 커집니다."],
                ["Foundations", "상", "데이터 분포의 첨도(Kurtosis)가 크다는 의미는?", "multiple-choice", ["꼬리가 두껍다.", "꼬리가 얇다.", "대칭성이 높다.", "분산이 작다."], "꼬리가 두껍다.", "첨도가 크면 분포의 중앙이 뾰족하고 꼬리가 두꺼워(Heavy-tailed) 이상치가 발생할 확률이 높습니다."],
                ["Modeling", "중", "분류 문제에서 손실함수로 MSE보다 Cross-Entropy가 더 적합한 이유는?", "multiple-choice", ["로그우도 형태로 확률적 출력의 경사 해상도가 높기 때문", "오차 제곱합을 최소화하기 때문", "이상치에 강건하기 때문", "회귀 문제 전용이기 때문"], "로그우도 형태로 확률적 출력의 경사 해상도가 높기 때문", "Cross-Entropy는 확률 분포 간의 차이를 측정하며, 오차가 클 때 더 큰 Gradient를 발생시켜 학습이 빠릅니다."],
                ["Modeling", "중", "ReLU 활성함수의 대표적인 단점은 무엇인가?", "multiple-choice", ["계산량이 많다.", "음수 입력 구간에서 Gradient가 0이 되어 Dead Neuron이 생긴다.", "Saturation 문제가 없다.", "출력이 확률로 제한된다."], "음수 입력 구간에서 Gradient가 0이 되어 Dead Neuron이 생긴다.", "입력값이 음수일 때 기울기가 0이 되어 가중치가 더 이상 업데이트되지 않는 Dying ReLU 현상이 발생할 수 있습니다."],
                ["Modeling", "중", "1차 모멘텀(Momentum)과 2차 모멘트(RMSProp)를 모두 이용하여 각 파라미터마다 적응적 학습률을 적용하는 최적화 알고리즘은?", "short-answer", null, "Adam", "Adam Optimizer는 SGD보다 빠르게 수렴하며 딥러닝에서 가장 널리 쓰이는 최적화 기법 중 하나입니다."],
                ["Modeling", "하", "학습 중 뉴런의 일부를 무작위로 비활성화하여 모델의 과적합(Overfitting)을 방지하는 기법은?", "short-answer", null, "Dropout (드롭아웃)", "Dropout은 신경망의 동조화(Co-adaptation)를 막아 일반화 성능을 높입니다."],
                ["Modeling", "중", "Batch Normalization(배치 정규화)의 주요 효과는?", "multiple-choice", ["입력값의 분산을 줄여 학습을 안정화한다.", "학습률을 자동 조정한다.", "과적합 방지 전용이다.", "출력층 가중치를 감소시킨다."], "입력값의 분산을 줄여 학습을 안정화한다.", "각 레이어의 입력을 정규화하여 내부 공변량 변화(Internal Covariate Shift)를 완화합니다."],
                ["Modeling", "하", "학습률(Learning Rate)이 너무 크게 설정되었을 때 나타날 수 있는 현상은?", "multiple-choice", ["최적점 근처에서 진동하거나 발산", "과적합", "학습 속도 저하", "손실 0 수렴"], "최적점 근처에서 진동하거나 발산", "Loss가 수렴하지 못하고 튀는(Bounce) 현상이나 발산(Divergence)이 발생합니다."],
                ["Modeling", "중", "검증 데이터(Validation)에 대한 오차가 더 이상 개선되지 않을 때 학습을 조기 중단하여 과적합을 방지하는 기법은?", "short-answer", null, "Early Stopping (얼리 스토핑)", "최적의 일반화 성능을 내는 지점에서 학습을 멈추게 합니다."],
                ["Modeling", "상", "L1 Regularization(L1 정규화)은 모델에 어떤 효과를 낳는가?", "multiple-choice", ["가중치 폭발 방지", "희소성(Sparsity) 유도", "학습률 감소", "Batch 효과 개선"], "희소성(Sparsity) 유도", "L1 정규화는 중요하지 않은 특징의 가중치를 0으로 만들어 모델을 가볍게(Sparse) 만듭니다."],
                ["Modeling", "중", "딥러닝 분류 문제에서 Optimizer와 손실함수의 조합 중 가장 일반적이고 안정적인 것은?", "multiple-choice", ["MSE + SGD", "CrossEntropy + Adam", "MAE + RMSProp", "CE + SGD"], "CrossEntropy + Adam", "분류 모델에서는 확률 예측의 차이를 잘 반영하는 CE와 적응형 학습률인 Adam의 조합이 표준입니다."],
                ["Modeling", "중", "Gradient Vanishing(기울기 소실) 문제가 심할 때 이를 완화하기 위해 사용하는 대표적인 활성함수는?", "multiple-choice", ["Sigmoid", "ReLU", "Softmax", "Tanh"], "ReLU", "ReLU는 양수 입력에 대해 기울기가 1로 유지되어 깊은 망에서도 기울기 소실이 적습니다."],
                ["Modeling", "중", "정규화(Regularization) 기법과 Dropout의 공통적인 최종 목표는 모델의 어떤 성능을 향상시키는 것인가?", "multiple-choice", ["일반화(Generalization) 성능 향상", "학습 속도 향상", "메모리 사용량 감소", "파라미터 수 증가"], "일반화(Generalization) 성능 향상", "모델 복잡도를 줄이거나 노이즈를 주어 테스트 데이터에서도 잘 동작하도록 만드는 것이 목표입니다."],
                ["Modeling", "중", "학습 과정 중 Epoch 진행에 따라 학습률을 점진적으로 조정해 수렴을 돕는 기법 또는 모듈은?", "short-answer", null, "Learning Rate Scheduler (학습률 스케줄러)", "학습 후반부로 갈수록 학습률을 줄여 최적점(Global Minimum)에 안정적으로 안착하게 돕습니다."],
                ["Modeling", "상", "Batch 크기를 너무 크게 설정하면 생길 수 있는 주된 문제는?", "multiple-choice", ["학습 불안정", "일반화 성능 저하", "GPU 메모리 감소", "수렴속도 향상"], "일반화 성능 저하", "Batch가 너무 크면 모델이 Sharp Minima에 빠지기 쉬워져 일반화(Generalization) 성능이 떨어질 수 있습니다."],
                ["Engineering", "상", "PyTorch에서 추론(Inference)을 수행할 때, Dropout이나 BatchNorm 등을 평가 모드로 전환하기 위해 모델 객체에 호출하는 메서드는?", "short-answer", null, "eval() (또는 model.eval())", "eval()을 호출하면 훈련용 레이어들이 추론용으로 동작 방식이 바뀝니다."],
                ["Engineering", "중", "Scikit-learn Pipeline의 주된 목적은?", "multiple-choice", ["코드 단축", "데이터 전처리와 모델 단계를 묶어 재현성을 보장", "속도 향상", "시각화"], "데이터 전처리와 모델 단계를 묶어 재현성을 보장", "전처리와 학습을 하나의 파이프라인으로 묶어 Data Leakage를 막고 배포를 용이하게 합니다."],
                ["Engineering", "상", "Knowledge Distillation에서 Teacher-Student 학습 관계로 옳은 설명은?", "multiple-choice", ["Teacher는 간단한 모델이다.", "Student가 Teacher의 soft label을 학습한다.", "Student가 Teacher를 fine-tuning한다.", "Teacher는 Student보다 작은 모델이다."], "Student가 Teacher의 soft label을 학습한다.", "큰 Teacher 모델이 출력하는 확률 분포(Soft Label)를 작은 Student 모델이 모사하도록 학습합니다."],
                ["Engineering", "중", "Transformer 구조에서 Positional Encoding이 필수적인 이유는?", "multiple-choice", ["Attention 구조는 순서를 인식하지 못하므로 위치 정보를 더하기 위해", "파라미터 수를 줄이기 위해", "연산 속도를 높이기 위해", "과적합을 방지하기 위해"], "Attention 구조는 순서를 인식하지 못하므로 위치 정보를 더하기 위해", "Self-Attention은 순서에 무관한 연산이므로, 토큰의 상대적/절대적 위치 정보를 주입해야 합니다."],
                ["Engineering", "중", "앙상블 기법 중 Bagging과 Boosting의 차이로 올바른 것은?", "multiple-choice", ["Bagging은 병렬 학습, Boosting은 순차적 학습", "둘 다 병렬", "둘 다 순차", "Bagging은 약한 학습기 가중"], "Bagging은 병렬 학습, Boosting은 순차적 학습", "Bagging(예: Random Forest)은 독립적인 병렬 모델의 평균을, Boosting(예: XGBoost)은 이전 모델의 오차를 순차적으로 보완합니다."],
                ["Engineering", "중", "학습 데이터에 의도적으로 Noise(잡음)를 추가하는 Regularization 기법의 주된 효과는?", "multiple-choice", ["일반화 성능 향상", "학습속도 저하", "Overfitting 증가", "Loss 불안정"], "일반화 성능 향상", "데이터의 다양성을 높여 모델이 노이즈에 강건해지고 일반화 성능이 향상됩니다."],
                ["Engineering", "하", "GPU에서 딥러닝 모델 학습 중 OOM(Out of Memory) 오류가 발생했을 때 가장 먼저 시도해야 할 조치는?", "multiple-choice", ["Batch size를 줄인다.", "Epoch를 늘린다.", "Optimizer를 변경한다.", "Dropout을 제거한다."], "Batch size를 줄인다.", "OOM은 GPU 메모리 초과로 발생하며, 가장 직접적인 해결책은 한 번에 연산하는 Batch 크기를 줄이는 것입니다."]
"""

# Insert questions into the concepts array
target_str = "            const concepts = ["
replacement = target_str + new_questions + ","

if target_str in html:
    html = html.replace(target_str, replacement)
    
    # Also add new categories to the dropdown
    select_target = '<option value="Optimization">Optimization</option>'
    select_replacement = select_target + """
                            <option value="Foundations">Foundations (통계/데이터)</option>
                            <option value="Modeling">Modeling (딥러닝/최적화)</option>
                            <option value="Engineering">Engineering (시스템/인프라)</option>"""
    if select_target in html and "Foundations" not in html:
        html = html.replace(select_target, select_replacement)
        
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print("Successfully added 30 PDF questions and new categories.")
else:
    print("Could not find the concepts array in index.html")
