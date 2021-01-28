To start the mysql server you need to do the following steps

$ /etc/init.d/mysql start
$ mysql
$ SET GLOBAL sql_mode="";

To build the docker

To run the a container e.g.

  `docker run  -p 5000:5000 --rm leguark/smartvp:v0.2.7`
  
To build the container e.g.
    `docker build --no-cache -t leguark/smartvp:v0.2.7 .` 