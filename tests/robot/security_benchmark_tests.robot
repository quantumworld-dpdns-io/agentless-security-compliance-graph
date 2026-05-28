*** Settings ***
Library           RequestsLibrary
Library           OperatingSystem
Library           Collections
Suite Setup       Create Session    api    http://localhost:8000

*** Variables ***
${API_BASE}       http://localhost:8000

*** Test Cases ***
Large Payload Rejection
    ${large_payload}=    Evaluate    {"node_type": "device", "name": "x" * 1000000, "attributes": {}}
    ${resp}=    POST    ${API_BASE}/api/v1/nodes    json=${large_payload}
    Should Be Equal As Integers    ${resp.status_code}    413    400

Rate Limiting Simulation
    FOR    ${i}    IN RANGE    100
        ${resp}=    GET    ${API_BASE}/health
        Exit For Loop If    ${resp.status_code} == 429
    END
    Log    Completed rate limit simulation

Content Type Validation
    ${resp}=    POST    ${API_BASE}/api/v1/nodes
    ...    data=not-json
    ...    headers={"Content-Type": "text/plain"}
    Should Be Equal As Integers    ${resp.status_code}    415    400

Method Not Allowed
    ${resp}=    DELETE    ${API_BASE}/api/v1/graph/summary
    Should Be Equal As Integers    ${resp.status_code}    405

Missing Content Type
    ${resp}=    POST    ${API_BASE}/api/v1/nodes
    ...    data={"node_type":"test","name":"test"}
    Should Be Equal As Integers    ${resp.status_code}    415    400
