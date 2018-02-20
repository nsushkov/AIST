# -*- coding: utf-8 -*-
*** Settings ***
Documentation        common variables for tests

*** Variables ***
${DB_NAME}           ../app/web/clients.db
${NAME_LEN}          6
${DEFAULT_BALANCE}   5
${BASE_API_URL}      http://localhost:5000/

${COMMON}           {
...                    'DB_NAME': "../app/web/clients.db",
...                    'NAME_LEN': 6,
...                    'DEFAULT_BALANCE': 5,
...                    'BASE_API_URL': "http://localhost:5000/"
...                  }