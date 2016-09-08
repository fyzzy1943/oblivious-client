import configparser

conf = configparser.ConfigParser()
conf.read('config.ini', 'utf-8')

def url():
    if conf.has_option('main', 'base_url'):
        return conf['main']['base_url']
    else:
        return None

def all():
    s = conf.sections()
    if 'main' in s:
        s.remove('main')
    return s

def get(section, option):
    pass
