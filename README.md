
# ML Model Serving

Serving a machine learning model on a Flask-based website.

## Structure

```

.
├── README.md
├── aws-client                                           
│   ├── single_node_with_docker_ansible_client           <- Part 3: launching and contextualizing two ec2 vm's, otherwise similar to part 2.
│   ├── single_node_with_docker_client                   <- Part 2: launching and contextualizing ec2 vm, running docker-compose to start servers.
│   └── single_node_without_docker_client                <- Part 1: launching and contextualizing ec2 vm, starting servers.
├── ci_cd                                                
│   ├── development_server                               <- Running development server.
│   └── production_server                                <- Running production server.
├── single_server_with_docker
│   └── production_server                                <- Part 2: Running single production server with docker-compose.
└── single_server_without_docker
    └── production_server                                <- Part 1: Running single production server.
```


## Description
In this project, a whole application is build for serving a machine learning model to end users where 
they can use it for inference. The application consists of a frontend server so that users can communicate 
with the model, a backend server that runs the logic and distributes incoming tasks to workers, and 
worker machines that handle the serving and computation. 
The frontend is a `Flask-based` server, the backend is a `Celery-based` server for asynchronous task queueing 
and scheduling, which in turn utilizes a `RabbitMQ` server for message broking. An `aws ec2` virtual machine 
acts as the worker server.

The project is divided into four sections as follows:
1. Single Server Deployment: One VM worker responsible for everything. Namely, the modelling part, frontend and backend servers are tightly coupled with it. `cloud-init` is used to automatically contextualize the worker server.

2. Single Server Deployment with Docker containers: The frontend and backend servers are dockerized so that they can be scaled up and down dynamically, which enables scaleability, fault tolerance and removes tight coupling with the server machine. `docker-compose` runs containers for each of the services.

3. Deployment of multiple server using Ansible: A new worker VM is added to the scene and the model development part gets decoupled with the serving part and moved to the new development VM, while the fronend&backend servers will be on the production server. `Ansible` is used for managing and orchestrating the `production` and `development` VMs. 

4. `CI/CD` is introduced into the whole process. Every time the model is improved, we would like to continuously and automatically deploy it to the live production server, hence for this reason `git hooks` is used to trigger certain actions everytime new code is pushed to a remote production repository.




## The web server
An example of how the website looks like:

![alt text](media/webserver?raw=true "Title")


## Author

- Hardy Hasan


## Original Authors
This repo is a fork from `https://github.com/sztoor/model_serving`