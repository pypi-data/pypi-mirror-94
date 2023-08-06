## About
r2cloud python sdk makes it easier for you to work with your r2cloud server using the python programming language. The SDK uses an object-oriented design and tries to look like r2cloud API.

## Installation 

#### with pip3

```sh
pip install r2server
```

#### from repo

```sh
make install
make doc # for generate documentation
```

## Quick start

```python
import r2server.api

# init api
network = r2server.api()

# get all observations
obs = network.observation("NOAA 19")

# print all filtred observations ids
for ob in obs:
    print("Observation " + str(ob.id) + " by " + ob.name)

```

more examples you can find in `/examples` dir on github