# Cx-Flow Demo/Development Instance

This repository will allow you to create a demonstration system with the following properties:

* Has a running instance of Jira where vulnerability issues will be created
* Hosts a cx-flow instance that can receive webhook notifications
* Easy setup for multiple different instance configurations

# Prerequisites
* You must have Docker Desktop installed
* Docker will need access to write to your local disk
* The Docker memory setting should be bumped to 8GB rather than the default 2GB to make the demo system more performant
* The cx-flow webhook endpoint must be available via a public Internet URL to receive webhook calls
    * It is possible to use a tool such as [ngrok](https://ngrok.com/) to allow cx-flow to receive webhook calls
* The current configuration is designed to work with GitHub webhooks, but it is possible to customize it to consume webhook data from other SCM providers

# Webhook Setup Instructions


## Step 1: Configure your environment

In the `cxflow-docker` directory there is a file `application-general.yml` that can be modified to provide cx-flow settings.  It is also possible to make one or more copies of `application-general.yml` in the cxflow-docker directory for multiple configurations.  The naming convention for configuration files is `application-{config name}.yml`.

For example, if it was neccessary to make a configuration named "mypoc", a copy of `application-general.yml` can be made with the name `application-mypoc.yml`.  The configuration option `mypoc` can be provided as an argument to one of the execution powershell scripts (described later in this document).

In the `application-general.yml` file, there are several configuration fields with `# TODO:` comments that must be configured prior to executing cx-flow. For a simple demonstration environment, the other configuration options can be left unmodified.

## Step 2: Run the Cx-Flow and Jira Server Containers

The powershell script `run_cxflow+jira_server.ps1` will start a Docker instance of Jira and a cx-flow webhook server.  The Jira data is persisted to a local disk so that the Jira contents survives across restarts.  Note that the Jira evaluation license is only for 30 days.  If the license expires, all that is required is to delete the local Jira data and restart the containers.

`run_cxflow+jira_server.ps1` has a few options:

Option | Default | Description
--- | --- | ---
StorageLoc | ./jira-data | The folder where Jira data will be stored.  By default, it creates the folder `jira-data` in the working directory.  An absolute or relative path can be provided to store the data in an alternate location.
Config | general | The configuration option used to locate the `application-{config name}.yml` file for cx-flow startup.  Using `-Config mypoc` would cause cx-flow to start with the configuration file `application-mypoc.yml`.
Dbg | false | Including `-Dbg` starts cx-flow with a debugger available for connecting via port 1040.

The Jira and cx-flow servers will execute and display log output in your powershell window.  Press CTRL-C at any time to shut down the containers.  It is possible to tail logs of each individual container.  See the [docker logs](https://docs.docker.com/engine/reference/commandline/logs/) and [docker ps](https://docs.docker.com/engine/reference/commandline/ps/) command documentation for more details.


## Step 3: Configure Jira

By default, Jira will answer at the URL [http://localhost:8000](http://localhost:8000).  Jira will give options for setup which includes configuring a license.  The Jira configuration will allow you to navigate to the Atlassian site and generate a Jira evaluation license that will then be imported into your Jira instance.

When Jira has finished initializing, create an initial scrum software project with the name you provided in `application-{config name}.yml` under the `jira.project` configuration setting.  The `application-general.yml` configuration options have been configured to work with the default Jira project settings.  Configuring more advanced options is possible by customizing `application-{config name}.yml`, but this subject is beyond the scope of this document.

## Step 4: Configure the Webhook

### Testing Cx-Flow Configuration

By default, the cx-flow webhook server answers at [http://localhost:8585](http://localhost:8585).  By default all [Spring Boot Actuators](https://www.baeldung.com/spring-boot-actuators) have been enabled.  The use of the actuators is beyond the scope of this document, but some common actuators can be used to check that cx-flow is working:

Actuator Name | URL
--- | ---
Health | [http://localhost:8585/actuator/health](http://localhost:8585/actuator/health)
Info | [http://localhost:8585/actuator/info](http://localhost:8585/actuator/info)
ConfigProps | [http://localhost:8585/actuator/configprops](http://localhost:8585/actuator/configprops)


If the actuators don't respond or respond with errors, chances are that cx-flow is not configured correctly.

### Exposing Cx-Flow via a Public URL

For webhooks to be received, the cx-flow URL must be reachable from the public Internet.  For demonstration purposes, it is often possible to use a tool like `ngrok` as a reverse proxy with a publicly accessible url.  Execute `ngrok` with the following command line to obtain the webhook URL:

`.\ngrok.exe http 8585`

The URL given by ngrok can be used as the webhook endpoint when configuring the webhook with the SCM provider.

### Configuring a GitHub Webhook

1. Navigate to the GitHub code repository used for the demonstration.
2. Navigate to Setting->Webhooks.
3. Set the "Payload URL" to the ngrok URL or the publicly accessible URL for cx-flow.
4. Set the "Content Type" to `application/json`.
5. Set the "Secret" to the value supplied for `github.webhook-token` in `application-{config name}.yml`.
6. The events that trigger the webhook can be set to "Just push the event" or tuned for more specific events as needed.

## Step 5: Demonstrate

If everything has been configured correctly, pushing a change to the repository should deliver a webhook call to the cx-flow endpoint.  A scan should be invoked in the CxSAST server, and the results will be published as issues in Jira.

