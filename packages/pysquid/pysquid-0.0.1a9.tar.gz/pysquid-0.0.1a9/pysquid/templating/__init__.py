import uuid
from functools import reduce


TEMPLATE_STRUCT = {
    'priority': (int, 0, int, None),
    'tags': (list, [], set, None),
    'untags': (list, [], set, None),
    'variables': (dict, {}, dict, None),
    'global': (dict, {}, dict, None),
    'services': (dict, {}, dict, None),
}

TEMPLATE_INTERNALS = {
    '__uuid__': lambda k, v, id_: uuid.uuid4(),
}

SERVICE_STRUCT = {
    'tags': (list, [], set, None),
    'variables': (dict, {}, dict, None),
    '__matching__': (str, 'weak', str, None),  # weak | strong | exact
    '__enabled__': (bool, False, bool, None),  # weak | strong | exact
#    '__pool__': (int, 1, int, None),
#    '__depth__': (int, 1, int, None),
    '__mode__': (str, 'thread', str, None),
    '__workers__': (dict, {}, dict, None),
}

SERVICE_INTERNALS = {
    '__plugin__': lambda k, v, id_: v.get('__plugin__') if v.get('__plugin__') else id_,
    '__variable__': lambda k, v, id_: v.get('__variable__') if v.get('__variable__') else id_
}


def parse_template(d: dict, struct: dict, internals: dict, id_: str = None):
    
    for mkey, value in struct.items():

        type_, default_, converterf_, allowed_ = value

        value_from_template = d.get(mkey)

        if value_from_template and not isinstance(value_from_template, type_):
            raise ValueError

        current_ = value_from_template or default_

        if not isinstance(current_, converterf_):                    
            current_ = converterf_(current_)

        if allowed_ and current_ not in allowed_:
            raise ValueError

        d[mkey] = current_

    for mkey, func in internals.items():
        d[mkey] = func(mkey, d, id_)

    return d


def merge(a, b, path=None):
    "merges b into a"
    if path is None: path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge(a[key], b[key], path + [str(key)])            
        else:
            a[key] = b[key]
    return a


class Template():

    def __str__(self):
        import pprint
        return pprint.pformat(self.template)

    def __init__(self):
        self.template = {}
        self.subtemplates = []
        self.priorites = []
        self.tags = set()
        self.untags = set()             

    def add_subtemplate(self, subtemplate: dict = {}):

        d = parse_template(subtemplate, TEMPLATE_STRUCT, TEMPLATE_INTERNALS)

        tags = d.get('tags')
        untags = d.get('untags')

        self.tags = self.tags.union(tags)
        self.untags = self.untags.union(untags)

        services = d.get('services')
        variables = d.get('variables')
        
        for sid, service in services.items():
            d['services'][sid] = parse_template(service, SERVICE_STRUCT, SERVICE_INTERNALS, sid)
            variable_key = d['services'][sid].get('__variable__')
            variables = merge(variables.get(variable_key, {}), d['services'][sid].get('variables'))
            d['services'][sid]['variables'] = variables

        self.subtemplates.append(d)

        self.priorites.append(d.get('priority'))
        self.priorites.sort()
        
        return d
    
    def build(self, match: bool = True):

        templates = sorted(self.subtemplates, key=lambda k: k['priority']) 

        reduce(merge, templates)

        merged = templates[0]

        services = merged.get('services')
        variables = merged.get('variables')

        for sid, service in services.items():
            key = service.get('__variable__')
            variables = merge(variables.get(key, {}), service.get('variables'))
            service['variables'] = variables

        merged['__tags__'] = self.tags.difference(self.untags)

        self.template = merged

        if match:
            self.match()

        return self.template

    def match(self):

        services = self.template.get('services')
        tags = self.template.get('__tags__')

        matched_services = {}
        
        for sid, service in services.items():

            stags = service.get('tags')

            weak = tags.intersection(stags)
            strong = tags.difference(stags)

            matchmode = service.get('__matching__')

            if matchmode == 'weak' and weak:
                matched_services[sid] = service
                continue

            if matchmode == 'strong' and strong:
                matched_services[sid] = service
                continue
                
        self.template['services'] = matched_services

        return self.template
            

