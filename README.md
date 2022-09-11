# RealTimeDataProcessing-unibz-18697
Real-Time Big Data Processing Project Assignment 2022

# Building a real-time analytics dashboard with Streamlit, Apache Pinot, and Apache Kafka

Clone repository

[source, bash]
----
git clone 
----

Spin up all components

[source, bash]
----
docker-compose up
----

Setup Python

Ingest Wikipedia events

[source, bash]
----
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
----

Create Kafka topic

[source, bash]
----
docker exec -it kafka-wiki kafka-topics.sh \
  --bootstrap-server localhost:9092 \
  --partitions 5 \
  --topic stock_events \
  --create 
----

Ingest Wikipedia events

[source, bash]
----
python stocks_to_kafka.py
----

Check Wikipedia events are ingesting

[source, bash]
----
docker exec -it kafka-wiki kafka-run-class.sh kafka.tools.GetOffsetShell \
  --broker-list localhost:9092 \
  --topic stock_events
----

[souce, bash]
----
docker exec -it kafka-wiki kafka-console-consumer.sh \
  --bootstrap-server localhost:9092 \
  --topic stock_events \
  --from-beginning
----

Add Pinot Table

[source, bash]
----
docker exec -it pinot-controller-wiki bin/pinot-admin.sh AddTable \
  -tableConfigFile /config/table-stocks.json \
  -schemaFile /config/schema-stocks.json \
  -exec
----

Open the Pinot UI http://localhost:9000/

Run Streamlit app

[source, bash]
----
streamlit run streamlit/app.py
----


# Configure the AWS server
https://docs.docker.com/engine/install/ubuntu/

user: ubuntu

Install using the repository
Before you install Docker Engine for the first time on a new host machine, you need to set up the Docker repository. Afterward, you can install and update Docker from the repository.

#Set up the repository
Update the apt package index and install packages to allow apt to use a repository over HTTPS:

 `sudo apt-get update
 sudo apt-get install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
Add Docker’s official GPG key:`

 `sudo mkdir -p /etc/apt/keyrings`
 `curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg`


Use the following command to set up the repository:

 echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine
Update the apt package index, and install the latest version of Docker Engine, containerd, and Docker Compose, or go to the next step to install a specific version:

 sudo apt-get update
 sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin
 sudo apt install docker-compose

  sudo service docker start