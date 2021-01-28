To start the mysql server you need to do the following steps

$ /etc/init.d/mysql start
$ mysql
$ SET GLOBAL sql_mode="";

To build a Docker image (for example)

  `docker build --no-cache -t zimmerman/smartvp` 

To run the a container (for example)

  `docker run  -p 5000:5000 --rm zimmerman/smartvp`
  
