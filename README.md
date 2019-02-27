[issue-template]: ../../issues/new?template=BUG_REPORT.md
[feature-template]: ../../issues/new?template=FEATURE_REQUEST.md

![singnetlogo](docs/assets/singnet-logo.jpg 'SingularityNET')

## Gene Annotation service

- Accepts list of human [HGNC](https://www.genenames.org/tools/search/#!/genes) gene symbols, finds annotations from example databases and displays the results as a browser-based interactive graph visualization.

- Results can be downloaded as a JSON file viewable in cytoscape, a set of plain text tables, and an opencog atomese scheme file.


### Local Setup

1. Clone the Project

    ```git clone --recursive https://github.com/MOZI-AI/annotation-service.git```

2. Define the following Environment variables. `$SERVER_ADDR` and `$SERVER_PORT`. If running on a local machine set `$SERVICE_ADDR` to `localhost`


        $ export SERVICE_ADDR=<ADDR>

        $ export SERVER_PORT=<PORT>


3. Start the docker

        docker-compose up

3.  You should be able to access the annotation service UI at

        http://$SERVICE_ADDR:$SERVER_PORT

If you would like to run in production mode, which will load large datasets into the atompspace, you can change line number 15 in `docker-compose.yml` to `1`
If you don't want to run the [snet daemon](https://github.com/singnet/snet-daemon), you can comment lines 18-40 in `circus.ini` file.