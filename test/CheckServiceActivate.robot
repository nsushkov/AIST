*** Settings ***
Library           random
Library           DatabaseLibrary
Library           OperatingSystem
Library           JsonValidator
Library           Collections
Library           String
Library           ./libraries/APIClients.py
Library           ./libraries/DBClients.py


Documentation    Suite description

*** Variables ***
# ${client_id}      3

*** Test Cases ***
Get Cli
    ${client_id}=    DBClients.Get Suitable Client
    Log    ${client_id}
    Set Suite Variable    ${client_id}    ${client_id}
    Log     ${client_id}
    Run Keyword If    ${client_id}==${None}    ${client_id}=    DBClients.Add Rand Client

    ${start_balance}=    DBClients.Get Client Balance    ${client_id}
    Log    ${start_balance}
    Set Suite Variable    ${start_balance}    ${start_balance}

Get Client Services
    ${client_serv_list}=    APIClients.Get Client Services    client_id=${client_id}
    @{client_serv_list}=    JsonValidator.Get Elements    ${client_serv_list}    $.items[*].id
    Log    cli-${client_id}
    Log List    ${client_serv_list}

    ${all_serv_list}=    APIClients.Get Services
    @{all_serv_list}=    JsonValidator.Get Elements    ${all_serv_list}    $.items[*].id
    Log     serv
    Log List    ${all_serv_list}
    #Run Keyword If    ${all_serv_list}==[]
    #:FOR    ${elem}    IN    @{client_serv_list}
    #\    Collections.Remove Values From List    ${all_serv_list}    ${elem}
    #Log List    ${all_serv_list}

    #${lll}=    Create List    1    4    2    5    3
    #${one}=    Evaluate    random.choice(${lll})    random
    #Log    ${one}

    ${avail_serv_list}=    Get Available Services    client_id=${client_id}
    Log    ${avail_serv_list[0]}
    ${serv_id_list}=    JsonValidator.GetElements    ${avail_serv_list}    $.items[*].id
    Log    ${serv_id_list}
    Run Keyword If    ${serv_id_list}==${None}    Fail    Client ${client_id} has no avaible services
    ${service_id}=    Evaluate      random.choice(${serv_id_list})    random
    Log    ${service_id}
    Set Test Variable    ${service_id}    ${service_id}
    Log    Activating service: ${service_id}
    ${serv_cost}=    JsonValidator.GetElements    ${avail_serv_list}    $.items[?(@.id==${service_id})].cost
    Set Test Variable    ${serv_cost}    ${serv_cost[0]}
    Log    ${serv_cost}

    ${add}=    APIClients.Add Service    client_id=${client_id}    service_id=${service_id}
    Log     ${add}    # Добавить проверку
    #Should Be Equal    ${add.status_code}    202


    :FOR    ${attempt}    IN RANGE    1     6
    #\    ${list}=    Get Client Services    client_id=${client_id}
    #\    ${list}=    JsonValidator.GetElements    ${list}    $.items[*].id
    \    ${activated}=    APIClients.Check Service Activated    client_id=${client_id}    service_id=${service_id}
    \    Log    ${client_id}
    \    Log    ${service_id}
    \    Log    ${activated}
    \    Exit For Loop If    ${activated}
    \    Sleep    10S
    Run Keyword If    ${activated}==${False}    Fail    Service: ${service_id} was not activated for client ${client_id}

    Log    ${activated}


   ${expected_balance}=    Evaluate    ${start_balance}-${serv_cost}
   Log    exp${expected_balance}
   ${finish_balance}=    DBClients.Get Client Balance    ${client_id}
   Log    fin${finish_balance}
   Should Be Equal    ${expected_balance}    ${finish_balance}






*** Keywords ***