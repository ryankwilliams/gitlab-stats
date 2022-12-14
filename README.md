# gitlab-stats

Program collecting statistics for gitlab groups.

## Supports

1. Collect merge request counts per author for a given group

## Run

Select from one of the two ways to run the program below.

### Python

```shell
python3 -m venv venv
source venv/bin/activate
(venv) pip3 install -r requirements.txt
(venv) export GITLAB_URL=<GITLAB_URL>
(venv) export GITLAB_API_ACCESS_TOKEN=<GITLAB_API_ACCESS_TOKEN>
(venv) python3 merge_request_stats.py --group <GITLAB_GROUP>
```

### Container

```shell
podman run -e GITLAB_URL=<GITLAB_URL> \
-e GITLAB_API_ACCESS_TOKEN=<GITLAB_API_ACCESS_TOKEN> \
ghcr.io/ryankwilliams/gitlab-stats:main --group <GITLAB_GROUP>
```
