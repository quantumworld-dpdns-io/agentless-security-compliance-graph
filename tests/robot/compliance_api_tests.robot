*** Settings ***
Library           RequestsLibrary
Library           Collections
Suite Setup       Create Session    api    http://localhost:8000

*** Variables ***
${API_URL}        http://localhost:8000

*** Test Cases ***
Health Check Endpoint
    ${resp}=    GET    ${API_URL}/health
    Status Should Be    200
    ${json}=    Set Variable    ${resp.json()}
    Should Be Equal    ${json}[status]    ok

Create Device Node
    ${resp}=    POST    ${API_URL}/api/v1/nodes
    ...    json={"node_type":"device","name":"robot-test-device","attributes":{"ip":"10.0.0.99"}}
    Status Should Be    200
    ${json}=    Set Variable    ${resp.json()}
    Should Be Equal    ${json}[status]    created

Create CVE Node
    ${resp}=    POST    ${API_URL}/api/v1/nodes
    ...    json={"node_type":"cve","name":"CVE-2024-ROBOT","attributes":{"cvss_score":9.1,"severity":"CRITICAL"}}
    Status Should Be    200

Get Graph Summary
    ${resp}=    GET    ${API_URL}/api/v1/graph/summary
    Status Should Be    200
    ${json}=    Set Variable    ${resp.json()}
    Should Be True    ${json}[total_nodes] >= 0

Traverse From Node
    ${resp}=    POST    ${API_URL}/api/v1/nodes
    ...    json={"node_type":"device","name":"traversal-root"}
    ${node_id}=    Set Variable    ${resp.json()}[id]
    ${resp}=    GET    ${API_URL}/api/v1/traverse/${node_id}
    Status Should Be    200

Create Edge Between Nodes
    ${resp1}=    POST    ${API_URL}/api/v1/nodes
    ...    json={"node_type":"device","name":"edge-source"}
    ${src}=    Set Variable    ${resp1.json()}[id]
    ${resp2}=    POST    ${API_URL}/api/v1/nodes
    ...    json={"node_type":"device","name":"edge-target"}
    ${tgt}=    Set Variable    ${resp2.json()}[id]
    ${resp}=    POST    ${API_URL}/api/v1/edges
    ...    json={"source_id":${src},"target_id":${tgt},"edge_type":"CONNECTS","weight":1.0}
    Status Should Be    200
    Should Be Equal    ${resp.json()}[status]    created

Shortest Path Query
    ${resp1}=    POST    ${API_URL}/api/v1/nodes
    ...    json={"node_type":"device","name":"path-start"}
    ${s}=    Set Variable    ${resp1.json()}[id]
    ${resp2}=    POST    ${API_URL}/api/v1/nodes
    ...    json={"node_type":"device","name":"path-end"}
    ${e}=    Set Variable    ${resp2.json()}[id]
    POST    ${API_URL}/api/v1/edges
    ...    json={"source_id":${s},"target_id":${e},"edge_type":"CONNECTS"}
    ${resp}=    GET    ${API_URL}/api/v1/shortest-path?from_id=${s}&to_id=${e}
    Status Should Be    200
