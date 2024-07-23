## REST Backend Service for Visual Content Analysis

### Project Description
The project provides an asynchronous uploading, analysis, and retrieval of information about photo and video materials.

### Quickstart

#### Create ``.env`` file (or rename and modify ``.env.example``) in project root and set environment variables for application: ::
```shell
touch .env
echo "DEBUG=true" >> .env
echo "ONNX_MODEL_NAME=efficientnet-lite4-11.onnx" >> .env
echo "ONNX_MODEL_URL=https://github.com/onnx/models/blob/main/validated/vision/classification/efficientnet-lite4/model/efficientnet-lite4-11.onnx?raw=true" >> .env
echo "LABELS_MAP_PATH=labels_map.txt" >> .env
echo "LABELS_MAP_URL=https://github.com/onnx/models/blob/main/validated/vision/classification/efficientnet-lite4/dependencies/labels_map.txt?raw=true" >> .env
echo "MONGO_INITDB_ROOT_USERNAME=root" >> .env
echo "MONGO_INITDB_ROOT_PASSWORD=example" >> .env
echo "MONGODB_URL=mongodb://root:example@db:27017" >> .env
echo "MAX_CONNECTIONS_COUNT=10" >> .env
echo "MIN_CONNECTIONS_COUNT=1" >> .env
```

#### Run docker container
```bash
docker-compose up -d --build
```

### Swagger Documentation
You can access the automatically generated Swagger documentation for the API at http://localhost:8000/docs


### Testing Instructions

#### You can use [Postman collection](https://github.com/user-attachments/files/15876549/collection.json) to run requests for creating analyses and retrieving results.

#### Testing the POST `/analysis` Method
```bash
curl -X POST "http://localhost:8000/analysis" -F "file=@path/to/your/file.jpg"
```
> The response should contain a requestId.

#### Testing the GET `/analysis/{requestId}` Method
```bash
curl -X GET "http://localhost:8000/analysis/{requestId}"
```
> The response should contain the analysis results.

#### Testing the DELETE `/analysis/{requestId}` Method
```bash
curl -X DELETE "http://localhost:8000/analysis/{requestId}"
```
> The response should confirm the deletion of data.
