# -*- coding: utf-8 -*-

*** Settings ***
Resource          ./test/variables/common.robot
Library           JsonValidator
Library           Collections
Library           test/libraries/APIClients.py      ${BASE_API_URL}
Library           test/libraries/DBClients.py       ${DB_NAME}

Documentation    Check correctness of balance changing when service is being activated

*** Test Cases ***
Check Balance Service Activate
    ${client_id}=    DBClients.Get Suitable Client

    Set Test Variable    ${client_id}    ${client_id}

    ${start_balance}=    DBClients.Get Client Balance    ${client_id}

    Set Suite Variable    ${start_balance}    ${start_balance}

    ${avail_serv_list}=    APIClients.Get Available Services    client_id=${client_id}

    ${serv_id_list}=    JsonValidator.GetElements    ${avail_serv_list}    $.items[*].id

    Run Keyword If    ${serv_id_list}==${None}    Fail    Client ${client_id} has no avaible services
    ${service_id}=    Evaluate      random.choice(${serv_id_list})    random
    Set Test Variable    ${service_id}    ${service_id}

    ${serv_cost}=    JsonValidator.GetElements    ${avail_serv_list}    $.items[?(@.id==${service_id})].cost
    Set Test Variable    ${serv_cost}    ${serv_cost[0]}

    Log    Activating service: ${service_id}
    ${add}=    APIClients.Add Service    client_id=${client_id}    service_id=${service_id}

    Should Be Equal As Integers    ${add.status_code}    ${SUCCESS_CODE}    msg=Unable to activate service!

    :FOR    ${attempt}    IN RANGE    1     6
    \    ${activated}=    APIClients.Check Service Activated    client_id=${client_id}    service_id=${service_id}
    \    Exit For Loop If    ${activated}
    \    Sleep    10S
    Run Keyword If    ${activated}==${False}    Fail    msg=Service: ${service_id} was not activated for client ${client_id}

   ${expected_balance}=    Evaluate    ${start_balance}-${serv_cost}

   ${finish_balance}=    DBClients.Get Client Balance    ${client_id}

   Should Be Equal    ${expected_balance}    ${finish_balance}    msg=Balance is not correct after service was activated!

*** Keywords ***