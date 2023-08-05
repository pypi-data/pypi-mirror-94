import os
import json
import argparse

from barbell2.createh5 import CreateHDF5
from autosegl3 import AutoSegL3CNN


class AutoSegL3:

    def __init__(self, params):
        super(AutoSegL3, self).__init__()
        self.params = params

    @staticmethod
    def get_output_files(output_dir, test_size):
        output_files = list()
        output_files.append(os.path.join(output_dir, 'training.h5'))
        if test_size > 0.0:
            output_files.append(os.path.join(output_dir, 'test.h5'))
        return output_files

    def train(self, dir_path):
        output_dir = self.params['output_dir']
        os.makedirs(output_dir, exist_ok=True)
        output_files = self.get_output_files(output_dir, self.params['test_size'])
        creator = CreateHDF5(
            dir_path=dir_path,
            output_files=output_files,
            rows=self.params['image_shape'][0],
            columns=self.params['image_shape'][1],
            test_size=self.params['test_size'],
            is_training=True,
            log_dir=self.params['output_dir'],
        )
        training_file, test_file = creator.create_hdf5()
        network = AutoSegL3CNN(training_file, test_file, self.params)
        network.run()

    def predict(self, file_or_dir_path):
        pass


parser = argparse.ArgumentParser()
parser.add_argument('param_file', help="""JSON parameter file. Use parameter 'test_size' to indicate whether you
want to split up the training data or not. If test_size = 0.0, all data will be used for training which would be
the case just before you start using the model for prediction.
""")
parser.add_argument('dir_path', help='Path to data directory with training/test data')
parser.add_argument('procedure', help='Procedure to run, [train|predict] (default: train)', default='train')
args = parser.parse_args()


def main():
    with open(args.param_file, 'r') as f:
        params = json.load(f)
        auto_seg = AutoSegL3(params)
        if args.procedure == 'train':
            auto_seg.train(args.dir_path)
        elif args.procedure == 'predict':
            auto_seg.predict(args.dir_path)
        else:
            print('Unknown procedure {}'.format(args.procedure))


if __name__ == '__main__':
    main()
