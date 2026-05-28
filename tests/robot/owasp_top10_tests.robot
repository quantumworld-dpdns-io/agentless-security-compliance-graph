*** Settings ***
Library           RequestsLibrary
Library           JSONLibrary
Library           Collections
Suite Setup       Create Session    api    http://localhost:8000

*** Variables ***
${API_BASE}       http://localhost:8000
${ADMIN_USER}     admin
${ADMIN_PASS}     admin_secret

*** Test Cases ***
A01 Broken Object Level Authorization
    [Tags]    OWASP-A01    SECURITY
    ${resp}=    GET    ${API_BASE}/api/v1/nodes/unknown-node-id
    Should Be Equal As Integers    ${resp.status_code}    403    401

A02 Broken Authentication
    [Tags]    OWASP-A02    SECURITY
    ${headers}=    Create Dictionary    Authorization=Bearer invalid_token
    ${resp}=    GET    ${API_BASE}/api/v1/graph/summary    headers=${headers}
    Should Be Equal As Integers    ${resp.status_code}    401    403

A03 SQL Injection
    [Tags]    OWASP-A03    SECURITY
    ${resp}=    GET    ${API_BASE}/api/v1/traverse/test-id; DROP TABLE nodes--
    Should Be Equal As Integers    ${resp.status_code}    400    422
    ${resp}=    GET    ${API_BASE}/api/v1/traverse/test-id' OR '1'='1
    Should Be Equal As Integers    ${resp.status_code}    400    422

A04 Insecure Design
    [Tags]    OWASP-A04    SECURITY
    ${resp}=    POST    ${API_BASE}/api/v1/nodes    json={"node_type":"","name":"","attributes":{}}
    Should Be Equal As Integers    ${resp.status_code}    422

A05 Security Misconfiguration
    [Tags]    OWASP-A05    SECURITY
    ${resp}=    OPTIONS    ${API_BASE}/api/v1/nodes
    Should Be Equal As Integers    ${resp.status_code}    405    400
    ${headers}=    GET    ${API_BASE}/health
    Dictionary Should Contain Key    ${headers.headers}    Content-Type

A06 Sensitive Data Exposure
    [Tags]    OWASP-A06    SECURITY
    ${resp}=    GET    ${API_BASE}/api/v1/graph/summary
    Should Be Equal As Integers    ${resp.status_code}    200
    ${body}=    To Json    ${resp.content}
    Should Not Contain    ${resp.text}    password
    Should Not Contain    ${resp.text}    secret
    Should Not Contain    ${resp.text}    token

A08 SSRF
    [Tags]    OWASP-A08    SECURITY
    ${resp}=    GET    ${API_BASE}/api/v1/traverse/test?url=http://169.254.169.254/latest/meta-data/
    Should Be Equal As Integers    ${resp.status_code}    400    422

A09 Security Logging & Monitoring
    [Tags]    OWASP-A09    SECURITY
    ${log_resp}=    GET    ${API_BASE}/health
    Should Be Equal As Integers    ${log_resp.status_code}    200
    Should Not Be Empty    ${log_resp.headers}

A10 SSRF (Server Side Request Forgery)
    [Tags]    OWASP-A10    SECURITY
    ${resp}=    GET    ${API_BASE}/api/v1/nodes?url=http://internal-admin-panel/
    Should Be Equal As Integers    ${resp.status_code}    400    422
