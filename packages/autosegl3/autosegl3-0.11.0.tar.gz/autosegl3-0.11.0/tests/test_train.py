import json

from types import SimpleNamespace
from autosegl3 import TrainL3


def test_train():
    with open('data/params.json', 'r') as f:
        args = SimpleNamespace(**json.load(f))
        x = TrainL3(args)
        model_path = x.execute()
        assert 'final_model' in model_path
