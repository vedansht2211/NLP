# =========================
# KAFKA TERMINAL COMMANDS
# =========================

# Step 1: Navigate to the Kafka installation folder
# cd C:\kafka_2.13-4.3.1

# Step 2: Generate a unique Cluster ID (UUID)
# .\bin\windows\kafka-storage.bat random-uuid

# Step 3: Format Kafka storage (replace <Your-UUID>)
# .\bin\windows\kafka-storage.bat format -t <Your-UUID> -c .\config\server.properties --standalone

# Step 4: Start the Kafka broker (keep this terminal open)
# .\bin\windows\kafka-server-start.bat .\config\server.properties

# -------- Open a NEW PowerShell --------

# Step 5: Create the topic
# cd C:\kafka_2.13-4.3.1
# .\bin\windows\kafka-topics.bat --create --topic system-metric --bootstrap-server localhost:9092

# -------- Open another NEW PowerShell --------

# Step 6: Start the console producer
# .\bin\windows\kafka-console-producer.bat --topic system-metric --bootstrap-server localhost:9092

# Example messages:
# {"server_id":"server01","cpu_usage":82,"memory_usage":65}
# {"server_id":"server02","cpu_usage":45,"memory_usage":58}
# {"server_id":"server03","cpu_usage":91,"memory_usage":70}

# -------- Open another NEW PowerShell --------

# Step 7: Start the console consumer
# .\bin\windows\kafka-console-consumer.bat --topic system-metric --from-beginning --bootstrap-server localhost:9092


# =========================
# IMPORTS
# =========================

from datetime import datetime
import json
import time

from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator

from kafka import KafkaAdminClient, KafkaConsumer, KafkaProducer
from kafka.admin import NewTopic

import matplotlib.pyplot as plt
import pandas as pd


# =========================
# 1. KAFKA ADMIN
# =========================
# Imports used:
# from kafka import KafkaAdminClient
# from kafka.admin import NewTopic

from kafka.admin import KafkaAdminClient , NewTopic
admin=KafkaAdminClient(
    bootstrap_servers="localhost:9092"
)
topic = NewTopic(
    name="testing",
)
admin.create_topics(new_topics=[topic])
admin.close()



# =========================
# 2. KAFKA PRODUCER
# =========================
# Imports used:
# import json
# import time
# from kafka import KafkaProducer

from kafka import KafkaProducer
import json
import time

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda x: json.dumps(x).encode("utf-8")
)

for i in range(10):
    message = {
        "server_id": f"server{i+1}",
        "cpu_usage": 50 + i * 4,
        "memory_usage": 60 + i
    }

    producer.send(
        "testing",
        value=message
    )

    print("Sent:", message)

    time.sleep(1)

producer.flush()
producer.close()

# =========================
# 3. KAFKA CONSUMER
# =========================
# Imports used:
# import json
# from kafka import KafkaConsumer

from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    "testing",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="aiops-monitor",
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

print("Waiting for messages...")

for message in consumer:
    data = message.value

    server = data["server_id"]
    cpu = data["cpu_usage"]
    memory = data["memory_usage"]

    print("\nReceived:")
    print("Server:", server)
    print("CPU:", cpu, "%")
    print("Memory:", memory, "%")

    if cpu > 80:
        print("ALERT: High CPU detected on", server)

# =========================
# 4. PANDAS + MATPLOTLIB ANALYSIS
# =========================
# Imports used:
# import pandas as pd
# import matplotlib.pyplot as plt

import pandas as pd
import matplotlib.pyplot as plt

data = {
    "Timestamp":[f"10:{str(i).zfill(2)}" for i in range(20)],
    "CPU":[45,50,55,60,62,95,58,61,65,70,75,97,68,72,78,80,82,92,76,74],
    "Memory":[40,42,45,48,50,60,52,55,58,60,62,65,61,63,64,66,68,70,65,64],
    "ResponseTime":[180,190,200,210,220,450,215,220,230,240,250,480,235,240,260,270,290,500,250,260]
}

df = pd.DataFrame(data)

print("Basic Statistics")
print(df[["CPU","Memory","ResponseTime"]].describe())

anomalies = df[df["CPU"] > 90]

print("\nTotal records:", len(df))
print("Anomalies detected:", len(anomalies))

print("\nTimestamp\tCPU\tStatus")
for _, row in anomalies.iterrows():
    print(f"{row['Timestamp']}\t{row['CPU']}%\tANOMALY")

plt.figure(figsize=(8,4))
plt.plot(df["Timestamp"], df["CPU"], marker="o", label="CPU")
plt.scatter(anomalies["Timestamp"], anomalies["CPU"], color="red", label="Anomaly", s=80)
plt.xticks(rotation=45)
plt.ylabel("CPU Usage")
plt.legend()
plt.tight_layout()
plt.show()




# =========================
# 6. AIRFLOW DAG
# =========================

from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime

def collect_metrics():
    print("CPU = 87")
    print("Memory = 65")
    print("Response Time = 420ms")

def process_metrics():
    print("Processing metrics...")

def detect_anomaly():
    cpu = 87
    if cpu > 80:
        print("Anomaly detected: High CPU usage")
    else:
        print("No anomaly detected")

def generate_report():
    print("===== AIOps Report =====")
    print("Metrics collected successfully")
    print("Metrics processed successfully")
    print("Anomaly detection completed")
    print("========================")

with DAG(
    dag_id="server_metric",
    start_date=datetime(2026,9,15),
    schedule=None,
    catchup=False
) as dag:

    collect = PythonOperator(
        task_id="collect_metrics",
        python_callable=collect_metrics
    )

    process = PythonOperator(
        task_id="process_metrics",
        python_callable=process_metrics
    )

    detect = PythonOperator(
        task_id="detect_anomaly",
        python_callable=detect_anomaly
    )

    report = PythonOperator(
        task_id="generate_report",
        python_callable=generate_report
    )

    collect >> process >> detect >> report




    """

# Update package list
sudo apt update

# Install curl (needed for downloading uv)
sudo apt install -y curl

# Install uv (Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Load uv into the current terminal
source ~/.local/bin/env

# Create Airflow project folder and dags folder
mkdir -p ~/air/dags

# Enter the project folder
cd ~/air

# Create a Python 3.11 virtual environment
uv venv --python 3.11

# Activate the virtual environment
source .venv/bin/activate

# Set Airflow's working directory
export AIRFLOW_HOME=~/air

# Install Airflow 3.1.0 with the official constraints
uv pip install "apache-airflow[celery]==3.1.0" \
--constraint "https://raw.githubusercontent.com/apache/airflow/constraints-3.1.0/constraints-3...."

# Start Airflow (first-time setup)
airflow standalone
    

"""