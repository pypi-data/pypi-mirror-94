import platform, os

url = "https://sensccf.eastus.cloudapp.azure.com/secure_cloud_api/v1/"
url = "https://40.76.33.226/secure_cloud_api/v1/"
url = "https://168.62.171.28/secure_cloud_api/v1/"
end_statuses = ["READY", "PENDING", "CREATED", "RUNNING"]
sleep_time = 5
creds_conf_path = '/home/%s/.nfer-sandbox/' if platform.system() == "Linux" else '/Users/%s/.nfer-sandbox/'
setup_conf_path = '/home/%s/.nfer-sandbox/' if platform.system() == "Linux" else '/Users/%s/.nfer-sandbox/'
creds_conf_file = 'credentials.txt'
setup_conf_file = '.setup.db'
setup_server_addr = '127.0.0.1'
setup_server_port = 5112
NFER_CLI_HOME = "/home/%s/nfer-secure-sandbox-cli"
ss_ca_conf = {
    "country": "DE", "state": "NRW", "city": "Berlin",
    "org": "Nference", "unit": "Locus", "cn": "www.example.com", "email": "nfer@devnull.com"
}
cert_upload_url = "http://0.0.0.0:8282/nfer-sandbox/upload-cert"
nfer_sdbx_url = "http://0.0.0.0:8282/nfer-sandbox"
data_upload_url = "http://0.0.0.0:8383/nfer-sandbox"
docker_upload_url = "http://0.0.0.0:8181/nfer-sandbox"
support_email_id = "locus@devnull.com"
#auth_url = 'https://preview.nferx.com/api/is_authenticated'
auth_url = 'https://nferx-sandbox-controller-0.nferx.com/app/is_authenticated'

cert_upload_url = "https://nferx-sandbox-controller-0.nferx.com/nfer-sandbox-controller-api/nfer-sandbox/upload-cert"
nfer_sdbx_url = "https://nferx-sandbox-controller-0.nferx.com/nfer-sandbox-controller-api/nfer-sandbox"
data_upload_url = "https://nferx-sandbox-controller-0.nferx.com/nfer-sandbox-data-projection/nfer-sandbox"
docker_upload_url = "https://nferx-sandbox-controller-0.nferx.com/nfer-sandbox-docker-registry/nfer-sandbox"
support_email_id = "locus@devnull.com"
auth_url = 'https://preview.nferx.com/api/is_authenticated'

sensoriant_docker_login_user = "bb3fd7f0-72e4-4d76-ace4-b17582cc1993"
sensoriant_docker_login_passwd = "50b77c07-fc54-4c93-bd5b-e1d5aa5e26d1"
sensoriant_docker_registry = "sensoriant.azurecr.io"
dest_sens_docker_registry = "nferalgos.azurecr.io"
sensoriant_docker_repository = "testskpharma"
sensoriant_docker_image = "testskpharmav1"
sensoriant_docker_tag = "sktest1"

dest_sens_docker_registry = "docker-registry.nferx.com"

clone_temp_dir = "temp"
git_replace_from = "https://github.com"
git_replace_to = "https://%s:%s@github.com"

# algo_app_dir = "algo/app"
algo_app_dir = "app"
# algo_deps_dir = "algo/deps"
algo_deps_dir = "app"
scli_tasks = ["algo encryption", "algo signing", "image upload"]

client_docker_registry = "localhost:5000"

pharma_domain = "Testpharma.com"

default_algo_tar_file = "algo.tar.gz"

version = "VERSION_1_1_0"

scli_ref_algo_image = 'sensoriant.azurecr.io/priv-comp/sensrefimage:11302020'
ref_algo_dir = "/tmp/nfer-cli-space/"
ref_algo_tar = "REF_ALGO_BASE.tar"

google_credentials_json = {
  "type": "service_account",
  "project_id": "sensoriant",
  "private_key_id": "6ca0455d250cbc302d8c8de5ae9e3c94ae4d0df7",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC9UcxYsNm4Zg9k\n0OEJHYPMsnQCe4mL9oPG1z2vqRFN6L8dGyhNLtbXBYZsAEqTu9aMvqZsgt65Eanx\nZURK5Z2djSA+LO+tvxD9SglxNaS7uwX4ZU2hLGZNY1Ceu8vBMZ4egKp+zSfOZvEL\n5w4EcTJ+9qB2C4+3Wu7eDZv1y4GMp1WkGe26pomN8FMwDVlqvpKsRQo8rYzuM4UL\nrmqn2WIEcmVUSNXaeJi9veStebToCx7geesBttXCjgay97namJbBH71NkuqdmFL4\nEUFtWBdjQ2O98ackIBxLyZhrYXlM4HAaymIFV4bioUOcnf+naUP7FjHz2zwfE0np\n5bw9AUzHAgMBAAECggEAH6r3nhxTBvPXflssUVyFB/AP1Lx6aRWevFuTv3bt5JTa\npxE8YBDGMiiD8DvqPaUNgfSAHSWVAOsR/MWeM1MOVuTc8FmO7AbKXjwMsUmyWQ6z\nNHYpkpy9LhO/UBYEwre8hciq/FPv5Sg2CPIo15hhxHgXpjdP3nFRBIbNQEO+01p+\nKO/6ZTSDKCb6+DE31ZVBCrAZdfexDByy9WFsnwmV292aM2RXxnhsOMJzSe+xNJaf\nQO5d1ggkrkOkPmrrUne5mTZrCeU1dML2zcN8KaoUYb/nV1g3e7HYDVTyPr1RTDfk\nzKuG5OWxAgI+zZ7giAqpYHwH37Fkft7WKouQD9SGmQKBgQD2wGmLoIhWPQfTxbtm\n6THTqCB5lCBiGyKd2SkMOgEoRHMHC4OJBhCTPfXmKgQBBImCdiBfqCHGUXbyjnBV\n58MU2DO0vbsVQ+ZqREigUcScns9BgCcS+ZptpUcv/uZ6VHaSlcqzxIw8Cj5nF6Xd\nlIvQXczlz35Uw7kysa7ZO2k+iQKBgQDEalLcatNn+ML3uPdl4gck/0hBchoWLIXo\nicqYyZdU9OQ4O1SWDinpVPvqv5etUfSIEwVaWPDIiNf4A29O/hO6bIkPdIbZ2KzX\nCuePq/U7OsvvuXbFcQzf9GytQBwLZJm2vdGs0ZaZm6cK/mKyrFr+5WCMSSL5TwOd\nu1gXXVrczwKBgQCyOEFDVxyB5SzNGWkEqHOTo0Bpb8J/+YdkKSBLs214jw/hy8Ai\nbN3162+64SfpMES9lOJHFOHoIpjeEmEyuuWdHZci+VKxxkwa/tzR5p0yXkXl0lDm\nlJ+kiBbFpL8FJhJKR6STeOesyd1OircDNrJROh6u8dIWGROfeNSIFDAsuQKBgQCo\nT/RxrZk7n5Bzd62JQQeeTKQ+cOip171oZ6uVAisMQk7PYQg7DigcKxc1MrlnbLN/\nZ81OfqjXL2ziuw7HQjLlrdxFwjVMuMBkBpQoKdMbzma0JtoAl7/QqkP2stlVaf/O\n+RqUXYYQW7HpWdR6B/hyNV1m2cV+npcas0/ptbYHQQKBgC4Jzcsyt9sZS/iRj5/Z\naWHGIRkrp5MQvCzMwTqMbauASeBqDJDKW+yfsjDfkLXVaB+zhn1NVrTasymRvoNM\nKbqZ7smMkcxQo0A0fpPnpgHIuY00IweJxiNqCnoyCI/ZzbWNEZTCW2U87e3UkA8d\n5Za+kdW93go1uN3Kd3QfrkPT\n-----END PRIVATE KEY-----\n",
  "client_email": "327820435396-compute@developer.gserviceaccount.com",
  "client_id": "103159402627307722102",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/327820435396-compute%40developer.gserviceaccount.com"
}

sens_storage_bucket = "sensoriant-nferx-dev-storage"
