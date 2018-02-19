# -*- coding: utf-8 -*-
import requests
import common_variables as com_vars
from JsonValidator import *


class APIClients:

    def get_client_services(self, client_id):
        headers = {'content-type': 'application/json'}
        body = {"client_id": client_id}
        body = json.dumps(body)
        r = requests.post(com_vars.BASE_API_URL+'client/services', headers=headers, data=body)
        services = r.content
        #services = json.loads(r.content)
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
        return r.content

    def get_available_services(self, client_id):
        validator = JsonValidator()
        all_serv = self.get_services()
        cli_serv = self.get_client_services(client_id)
        avail_serv_list = []
        cl_serv_id_list = validator.get_elements(cli_serv, "$.items[*].id")
        if not cl_serv_id_list:
            cl_serv_id_list = []
        all_id_list = validator.get_elements(all_serv, "$.items[*].id")


        for id in cl_serv_id_list:
            while id in all_id_list:
                all_id_list.remove(id)

        id_list = all_id_list
        #id_list = [10, 22]

        for id in id_list:
            elem = validator.get_elements(all_serv, ("$.items[?(@.id == %s)]" %(id)))
            if not elem:
                continue
            avail_serv_list.append(elem[0])

        resp = {"count": len(avail_serv_list), "items": avail_serv_list}

        return json.dumps(resp)

    def check_service_activated(self, client_id, service_id):
        validator = JsonValidator()
        serv_list = self.get_client_services(client_id)
        id_list = validator.get_elements(serv_list, "$.items[*].id")
        if not id_list:
            return False
        if service_id in id_list:
            return True
        else:
            return False


id_list = [1, 22]
value = 33
while value in id_list:
    id_list.remove(value)
#print id_list





client = APIClients()

#print client.get_client_services(3)

#print client.get_available_services(10)

#print client.check_service_activated(3, 5)

