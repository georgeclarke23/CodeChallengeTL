# CodeChallenge True Layer

### Tech
This project is based on a code challenge given by True Layer.

This project is dependent on:
- PySpark - Apache Spark is an open-source cluster-computing framework, built around speed, ease of use, and streaming analytics whereas Python is a general-purpose, high-level programming language that can interact with Spark framework through pyspark.
- Docker - Docker is a tool designed to make it easier to create, deploy, and run applications by using containers.
- Postgresql - An RDBMS database and was required in the project brief.

Note: The datasets had to be scaled down for storage purposes, you can replace the datasets with the complete datasets. The movie and rating datasets were randomly sampled. 

##  Challenges and Choices
- I have chosen to run my script on the top of Apache Spark framework as it uses the full multiple VCPU efficiently and it fully supports reading large structured xmls through [spark-xml](https://github.com/databricks/spark-xml).
- Spark dataframe supports numerical, long list of functions and string regex operations on columns.

- Pyspark and Postgres require a long setup process that is OS type and version dependant.  I have used [official postgres docker container](https://hub.docker.com/_/postgres) and for Pyspark I have built a reproducable docker from unix container setup process.
- I have pulled the docker container for an OS independent reliable deployment and all shell scripts are minimal to make the project transferrable to other OSs.
 
## Algorithm choice 
The Jaccard Index, also known as the Jaccard similarity coefficient, is a statistic used in understanding the similarities between sample sets. The measurement emphasizes similarity between finite sample sets, and is formally defined as the size of the intersection divided by the size of the union of the sample sets.

For each movie, there was multiple matches to wiki abstracts. To decipher which match was the closets, I used the jaccard index to calculate  a score and the match with the highest score was selected. 


## Getting Started Running The Project
If you have docker and python  already installed in an environment, just clone the project and run the following command:

```bash
make venv 
. .venv/bin/activate
make docker/compose
``` 
#### or
You can  provision an EC2 instance that uses Ubuntu operating system, ssh into the EC2 instance and run the following commands: 
```bash
sudo apt-get update

# Install packages to allow apt to use a repository over HTTPS:
sudo apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    make \
    unzip \
    python3-pip \
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


Once this is done, time to run the pyspark job and postgress database in a container. SSH back into the EC2 instance and execute the following commands 
```bash
cd CodeChallengeTL-master/

# install python requirements.
pip3 install -r requirements.txt

# This command will start the docker containers on the EC2 instance
make docker/compose
```
## Query database

To run a query on the database update `PGHOST` in `.env` file to the host of the postgress database. This can be either locally `localhost` or the public IP address of the EC2 instance. Execute the following commands:

```bash
make query q="SELECT * FROM films"
```
NOTE: This will save the query results to a file `results.csv`

## Testing
To check the data for correctness, I have been using test driven approach where I was downloading random samples of my data as CSV and examining trends through excel in my local computer environemnt.