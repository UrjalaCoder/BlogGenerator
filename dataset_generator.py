import numpy as np
from data_parser import load_post_data

# Returns a 2d array of hotvectors for each word in line
def make_to_hotvector(line, word_list_size):
    line_array = np.array(line)
    b = np.zeros((line_array.size, word_list_size))
    b[np.arange(line_array.size), line_array] = 1
    return b

# Generates training examples that have feature_count elements.
def get_training_example(post, word_list_size, feature_count=4):
    training_example = []
    for i in range(0, len(post) - feature_count + 1):
        label = post[(i + feature_count - 1)]
        hotvectors = make_to_hotvector(label, word_list_size)
        label = hotvectors[-1]
        training_data = post[i:(i + feature_count - 1)]
        training_example.append((np.array(training_data), label))
    return training_example

def generate_training_dataset(posts, word_list, feature_count=4):
    dataset = []
    word_list_size = len(word_list)
    for post in posts:
        post_set = get_training_example(post, word_list_size, feature_count=feature_count)
        dataset += (post_set)
    dataset = np.array(dataset)
    return dataset

def test_make_to_hotvektor():
    line = [1, 3, 2, 1, 4]
    word_list_size = 5
    hotvector = make_to_hotvector(line, word_list_size)
    print(hotvector)

def test_get_training_example():
    line = [0, 1, 2, 3, 4, 5]
    word_list_size = 6
    feature_count = 4

    training_examples = get_training_example(post=line, word_list_size=word_list_size, feature_count=feature_count)
    training_examples = np.array(training_examples)
    print(training_examples)

def test_generate_training_dataset():
    posts = [[1, 2, 3, 4, 5, 1, 2, 4, 1, 3], [0, 1, 3, 5, 2]]
    word_list = [x for x in range(6)]
    dataset = generate_training_dataset(posts, word_list)
    print(dataset)

def generate_dataset(input_filename="data", filename="dataset", cutoff=10, feature_count=4):
    try:
        posts, word_list = load_post_data(filename=input_filename)
        dataset = generate_training_dataset(posts[0:cutoff], word_list, feature_count=feature_count)
        path = f"datasets/{filename}"
        np.save(path, dataset)
        print(f"Saved {len(dataset)} elements in {path}")
    except Exception:
        print(f"failed to generate dataset with args: {input_filename} {filename} {cutoff} {feature_count}")

def test_for_real_data(cutoff=10):
    posts, keys = load_post_data(filename="data")
    word_list = keys
    feature_count = 4
    dataset = generate_training_dataset(posts[0:cutoff], word_list, feature_count=feature_count)

# Testing
generate_dataset()
