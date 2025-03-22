This is a [Next.js](https://nextjs.org) project bootstrapped with [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app).

Currently a WIP - Initial design depicted on [portfolio](https://dev.en-nox.com/#projects)

# Getting Started

## Requirements
* [Docker Desktop](https://docs.docker.com/desktop/setup/install/windows-install/)
* [kubectl](https://kubernetes.io/docs/tasks/tools/)
* [kind](https://kind.sigs.k8s.io/docs/user/quick-start/#installation)
* Docker Hub credentials and access to repository (Currently Private)

## Setting Up Local Environment

For starting the application locally with docker:

* Ensure Docker Desktop is running
* Run the following command:

```bash
# This will run docker-compose.yaml
# Run local Docker Desktop, then
pnpm run dev
```

Open [https://localhost:3000](https://localhost:3000) with your browser to see the result.
GraphQL documentation will be available at [https://localhost:8000/api/graphql](http://localhost:8000/api/graphql).

## Adding a new Document and Schema Type

* Define the MongoDB document in [src/api/db/](./src/api/db/).
* Define GraphQL Schema in [src/api/schemas/](./src/api/schemas/).
