from helper import conf

base_url = conf.url()

for section in conf.all():
    print(section)
