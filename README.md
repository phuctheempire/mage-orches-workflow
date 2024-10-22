<div>
<img src="https://github.com/mage-ai/assets/blob/main/mascots/mascots-shorter.jpeg?raw=true">
</div>


# Mini-Project: Building an ETL Pipeline Orchestrated by Mage

This project is based on the workflow orchestration framework [Mage](https://www.mage.ai/). 

More about the framework, please see the document [here](https://docs.mage.ai/introduction/overview). 

[Get Started](https://github.com/mage-ai/mage-zoomcamp?tab=readme-ov-file#lets-get-started)
[Assistance](https://github.com/mage-ai/mage-zoomcamp?tab=readme-ov-file#assistance)

## Mage installation

This repo contains a Docker Compose template for getting started with a new Mage project. It requires Docker to be installed locally.

You can start by cloning the repo:

```bash
git clone https://github.com/mage-ai/mage-zoomcamp.git mage-zoomcamp
```

Navigate to the repo:

```bash
cd mage-data-engineering-zoomcamp
```

Rename `dev.env` to simply `.env`— this will _ensure_ the file is not committed to Git by accident, since it _will_ contain credentials in the future.

Build the container

```bash
docker compose build
```

Finally, start the Docker container:

```bash
docker compose up
```

Now, navigate to http://localhost:6789 in your browser!

### What just happened?

We just initialized a new mage repository. It will be present in your project under the name `magic-zoomcamp`. If you changed the varable `PROJECT_NAME` in the `.env` file, it will be named whatever you set it to.

This repository should have the following structure:

```
.
├── mage_data
│   └── magic-zoomcamp
├── magic-zoomcamp
│   ├── __pycache__
│   ├── charts
│   ├── custom
│   ├── data_exporters
│   ├── data_loaders
│   ├── dbt
│   ├── extensions
│   ├── interactions
│   ├── pipelines
│   ├── scratchpads
│   ├── transformers
│   ├── utils
│   ├── __init__.py
│   ├── io_config.yaml
│   ├── metadata.yaml
│   └── requirements.txt
├── Dockerfile
├── README.md
├── dev.env
├── docker-compose.yml
└── requirements.txt
```