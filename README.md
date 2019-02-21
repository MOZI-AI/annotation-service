[issue-template]: ../../issues/new?template=BUG_REPORT.md
[feature-template]: ../../issues/new?template=FEATURE_REQUEST.md

![singnetlogo](docs/assets/singnet-logo.jpg 'SingularityNET')

## Gene Annotation service

- Accepts list of human [HGNC](https://www.genenames.org/tools/search/#!/genes) gene symbols, finds annotations from example databases and displays the results as a browser-based interactive graph visualization.

- Results can be downloaded as a JSON file viewable in cytoscape, a set of plain text tables, and an opencog atomese scheme file.

### List of annotations for a given list of genes:

1. Gene Ontology Annotation:

	Find list of [Gene Ontology (GO)](http://geneontology.org/) terms that the gene is a member of, it can also traverse to `n` number of parent GO's.

2. Pathway Annotation:

	Finds the [Small Molecule Pathway Database (SMPDB)](http://smpdb.ca/) and [Reactome](https://reactome.org/) pathways ID's for a given list of genes and the small molecules and Proteins in the selected pathways.

3. Protein Interaction Annotation:

	Find known interacting proteins from the [BIOGRID](https://thebiogrid.org/) protein interaction database.

###### Datasets

1. [Gene Ontology](http://www.berkeleybop.org/ontologies/go.obo):

Three sets of concepts describing biological processes, chemical functions, and cellular locations associated with gene products, organized as directed acyclic graphs.

2.  [GO annotation](http://geneontology.org/gene-associations/gene_association.goa_ref_human.gz):

Assigns human gene symbols to GO and their corresponding GO term
(Gene ID (gene symbol) and GO ID)


3. [Reactome](https://reactome.org/download/current/interactors/reactome.homo_sapiens.interactions.psi-mitab.txt):

Curated metabolic and signaling pathways


4. [SMPDB](http://smpdb.ca/downloads/smpdb_proteins.csv.zip):

Includes mostly metabolic pathways with proteins and small molecules.


5. [BIOGRID](BIOGRID-ORGANISM-Homo_sapiens-3.5.166.tab2.txt):

Contains experimentally verified protein-protein interactions

### Running

1. Clone the Project

    ```git clone --recursive https://github.com/MOZI-AI/annotation-service.git```

2. Define the following Environment variables. `$SERVER_ADDR` and `$SERVER_PORT`. If running on a local machine set `$SERVER_ADDR` to `http://localhost`


        $ export SERVER_ADDR=<ADDR>

        $ export SERVER_PORT=<PORT>


3. Start the docker

        docker-compose up

3.  You should be able to access the annotation service UI at

        http://$SERVER_ADDR:$SERVER_PORT

If you would like to run in production mode, which will load large datasets into the atompspace, you can change line number 15 in `docker-compose.yml` to `1`
If you don't want to run the snet kovan network, you can comment lines 18-40 in `circus.ini` file.