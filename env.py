from dotenv import dotenv_values

__ON_DOCKER = True

if __ON_DOCKER:
    ENV = dotenv_values('.env')
else:
    ENV = dotenv_values('../.env')

print('')

# if __env_type == 'PROD':
#     print('============ ENV PROD ===========')
#     # ENV = dotenv_values('../envs/.env.prod')
#     ENV = dotenv_values('../scraping-the-world/envs/.env.prod')
# elif __env_type == 'HOMOLOG':
#     print('============ ENV HOMOLOG ===========')
#     ENV = dotenv_values('../envs/.env.homolog')
# elif __env_type == 'DEV':
#     print('============ ENV DEV ===========')
#     # ENV = dotenv_values('../envs/.env.dev')
#     ENV = dotenv_values('../scraping-the-world/envs/.env.dev')
# else:
#     ENV = dotenv_values('.')

