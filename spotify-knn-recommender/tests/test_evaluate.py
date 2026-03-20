import pytest
from src.evaluate import precision_at_k, recall_at_k, ndcg_at_k, hit_rate_at_k, mrr_at_k

def test_precision_at_k():
    recommended = ['track1', 'track2', 'track3', 'track4', 'track5']
    ground_truth = ['track1', 'track6']
    assert precision_at_k(recommended, ground_truth, k=5) == 0.2

def test_recall_at_k():
    recommended = ['track1', 'track2', 'track3', 'track4', 'track5']
    ground_truth = ['track1', 'track6']
    assert recall_at_k(recommended, ground_truth, k=5) == 0.5

def test_ndcg_at_k():
    recommended = ['track1', 'track2', 'track3', 'track4', 'track5']
    ground_truth = ['track1', 'track6']
    assert ndcg_at_k(recommended, ground_truth, k=5) > 0.0

def test_hit_rate_at_k():
    recommended = ['track1', 'track2', 'track3', 'track4', 'track5']
    ground_truth = ['track1', 'track6']
    assert hit_rate_at_k(recommended, ground_truth, k=5) == 1.0

def test_mrr_at_k():
    recommended = ['track1', 'track2', 'track3', 'track4', 'track5']
    ground_truth = ['track1', 'track6']
    assert mrr_at_k(recommended, ground_truth, k=5) == 1.0