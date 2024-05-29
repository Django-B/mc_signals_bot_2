import configparser, sys

config_filename = 'config'
config_filename += '.ini'

def get_config(section='main'):
    '''Считывает файл config.ini'''
    config = configparser.ConfigParser()
    config.read(config_filename)

    config = config[section] if section in config else config

    return config

def get_or_create_config(var, val=None, section='variables'):
    config = configparser.ConfigParser()
    config.read(config_filename)

    if not section in config:
        config[section] = {}

    if val:
        config[section][var] = val
        with open(config_filename, 'w') as f:
            config.write(f)
        
    if var in config[section]:
        print('VAR IN SECTION')
        print('VAR:', config[section][var])
        return config[section][var]
    else:
        print('VAR NOT IN SECTION')



if __name__=='__main__':
    print(get_config())
