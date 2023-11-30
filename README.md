# market-stream

## gRPC
```commandline
python -m grpc_tools.protoc -I./protoc/ --python_out=./generated/ --grpc_python_out=./generated/ market_stream.proto
```

## PyPI
```commandline
python setup.py sdist bdist_wheel
twine upload dist/*
```

```commandline
username: __token__
password: <token>
```

## TODO
- Remove client to another repo
- Implement a GO version client
- Print status for recording symbol (*)
- Connection retry (**)
<<<<<<< HEAD
=======
- Auto push Docker image to DockerHub (*)

## Miscellaneous
`redis:://` is generally faster than `http/2`, but `http/2` is able to handle more complex 
application and less dependencies.  The first version publish data to redis and list grpc primitive stream as
the next feature.

