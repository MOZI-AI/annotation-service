[issue-template]: ../../issues/new?template=BUG_REPORT.md
[feature-template]: ../../issues/new?template=FEATURE_REQUEST.md

![singnetlogo](docs/assets/singnet-logo.jpg 'SingularityNET')

## Gene Annotation service

- Accepts list of human [HGNC](https://www.genenames.org/tools/search/#!/genes) gene symbols, finds annotations from selected databases, and displays the results as a browser-based interactive graph visualization.

- Current annotation sources include [Gene Ontology](http://geneontology.org), [Reactome](http://reactome.org) pathway database, and [BioGRID](http://thebiogrid.org) protein-protein interaction database.

- Results can be downloaded as a JSON file viewable in cytoscape, a set of plain text tables, and an opencog atomese scheme file.

!["gene annotation UI screenshot"](gene-annotation_Screen-Shot-2019-03-14.jpg?raw=true "gene annotation UI screenshot")

### Local Setup

    
1. Download Datasets

    ```
    wget -r --no-parent https://mozi.ai/datasets/
    mv mozi.ai/datasets/* datasets
    rm -rf mozi.ai
    rm datasets/index.html
    ```



2. Define the following Environment variables. `$SERVER_ADDR` and `$SERVER_PORT`. If running on a local machine set `$SERVICE_ADDR` to `localhost`


        $ export SERVICE_ADDR=<ADDR>

        $ export SERVER_PORT=<PORT>
        
        $ export DATASET=<directory dataset were downloaded>


3. Clone the Project

    ```git clone --recursive https://github.com/MOZI-AI/annotation-service.git```

4. Go the project directory and Start the services

        docker-compose up --build

5.  You should be able to access the annotation service UI at

        http://$SERVICE_ADDR:$SERVER_PORT

If you would like to run in production mode, which will load large datasets into the atompspace, you can change line number 15 in `docker-compose.yml` to `1`
If you don't want to run the [snet daemon](https://github.com/singnet/snet-daemon), you can comment lines 18-40 in `circus.ini` file.
