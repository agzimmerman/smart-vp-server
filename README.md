To build a Docker image (for example)

    cd smart-vp-server
  
    docker build --no-cache -t zimmerman/smartvp .

To run the a container (for example)

    docker run  -p 5000:5000 --rm zimmerman/smartvp
  
