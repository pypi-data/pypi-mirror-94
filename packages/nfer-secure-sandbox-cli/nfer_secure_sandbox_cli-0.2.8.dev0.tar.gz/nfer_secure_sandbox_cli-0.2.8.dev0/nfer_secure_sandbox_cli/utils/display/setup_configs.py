msg_intro = """

\033[96mThe Command \033[1m`nfer-sandbox-cli setup`\033[0m \033[96menables one to 'create' a \033[4mtemplate structure\033[0m \033[96mfor a new project,
and set it up seeking inputs from the developer. 

This will next, take you through a series of inputs and set up tasks like maintaining
algo code/dependencies, provisioning sandbox, launching a pipeline etc. all end to end.\033[0m

"""

msg_success = """

The project `%s` has been setup. cd into this project dir as :
`cd `%s/%s`
and "run" the project, end-to-end as:
`nfer-sandbox-cli run`
to see the pipeline execute.
"""

setup_project_1st = """

As a first step, \033[93m\033[1mplease enter a project name\033[0m. We create a folder by that name,
and set it up with your inputs:

"""

ack_project_1st = "\nThe dir \033[1m`%s`\033[0m created in path `%s`\n"

fetch_code_deps = """

Seeking a couple of inputs to fetch the code and dependencies from. \033[1mWe only support `git`
currently.\033[0m Inputs being sought are : 
`\033[4mdesc\033[0m`, `\033[4mmode\033[0m`, `\033[4mgit-url\033[0m`, `\033[4mcode_folder\033[0m`, `\033[4mmain_file\033[0m`, `\033[4mdeps_folder\033[0m`, `\033[4mdeps_file\033[0m`, `\033[4mstack\033[0m`
and `\033[4mcredentials\033[0m`. 

"""

ack_code_deps = "The source code retrieval configs to be found under `%s/algo` after `nfer-sandbox-cli run`"

get_cert_mode_input = """

\033[93m\033[1mNext\033[0m, \033[93mlet us just seek a certificate - it could be a \033[1mself-signed certificate\033[0m, OR \033[93m\033[1mone from a CA.\033[0m
\033[1mCurrently, only self-signed certificates are supported.\033[0m And those are not reusable for other projects.
\033[93mPlease enter the MODE for certificates retrieval\033[0m i.e \033[1m`from-CA`\033[0m, or \033[1m`self-signed`\033[0m, i.e
\033[96m- choose "1" for self-signed certificates.\033[0m
\033[96m- choose "2" for from-CA certificates.\033[0m
\033[1m"1" i.e "self-signed"\033[0m certificates BY DEFAULT:

"""

get_cert_action_input = """

\033[93mPlease enter the \033[1mACTION\033[0m \033[93mfor certificate creation i.e `create` or `fetch`\033[0m, i.e
- \033[96mchoose "1" for creating the self-signed certificate\033[0m
- \033[96mchoose "2" for fetching the self-signed certificate or a CA issued certificate\033[0m

"""

ack_cert_conf = """

\033[92mThe certificates have been fetched/created.\033[0m Inside path : \033[1m`%s`\033[0m. Files: 
- \033[4m`%s`-privkey.pem\033[0m
- \033[4m`%s`-pubkey.pem\033[0m

"""
br = "\n\n******************************************************************\n\n"

inputs_ack_lvl1 = """

\033[92mThe initial inputs w.r.t \033[1mCodebase, Certificates\033[0m, are complete\033[0m.
Next, we move on to \033[1mprovision / fetch a Sandbox VM\033[0m, that the algo feeding on a dataset shall be run upon.
\033[96mThe Public Key of the Sandbox above\033[0m, is critical for data projection / algorithm policies. \033[94mrefer \033[4mREADME.md\033[0m

Thereafter, we will specify a \033[4mdata projection\033[0m, which the algorithm will feed upon. 

\033[96mAll this is then encrypted, packaged, and run on the Sandbox VM.\033[0m  

"""

get_sandbox_input = """

\033[93mPlease select from the templates for creating a platform\033[0m. As of now, there shall always be, 
"a new sandbox" created. \033[4mSandboxes are created as per a template\033[0m. \033[93mYou may choose one amongst following\033[0m:
`%s`

"""

certs_path_for_platform_input = """

\033[96mSince the provisioning of platform has to be certified / attested\033[0m,
\033[93mPlease also enter the path of the certificates below\033[0m. You may either:
\033[94ma.) choose "1" for the default path i.e `certs/`\033[0m
\033[94mb.) enter a different certificate path e.g /<absolute>/<path>/<to>/<certificates>/\033[0m

"""

certs_name_for_platform_input = """

Likewise, \033[93mplease also enter the name of the certificates\033[0m, under the path above:
\033[96mShould you choose option a. i.e "1" above\033[0m, the default `%s` cert name with files:
\033[94m- `%s-privkey.pem`\033[0m
\033[94m- `%s-pubkey.pem`\033[0m

shall be picked up.

"""

inputs_ack_lvl2 = """

\033[92mThe Next set of inputs w.r.t Platform a.k.a Sandbox, are complete.\033[0m
Next, \033[94mwe move defining the dockerization of the algorithm+dependencies.\033[0m

Thereafter, we will specify a \033[4mdata projection\033[0m, which the algorithm will feed upon. 

\033[94mAll this is then encrypted, packaged, and run on the Sandbox VM provisioned above.  \033[0m

"""

docker_details_input = """

\033[92mThe algo code in the path \033[1m`algo/%s`\033[0m shall be dockerized, and persisted on the registry: \033[1m`%s`\033[0m. 
\033[93mPlease specify the name of the algorithm image, the tag associated, and the docker repo\033[0m, below:

"""

docker_details_ack = """

\033[96mThe docker container shall be created on \033[1m`nfer-sandbox-cli run`. \033[0m
\033[96mAnd be persisted on the docker registry i.e \033[4m`%s`\033[0m, With the following details:

\033[94m- docker repo : %s\033[0m
\033[94m- image name : %s\033[0m
\033[94m- image tag : %s\033[0m

"""

inputs_ack_lvl3 = """

\033[92mThe Next set of inputs w.r.t Dockerization of the Algorithm, are complete.\033[0m
Next, we move ahead to specify a \033[4mdata projection\033[0m, which the algorithm will feed upon. 

\033[96mThereafter, we will seek attributes for the entire packaged Policy comprising the Algo, the Dataset, and VM.\033[0m

All this is then encrypted, packaged as this Policy, and run on the Sandbox VM provisioned above.  

"""

get_dataset_input = """

\033[93mPlease select from the datasets for choosing dataset projection.\033[0m The algorithm shall be fed upon
this dataset projection - which is passed over to the VM in a secure, encrypted fashion. 
\033[4mDatasets correspond to an aleady created Projection ID.\033[0m \033[93mPlease choose one amongst the below\033[0m:
\033[94m`%s`\033[0m

"""

dataset_conf_ack = """

\033[92mThe dataset inputs have been sought, and correspond to the following:
- \033[1mprojection ID\033[0m : \033[4m%s\033[0m         - \033[1mprojection Name\033[0m : \033[4m%s\033[0m

"""

inputs_ack_lvl4 = """

\033[92mThe Next set of inputs w.r.t Dataset Projections, are complete too.\033[0m
Next, we move ahead to seek few attributes related to the package of all above, a.k.a policy / pipeline.

\033[96mThe policy is what, runs as a "Pipeline" on the "Sandbox" sought above during \033[1m`nfer-sandbox-cli run`.\033[0m

"""

unique_project_name = """
\033[93mPlease specify, a unique name for your project / pipeline\033[0m. This is further rendered unique
"""

inputs_ack_lvl5 = """

\033[92mAll the inputs have been honored, and reflected in the following file `main.yml`. \033[0m
Basis inputs, \033[94mthe following dirs have also been created with purpose mentioned against them below\033[0m:

- \033[4malgo\033[0m : \033[1mcontaining further folders `%s` for the code and `%s` for the dependencies.\033[0m
- \033[4mcerts\033[0m : containing the cert files `%s` and `%s` for public and private keys respectively.\033[0m
- \033[4mdocker-files\033[0m : this is an internal purpose folder, suitable for creating on-the-fly few necessary DockerFiles.\033[0m
- \033[4mdocker-images\033[0m : some necessary docker images pulled to run the pipeline end-to-end, are stored here.\033[0m
- \033[4mkeys\033[0m : Some keys, symmetric / assymetric, to vouch for encryption end-to-end, are stored here.\033[0m
- \033[4mlogs\033[0m : Once the logs are curated from the runtime, those are stored here at the developer's avail.\033[0m
- \033[4moutput\033[0m : The Output retrieved, from the sandbox, in an encrypted form, is fetched and stored here.\033[0m
- \033[4mpolicy\033[0m : The Policy package, as a .json document, is stored here.\033[0m
- \033[4mbuild\033[0m : Various files, on the fly, are generated here, e.g the "tar" of the "Encrypted" Algorithm docker image.\033[0m

\033[96mAdditionally, as we do the \033[1m`nfer-sandbox-cli run`\033[0m, the :

\033[94m- "state" of the execution is stored in a `.pbstate` file. This is a checkpoint for the tasks in the execution (.yml file)\033[0m
\033[94m- "register" of the tasks in the execution are stored in `.register` file. \033[0m
  This helps us choose fields from the output of tasks above in the execution order.
  
"""

verbpose_default = "debug"

codebase_desc_default = "Get algo+deps code in file structure"

certs_desc_default = "Get Certificates (Self-Signed)"

asymmetric_desc_default = "Get Asymmetric Pair for client"

symmetric_desc_default = "Get Symmetric Algo Key"

sandbox_desc_default = "Specify Sandbox Specs"

dockerize_desc_default = "Specify Algorithm to get Dockerized Image Encrypted (app and deps)"

data_desc_default = "Prepare / Choose Data Projections"

output_encr_desc_default = "Prepare Output Encryption Fields"

policy_prep_desc_default = "Prepare Policy (comprising algo, deps, data info)"

submit_policy_desc_default = "Submit Policy (created above)"

trigger_policydesc_default = "Trigger Policy a.k.a Pipeline"

retrieve_outputdesc_default = "Retrieve Output"

decrypt_outputdesc_default = "Decrypt Output"

code_folder_default = "src/"

main_file_default = "main.py"

deps_folder_default = "deps/"

deps_file_default = "requirements.txt"

stack_default = "python"

pl_ca_certs_path_default = '{{ cert_metadata "path" }}'

pl_ca_certs_name_default = '{{ cert_metadata "ca_cert" }}'

algo_lang_default = '{{ codebase_metadata "stack" }}'

algo_apps_dir_default = '{{ codebase_metadata "dest_code" }}'

algo_deps_dir_default = '{{ codebase_metadata "dest_deps" }}'

key_algo_default = '{{ algokey_metadata "path" }}'

sdbx_pubkey_default = '{{ sandbox_metadata "public_key" }}'

algo_ca_cert_name_default = '{{ cert_metadata "ca_cert" }}'

algo_ca_cert_path_default = '{{ cert_metadata "path" }}'

data_ca_cert_name_default = '{{ cert_metadata "ca_cert" }}'

data_ca_cert_path_default = '{{ cert_metadata "path" }}'

docker_image_default = '{{ algo_metadata "image" }}'

docker_tag_default = '{{ algo_metadata "tag" }}'

docker_repo_default = '{{ algo_metadata "repo" }}'

sandbox_name_default = '{{ sandbox_metadata "instance_name" }}'

sandbox_id_default = '{{ sandbox_metadata "instance_id" }}'

policy_doc_default = '{{ policy_metadata "policy_file" }}'

template_id_default = '{{ policy_metadata "template_id" }}'

pipeline_name_default = '{{ properties "pipeline_name" }}'

execute_entity_regexp = '{{ submission_metadata "pipeline_id" }}'

output_dest_default = "output"

experiment_id_regexp = '{{ execution_metadata "exec_hash" }}'

decrypt_source_regexp = '{{ output_metadata "dest" }}'

output_keep_original_default = True

data_sym_ekey_regexp = '{{ data_metadata "data_sym_ekey" }}'

dataset_cid_regexp = '{{ data_metadata "cid" }}'

dataset_name_regexp = '{{ data_metadata "name" }}'

domain_regexp = '{{ algo_metadata "DOMAIN" }}'

pipeline_name_regexp = '{{ properties "pipeline_name" }}'

out_fspf_key_regexp = '{{ output_metadata "fspf_key" }}'

algo_fspf_tag_regexp = '{{ algo_metadata "FSPF_TAG" }}'

algo_fspf_key_regexp = '{{ algo_metadata "FSPF_KEY" }}'

mrenclave_regexp = '{{ algo_metadata "mrenclave" }}'

sandbox_measurement_regexp = '{{ sandbox_metadata "measurement" }}'

key_algo_regexp = '{{ algo_metadata "key_algo" }}'

pub_client_regexp = '{{ client_keypair_metadata "cert" }}'

data_loc_regexp = '{{ data_metadata "arn" }}'

algo_image_regexp = '{{ algo_metadata "image_id" }}'

ca_certificate_regexp = '{{ cert_metadata "ca_cert" }}'

ca_cert_path_regexp = '{{ cert_metadata "path" }}'

certificate_regexp = '{{ cert_metadata "cert" }}'

cert_path_regexp = '{{ cert_metadata "path" }}'

algo_certs_priv_regexp = '{{ cert_metadata "privkey" }}'



