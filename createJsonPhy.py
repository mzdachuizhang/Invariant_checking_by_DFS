import json


def createJsonPhy(n):
    ret_dict = {}
    ret_list = []
    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):
            list = ['c' + str(i), 'c' + str(j)]
            ret_list.append(list)
    key = 'c_phy'
    ret_dict[key] = ret_list
    json_str = json.dumps(ret_dict)
    file_path = 'c_phy.json'
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(json_str)


if __name__ == '__main__':
    createJsonPhy(2)
