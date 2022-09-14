# gitlab-stats

```shell
python3 -m venv venv
source venv/bin/activate
(venv) pip3 install -r requirements.txt
(venv) export GITLAB_URL=<GITLAB_URL>
(venv) export GITLAB_API_ACCESS_TOKEN=<GITLAB_API_ACCESS_TOKEN>
(venv) export GITLAB_GROUP=<GITLAB_GROUP>
(venv) python3 merge_request_stats.py
```
