# S4Gpy a python client library for Stream-for-Good Project

This client api can be used to perform analysis of S4G dataset with Python3.

It closely mirros the HATEAOS from the Rest API so that when requesting data, the `links` information are automatically converted to functions that can be called from the API.

For example with the user API

![](userAPI.png)

you can get a Python version with the following syntax:

```python
from s4gpy.s4gpy import S4GAPI
#first register with your vod-prime.space credentials
api=S4GAPI("foo","bar")
#then get a user API object
user_api=api.get_user_api()

#get the users from the API
for u in user_api.get_users(): 
    #for each user, follow the all-thumbnails link by calling the all_thumbnails() function.
    for t in u.all_thumbnails()["thumbnails"]: 
        print(f"{u.user.user_id};{t.row};{t.col};{t.video_id};{t.timestamp}")
```

this code prints out the users' id, and some metadata on thumbnails that were proposed to her.

```csv
1f52213c-f31d-4dc9-bac5-35464b2ff1b9;4;1;81074110;1610984583.0
1f52213c-f31d-4dc9-bac5-35464b2ff1b9;4;0;80994082;1610984583.0
1f52213c-f31d-4dc9-bac5-35464b2ff1b9;6;0;81277950;1610984583.0
1f52213c-f31d-4dc9-bac5-35464b2ff1b9;5;2;80232398;1610984583.0
1f52213c-f31d-4dc9-bac5-35464b2ff1b9;5;3;80234304;1610984583.0
1f52213c-f31d-4dc9-bac5-35464b2ff1b9;4;3;80095697;1610984583.0
1f52213c-f31d-4dc9-bac5-35464b2ff1b9;5;0;80025678;1610984584.0
```


## Installation

### From Pypi

```bash
pip install s4gpy
```

### From source

```bash
#uninstall first
pip uninstall s4gpy
make build
pip install dist/*.whl
```

## Examples

### Direct API

Get the current direct schedule, with metadata from the companion platform-api

```python
from s4gpy.s4gpy import S4GAPI
api=S4GAPI(<add your user here>,<add your password here>)
for s in api.get_direct_api().get_direct_schedule(): 
    try:
        imdb_data=s.content().imdb_id()
        genres="+".join([g["genre"] for g in imdb_data.data.genres])
    except AttributeError: #in case platform.vod-prime.space fucks up things
        print(f"{s.airing_time};{s.video_id};UNKNOWN;UNKNOWN")
        continue
    print(f"{s.airing_time};{s.video_id};{imdb_data.data.title};f{genres}")
```

### User API

Show the row/cols of every watched video for each user

```python
from s4gpy.s4gpy import S4GAPI
#create an API entrypoint
api=S4GAPI("foo","bar")
#get the user_api
user_api=api.get_user_api()

#for each user
for u in user_api.get_users(): 
    #get all the video she watched
    watched_videos=[w.video_id for w in u.all_watches().watches]
    #for all the thumbnails
    for t in u.all_thumbnails()["thumbnails"]: 
        #only dump the informations if the user has wached the video
        if t.video_id in watched_videos:
            print(f"{u.user.user_id};{t.row};{t.col};{t.video_id};{t.timestamp}")
```

### Direct API

Get the current direct schedule, with metadata from the companion platform-api

```python
from s4gpy.s4gpy import S4GAPI
api=S4GAPI(<add your user here>,<add your password here>)
for s in api.get_direct_api().get_direct_schedule(): 
    try:
        imdb_data=s.content().imdb_id()
        genres="+".join([g["genre"] for g in imdb_data.data.genres])
    except AttributeError: #in case platform.vod-prime.space fucks up things
        print(f"{s.airing_time};{s.video_id};UNKNOWN;UNKNOWN")
        continue
    print(f"{s.airing_time};{s.video_id};{imdb_data.data.title};f{genres}")
```

### Credential API

Get some credentials for netflix to run a robot run

```python
from s4gpy.s4gpy import S4GAPI
api=S4GAPI("foo","bar")
login, password = api.get_credentials_api().get_credentials("netflix")
```