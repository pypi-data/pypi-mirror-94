To regenerate python proto, download new proto files from https://github.com/Netflix/conductor/tree/master/grpc/src/main/proto
Rename the directory grpc to conductor grpc. Rename any imports in the proto files referencing grpc to be conductor_grpc.
Then run `python -m grpc_tools.protoc -I=proto --python_out=. --grpc_python_out=. proto/*/*.proto`
