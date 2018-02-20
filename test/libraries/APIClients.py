# -*- coding: utf-8 -*-
import requests
import common_variables as com_vars
from JsonValidator import *


class APIClients:
    """Класс для работы с Api тестируемого приложения """
    def __init__(self):
        pass

    def get_client_services(self, client_id):
        """
        Получение списка подключенных клиенту сервисов
        
        *Args:*\n
        client_id - id клиента

        *Returns:*\n
        Json структура

        *Example:*\n
        | *Test Cases* | *Action* |  *Action* |*Argument* |
        | Get Client Services  | ${services}=   | APIClients.Get Client Services |   ${client_id}  |

        """
        headers = {'content-type': 'application/json'}
        body = {"client_id": client_id}
        body = json.dumps(body)
        r = requests.post(com_vars.BASE_API_URL+'client/services', headers=headers, data=body)
        services = r.content
        return services

    def get_services(self):
        """
        Получение списка всех сервисов
        *Args:*\n

        *Returns:*\n
        Json структура

        *Example:*\n
        | *Test Cases* | *Action* | *Action* |
        | Get Services  | ${services}=   | APIClients.Get Services |

        """
        headers = {'content-type': 'application/json'}
        r = requests.get(com_vars.BASE_API_URL + 'services', headers=headers)
        services = r.content
        return services

    def add_service(self, client_id, service_id):
        """
        Активирование сервиса для клиента
        *Args:*\n
        client_id - id клиента
        service_id - id сервиса
        *Returns:*\n
        http-response

        *Example:*\n
        | *Test Cases* | *Action* | *Action* | *Argument* | *Argument* |
        | Add Service  | ${resp}= | APIClients.Add Service | 1 | 2 |
        |              |  Log     | ${resp}
        =>

        """
        headers = {'content-type': 'application/json'}
        body = {"client_id": client_id, "service_id": service_id}
        body = json.dumps(body)
        r = requests.post(com_vars.BASE_API_URL + 'client/add_service', headers=headers, data=body)
        return r

    def get_available_services(self, client_id):
        """
        Получение списка доступных сервисов для подключения клиенту
        *Args:*\n
        client_id - id клиента
        *Returns:*\n
        Json структура

        *Example:*\n
        | *Test Cases* | *Action* | *Action* | *Argument* | *Argument* |
        | Get Available Services  | ${services}= | APIClients.Get Available Services | 1 |

        """
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

        for id in id_list:
            elem = validator.get_elements(all_serv, ("$.items[?(@.id == %s)]" %(id)))
            if not elem:
                continue
            avail_serv_list.append(elem[0])

        resp = {"count": len(avail_serv_list), "items": avail_serv_list}

        return json.dumps(resp)

    def check_service_activated(self, client_id, service_id):
        """
        Проверка наличия подключенного сервиса у клиента
        *Args:*\n
        client_id - id клиента
        service_id - id сервиса
        *Returns:*\n
        Boolean

        *Example:*\n
        | *Test Cases* | *Action* | *Action* | *Argument* | *Argument* |
        | Check Services Activated  | ${services}= | APIClients.Check Services Activated | 1 | 2 |

        """
        validator = JsonValidator()
        serv_list = self.get_client_services(client_id)
        id_list = validator.get_elements(serv_list, "$.items[*].id")
        if not id_list:
            return False
        if service_id in id_list:
            return True
        else:
            return False
