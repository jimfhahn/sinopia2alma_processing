from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import RDF
from name_space.alma_ns import alma_namespaces


def lc_bfxml_work(uri):
    instance_uri = uri
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

    # serialize the work graph to an xml file
    work_graph.serialize(destination="lc_bfxml_work.xml", format="pretty-xml")


def remove_last_line():
    with open("lc_bfxml_work.xml", 'r') as file:
        lines = file.readlines()

    # remove last line if it is '</rdf:RDF>\n'
    if lines and lines[-1] == '</rdf:RDF>\n':
        lines = lines[:-1]

    with open("lc_bfxml_work.xml", 'w') as file:
        file.writelines(lines)
