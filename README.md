To start the mysql server you need to do the following steps

$ /etc/init.d/mysql start
$ mysql
$ SET GLOBAL sql_mode="";

To build the docker

To run the docker
`docker run  -p 5000:5000 --rm leguark/smartvp:v0.2.4`