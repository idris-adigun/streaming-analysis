##Build image

```
docker build -t network_monitor:1.0.0 .
```

#run container

```
docker run -dit --name test_monitor -e PORTS=514 -e LOG_PATH=/app/logs/data.log test_monitor:1.0.1
```
