
path_to_exe = ''

def get_bins():
    try:
        with open(path_to_exe, 'r+b') as file_binary:
            for line in file_binary:
                print(line)
    except Exception as error:
        print("Error reading file binary: {}".format(error))

if __name__ == '__main__':
    get_bins()