import flask
from flask import request
import flask_restful
from rdflib import Graph
from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import RDF
from lxml import etree as ET
from name_space.alma_ns import alma_namespaces

app = flask.Flask(__name__)
api = flask_restful.Api(app)

@app.route('/rdf2instancexml', methods=['POST'])
def rdf2instancexml():
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
        instance_graph.bind(prefix, url)
    work_uri = instance_graph.value(subject=URIRef(instance_uri), predicate=bf.instanceOf)
    work_uri = URIRef(work_uri)
    # Explicitly state that work_uri is of type bf:Work
    work_graph.add((work_uri, RDF.type, bf.Work))
    # add the work to the instance graph
    instance_graph.add((instance_uri, bf.instanceOf, URIRef(work_uri)))
    # serialize the instance graph
    instance_alma_xml = instance_graph.serialize(format="pretty-xml", encoding="utf-8")
    tree = ET.fromstring(instance_alma_xml)
    # apply xslt to normalize instance
    xslt = ET.parse("xsl/normalize-instance-sinopia2alma.xsl")
    transform = ET.XSLT(xslt)
    instance_alma_xml = transform(tree)
    instance_alma_xml = ET.tostring(
        instance_alma_xml, pretty_print=True, encoding="utf-8"
        )
    return instance_alma_xml, 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
