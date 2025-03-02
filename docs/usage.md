Initilize Gobrid (Docker must be running): 
```
docker run --rm --init --ulimit core=0 -p 8070:8070 lfoppiano/grobid:0.8.0
```

Once Gobrid is up and running you just need to execute the 'main.py' file. 
