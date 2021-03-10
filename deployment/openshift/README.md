# formsflow.ai

This page describes the setup of Forms Flow AI on Red Hat Openshift.


## Table of Contents
* [Prerequisites](#prerequisites)
* [Solution Setup](#solution-setup)
  * [Step 1 : Keycloak Setup](#keycloak-setup)
  * [Step 2 : Installation](#installation)
  * [Step 3 : Running the Application](#running-the-application)
  * [Step 4 : Health Check](#health-check) 


## Prerequisites

The system is deployed on Red Hat Openshift and will need Openshift client tools intalled on local machine. 

## Solution Setup

### Keycloak Setup

Follow the instructions given on [link](../../forms-flow-idm/keycloak-setup.md)

      
### Installation

   * Download the build and deployment templates from the current folder on the local machine. 
   * On command line, navigate to the folder where the templates were downloaded from the previous step. 
   * Follow the below order for deploying the components
     * Mongo DB and Postgresql. In case of HA, please deploy patroni instances using the build/deployment configs from [here](../../deployment/openshift/patroni)
     * Forms Flow BPM
     * Forms Flow API
     * Forms Flow Forms
     * Forms Flow Web
     * Forms Flow Analytics
   * Configure the build on Openshift using the below command. Set the values of the parameters in the build config based on the repository and branch being used. 
     oc process -f template_bc.yaml | oc create -f -
     Verify if the build is successful for each of the components on Openshift. 
   * Deploy each of the components using the below command. Set the values of the parameters in the parameter file and the deployment config based on the environment. 
     oc process -f template_dc.yaml --param-file=template_params.yaml | oc create -f -
   * Import the predefined Roles and Forms using [sample.json](../../forms-flow-forms/sample.json) using instructions from [Import the predefined Roles and Forms](../../forms-flow-forms/README.md#import-of-predefined-roles-and-forms)
   * Modify the configuration values as needed. Details below. 
 
**formsflow.ai Role Mapping:**

 Variable name | Meaning | Possible values | Default value |
--- | --- | --- | ---
`CLIENT_ROLE`|	The role name used for client users|| formsflow-client
`CLIENT_ROLE_ID`|form.io client role Id|eg. 10121d8f7fadb18402a4c|must get the value from form.io resource **http://localhost:3001/role**
`REVIEWER_ROLE`|The role name used for staff/reviewer users||`formsflow-reviewer`
`REVIEWER_ROLE_ID`|form.io reviewer role Id|eg. 5ee10121d8f7fa03b3402a4d|must get the value from form.io resource **http://localhost:3001/role**
`DESIGNER_ROLE`|The role name used for designer users||`formsflow-designer`
`DESIGNER_ROLE_ID`|form.io administrator role Id|eg. 5ee090afee045f1597609cae|must get the value from form.io resource **http://localhost:3001/role**
`ANONYMOUS_ID`|form.io anonymous role Id|eg. 5ee090b0ee045f28ad609cb0|must get the value from form.io resource **http://localhost:3001/role** 
`USER_RESOURCE_ID`|User forms form-Id|eg. 5ee090b0ee045f51c5609cb1|must get the value from form.io resource **http://localhost:3001/user**

**formsflow.ai Datastore Settings:**

Variable name | Meaning | Possible values | Default value |
--- | --- | --- | ---
`WEB_API_DATABASE_URL`|JDBC DB Connection URL for formsflow.ai||`postgresql://postgres:changeme@forms-flow-webapi-db:5432/formsflow`
`WEB_API_POSTGRES_USER`|formsflow.ai database postgres user|Used on installation to create the database.Choose your own|`postgres`
`WEB_API_POSTGRES_PASSWORD`|formsflow.ai database postgres password|ditto|`changeme`
`WEB_API_POSTGRES_DB`|formsflow.ai database name||`formsflow`

**formsflow.ai Integration Settings:**

Variable name | Meaning | Possible values | Default value |
--- | --- | --- | ---
`NODE_ENV`| Define project level configuration | `development, test, production` | `development`
`CAMUNDA_API_URI`|Camunda Rest API URI||`http://localhost:8000/camunda`
`FORMIO_DEFAULT_PROJECT_URL`|The URL of the form.io server||`http://localhost:3001`
`WEB_API_BASE_URL`|formsflow.ai Rest API URI||`http://localhost:5000`
`MONGODB_URI`|Mongo DB Connection URL of formio for sentiment analysis||`mongodb://username:password@host:port/analytics?authSource=admin&authMechanism=SCRAM-SHA-256`

**Authentication Provider (Keycloak) Settings:**

Variable name | Meaning | Possible values | Default value |
--- | --- | --- | ---
`KEYCLOAK_TOKEN_URL`|Keycloak OIDC token API for clients|Plug in your Keycloak base url and realm name|`{Keycloak URL}/auth/realms/<realm>/protocol/openid-connect/token`
`KEYCLOAK_JWT_OIDC_CONFIG`|Path to Keycloak well-know config for realm|Plug in your Keycloak URL plus realm|`{Keycloak URL}/auth/realms/<REALM>/.well-known/openid-configuration`
`KEYCLOAK_JWT_OIDC_JWKS_URI`|Keycloak JWKS URI|Plug in Keycloak base url plus realm|`{Keycloak URL}/auth/realms/<REALM>/protocol/openid-connect/certs`
`KEYCLOAK_JWT_OIDC_ISSUER`|The issuer of JWT's from Keycloak for your realm|Plug in your realm and Keycloak base url|`{Keycloak URL}/auth/realms/forms-flow-ai`
`KEYCLOAK_BPM_CLIENTID`|Client ID for Camunda to register with Keycloak|eg. forms-flow-bpm|must be set to your Keycloak client id
`KEYCLOAK_BPM_CLIENTSECRET`|Client Secret of Camunda client in realm|eg. 22ce6557-6b86-4cf4-ac3b-42338c7b1ac12|must be set to your Keycloak client secret
`KEYCLOAK_WEB_CLIENTID`|Client ID for formsflow.ai to register with Keycloak|eg. forms-flow-web|must be set to your Keycloak client id

**BPM (Camunda) Datastore Settings:**

Variable name | Meaning | Possible values | Default value |
--- | --- | --- | ---
`CAMUNDA_JDBC_URL`|Postgres JDBC DB Connection URL|Used on installation to create the database.Choose your own|`jdbc:postgresql://forms-flow-bpm-db:5432/postgres`
`CAMUNDA_JDBC_DRIVER`|Postgres JDBC Database Driver||`org.postgresql.Driver`
`CAMUNDA_POSTGRES_USER`|Postgres Database Username|Used on installation to create the database.Choose your own|`postgres`
`CAMUNDA_POSTGRES_PASSWORD`|Postgres Database Password|Used on installation to create the database.Choose your own|`changeme`
`CAMUNDA_POSTGRES_DB`|Postgres Database Name|Used on installation to create the database.Choose your own|`camunda`


**Analytics (Redash) Integration Settings:**
 
 Variable name | Meaning | Possible values | Default value |
--- | --- | --- | ---
`INSIGHT_API_BASE`|Insight Api base end-point||`http://localhost:7000`
`INSIGHT_API_KEY`|API_KEY from REDASH|eg. G6ozrFn15l5YJkpHcMZaKOlAhYZxFPhJl5Xr7vQw| must be set to your ReDash API key
   
   **Additionally, you may want to change these**
   * The value of database details (especially if this instance is not just for testing purposes)
  
  
### Health Check
  * Analytics should be up and available for use at port defaulted to 7000 i.e. http://localhost:7000/
  * Business Process Engine should be up and available for use at port defaulted to 8000 i.e. http://localhost:8000/camunda/
  * FormIO should be up and available for use at port defaulted to 3001 i.e. http://localhost:3001/
  * formsflow.ai Rest API should be up and available for use at port defaulted to 5000 i.e. http://localhost:5000/api/
  * formsflow.ai web application should be up and available for use at port defaulted to 3000 i.e. http://localhost:3000/
  