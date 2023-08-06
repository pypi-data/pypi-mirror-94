import os


def get_available():

    # Generate output nvidia-smi
    file_path = '{}/nvidia-smi.txt'.format(os.environ['HOME'])
    cmd = 'nvidia-smi > {}'.format(file_path)
    os.system(cmd)

    # In the following I'm assuming that the GeForce cards are listed in order
    # meaning that the first GeForce encountered gets ID = 0, the second ID = 1
    # So even though nvidia-smi reports the 2nd GeForce card to have ID = 2, this
    # code will list it as ID = 1. This seems to work for now.
    memory_usage = {}
    with open(file_path, 'r') as f:
        idx = 0
        for line in f.readlines():
            if 'GeForce RTX' in line:
                memory_usage[idx] = 0
                continue
            if idx in memory_usage.keys() and memory_usage[idx] == 0:
                memory_usage[idx] = int(line.split()[12][:-1])
                idx += 1

    # Find GPU device ID with least amount of memory usage
    available_gpu = -1
    min_mu = 100
    for gpu in memory_usage.keys():
        if memory_usage[gpu] < min_mu:
            min_mu = memory_usage[gpu]
            available_gpu = gpu
    return available_gpu


if __name__ == '__main__':
    print(get_available())
