# -*- coding: utf-8 -*-
import random
import string
import sqlite3
import common_variables as com_vars

class DBClients:

    def get_client_balance(self, client_id):
        with sqlite3.connect(com_vars.DB_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT BALANCE FROM BALANCES AS bl WHERE bl.CLIENTS_CLIENT_ID=%s;" %(client_id))
            #cursor.execute("SELECT BALANCE FROM BALANCES AS bl WHERE bl.CLIENTS_CLIENT_ID={client_id}")
            balance = cursor.fetchall()
            if not balance:
                balance = None
            else:
                balance = balance[0][0]
        return balance

    def get_clients(self):
        with sqlite3.connect(com_vars.DB_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute("select cl.CLIENT_ID from CLIENTS AS cl INNER JOIN BALANCES AS bl ON cl.CLIENT_ID = bl.CLIENTS_CLIENT_ID WHERE bl.BALANCE > 0 LIMIT 30;")
            clients = cursor.fetchall()
            print("CLIENTS")
            print clients
        return clients

    def get_suitable_client(self):
        with sqlite3.connect(com_vars.DB_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute("select cl.CLIENT_ID from CLIENTS AS cl INNER JOIN BALANCES AS bl ON cl.CLIENT_ID = bl.CLIENTS_CLIENT_ID WHERE bl.BALANCE > 0 LIMIT 30;")
            client_id_list = cursor.fetchall()
            if not client_id_list:
                client_id = None
            else:
                client_id = random.choice(client_id_list)[0]
            print("CLIENT")
        return client_id

    def test_select(self):
        with sqlite3.connect(com_vars.DB_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute("select * from CLIENTS;")

            results = cursor.fetchall()
            print("CLIENTS")
            print(type(results))
            print(results)
        return results

    def add_rand_client(self):
        client_name = ''.join(random.choice(string.ascii_letters) for _ in range(com_vars.NAME_LEN))
        with sqlite3.connect(com_vars.DB_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO CLIENTS (CLIENT_NAME) VALUES ('%s')" %(client_name))
            cursor.execute("INSERT INTO BALANCES VALUES (%s, %s)" %(cursor.lastrowid, com_vars.DEFAULT_BALANCE))
            connection.commit()
        return cursor.lastrowid

client = DBClients()
print client.get_client_balance(11)

with sqlite3.connect(com_vars.TEST_DB_PATH) as conn:
    #cursor = connection.cursor()
    #cursor.execute("select * from CLIENTS;")
    #results = cursor.fetchall()
    dirs = dir(conn)

