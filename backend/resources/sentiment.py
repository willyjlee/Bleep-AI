import requests

subscription_key = '64d30c5b3fe84d2481a87ac96f1029c9'
sentiment_api_url = 'https://westcentralus.api.cognitive.microsoft.com/text/analytics/v2.0/sentiment'
headers = { "Ocp-Apim-Subscription-Key": subscription_key }

def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

def sentiment_analysis(transcript):
    words = []

    for wordRes in transcript:
        words.append(wordRes["word"])
    wordArray = list(chunks(words, 7))

    sentences = []
    for words in wordArray:
        sentences.append(" ".join(words))
    print(sentences)

    documents = { 'documents': [] }

    for index in range(len(sentences)):
        documents['documents'].append({ 'id': str(index + 1), 'language': 'en', 'text': sentences[index] })

    response = requests.post(sentiment_api_url, headers=headers, json=documents)
    scores = response.json()['documents']

    ret = []
    for index in range(len(sentences)):
        ret.append({'sentence': sentences[index], 'score': scores[index]['score']})

    return ret
