# perfguard

## Test mock application

```shell
curl -X POST http://localhost:8080/login -H "Content-Type: application/json" -d '{"user":"alice"}'
curl "http://localhost:8080/search?query=test"
```

## Locust

```shell
pip install locust
locust --host=http://localhost:8080
```