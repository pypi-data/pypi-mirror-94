import os

from autosegl3 import AutoSegL3


def test_autosegl3():
    params = {
        'image_shape': [512, 512, 1],
        'patch_shape': [512, 512, 1],
        'output_dir': '/tmp/auto_seg',
        'test_size': 0.2,
        'learning_rate': 0.001,
        'l2_loss': 0.001,
        'num_steps': 100000,
        'num_classes': 4,
        'dropout_rate': 0.05,
        'min_bound': -200,
        'max_bound': 200,
        'batch_size': 1,
        'train_eval_step': 100,
        'val_eval_step': 100,
        'save_model_step': 1000,
    }
    d = '{}/data/surfdrive/projects/20210203_autosegl3/dicom_and_tag'.format(os.environ['HOME'])
    tool = AutoSegL3(params=params)
    print(tool.train(d))
