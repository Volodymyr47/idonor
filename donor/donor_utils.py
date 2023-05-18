import logging


def sort_answer_in_dict(data, key_num):
    ordering_data = {}
    for key, value in data.items():
        if len(value.strip()) > 0:
            if not key.startswith('text'):
                ordering_data.update({key: value})
            if key.startswith('text'):
                ordering_data[key[key_num:]] = ordering_data.get(key[key_num:]) + '. ' + data.get(key)
    return ordering_data


  # test_result = {}
        # for key, value in pre_test_result.items():
        #     if len(value.strip()) > 0:
        #         if not key.startswith('text'):
        #             test_result.update({key: value})
        #         if key.startswith('text'):
        #             test_result[key[5:]] = test_result.get(key[5:]) + '.  Коментар: ' + pre_test_result.get(key)