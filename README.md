This is a [Next.js](https://nextjs.org) project bootstrapped with [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app).

# Getting Started

## Requirements
* [Docker Desktop](https://docs.docker.com/desktop/setup/install/windows-install/)
* [kubectl](https://kubernetes.io/docs/tasks/tools/)
* [kind](https://kind.sigs.k8s.io/docs/user/quick-start/#installation)
* Docker Hub credentials and access to repository (Currently Private)


## Installation
```bash
# API requirements
python3 -m venv multicat-env
source multicat-env/bin/activate
pip install -r src/api/requirements.txt

# Frontend requirements
pnpm install
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

## Setting Up Local Environment

For starting the backend locally environment with docker:

* Ensure Docker Desktop is running
* Run the following command:

```bash
pnpm run dev
```

GraphQL documentation will be available at [http://localhost:8000/api/graphql](http://localhost:8000/api/graphql).

```bash
# Using kubernetes
# Requires kind and local files defining Docker secrets
sh ./create-local-k8s-cluster.sh
```