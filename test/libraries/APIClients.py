# -*- coding: utf-8 -*-
import requests
import json
import common_variables as com_vars

class APIClients:

    def get_client_services(self, client_id):
        headers = {'content-type': 'application/json'}
        body = {"client_id": client_id}
        body = json.dumps(body)
        r = requests.post(com_vars.BASE_API_URL+'client/services', headers=headers, data=body)
        # services = json.loads(r.content)
        services = r.content
        return services

    def get_services(self):
        headers = {'content-type': 'application/json'}
        r = requests.get(com_vars.BASE_API_URL + 'services', headers=headers)
        #services = json.loads(r.content)
        services = r.content
        return services

    def add_service(self, client_id, service_id):
        headers = {'content-type': 'application/json'}
        body = {"client_id": client_id, "service_id": service_id}
        body = json.dumps(body)
        r = requests.post(com_vars.BASE_API_URL + 'client/add_service', headers=headers, data=body)
        print dir(r)

        return r.content
