# Workshop for Kubernetes Demo


The application will be accessible at http:127.0.0.1:5000
 

##Endpoints

```/```
    return "Hello, from Python in Docker!!"


```/create/<float:coordinate>/<string:name>```
	return "Success | Error" coordinate is created.


``'/get/<string:name>'``
	return "Coordinates to given name"



##Get Started

Build the image using the following command

```bash
$ docker build -t dynamo-flask:latest .
```

Run the Docker container using the command shown below.

```bash
$ docker run -d -p 5000:5000 dynamo-flask:latest
```

