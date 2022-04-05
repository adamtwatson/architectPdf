#!/usr/bin python3
import time
from random import SystemRandom

from mimesis import Person, BaseDataProvider

random = SystemRandom()


def recursive_binary_search(search_value, data_set: tuple):
    data_length = len(data_set)
    # print(f'data too long pairing it down, data_length: {data_length}')
    if data_length == 1:
        # print(data_set)
        return data_set[0]
    # f_start_time = time.perf_counter()
    middle_index = int(data_length // 2)  # floor divide to round down
    # grab the middle_index, and select an array to replace the original with
    # data_set = list(data_set)
    # middle_id = itemgetter(middle_index)(data_set)
    middle_id, user_profile = data_set[middle_index]
    # print(f'middle_id: {middle_id}, value: {user_profile}')
    if middle_id == search_value:
        # f_elapsed_time = time.perf_counter() - f_start_time
        # print(f'recursive_binary_search ran in: {f_elapsed_time}')
        # print(list(data_set))
        return middle_id, user_profile
    if middle_id > search_value:
        print(f'{middle_id} is greater than {search_value}, selecting first half of data...')
        # next_data_set = itertools.islice(data_set, 0, middle_index)
        # f_elapsed_time = time.perf_counter() - f_start_time
        # print(f'recursive_binary_search ran in: {f_elapsed_time}')
        # print(data_set[:10])
        return recursive_binary_search(search_value, data_set[:middle_index])
    else:
        print(f'{middle_id} is less than {search_value}, selecting second half of data...')
        # next_data_set = itertools.islice(data_set, middle_index, data_length)
        # f_elapsed_time = time.perf_counter() - f_start_time
        # print(f'recursive_binary_search ran in: {f_elapsed_time}')
        return recursive_binary_search(search_value, data_set[middle_index:])


class CustomPerson(Person):
    def json(self):
        data = {}
        function_black_list = [func for func in dir(BaseDataProvider)] + ['Meta']
        keys = filter(lambda x: x not in function_black_list, [func for func in dir(Person) if callable(getattr(Person, func))])
        for key in keys:
            data.update({key: getattr(self, key)()})
        return data
            

if __name__ == '__main__':
    random_count = 1293  # random.randint(10000000, 99999999)
    print(f'generating a list with {random_count} values')
    # start_time = time.perf_counter()
    # near_infinite_tuple = [1 * x for x in range(random_count)]
    # elapsed_time = time.perf_counter() - start_time
    # print(f'created a list with {random_count} values in {elapsed_time}')
    #
    # start_time = time.perf_counter()
    # near_infinite_tuple = [x for x in range(random_count)]
    # elapsed_time = time.perf_counter() - start_time
    # print(f'created a list with {random_count} values in {elapsed_time}')
    
    # start_time = time.perf_counter()
    # near_infinite_tuple = [range(random_count)]
    # elapsed_time = time.perf_counter() - start_time
    # print(f'created a list with {random_count} values in {elapsed_time}')

    start_time = time.perf_counter()
    # near_infinite_tuple = tuple(range(random_count))
    # near_infinite_set = tuple(set((x, "{'id': {x}}".format(x=x)) for x in range(random_count)))

    near_infinite_tuple = tuple([(x, CustomPerson()) for x in range(random_count)])
    # print(near_infinite_tuple[0])
    elapsed_time = time.perf_counter() - start_time
    print(f'created a list with {random_count} values in {elapsed_time}')
    # 
    # print(near_infinite_tuple1[50] == near_infinite_tuple[50])
    
    random_id = random.randint(0, random_count)
    print(f'Attempting to find user id: {random_id}')
    # print(f'{random_id} index in near_infinite_set: {near_infinite_set.index(random_id)}')

    start_time = time.perf_counter()
    user_id, value = recursive_binary_search(random_id, near_infinite_tuple)
    value = value.json()
    print(f'user_id: {user_id}, value: {value}')
    print(value.get('name', None))
    assert user_id == random_id  # Through some stroke of luck we found the id!
    elapsed_time = time.perf_counter() - start_time
    print(f'We found id {user_id} in {elapsed_time} seconds!!!')


# "{'id': " + "{x}".format(x=3) + "}"
# "{'id': " + "{0}".format(3) + "}"
# "{'id': {x}}".format(x=3)
# "{'id': {0}}".format(3)
# tuple(set((x, "{'id': {x}}".format(x=x)) for x in range(100)))
