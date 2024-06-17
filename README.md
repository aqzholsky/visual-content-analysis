## REST Backend Service for Visual Content Analysis

### Project Description
The project provides an asynchronous uploading, analysis, and retrieval of information about photo and video materials.

### Quickstart

#### Create .env file
```shell
DEBUG=<true|false> # true
ONNX_MODEL_NAME=<path_to_model.onnx> # efficientnet-lite4-11.onnx
ONNX_MODEL_URL=<url_to_model.onnx> # https://github.com/onnx/models/blob/main/validated/vision/classification/efficientnet-lite4/model/efficientnet-lite4-11.onnx?raw=true
LABELS_MAP_PATH=<path_to_labels_map.txt> # labels_map.txt
LABELS_MAP_URL=<url_to_labels_map.txt> # https://github.com/onnx/models/blob/main/validated/vision/classification/efficientnet-lite4/dependencies/labels_map.txt?raw=true

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
