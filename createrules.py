def createrules(es:host, es_port, nb_url):
    """ create rules is a function that receives as input a string 
    containing hostname:port combinations for elasticsearch and 
    nagbot HTTP endpoints and outputs a YAMl formatted file that
    will be used by the setup process to give setup instructions 
    to the installer.
    """
    """ you will need to :
    1) take the es_host, es_port and nb_url variables and insert the values 
    into the jinja2 template below : 
    
    https://github.com/hilt86/NAGBOT/blob/master/ssh_yaml.j2
    
    also see https://realpython.com/primer-on-jinja-templating/
    
    2) you will need to return the python object containing the template
    containing the values of passed variables, for example :
    
    name: ssh_multiple_failures
    es_host: {{ es_host }}
    
    if we set :
    es_host = 'elastic01.nixmechanix.com'
    es_port = 9200
    nb_url = 'http://13.210.205.72:5000/api/nagbot/json/'
    
    and then run your function createRules(es_host, es_port, nb_url)
    
    it will return an object like :
    
    name: ssh_multiple_failures
    es_host: elastic01.nixmechanix.com
    """
    return
