import configparser

conf = configparser.ConfigParser()
conf.read('config.ini', 'utf-8')

def main(option):
    if conf.has_option('main', option):
        return conf['main'][option]
    else:
        return None

def all():
    s = conf.sections()
    if 'main' in s:
        s.remove('main')
    return s

def get(section, option):
    if conf.has_option(section, option):
        return conf[section][option]
    else:
        return None
