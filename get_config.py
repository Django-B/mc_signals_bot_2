import configparser, sys

config_filename = 'config'
config_filename += '.ini'

def get_config():
    '''Считывает файл config.ini'''
    config = configparser.ConfigParser()
    config.read(config_filename)

    args = sys.argv
    if len(args) > 1 and args[1] in config:
        config = config[args[1]]
    else:
        config = config['main']

    return config

if __name__=='__main__':
    print(get_config())
