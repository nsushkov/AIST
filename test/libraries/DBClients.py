# -*- coding: utf-8 -*-
import random
import string
import sqlite3


class DBClients:

    """Класс для работы с базой данных тестируемого приложения """

    name_len = 6
    default_balance = 5

    def __init__(self, db_path):
        self.db_path = db_path

    def get_client_balance(self, client_id):
        """
        Получение текущего баланса клиента
        *Args:*\n
        client_id - id клиента

        *Returns:*\n
        balance

        *Example:*\n
        | *Test Cases* | *Action* | *Action* | *Argument* |
        | Get Client Balance  | ${balance}= | DBClients.Get Client Balance | 1 |

        """
        try:
            with sqlite3.connect(self.db_path) as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT BALANCE FROM BALANCES AS bl WHERE bl.CLIENTS_CLIENT_ID=%s;" %(client_id))
                balance = cursor.fetchall()
                if not balance:
                    balance = None
                else:
                    balance = balance[0][0]
                return balance
        except sqlite3.DatabaseError as err:
            print("Error: ", err)
            return None

    def get_suitable_client(self):
        """
        Получение клиента для теста, удовлетворяющего требованиям: с положительным балансом
        В случае, если такой клиент не найден - возвращается None
        *Args:*\n

        *Returns:*\n
        client_id - id клиента

        *Example:*\n
        | *Test Cases* | *Action* | *Action* |
        | Get Suitable Client  | ${client_id}= | DBClients.Get Suitable Client |

        """
        try:
            with sqlite3.connect(self.db_path) as connection:
                cursor = connection.cursor()
                cursor.execute("select cl.CLIENT_ID from CLIENTS AS cl "
                               "INNER JOIN BALANCES AS bl ON cl.CLIENT_ID = bl.CLIENTS_CLIENT_ID "
                               "WHERE bl.BALANCE > 0 LIMIT 30;")
                client_id_list = cursor.fetchall()
                if not client_id_list:
                    client_id = self.add_rand_client()
                    print "Suitable client was not found, created client with ID: ", client_id
                else:
                    client_id = random.choice(client_id_list)[0]
                return client_id
        except sqlite3.DatabaseError as err:
            print("Error: ", err)
            return None

    def add_rand_client(self):
        """
        Создание клиента со случайным именем и положительным балансом
        *Args:*\n

        *Returns:*\n
        client_id - id клиента

        *Example:*\n
        | *Test Cases* | *Action* | *Action* |
        | Add Rand Client  | ${client_id}= | DBClients.Add Rand Client |

        """
        client_name = ''.join(random.choice(string.ascii_letters) for _ in range(DBClients.name_len))
        try:
            with sqlite3.connect(self.db_path) as connection:
                cursor = connection.cursor()
                cursor.execute("INSERT INTO CLIENTS (CLIENT_NAME) VALUES ('%s')" %(client_name))
                cursor.execute("INSERT INTO BALANCES VALUES (%s, %s)" %(cursor.lastrowid, DBClients.default_balance))
                return cursor.lastrowid
        except sqlite3.DatabaseError as err:
            print("Error: ", err)
            return None


