import yaml

def createrules(es_host, es_port, nb_url):
    data = dict(es_host = es_host, es_port = es_port, nb_url = nb_url)
    with open(filepath, 'a') as outfile:
        yaml.dump(data, outfile, default_flow_style=False)
        outfile.close()
        

def yaml_loader(filepath):
   with open(filepath, "r") as file_descriptor:
       data = yaml.load(file_descriptor)
   return data

es_host = 'elastic01.nixmechanix.com'
es_port = 9200
nb_url = 'http://13.210.205.72:5000/api/nagbot/jason/'
filepath = "./ssh_yaml.j2"


if __name__ == '__main__':
    createrules(es_host, es_port, nb_url)

    data = yaml_loader(filepath)
    for n, m in data.iteritems():
        print n, ":", m
