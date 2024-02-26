from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import RDF
from name_space.alma_ns import alma_namespaces
from marc_xml import work_xml_modifier


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

    # check if the file has any relation elements that need to be processed to the Work graph
    # call the submodule to handle the work relationship
    work_xml_modifier.modify_xml("lc_bfxml_work.xml", "rel_lc_bfxml_work.xml")


def remove_last_line():
    with open("rel_lc_bfxml_work.xml", 'r') as file:
        lines = file.readlines()

    # remove last non-empty line if it is a closing RDF tag
    if lines[-1].strip() == "</rdf:RDF>":
        lines.pop()

    with open("bfxml_work.xml", 'w') as file:
        file.writelines(lines)
