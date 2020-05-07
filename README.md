[issue-template]: ../../issues/new?template=BUG_REPORT.md
[feature-template]: ../../issues/new?template=FEATURE_REQUEST.md

![singnetlogo](docs/assets/singnet-logo.jpg 'SingularityNET')

## Gene Annotation service

- Accepts list of human [HGNC](https://www.genenames.org/tools/search/#!/genes) gene symbols, finds annotations from selected databases, and displays the results as a browser-based interactive graph visualization.

- Current annotation sources include [Gene Ontology](http://geneontology.org), [Reactome](http://reactome.org) pathway database, and [BioGRID](http://thebiogrid.org) protein-protein interaction database.

- Results can be downloaded as a JSON file viewable in cytoscape, a set of plain text tables, and an opencog atomese scheme file.

!["gene annotation UI screenshot"](gene-annotation-screenshot.png?raw=true "gene annotation UI screenshot")

### Local Setup & Development

0. Download the datasets from https://mozi.ai/datasets


    **Note**: The datasets are compressed and you have to extract the files before using them.

1. Create `datasets` folder in your home directory and move the extracted datasets to that directory

2. Create `results` folder in your home directory and define a `RESULT_DIR` environment variable that points to the directory. This is where the scheme results will be stored. 

    ```
    cd $HOME
    mkdir results 
    export RESULT_DIR=$HOME/results
    ```

3. Define the following Environment variables.


        $ export SERVICE_ADDR=localhost

        $ export GRPC_ADDR=http://localhost:3001

        $ export RESULT_ADDR=http://localhost:3002
        
        $ export DATASET=$HOME/datasets


4. Clone the Project and checkout to the development branch.

    ```git clone --recursive https://github.com/MOZI-AI/annotation-service.git```


5. Go the project directory and Start the services

        docker-compose -f docker-compose-dev.yml up --build

6.  You should be able to access the annotation service UI at

        http://localhost:3003

If you would like to run in production mode, which will load large datasets into the atompspace, you can change line number 15 in `docker-compose.yml` to `1`
