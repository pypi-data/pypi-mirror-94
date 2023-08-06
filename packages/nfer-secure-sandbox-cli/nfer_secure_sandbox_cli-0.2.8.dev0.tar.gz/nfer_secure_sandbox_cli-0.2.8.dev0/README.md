# Nfer-Secure-Sandbox-Cli

[![Nference](https://nference.ai/static/logo-black.svg)](https://nference.ai/)

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

Nfer-Secure-Sandbox-Cli is utility to interact with Confidential Computing enabled Secure Sandboxes powered by Nference.
  - "configure" with your credentials.
  - "setup" a project adhering to a data/algo pipeline, honoring a policy.
  - "run" the pipeline, encompassing data-projection, algorithm development, and execution on a desired, secure sandbox.  

# New Features!

  - State maintenance: checkpointing on chronology of tasks in execution.
  - Templatised Sandboxes: choose the VM to be provisioned.


You can also:
  - Import code as GitHub Repositories.
  - Manage Sandbox Lifecycles with intents to create/start/stop/delete.

### Tech

Nfer-Secure-Sandbox-Cli has following simple usage milestones:

* [configure]() - Add your credentials, saves on FileSystem.
* [setup]() - gets a project directory created, with User inputs sought and converted into a `main.yml` file.
* [run]() - Execution of tasks in `main.yml` generated above.

These steps are explained finely later.

### Installation

Nfer-Secure-Sandbox-Cli requires [Docker](https://docs.docker.com/engine/install/) 19.03.6, [Docker-Compose](https://docs.docker.com/compose/install/) v1.17.1 and [Node.js](https://nodejs.org/) v15.5+, [NPM](https://www.npmjs.com/) v7.3+ to run.

Nfer-Secure-Sandbox-Cli is only compatible Python3.4+.

```sh
$ pip3 install nfer-secure-sandbox-cli
```

### Credentials Configuration

### Project Setup

```shell script
nfer-sandbox-cli setup
```

A tab pointing at 0.0.0.0:3000 opens in the client’s browser, which is basically taking the client, to a UI seeking inputs about the pipeline being set, e.g code repo, docker image details, platform/pipeline template id, etc. 

The UI form, when filled, makes a call to a mini “setup server” which is a local flask app, at 5112, and this server handler, plays with the filesystem in `pwd`, creating :

- a “main.yml” file as a “plan”, or “chronology” of tasks to be executed.
- a bunch of needed folders : “build”, “output”, “certs”, “app”, “policy”, “artefacts” etc. 
- recordkeeping / state of the pipeline/execution maintenance files like “.pbstate”, “.register”. 

### Pipeline Execution

```shell script
nfer-sandbox-cli run
```

The “Run” action, that under-the-hood runs the “main.yml” generated during the “Setup” phase, comprises of following activities:

* [Code Retrieval]() : Retrieves the codebase (i.e app code and deps file), from integrated sources e.g Git Repository into “./app” folder, the specified repository is cloned.

* [Certificate Generation]() : generate self-signed certificates inside “./certs” folder of project structure dir on the client. Certificate name and pubkey are uploaded to the nference middleware (db and filesystem), maintained as a mapping between the client and certificate - for re-usability of the certificates.

* [Sandbox Provisioning]() : Seek intent via nfer-sandbox-cli from Client on one’s system, received at Nference Middleware that either further using IaaC Templates provisions, maintains, maps the Sandbox VMs, OR delegates the work to Controller API. End product is Machine Key retrieved, sent back to Client.

* [Dockerization, Encryption, Upload Image]() : Dockerizing the Client’s Algorithm - as a local image first, further encrypting layers combined and compressed as a .tar file. The .tar file is further uploaded onto Docker Registry Middleware, from where, it then using the Sensec ability, gets persisted into Docker Registry.

* [Data Projection]() : Seeking (internal-to-nference) data projection ID as input, this task encrypts the data against it. This data is further pulled into the Sandbox VM during Pipeline execution. 

* [Output Encryption Bundle]() : Take a measurement of the output folder - “encrypt-output”, “decrypt-input” and “decrypt-output” spaces. These all get along with an “output key”. Which is further encrypted.

* [Prepare and Submit Policy]() : Create a policy document, inside “./policy” folder. This policy document, later becomes the REQUEST PAYLOAD while “CREATING” a pipeline against a Name and Template ID. 

* [Execute Policy]() : Begin Execution of the Submitted Pipeline (recognized as pipeline ID). The Pipeline metadata contains know-hows of the sandbox/platform, which is started and the docker image, dataset and measurements to be tallied and decryption keys to be used are known using Machine’s Private Key.  

* [Output Generation, Retrieval and Decryption]() : After the pipeline execution is successful, the output generated, needs to be brought to Nference environment, either “CDAP” or Azure/OVH’s GCP Bucket. From there, it has to be retrieved by the client, where it is decrypted too.




License
----

MIT


**Nference Proprietary**

[//]: # 

   [Twitter Bootstrap]: <http://twitter.github.com/bootstrap/>
   [jQuery]: <http://jquery.com>


