import os
import json
import shutil
import argparse

from barbell2.utils import Logger
from barbell2.lib.dicom import is_dicom
from types import SimpleNamespace


class GenID:

    def __init__(self, args):
        if isinstance(args, dict):
            self.args = SimpleNamespace(**args)
        else:
            self.args = args
        self.include_types = [x.strip() for x in self.args.include_types.split(',')]
        self.logger = Logger(prefix='genID', to_dir=self.args.log_dir, timestamp=False)
        self.prefix = self.args.prefix
        self.nr_digits = self.args.nr_digits
        self.idx = 1

    @staticmethod
    def get_tag_file(dcm_file):
        tag_file = dcm_file[:-4] + '.tag'
        if os.path.isfile(tag_file):
            return tag_file
        tag_file = dcm_file + '.tag'
        if os.path.isfile(tag_file):
            return tag_file
        return None

    def next_file_id(self):
        file_id = '{}{}'.format(self.prefix, str(self.idx).zfill(self.nr_digits))
        self.idx += 1
        return file_id

    def execute(self):
        file_ids = {}
        os.makedirs(self.args.output_dir, exist_ok=False)
        for root, dirs, files in os.walk(self.args.root_dir):
            for f in files:
                f = os.path.join(root, f)
                file_id = self.next_file_id()
                if 'dicom' in self.include_types and 'tag' in self.include_types and is_dicom(f):
                    dcm_file = f
                    tag_file = self.get_tag_file(dcm_file)
                    if tag_file is None:
                        continue
                    target_dcm_file = os.path.join(self.args.output_dir, file_id + '.dcm')
                    shutil.copyfile(dcm_file, target_dcm_file)
                    target_tag_file = os.path.join(self.args.output_dir, file_id + '.tag')
                    shutil.copyfile(tag_file, target_tag_file)
                    file_ids[file_id] = [target_dcm_file, target_tag_file]
                elif 'dicom' in self.include_types:
                    dcm_file = f
                    target_dcm_file = os.path.join(self.args.output_dir, file_id + '.dcm')
                    shutil.copyfile(dcm_file, target_dcm_file)
                    file_ids[file_id] = target_dcm_file
                else:
                    pass
        with open(os.path.join(self.args.output_dir, '..', 'file_ids.txt'), 'w') as f:
            json.dump(file_ids, f, indent=4)
        return self.args.output_dir


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'root_dir',
        help='Root directory containing DICOM and (optionally) TAG files',
    )
    parser.add_argument(
        'output_dir',
        help='Directory where to write renamed files',
    )
    parser.add_argument(
        'include_types',
        help='File types to include (default: dicom,tag)',
        default='dicom,tag',
    )
    parser.add_argument(
        'prefix',
        help='Optional prefix to put in front of file index',
        default='P',
    )
    parser.add_argument(
        'nr_digits',
        help='Number of digits to use in file name',
        default=4,
    )
    parser.add_argument(
        '--log_dir',
        help='Directory where to write logging info (default: .)',
        default='.',
    )
    args = parser.parse_args()
    x = GenID(args)
    x.execute()


if __name__ == '__main__':
    main()
