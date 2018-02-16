*** Settings ***

Library           DatabaseLibrary
Library           OperatingSystem
Library           JsonValidator
Library           Collections
Library           String
Library           ./libraries/APIClients.py
Library           ./libraries/DBClients.py


Documentation    Suite description

*** Variables ***
${client_id}      1

*** Test Cases ***
Get Cli
    ${client_id}=    DBClients.Get Suitable Client
    Log    ${client_id}
    Set Suite Variable    ${client_id}    ${client_id}
    Run Keyword If    ${client_id}==${None}    ${client_id}=    DBClients.Add Rand Client
    ${start_balance}=    DBClients.Get Client Balance    ${client_id}
    Log    ${start_balance}
    Set Suite Variable    ${start_balance}    ${start_balance}

Get Client Services
    ${client_serv_list}=    APIClients.Get Client Services    client_id=${client_id}
    @{client_serv_list}=    JsonValidator.Get Elements    ${client_serv_list}    $.items[*]
    Log List    cl@{client_serv_list}

    ${all_serv_list}=    APIClients.Get Services
    @{all_serv_list}=    JsonValidator.Get Elements    ${all_serv_list}    $.items[*]
    Log List    all@{all_serv_list}
    #Run Keyword If    ${all_serv_list}==[]
    ${avail_serv_list}=    Collections.Remove Values From List    ${all_serv_list}    @{client_serv_list}
    Log List    ${avail_serv_list}



    #${add}=    APIClients.Add Service    client_id=${client_d}    service_id=5
    #Should Be Equal    ${add.status_code}    202





*** Keywords ***