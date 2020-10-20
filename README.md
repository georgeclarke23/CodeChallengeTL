# CodeChallenge True Layer

### Tech
This project is based on a code challenge given by True Layer.

This project is dependent on:
- PySpark - Apache Spark is an open-source cluster-computing framework, built around speed, ease of use, and streaming analytics whereas Python is a general-purpose, high-level programming language that can interact with Spark framework through pyspark.
- Docker - Docker is a tool designed to make it easier to create, deploy, and run applications by using containers.
- Postgresql - An RDBMS database and was required in the project brief.



## Getting Started Running The Project
If you have docker and pyspark already installed in an environment, just clone the project and run the following command:

```bash
make docker/compose
``` 
#### or

You will need to provision an EC2 instance that uses Ubuntu operating system, ssh into the EC2 instance and run the following commands: 
```bash
sudo apt-get update

# Install packages to allow apt to use a repository over HTTPS:
sudo apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    make \
    unzip \
    software-properties-common

# Download the code into the instance and unzip it.
wget https://github.com/georgeclarke23/CodeChallengeTL/archive/master.zip
unzip master.zip

# Add Docker’s official GPG key:
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

# set up the stable repository.
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"

# install docker
sudo apt-get update
sudo apt-get install -y docker-ce docker-compose

# give ubuntu permissions to execute docker
sudo usermod -aG docker $(whoami)
# log out
exit
```


Once this is done, time to run the pyspark job and postgress database in a container

```bash
cd CodeChallengeTL-master/

# This command will start the docker containers on the EC2 instance
make docker/compose
```
## Query database



## Testing
To check the data for correctness, I have been using test driven approach where I was downloading random samples of my data as CSV and examining trends through excel in my local computer environemnt.