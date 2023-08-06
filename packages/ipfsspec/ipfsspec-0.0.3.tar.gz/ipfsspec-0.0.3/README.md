# ipfsspec

A readonly implementation of fsspec for IPFS.

This project is currently very rudimentaty. It is not yet optimized for efficiency and is not yet feature complete. However it should be enough to list directory contents and to retrieve files from `ipfs://` resources via fsspec. A simple hello worlds would look like:

```python
import ipfsspec  # this is needed to register the protocol with fsspec
import fsspec

with fsspec.open("ipfs://QmZ4tDuvesekSs4qM5ZBKpXiZGun7S2CYtEZRB3DYXkjGx", "r") as f:
    print(f.read())
```

The current implementation uses a HTTP gateway to access the data. It tries to use a local one (which is expected to be found at `http://localhost:8080`) and falls back to `ipfs.io` if the local gateway is not available.
