import numpy as np

def precision_at_k(recommended, ground_truth, k=10):
    top_k = recommended[:k]
    hits = sum([1 for t in top_k if t in ground_truth])
    return hits / k

def recall_at_k(recommended, ground_truth, k=10):
    top_k = recommended[:k]
    hits = sum([1 for t in top_k if t in ground_truth])
    return hits / len(ground_truth) if len(ground_truth) > 0 else 0.0

def ndcg_at_k(recommended, ground_truth, k=10):
    dcg = 0.0
    for i, t in enumerate(recommended[:k]):
        if t in ground_truth:
            dcg += 1 / np.log2(i + 2)
    ideal_hits = min(len(ground_truth), k)
    idcg = sum([1 / np.log2(i + 2) for i in range(ideal_hits)])
    return dcg / idcg if idcg > 0 else 0.0

def hit_rate_at_k(recommended, ground_truth, k=10):
    top_k = recommended[:k]
    return 1.0 if any(t in ground_truth for t in top_k) else 0.0

def mrr_at_k(recommended, ground_truth, k=10):
    top_k = recommended[:k]
    for i, t in enumerate(top_k):
        if t in ground_truth:
            return 1.0 / (i + 1)
    return 0.0
