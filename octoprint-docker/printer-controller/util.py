import json, socket


def write_to_file(data):
    with open('dockertests-ports.txt', 'w') as outfile:
        json.dump(data, outfile)


def read_from_file():
    with open('dockertests-ports.txt') as json_file:
        data = json.load(json_file)
        print(data['printer-dockers'])
        return data


def get_available_port_numbers(number):
    print("incoming number:", number)
    # starting point 50000
    plist = []
    i = 0
    number = int(number)
    while i < number:
        if is_port_free(int("5000"+str(i))) is True:
            plist.append("5000"+str(i))
        else:
            number = number +1
        i += 1
    return plist


def is_port_free(port):

    a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    location = ("127.0.0.1", port)
    result_of_check = a_socket.connect_ex(location)

    if result_of_check == 0:
        result = False
    else:
        result = True
    a_socket.close()
    return result