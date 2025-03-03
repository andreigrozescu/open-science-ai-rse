# AI and Open Science in Research Software Engineering

I am a Computer Science student working on this project as part of my coursework. The objective is to apply text analysis techniques to open-access research articles using Grobid. The project involves:

    -Extracting text from 10 open-access research papers.
    -Generating a keyword cloud from the abstracts.
    -Visualizing the number of figures per article.
    -Compiling a list of links found in each paper.
    
    # Docker Installation Guide

## Prerequisites
Before running the project using Docker, ensure you have the following installed:
- **Docker**: Install it from [Docker's official website](https://docs.docker.com/get-docker/)

## 1. Clone the Repository
First, clone the project repository from GitHub:
```bash
git clone https://github.com/andreigrozescu/open-science-ai-rse.git
cd open-science-ai-rse
```

## 2. Build the Docker Image
Since the `Dockerfile` is already provided in the repository, simply run the following command to build the Docker image:
```bash
docker build -t open-science-ai-rse .
```
This command:
- Reads the `Dockerfile`
- Pulls the Python 3.10 base image
- Installs dependencies
- Copies the project files
- Creates the image `open-science-ai-rse`

## 3. Verify the Image
Once the build is complete, verify that the image was created successfully:
```bash
docker images
```
You should see `open-science-ai-rse` listed.

## 4. Run the Grobid Server (Required for Processing)
Start the Grobid server before running the analysis:
```bash
docker run -d --name grobid-server -p 8070:8070 -p 8071:8071 lfoppiano/grobid:0.8.0
```
This command runs the Grobid server in the background (`-d`).

## 5. Run the Analysis Container
Now, run the project container, connecting it to the Grobid server:
```bash
docker run --rm --name paper_analysis --network="host" \
    -v $(pwd)/papers:/app/papers \
    -v $(pwd)/output:/app/output \
    open-science-ai-rse
```
Explanation:
- `--rm`: Deletes the container after execution
- `--network="host"`: Ensures the container can communicate with Grobid
- `-v $(pwd)/papers:/app/papers`: Maps local `papers/` folder to the container
- `-v $(pwd)/output:/app/output`: Stores results in the local `output/` folder

## 6. (Optional) Check Logs
To monitor the execution logs:
```bash
docker logs -f paper_analysis
```

## 7. Stop and Clean Up
After execution, you can stop and remove all containers:
```bash
docker stop grobid-server
```
If needed, remove all containers and images:
```bash
docker system prune -a
```

## Conclusion
You have successfully deployed and run the project using Docker. The analysis results can be found in the `output/` directory.


