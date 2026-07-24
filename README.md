\# NexusDeploy — Enterprise CI/CD Platform



Production-grade CI/CD automation platform that takes an application from code commit to a monitored, running deployment on Kubernetes — built end-to-end on AWS.



!\[CI/CD](https://img.shields.io/badge/CI%2FCD-Jenkins-red)

!\[Kubernetes](https://img.shields.io/badge/Kubernetes-EKS-blue)

!\[IaC](https://img.shields.io/badge/IaC-Terraform-purple)

!\[Monitoring](https://img.shields.io/badge/Monitoring-Prometheus%20%7C%20Grafana-orange)



\---



\## Overview



NexusDeploy simulates a real-world enterprise DevOps pipeline. A commit pushed to `main` triggers an automated chain: unit tests run, a Docker image is built and pushed to a private registry, and the new version is rolled out to a live Kubernetes cluster — all provisioned and observed as code.



\*\*What this project demonstrates:\*\*

\- Automated CI/CD with Jenkins, triggered by GitHub webhooks

\- Application containerization with Docker

\- Container orchestration on Amazon EKS, packaged and versioned with Helm

\- Infrastructure entirely defined and reproducible with Terraform

\- Full observability stack with Prometheus, Grafana, and Slack-integrated alerting



\---



\## Architecture



```mermaid

flowchart LR

&#x20;   A\[Developer pushes to GitHub] -->|webhook| B\[Jenkins]

&#x20;   B --> C\[Run unit tests]

&#x20;   C --> D\[Build Docker image]

&#x20;   D --> E\[Push to Amazon ECR]

&#x20;   E --> F\[Helm upgrade --install]

&#x20;   F --> G\[Amazon EKS Cluster]

&#x20;   G --> H\[Prometheus]

&#x20;   H --> I\[Grafana Dashboards]

&#x20;   H --> J\[AlertManager]

&#x20;   J -->|alerts| K\[Slack]



&#x20;   L\[Terraform] -.provisions.-> G

&#x20;   L -.provisions.-> E

```



\*\*Flow summary:\*\* GitHub → Jenkins (CI) → Amazon ECR (registry) → Amazon EKS (runtime, deployed via Helm) → Prometheus/Grafana (observability) → Slack (alerting). All infrastructure — the VPC, the EKS cluster, and the ECR repository — is provisioned by Terraform, not created by hand.



\---



\## Tech stack



| Layer | Tools |

|---|---|

| Source control | GitHub, GitHub Webhooks |

| CI orchestration | Jenkins (Pipeline as Code — `Jenkinsfile`) |

| Containerization | Docker |

| Image registry | Amazon ECR |

| Orchestration | Amazon EKS (Kubernetes), Helm |

| Infrastructure as Code | Terraform (VPC, EKS, ECR modules, S3 + DynamoDB remote state) |

| Observability | Prometheus, Grafana, AlertManager |

| Alerting | Slack (via AlertManager webhook) |

| Application | Python (Flask) |



\---



\## Repository structure



```

nexusdeploy/

├── app/

│   ├── app.py                 # Flask application (/health, /api)

│   ├── test\_app.py            # Unit tests (pytest)

│   ├── requirements.txt

│   └── Dockerfile

├── k8s/

│   ├── deployment.yaml

│   ├── service.yaml

│   └── alerts.yaml            # PrometheusRule definitions

├── nexusdeploy-chart/         # Helm chart

│   ├── templates/

│   └── values.yaml

├── terraform/

│   ├── main.tf

│   ├── vpc.tf

│   ├── eks.tf

│   ├── ecr.tf

│   ├── variables.tf

│   ├── outputs.tf

│   └── backend.tf

├── Jenkinsfile

└── README.md

```



\---



\## CI/CD pipeline stages



1\. \*\*Checkout\*\* — pulls the latest commit from GitHub

2\. \*\*Install \& Unit Test\*\* — installs dependencies, runs the pytest suite; pipeline stops here on failure

3\. \*\*ECR Login\*\* — authenticates Docker to the private registry using the Jenkins EC2 instance role

4\. \*\*Docker Build \& Tag\*\* — builds the image, tagging both `:latest` and `:<git-commit-sha>` for traceability

5\. \*\*Docker Push\*\* — pushes both tags to Amazon ECR

6\. \*\*Deploy to EKS\*\* — runs `helm upgrade --install`, rolling out the new image version to the cluster



Triggered automatically on every push to `main` via a GitHub webhook.



\---



\## Infrastructure (Terraform)



All infrastructure is defined as code and stored with remote state in S3 with DynamoDB locking to prevent concurrent modification.



```bash

cd terraform

terraform init

terraform plan

terraform apply

```



Provisions:

\- A VPC with public/private subnets across two Availability Zones

\- An EKS cluster with a managed node group (auto-scaling between 2–4 nodes)

\- An ECR repository with a lifecycle policy retaining the last 10 images



\---



\## Observability



\- \*\*Prometheus\*\* scrapes cluster and application metrics via `kube-prometheus-stack`

\- \*\*Grafana\*\* dashboards visualize pod CPU/memory, HTTP request rate, and error rate

\- \*\*AlertManager\*\* rules fire on:

&#x20; - `PodCrashLooping` — restart rate exceeding threshold over 15 minutes

&#x20; - `HighMemoryUsage` — pod memory usage above 85% of its limit for 5+ minutes

\- Alerts route to a dedicated Slack channel in real time



\---



\## Getting started locally



```bash

\# Clone

git clone https://github.com/<your-username>/nexusdeploy.git

cd nexusdeploy/app



\# Run the app

python3 -m venv venv \&\& source venv/bin/activate

pip install -r requirements.txt

python app.py



\# Run tests

pytest -v



\# Build and run the container

docker build -t nexusdeploy-app .

docker run -p 3000:3000 nexusdeploy-app

curl http://localhost:3000/health

```



Full cluster deployment, Jenkins setup, and Terraform provisioning steps are documented in the build phases below.



\---



\## Results



\- Full pipeline (commit → tested → built → deployed) completes in \*\*\[fill in your actual measured time]\*\*

\- Load tested with Apache Bench at \*\*\[fill in: e.g. 1000 requests, concurrency 50]\*\* — zero failed requests

\- Terraform `plan` after `apply` shows zero drift, confirming full infrastructure reproducibility



<!-- Add screenshots here -->

<!-- !\[Grafana dashboard under load](screenshots/grafana-load.png) -->

<!-- !\[Jenkins pipeline success](screenshots/jenkins-pipeline.png) -->



\---



\## Skills demonstrated



CI/CD pipeline design · Docker containerization · Kubernetes deployments (EKS) · Helm chart authoring · Infrastructure as Code (Terraform) · Cloud monitoring and alerting · Production DevOps practices



\## Future enhancements



\- GitOps with ArgoCD

\- Blue-green and canary deployment strategies

\- Service mesh integration (Istio/Linkerd)

\- Security scanning in the pipeline (Trivy, Snyk)

\- Multi-cloud deployment target



\---



