import flask
from flask import request
import flask_restful
from rdflib import Graph
from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import RDF
from lxml import etree as ET
from alma_ns import alma_namespaces

app = flask.Flask(__name__)
api = flask_restful.Api(app)

@app.route('/rdf2workxml', methods=['POST'])
def rdf2workxml():
    # a uri is passed in the request
    instance_uri = request.args.get('instance_uri')
    #quality check the file
    if instance_uri is None:
        #return 500 error
        return "No data received", 500
    instance_uri = URIRef(instance_uri)
    work_uri = None
    instance_graph = Graph()
    work_graph = Graph()
    instance_graph.parse(instance_uri)
     # Define the bf and bflc namespaces
    bf = Namespace("http://id.loc.gov/ontologies/bibframe/")
    for prefix, url in alma_namespaces:
        work_graph.bind(prefix, url)
    work_uri = instance_graph.value(
        subject=URIRef(instance_uri), predicate=bf.instanceOf
        )
    work_uri = URIRef(work_uri)
    # Explicitly state that work_uri is of type bf:Work
    work_graph.add((work_uri, RDF.type, bf.Work))

    # parse the work graph
    work_graph.parse(work_uri)

    # add the instance to the work graph
    work_graph.add((work_uri, bf.hasInstance, URIRef(instance_uri)))

    # serialize the work graph
    bfwork_alma_xml = work_graph.serialize(format="pretty-xml", encoding="utf-8")
    tree = ET.fromstring(bfwork_alma_xml)
    
    # serialize to xml
    bfwork_alma_xml = work_graph.serialize(format="pretty-xml", encoding="utf-8")
    tree = ET.fromstring(bfwork_alma_xml)
    # apply xslt to normalize instance
    xslt = ET.parse("normalize-work-sinopia2alma.xsl")
    transform = ET.XSLT(xslt)
    bfwork_alma_xml = transform(tree)
    bfwork_alma_xml = ET.tostring(
        bfwork_alma_xml, pretty_print=True, encoding="utf-8"
        )
    return bfwork_alma_xml

if __name__ == '__main__':
    app.run(debug=True, port=5000)
