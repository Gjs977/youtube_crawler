from transformers import pipeline
from collections import Counter

def analyze_sentiment(comments):
    if not comments:
        return "댓글이 없어서 감정 분석을 진행할 수 없습니다."

    model = pipeline("text-classification", model="tabularisai/multilingual-sentiment-analysis")
    
    results = []
    for comment in comments:
        try:
            prediction = model(comment)
            if prediction:  
                results.append(prediction[0]['label'])
        except Exception as e:
            continue  

    if not results:
        return "분석 가능한 댓글이 없습니다."

    simplified = []
    for r in results:
        if r in ['Very Positive', 'Positive']:
            simplified.append('긍정적')
        elif r in ['Very Negative', 'Negative']:
            simplified.append('부정적')
        else:
            simplified.append('중립')

    counts = Counter(simplified)
    overall_emotion = counts.most_common(1)[0][0]

    formatted_result = (
        f"- 긍정적: {counts.get('긍정적',0)}\n"
        f"- 부정적: {counts.get('부정적',0)}\n"
        f"- 중립: {counts.get('중립',0)}\n"
        f"전체적인 분위기: {overall_emotion}입니다"
    )

    return formatted_result
