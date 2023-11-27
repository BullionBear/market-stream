# market-stream

## gRPC
```commandline
python -m grpc_tools.protoc -I./protoc/ --python_out=./generated/ --grpc_python_out=./generated/ market_stream.proto
```