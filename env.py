import os

from dotenv import dotenv_values


def path_to_file(file):
    path = None
    for root, dirs, files in os.walk('.'):
        for name in files:
            if name == file:
                path = (os.path.abspath(os.path.join(root, name)))

    return path


__env_type = dotenv_values(path_to_file('.env'))
__env_type = __env_type['ENV']

if __env_type == 'PROD':
    print('============ ENV PROD ===========')
    ENV = dotenv_values(path_to_file('.env.prod'))
elif __env_type == 'HOMOLOG':
    print('============ ENV HOMOLOG ===========')
    ENV = dotenv_values(path_to_file('.env.homolog'))
elif __env_type == 'DEV':
    print('============ ENV DEV ===========')
    ENV = dotenv_values(path_to_file('.env.dev'))
