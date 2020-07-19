[issue-template]: ../../../../../issues/new?template=BUG_REPORT.md
[feature-template]: ../../../../../issues/new?template=FEATURE_REQUEST.md

![singnetlogo](../assets/singnet-logo.jpg?raw=true 'SingularityNET')

# Gene Annotation Service


### List of annotations for a given list of genes:

1. **Gene Ontology Annotation**:

	Find list of [Gene Ontology (GO)](http://geneontology.org/) terms that the gene is a member of, it can also return `n` number of parent GO terms.

2. **Pathway Annotation**:

	Finds the [Reactome](https://reactome.org/) pathways ID's including a given list of genes and the small molecules and proteins in the selected pathways.

3. **Protein Interaction Annotation**:

	Find known interacting proteins from the [BIOGRID](https://thebiogrid.org/) protein interaction database.

###### Datasets

1. [Gene Ontology](http://www.berkeleybop.org/ontologies/go.obo):

Three sets of concepts describing biological processes, chemical functions, and cellular locations associated with gene products, organized as directed acyclic graphs

2.  [GO annotation](http://geneontology.org/gene-associations/gene_association.goa_ref_human.gz):

Assigns human gene symbols to relevant concepts (GO terms) in the Gene Ontology
(Gene ID (gene symbol) and GO ID)


3. [Reactome](https://reactome.org/download/current/interactors/reactome.homo_sapiens.interactions.psi-mitab.txt):

Curated metabolic and signaling pathways



4. [BIOGRID](BIOGRID-ORGANISM-Homo_sapiens-3.5.166.tab2.txt):

Contains experimentally verified and computationally predicted protein-protein interactions


## Getting Started


### Requirements

- [Python 3.6.5](https://www.python.org/downloads/release/python-365/)
- [Node 8+ w/npm](https://nodejs.org/en/download/)



### Development

Clone this repository:

```
$ git clone --recursive https://github.com/mozi-ai/annotation-service.git

$ cd annotation-service
```

### Calling the service:


#### 1. Using the [SingularityNET DApp](beta.singularitynet.io)

1a. Input a list of space separated Human gene symbols or upload a file that has gene symbols on each line and click `Enter`

1b. Select the Annotation you want along with the filter options

1c. Click Submit and Sign your request to send it to the service


#### 2. Using the [snet-cli](https://github.com/singnet/snet-cli)

2a. Assuming that you have an open channel (`id: 0`) to this service call using the following command

```
$ snet client call snet gene-annotation-service Annotate query.json
```

The **query.json** file has the gene symbol(s) and the annotations you want to use. A sample JSON file looks like this:



    {
        "annotations": [{
            "functionName": "gene-go-annotation",
            "filters": [{
                "filter": "namespace",
                "value": "biological_process cellular_component molecular_function"
            },
            {
                "filter": "parents",
                "value": "0"
            }]
        }, {
            "functionName": "biogrid-interaction-annotation",
            "filters": []
        }],
        "genes": [{
            "geneName": "SPAG9"
        }]
    }

## Contributing and Reporting Issues

Please read our [guidelines](https://github.com/singnet/wiki/blob/master/guidelines/CONTRIBUTING.md#submitting-an-issue) before submitting an issue.
If your issue is a bug, please use the bug template pre-populated [here][issue-template].
For feature requests and queries you can use [this template][feature-template].

## Authors
* **Michael Duncan** - *michael@singularitynet.io*
* **Enkuselassie Wondeson** - *enku@singularitynet.io*
* **Abdulrahman Semrie** - *xabush@singularitynet.io*
* **Yisehak Abreham** - *abrehamy@singularitynet.io* 

<i class="fa fa-copyright"/>2019 [SingularityNET](https://www.singularitynet.io)
