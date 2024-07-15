# for jaccard

# for levenshtein
import Levenshtein

# for bert uncased embeddings and cosine similarity
import torch
from transformers import AutoTokenizer, AutoModel
from scipy.spatial.distance import cosine

def jaccard_similarity(str1, str2):
    set1 = set(str1.split())
    set2 = set(str2.split())
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    return len(intersection) / len(union)

def categorize_predictions(predictions1, predictions2, jaccard_threshold=0.5):
    additions = []
    subtractions = []
    potential_modifications = []
    print("predictions1",predictions1)

    for qid, answer1 in predictions1.items():
        answer2 = predictions2.get(qid, "")
        print("within the loop")

        if answer1 and not answer2:
            subtractions.append((qid, answer1))
        elif not answer1 and answer2:
            additions.append((qid, answer2))
        elif answer1 and answer2:
            jaccard_sim = jaccard_similarity(answer1, answer2)
            if jaccard_sim < jaccard_threshold:
                potential_modifications.append((qid, answer1, answer2))

    return additions, subtractions, potential_modifications

def normalized_levenshtein_distance(text1, text2):
    if not text1 and not text2:
        return 0.0
    return Levenshtein.distance(text1, text2) / max(len(text1), len(text2))

def categorize_predictions_levenshetin(predictions1, predictions2, levenshtein_threshold=0.2):
    additions = []
    subtractions = []
    potential_modifications = []

    for qid, answer1 in predictions1.items():
        answer2 = predictions2.get(qid, "")
        # print("answer1 is",answer1,"answer2 is", answer2)

        if answer1 and not answer2:
            subtractions.append((qid, answer1))
        elif not answer1 and answer2:
            additions.append((qid, answer2))
        else:
            lev_dist = normalized_levenshtein_distance(answer1, answer2)
            if lev_dist > levenshtein_threshold:
                potential_modifications.append((qid, answer1, answer2))

    return additions, subtractions, potential_modifications


def get_embeddings(texts, model_name='bert-base-uncased'):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)
    model.eval()

    embeddings = []
    for text in texts:
        inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=512)
        with torch.no_grad():
            outputs = model(**inputs)
        # Use the mean of the last hidden states as the sentence embedding
        embedding = outputs.last_hidden_state.mean(dim=1).squeeze()
        embeddings.append(embedding.numpy())

    return embeddings

def cosine_similarity(embedding1, embedding2):
    return 1 - cosine(embedding1, embedding2)

def categorize_predictions_with_embeddings(predictions1, predictions2, model_name='bert-base-uncased', similarity_threshold=0.8):
    additions = []
    subtractions = []
    potential_modifications = []

    all_texts1 = [predictions1[qid] for qid in predictions1]
    all_texts2 = [predictions2[qid] for qid in predictions2]

    embeddings1 = get_embeddings(all_texts1, model_name)
    embeddings2 = get_embeddings(all_texts2, model_name)

    for idx, (qid, answer1) in enumerate(predictions1.items()):
        answer2 = predictions2.get(qid, "")

        if answer1 and not answer2:
            additions.append((qid, answer1))
        elif not answer1 and answer2:
            subtractions.append((qid, answer2))
        else:
            emb1 = embeddings1[idx]
            emb2 = embeddings2[list(predictions2.keys()).index(qid)]
            similarity = cosine_similarity(emb1, emb2)
            # print(similarity)
            if similarity < similarity_threshold:
                potential_modifications.append((qid, answer1, answer2))

    return additions, subtractions, potential_modifications
