import random
import os


def read_specific_lines(file_name, numbers, mode):
    file = open(file_name, "r")
    found = 0
    result = ""
    if mode:
        for i, line in enumerate(file):
            if i in numbers:
                found += 1
                result += line
    else:
        for i, line in enumerate(file):
            if i not in numbers:
                result += line
    file.close()
    return result


def write_specific_lines(file_name, text):
    file = open(file_name, "w")
    file.write(text)
    file.close()



original_dir_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'original_dataset')
original_profile_name = os.path.join(original_dir_path, 'profile.txt')
original_TS1_name = os.path.join(original_dir_path, 'TS1.txt')
original_TS2_name = os.path.join(original_dir_path, 'TS2.txt')
original_TS3_name = os.path.join(original_dir_path, 'TS3.txt')
original_TS4_name = os.path.join(original_dir_path, 'TS4.txt')

train_dir_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'training_dataset')
train_profile_name = os.path.join(train_dir_path, 'profile.txt')
train_TS1_name = os.path.join(train_dir_path, 'TS1.txt')
train_TS2_name = os.path.join(train_dir_path, 'TS2.txt')
train_TS3_name = os.path.join(train_dir_path, 'TS3.txt')
train_TS4_name = os.path.join(train_dir_path, 'TS4.txt')

thing_dir_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'thing_dataset')
thing_profile_name = os.path.join(thing_dir_path, 'profile.txt')
thing_TS1_name = os.path.join(thing_dir_path, 'TS1.txt')
thing_TS2_name = os.path.join(thing_dir_path, 'TS2.txt')
thing_TS3_name = os.path.join(thing_dir_path, 'TS3.txt')
thing_TS4_name = os.path.join(thing_dir_path, 'TS4.txt')


for f in os.listdir(thing_dir_path):
    file_path = os.path.join(thing_dir_path, f)
    os.remove(file_path)

for f in os.listdir(train_dir_path):
    file_path = os.path.join(train_dir_path, f)
    os.remove(file_path)


numbers = []

for j in range(0, 100):
    rand_int = random.randint(0, 2200)
    while rand_int in numbers:
        rand_int = random.randint(0, 2200)
    numbers.append(random.randint(0, 2200))

write_specific_lines(thing_profile_name, read_specific_lines(original_profile_name, numbers, True))
write_specific_lines(thing_TS1_name, read_specific_lines(original_TS1_name, numbers, True))
write_specific_lines(thing_TS2_name, read_specific_lines(original_TS2_name, numbers, True))
write_specific_lines(thing_TS3_name, read_specific_lines(original_TS3_name, numbers, True))
write_specific_lines(thing_TS4_name, read_specific_lines(original_TS4_name, numbers, True))

write_specific_lines(train_profile_name, read_specific_lines(original_profile_name, numbers, False))
write_specific_lines(train_TS1_name, read_specific_lines(original_TS1_name, numbers, False))
write_specific_lines(train_TS2_name, read_specific_lines(original_TS2_name, numbers, False))
write_specific_lines(train_TS3_name, read_specific_lines(original_TS3_name, numbers, False))
write_specific_lines(train_TS4_name, read_specific_lines(original_TS4_name, numbers, False))