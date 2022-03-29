from dotenv import dotenv_values

try:
    __env_type = dotenv_values('.env')
    __env_type = __env_type['ENV']
    __ON_DOCKER = True
except:
    __env_type = dotenv_values('../.env')
    __env_type = __env_type['ENV']
    __ON_DOCKER = False

if __ON_DOCKER:
    if __env_type == 'PROD':
        print('============ ENV PROD ===========')
        ENV = dotenv_values('./envs/.env.prod')
    elif __env_type == 'HOMOLOG':
        print('============ ENV HOMOLOG ===========')
        ENV = dotenv_values('./envs/.env.homolog')
    elif __env_type == 'DEV':
        print('============ ENV DEV ===========')
        ENV = dotenv_values('./envs/.env.dev')
else:
    if __env_type == 'PROD':
        print('============ ENV PROD ===========')
        ENV = dotenv_values('../envs/.env.prod')
    elif __env_type == 'HOMOLOG':
        print('============ ENV HOMOLOG ===========')
        ENV = dotenv_values('../envs/.env.homolog')
    elif __env_type == 'DEV':
        print('============ ENV DEV ===========')
        ENV = dotenv_values('../envs/.env.dev')

