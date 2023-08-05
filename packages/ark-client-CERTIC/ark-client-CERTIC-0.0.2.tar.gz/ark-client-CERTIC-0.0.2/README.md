# Ark Python client

Basic usage:

```
from ark import Client, ClientError
api = Client(YOUR_APP_ID, YOUR_SECRET_KEY, "https://ark.provider.tld/api/v1/")

ark_name = api.create(
    "http://somewhere.tld/some-resource/", {
        "who": "someone", 
        "what": "something", 
        "where": "somewhere" 
    }
)

ark_infos = api.read(ark_name)

api.update(ark_name, "http://somewhereelse.tld/some-resource/")

try:
    api.read("doesnot/exist")
except CLientError as e:
    print(e.response.status_code)  # response contains a Python/Requests response object
```

Batch mode:

```
batch = api.batch()
batch.read(ark_name)
batch.create("http://somewhere.tld/some-resource/")
batch.update(anothe_ark_name,"http://somewhere.tld/some-other-resource/")
for item in batch.commit():
    print("{}: {}".format(item["ark_name"], item["ark_location"]))

```

In batch mode, method chaining is available:

```
api.batch()
   .read(some_ark_name)
   .read(some_other_ark_name)
   .update(yet_another_name, "http://somewhereelse.tld/")
   .commit()
```