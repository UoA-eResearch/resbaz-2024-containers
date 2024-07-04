## Running containers

Docker main commands:
```
docker
  run        # Create and run a new container from an image
  ps         # List containers
  rm         # Remove one or more containers
  kill       # Kill one or more running containers
  exec       # Execute a command in a running container
  pull       # Download an image from a registry
  image      # Operations with images
  cp         # Copy files/folders between a container and the local filesystem
  logs       # Fetch the logs of a container
```

Docker run options:
```
docker run [options] image [command]
  --rm                                          # Automatically remove the container when it exits
  --interactive -i                              # Interactive session
  --tty         -t                              # Allocate a pseudo-TTY

  --name             name                       # Assign a name to the container
  --detach      -d                              # Run container in background

  --volume      -v   host_dir:container_dir     # Share a host directory inside the container
  --workdir     -w   container_dir              # Starting working directory inside the container
  --port        -p   host_port:container_port   # Publish a container's port(s) to the host
  --env         -e   VAR=value                  # Set environment variable inside container
  --env-file         /path/to/file              # Pass environment variables from file

  --user        -u   user                       # Use username in container
  --entrypoint       /path/to/executable        # Overwrite the default entrypoint of the image
```

### Examples

Run python code:
```
cd hello-world
docker run --rm -it -v ./python:/app python:alpine /app/hello-world.py
```

Run Node.js code:
```
docker run --rm -it -v ./nodejs:/app node:alpine node /app/hello-world.js
```

Run R code:
```
docker run --rm -it -v ./R:/app -w /app rocker/r-base R -f hello-world.R
```

Run R interactively:
```
docker run --rm -it -v ./R:/app -w /app rocker/r-base
```

Run an nginx web servers with a custom webpage:
```
docker run --rm -it --name nginx -p 8080:80 -d -v ./nginx:/usr/share/nginx/html nginx:alpine
curl localhost:8080
```

Run Rstudio (needs a browser!):
```
docker run --rm -it --name rstudio -e PASSWORD=password -p 8787:8787 -d rocker/rstudio
```

Clean up:
```
docker rm -f nginx rstudio
```

### Run, list, remove containers

Let's run the "official" hello-world example:
```
docker run hello-world
docker ps
docker ps -a
# docker rm (by name or id)
```

Notes:
- Image `hello-world` gets automatically pulled (downloaded) if not already present locally
- Containers have a default command to run (we'll see later how to change it)
- A container "dies" after running (unless we specify otherwise), but is not automatically removed
- Containers can be referenced by their ID or name (one is assigned by docker if none is specified by us)

Containers can be instructed to be removed after they run with `--rm`.:
```
docker run --rm hello-world
docker ps -a
```

Removing containers from another terminal:
```
docker run alpine sleep 3600
```

Practice: Remove previous container!

Syntactic sugar to kill and remove all containers:
```
docker rm -f $(docker ps -aq)
```

### Naming containers (`--name`)

Container names have to be unique, even if container is not running:
```
docker run --name my-first-container hello-world
docker ps -a
docker run --name my-first-container hello-world
docker rm my-first-container
```

### Executing non default commands

Each container is a new instance, where commands are executed inside the container:
```
docker run --rm alpine hostname
docker run --rm alpine hostname
docker run --rm alpine printenv
docker run --rm alpine cat /etc/os-release
```

Complex commands, pipes and redirections might need escaping and/or special syntax to differentiate what runs inside vs outside the container:
```
docker run --rm alpine hostname; hostname
docker run --rm alpine sh -c 'hostname; hostname'

docker run --rm alpine cat /etc/os-release | grep VERSION -1
docker run --rm alpine sh -c 'cat /etc/os-release | grep VERSION -1'
docker run --rm alpine sh -c 'cat /etc/os-release | grep VERSION -C 1'

docker run --rm alpine hostname > container-hostname.out && cat container-hostname.out
docker run --rm alpine sh -c 'hostname > container-hostname.in' && cat container-hostname.in
docker run --rm alpine sh -c 'hostname > container-hostname.in && cat container-hostname.in'
```

### Access container interactively (`-it`)

```
docker run --rm -it alpine
```

Sensible defaults: `--rm -it`

### Foreground vs background (`-d`): exec, logs, kill

We can run multiple containers in the background. Running containers in the background return the container ID:
```
docker run --rm -it -d --name sleeping-beauty-1 alpine
docker run --rm -it -d --name sleeping-beauty-2 alpine
docker ps
docker kill sleeping-beauty-1 sleeping-beauty-2
```

We can execute commands or access a container running in the background with `docker exec`:
```
docker run -d -it --name container-1 alpine
docker exec container-1 hostname
docker exec -it container-1 sh
```

Note that the container might need to run interactively if the command expects so:
```
docker run -d --name container-2 alpine
docker ps -a
docker run -d --name container-3 alpine sleep 3600
docker ps -a
docker rm -f container-1 container-2 container-3
```

We can access the container's STDOUT at any time:
```
docker run --rm --name logger -d alpine sh -c 'while true; do echo "$HOSTNAME is sleeping..."; sleep 2; done'
docker logs logger
docker logs -f logger           # Cancel with Ctrl+C
docker kill logger
```

### Exposing ports (`-p`)

Ports inside the container can be exposed and map to hosts in the port:

```
docker run --rm -d --name web-server -p 8080:80 nginx:alpine
docker logs web-server
curl localhost:8080
curl localhost:80          # Cannot access the port directly inside the container
docker exec web-server curl localhost:80
docker logs web-server
docker kill web-server
```

Keep in mind that the port must be free in the host.

### Sharing files (`-v`)

We can share our local filesystem with the container to provide input and/or preserve the output. Changes to a container are lost when it is removed.

Local paths can be mounted inside the container:
```
docker run --rm -v ./:/app alpine tree /app
```

We can specified a working ("starting") directory with `-w`:
```
docker run --rm -v ./:/app -w /app alpine pwd
```

Pratice: which is the default directory in the container?

Sharing files works as well in interactive containers:
```
docker run --rm -it -v ./:/app -w /app alpine                        # Exit with Ctrl+C
```

And background containers:
```
docker run --rm -it -d -v ./:/app -w /app --name shared alpine
docker exec -it shared sh
```

Mounting a single file is also possible:
```
echo 'File created in the host' > file.txt
docker run --rm -it -v ./file.txt:/app/inside-file.txt alpine ls -l /app
docker run --rm -it -v ./file.txt:/app/inside-file.txt alpine cat /app/inside-file.txt
```

Any modifications to shared files will be persisted in the host once the container exits, but you might run into permissions issues, depending on the user running in the host vs inside the container.

### Environment variables (`-e` and `--env-file`)

Environment variables can be passed to the container one by one, or set of them in a file:

```
docker run --rm nginx:alpine printenv
docker run --rm -e VAR0=value nginx:alpine printenv
docker run --rm --env-file my-env nginx:alpine printenv
docker run --rm -e VAR0=value --env-file my-env nginx:alpine printenv
```

Many popular containers use environment variables to configure their behaviour.

### Commands and Entrypoints

There are two ways of defining which command runs by default in a container: `COMMAND` and `ENTRYPOINT`. As we have seen earlier, to override the default command, one only needs to specify a new one at the end of the line. However, if the container defines `ENTRYPOINT`, the command parameter is instead appened to the one specified as entrypoint. To override this, one can use the `--entrypoint` option:

```
docker run --rm -it luisico/hostname                      # default entrypoint  --> "hostname"
docker run --rm -it luisico/hostname -h                   # append command "-h" --> "hostname -h"
docker run --rm -it luisico/hostname sh                   #             error   --> "hostname sh"
docker run --rm -it --entrypoint sh luisico/hostname      # change entrypoint   --> "sh"
```

Note that most modern containers implement a "smart" entrypoint that will execute arbitrary commands if the one passed does not follow a useful pattern.

### Permissions

By default containers run as the user defined when creating the image, and files created inside the container will transfer those permissions back to the host. This can create problems if the user in the host does not have permissions to read/write the new files:

```
docker run --rm -it -v ./:/app -w /app alpine id
docker run --rm -it -v ./:/app -w /app alpine sh -c 'echo "Inside container $HOSTNAME" > inside.txt'
ls -l
```

The result file `inside.txt` will have root as owner/group.

We can run as a different user with option `-u`. The user name needs to exist within the container:

```
docker run --rm -it -u user -v ./:/app -w /app alpine id
docker run --rm -it -u guest -v ./:/app -w /app alpine id
```

Or we can use any numeric id for the user (and the group if want too):

```
docker run --rm -it -u 1000 -v ./:/app -w /app alpine id
docker run --rm -it -u $(id -u) -v ./:/app -w /app alpine id
docker run --rm -it -u $(id -u):$(id -g) -v ./:/app -w /app alpine id

docker run --rm -it -u $(id -u):$(id -g) -v ./:/app -w /app alpine sh -c 'echo "Inside container $HOSTNAME" > inside-user.txt'
ls -l
```

Also note, that running containers as root can create security risks on the hosts and is considered bad practice.

## Creating Containers Images

Notes:
- When a container stops, changes are lost (i.e. pip install)
- We can create images with everything we need pre-installed:
  - Reproducible
  - Fast start, ready-to-go
- Reproducible process:
  - Provenance: how was the image created
  - Reproducible: the image does not change if we version it

### Images

```
docker image
  ls        # List images (or `docker images`)
  pull      # Download an image from a registry
  push      # Upload an image to a registry
  rm        # Remove an image
  prune     # Remove unused images
  build     # Build an image from a Dockerfile definition (or `docker build`)
  inspect   # Inspect build and properties of an image (or `docker inspect`)
  history   # Show the build history of an image
```

- Naming: `registry/org/name:tag`
  - `registry`: default is Docker Hub
    - Docker Hub: https://hub.docker.com
    - Quay: https://quay.io/search
    - Git platform: GitHub, GitLab
    - AWS, Google Cloud, Azure
    - Private
  - `org/name` is usually called the `repository` or image name
  - Only `name` is mandatory
  - Default tag is `latest`
  - Examples:
    - `ubuntu:24.04`
    - `ubuntu`
    - `ubuntu/mysql`
    - `quay.io/quay/ubuntu`
    - `localhost:5000/testing/ubuntu`
- Pull:
  - `docker pull image`
  - Image is downloded layer by layer
  - Existing layers are reused
  - `docker run` will pull the image if not present locally, but it will not check if there is a newer version in the registry
  - `docker pull` will download newer versions of an image already present locally
- Inspect: `docker inspect image`
- Keep an eye on disk space: `docker system df`

Practice:
- Search "python" at https://hub.docker.com
- Find "latest" tag
- Find "alpine" tag
- Pull different versions of python alpine images:
  ```
  docker pull python:alpine
  docker pull python:3-alpine
  docker pull python:3.12.4-alpine3.20

  docker pull python:3.9-alpine
  ```

### Creating an image from a Dockerfile

```
docker build [options] path
  --tag      -t   Tag name            # Image name

  --file     -f   Dockerfile          # Path to Dockerfile
  --progress      auto|plain|tty      # Verbosity
  --build-arg     ARG=value           # Pass build argument
  --no-cache                          # Invalidate cache
```

#### Campsites (develop and share your software)

We'll create a small python program to tally DOC campsites by region and type.

Build an image with our custom software:
```
cd campsites
docker build --progress plain -t campsites:1.0.0 .
docker image ls campsites
```

Test our image with a small test dataset:
```
cp test.csv data.csv
docker run --rm -it -v ./:/app campsites:1.0.0
```

Run with a full dataset from [DOC](https://doc-deptconservation.opendata.arcgis.com) or [data.gov.nz](https://www.data.govt.nz):
```
curl -L https://doc-deptconservation.opendata.arcgis.com/api/download/v1/items/c417dcd7c9fb47b489df1f9f0a673190/csv?layers=0 > data.csv
docker run --rm -it -v ./:/app campsites:1.0.0
```

#### Fastutils

[Fastutils](https://github.com/haghshenas/fastutils) is a light toolkit for parsing, manipulating and analysis of FASTA and FASTQ files.

Build images based on Debian and Alpine:
```
cd fastutils
docker build -t fastutils:3 .
docker build -t fastutils:3-alpine -f Dockerfile.alpine .
docker image ls fastutils
```

Test the images by calculating aminoacid content statistics on the human hemoglobin subunit beta from UniProt:
```
curl -L https://rest.uniprot.org/uniprotkb/P68871.fasta > hemoglobin.fasta
docker run --rm -v ./:/work -w /work fastutils:3 fastutils stat -i hemoglobin.fasta
```

We could also run the same command different ways:
```
docker run --rm -i fastutils:3 fastutils stat < hemoglobin.fasta
cat hemoglobin.fasta | docker run --rm -i fastutils:3 fastutils stat
```

Finally, we use the alpine image to convert from FASTA to FASTQ format:
```
docker run --rm -i fastutils:3-alpine fastutils format -q < hemoglobin.fasta > hemoglobin.fastq
```

#### Open Babel (compile open source software)

[Open Babel](https://openbabel.org) is a chemical toolbox designed to speak the many languages of chemical data.

[Instructions](https://openbabel.org/docs/Installation/install.html) to compile have been added to our Dockerfile.

Build the image for the latest code (previous released versions don't work correctly in Linux and the authors have not release a new one with the latests fixes):
```
cd openbabel
docker build --progress plain -t openbabel:latest .
docker image ls openbabel
```

We could have versioned the image using a specific commit:
```
docker build --progress plain -t openbabel:756ebaa --build-arg OPENBABEL_REF=756ebaa .
docker image ls | grep openbabel
```

Use the new image to display serotonin in the terminal and create a PNG image:
```
curl -L https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/CID/5202/record/SDF > serotonin.sdf
docker run --rm -it -v ./:/work -w /work openbabel serotonin.sdf -o ascii
docker run --rm -it -v ./:/work -w /work openbabel serotonin.sdf -O serotonin.png
```

Display ethanol from SMILES format:
```
docker run --rm openbabel -':CCO' -o ascii
docker run --rm openbabel -':CCO' -o ascii -h
docker run --rm openbabel -':CCO' -o png -h -xa > ethanol.png
```
