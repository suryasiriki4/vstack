import torch
import os
import json 
from transformers import T5Tokenizer, T5Config, T5ForConditionalGeneration

# luhns heuristic method

# we load our file and thus take each sentence indivisually in lowercase.
def load_common_words() :
    f = open('./words.txt', 'r')
    common_words = set()
    for word in f :
        common_words.add(word.strip('\n').lower())
    f.close()
    return common_words

#  finding the most common words to our document based on their frequency and removing the unwanted stopwords.
def top_words(answer) :
    record = {}
    common_words = load_common_words()
    for line in answer:
        words = line.split()
        for word in words :
            w = word.strip('.!?,()\n').lower()
            if w in record :
                record[w] += 1
            else :
                record[w] = 1
    
    for word in record.keys() :
        if word in common_words :
            record[word] = -1
    occur = [key for key in record.keys()]
    occur.sort(reverse = True, key = lambda x : record[x])
    return set(occur[: int(len(occur) / 10) ])

# calculating the score of each sentence
def calculate_score(sentence, metric) :
    words = sentence.split()
    imp_words, total_words, begin_unimp, end, begin = [0]*5
    for word in words:
        w = word.strip('.!?,();').lower()
        end += 1
        if w in metric :
            imp_words += 1
            begin = total_words
            end = 0
        total_words += 1
    unimportant = total_words - begin - end
    if(unimportant != 0) :
        return float(imp_words**2)/float(unimportant)
    return 0.0

# summarizing(extractive)
def summarize(answer) :
    text = ""
    for line in answer :
        text += line.replace('!','.').replace('?','.').replace('\n',' ')
    sentences = text.split(".")
    metric = top_words(answer)
    scores = {}
    for sentence in sentences :
        scores[sentence] = calculate_score(sentence, metric)
    top_sentences = list(sentences)                             # make a copy
    top_sentences.sort(key=lambda x: scores[x], reverse=True)   # sort by score
    top_sentences = top_sentences[:int(len(scores)*0.5)]        # get top 5%
    top_sentences.sort(key=lambda x: sentences.index(x))        # sort by occurrence       
    return '. '.join(top_sentences) 


# getting answer from file
f = open('./answers.txt', 'r')
splited_answer = f.readlines()
answer_string = "".join(splited_answer)


# final summarization(abstarctive using T5 trannsformers technique)
def get_summarised_answer(answers):

    answer = [answer_string]

    intermediate_answer = summarize(answers)

    # preparing a model and tokenizer from t5-small parameters
    model = T5ForConditionalGeneration.from_pretrained('t5-small')
    tokenizer = T5Tokenizer.from_pretrained('t5-small')
    device = torch.device('cpu')
    # summarizing
    preprocess_text = intermediate_answer.strip().replace("\n","")
    t5_prepared_Text = "summarize: "+preprocess_text

    tokenized_text = tokenizer.encode(t5_prepared_Text, return_tensors="pt").to(device)

    
    summary_ids = model.generate(tokenized_text,
                                        num_beams=4,
                                        no_repeat_ngram_size=2,
                                        min_length=30,
                                        max_length=100,
                                        early_stopping=True)
    # take most perfectly summarized one
    final_answer = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    print (final_answer)

    return final_answer

