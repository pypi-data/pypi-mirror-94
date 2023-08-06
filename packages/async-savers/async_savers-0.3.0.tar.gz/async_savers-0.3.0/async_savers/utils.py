import os
from pickle import load, UnpicklingError


DEFAULT_MAX_N_SHARDS = 6


def make_shard_template(n):
    return 'shard_{:0' + str(n) + 'd}.pkl'


def load_shards_generator(data_dir, max_n_shards=DEFAULT_MAX_N_SHARDS):
    shard_template = make_shard_template(max_n_shards)
    n_shards = len(os.listdir(data_dir))
    
    for i in range(n_shards):
        fp = os.path.join(data_dir, shard_template.format(i))
        try:
            with open(fp, 'rb') as f:
                shard = load(f)
        except (UnicodeDecodeError, UnpicklingError):
            with open(fp, 'rb') as f:
                shard = load(f, encoding='latin1')
        yield shard
    

def load_shards(data_dir, max_n_shards=DEFAULT_MAX_N_SHARDS):
    data = []
    shards_gen = load_shards_generator(data_dir, max_n_shards=max_n_shards)
    for shard in shards_gen:
        data.extend(shard)
    
    return data


def process_shards(process, data_dir, saver, max_n_shards=DEFAULT_MAX_N_SHARDS):
    shards_gen = load_shards_generator(data_dir, max_n_shards=max_n_shards)
    for shard_idx, shard in enumerate(shards_gen):
        for data_idx, data in enumerate(shard):
            processed_data = process(data, data_idx, shard_idx)
            saver.save(processed_data)
