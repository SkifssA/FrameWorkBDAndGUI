from fastapi.templating import Jinja2Templates

from webapp.utils.build_client_config_tables import build_table_config_from_meta

def sutup_jinja(t: Jinja2Templates):
    g = t.env.globals

    #Постоение данный для таблиц (build_table_config(meta))
    g['build_table_config'] = build_table_config_from_meta