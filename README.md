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
- Implement a GO version
- Print status for recording symbol (*)
- Connection retry (**)
- Auto push Docker image to DockerHub (*)
- 