import numpy as np

# Returns a 2d array of hotvectors for each word in line
def make_to_hotvector(line, word_list_size):
    line_array = np.array(line)
    b = np.zeros((a.size, word_list_size))
    b[np.arange(a.size), a] = 1
    return b

def get_training_example(post, world_list):
    pass

def generate_training_dataset(posts, word_list):
    pass

def test_make_to_hotvektor():
    line = [0, 1, 2, 3, 4]
    word_list_size = 5
    hotvektor = make_to_hotvector(line, word_list_size)
    print(hotvektor)

# Testing
test_make_to_hotvektor()
