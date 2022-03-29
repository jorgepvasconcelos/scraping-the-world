from dotenv import dotenv_values


__env_chosen = dotenv_values('.env')
__env_type = __env_chosen['ENV']

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
    ENV = dotenv_values('.')

