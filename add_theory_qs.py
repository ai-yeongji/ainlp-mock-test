import re

html_path = '/Users/yeongji/Documents/LLM/ss/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

new_theory_questions = """
                ["Engineering", "상", "PyTorch에서 텐서 연산 시 자동으로 미분값을 계산하여 역전파(Backpropagation)를 돕는 핵심 엔진(기능)은 무엇인가?", "short-answer", null, "Autograd", "PyTorch의 Autograd는 연산 그래프를 동적으로 생성하여 미분값을 자동으로 계산해줍니다."],
                ["Engineering", "상", "대규모 딥러닝 모델 학습 시, 전체 데이터를 여러 개로 쪼개어 다수의 GPU에서 동일한 모델을 병렬로 학습시킨 후 기울기(Gradient)를 동기화하는 기법은?", "short-answer", null, "Data Parallelism (데이터 병렬처리)", "모델의 파라미터는 모든 GPU에 복제되며, 각 GPU는 서로 다른 미니배치를 처리합니다."],
                ["Engineering", "상", "모델 자체의 파라미터가 너무 커서 하나의 GPU 메모리에 다 들어가지 않을 때, 모델의 레이어나 텐서를 여러 GPU에 분할하여 올리는 학습 기법은?", "short-answer", null, "Model Parallelism (모델 병렬처리)", "Megatron-LM이나 DeepSpeed 같은 프레임워크에서 초거대 모델 학습을 위해 필수적으로 사용됩니다."],
                ["Modeling", "중", "딥러닝 모델 학습 도중 Train Loss는 계속 감소하지만 Validation Loss는 오히려 증가하기 시작했다면, 어떤 현상이 발생하고 있는 것인가?", "short-answer", null, "Overfitting (과적합)", "이때는 Early Stopping을 적용하여 학습을 중단하거나 Dropout 등의 정규화 기법을 도입해야 합니다."],
                ["Foundations", "상", "전처리 과정에서 스케일러(Scaler)를 전체 데이터에 먼저 Fit 한 후 Train/Test 셋을 분리하면, 테스트 데이터의 통계 정보가 훈련에 반영되어 실제 성능이 과대평가됩니다. 이러한 현상을 무엇이라고 하는가?", "short-answer", null, "Data Leakage (데이터 누수)", "데이터 누수는 모델 배포 후 실제 환경에서 성능이 크게 떨어지는 주된 원인 중 하나입니다."],
                ["Engineering", "하", "Git을 이용한 협업 시, 원격 저장소(Remote Repository)의 최신 변경 사항들을 로컬 저장소로 가져와서(fetch) 현재 로컬 브랜치에 자동으로 병합(merge)하는 명령어는?", "short-answer", null, "git pull", "충돌(Conflict)이 발생할 경우 수동으로 해결한 후 다시 커밋해야 합니다."],
                ["Modeling", "중", "트랜스포머(Transformer) 아키텍처에서 RNN과 달리 순차적 연산 없이 문장 내 모든 단어 쌍의 연관도를 병렬로 계산하여 문맥을 파악하는 핵심 메커니즘은?", "short-answer", null, "Self-Attention (셀프 어텐션)", "Self-Attention 덕분에 문장 길이가 길어져도 장거리 의존성(Long-range Dependency)을 잘 포착할 수 있습니다."],
                ["Modeling", "중", "깊은 신경망(DNN)에서 역전파를 수행할 때, Sigmoid 같은 활성화 함수를 통과하면서 기울기(Gradient)가 계속 곱해져 0에 수렴하게 되어 앞쪽 레이어가 학습되지 않는 현상은?", "short-answer", null, "Vanishing Gradient (기울기 소실)", "이를 해결하기 위해 ReLU 계열 활성함수 사용, Batch Normalization, ResNet의 잔차 연결(Residual Connection) 등이 도입되었습니다."],
                ["Foundations", "중", "분류 평가 지표 중, '모델이 양성(Positive)으로 예측한 샘플들 중에서 실제 양성인 샘플의 비율'을 나타내는 지표는? (스팸 메일 필터링 등 오진이 치명적일 때 중요)", "short-answer", null, "Precision (정밀도)", "정밀도(Precision) = TP / (TP + FP)"],
                ["Foundations", "중", "분류 평가 지표 중, '실제 양성(Positive)인 전체 데이터 중에서 모델이 올바르게 양성으로 찾아낸 샘플의 비율'을 나타내는 지표는? (암 진단 등 놓치는 것이 치명적일 때 중요)", "short-answer", null, "Recall (재현율)", "재현율(Recall) = TP / (TP + FN)"],
"""

# Insert questions into the concepts array
target_str = '["Foundations", "중", "다중공선성(Multicollinearity) 문제가 심할 때 가장 적절한 해결책은?"'
replacement = new_theory_questions + '                ' + target_str

if target_str in html:
    html = html.replace(target_str, replacement)
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print("Successfully added 10 theory questions.")
else:
    print("Could not find the target string in index.html")
