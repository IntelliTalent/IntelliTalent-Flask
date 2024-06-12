import pickle
with open('model.pkl','rb') as f:
    crf = pickle.load(f)

# Extract features function
def word2features(sent, i):
    word = sent[i]
    features = {
        'bias': 1.0,
        'word.lower()': word.lower(),
        'word[-3:]': word[-3:],
        'word[-2:]': word[-2:],
        'word.isupper()': word.isupper(),
        'word.istitle()': word.istitle(),
        'word.isdigit()': word.isdigit(),
    }
    if i > 0:
        prev_word = sent[i-1][0]
        features.update({
            '-1:word.lower()': prev_word.lower(),
            '-1:word.istitle()': prev_word.istitle(),
            '-1:word.isupper()': prev_word.isupper(),
        })
    else:
        features['BOS'] = True

    if i < len(sent)-1:
        next_word = sent[i+1][0]
        features.update({
            '+1:word.lower()': next_word.lower(),
            '+1:word.istitle()': next_word.istitle(),
            '+1:word.isupper()': next_word.isupper(),
        })
    else:
        features['EOS'] = True
    return features


def sent2features(sent):
    return [word2features(sent, i) for i in range(len(sent))]

def getStructuredJobDetails(prompt):
    prompt = prompt.split()
    features = sent2features(prompt)
    output = crf.predict(X=[features])
    job = {}
    i = 0
    while i < len(prompt):
        word,tag = prompt[i],output[0][i]
        if tag == 'O':
            i+=1
            continue
        elif tag.startswith('B'):
            attr = tag[2:].lower()
            value = ''
            if not job.get(attr,False):
                job[attr] = []
            word,tag = prompt[i],output[0][i]
            value += word
            while not tag.startswith('E'):
                i += 1
                word,tag = prompt[i],output[0][i]
                value += ' '+word
            i+=1
            job[attr].append(value)
    return job