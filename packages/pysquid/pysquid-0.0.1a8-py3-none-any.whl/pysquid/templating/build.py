import pandas as pd
import pysquid.templating


def to_df(lu_):

    data_types = {
        'priority': [], 'uuid': []
    }

    for uuid, template in lu_.items():    
        data_types['priority'].append(template.get('priority'))
        data_types['uuid'].append(str(uuid))
    
    return pd.DataFrame(data_types).sort_values('priority')


def merge(templates: list = []):

    lu_ = {}
    
    for template in templates:

        if not isinstance(template, dict):
            continue

        d_ = pysquid.templating.parse_template(template)

        uuid = str(d_.get('__uuid__'))
        lu_[uuid] = d_

    df = to_df(lu_)

    grouped = df.groupby(['priority'])

    tags = set()
    untags = set()

    services = {}
    variables = {}
    
    for gid, group in grouped:    
        
        uuids = group.get('uuid').tolist()
        
        for uuid in uuids:
            
            template = lu_.get(str(uuid))
            
            tags_ = template.get('tags')
            untags_ = template.get('untags')
                
            tags = tags.union(tags_)
            untags = untags.union(untags_)

            services_ = template.get('services')
            variables_ = template.get('variables')

            services = {**services, **services_}
            variables = {**variables, **variables_}
            
    parsed_template = {
        'tags': tags.difference(untags),
        'services': services,
        'variables': variables,
        'global': {},
    }

    return parsed_template


def build_services(parsed_template: dict):

    services = parsed_template.get('services')

    SERVICE_MAGICS = {
        'plugin_id': (str, '', str, None),
        'tags': (list, [], set, None),
        'variables': (dict, {}, dict, None),
    }

    services_ = {}
    variables_ = parsed_template.get('variables')

    for sid, service in services.items():
        parsed = pysquid.templating.parse_template(service, SERVICE_MAGICS)
        parsed['plugin_id'] = parsed['plugin_id'] or sid
        service_vars = variables_.get(sid) or {}
        parsed['variables'] = {**service_vars, **parsed.get('variables')}
        services_[sid] = parsed

    parsed_template['services'] = services


def merge_templates(templates: list = []):

    templates = sorted(templates, key=lambda k: k['priority']) 

    merged = {}

    for template in templates:
        merged = {**merged, **template}

    merged['__tags__'] = merged.get('tags').difference(merged.get('untags'))

    return merged
