python3 -m grpc.tools.protoc -I./modules/person-grpc --python_out=./modules/person-grpc --grpc_python_out=./modules/person-grpc ./modules/person-grpc/person_service.proto
python3 -m grpc.tools.protoc -I./modules/person-grpc --python_out=./modules/api/ --grpc_python_out=./modules/api/ ./modules/person-grpc/person_service.proto

python3 -m grpc.tools.protoc -I./modules/location-grpc --python_out=./modules/location-grpc/ --grpc_python_out=./modules/location-grpc/ ./modules/location-grpc/location_service.proto
