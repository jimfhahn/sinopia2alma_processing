from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import RDF
from name_space.alma_ns import alma_namespaces
from marc_xml import instance_xml_modifier


def lc_bfxml_instance(uri):
    filename = "lc_bfxml_instance.xml"
    instance_uri = uri
    instance_uri = URIRef(instance_uri)
    work_uri = None
    instance_graph = Graph()
    work_graph = Graph()
    instance_graph.parse(instance_uri)

    # Define the bf and bflc namespaces
    bf = Namespace("http://id.loc.gov/ontologies/bibframe/")
    for prefix, url in alma_namespaces:
        instance_graph.bind(prefix, url)
    work_uri = instance_graph.value(subject=instance_uri, predicate=bf.instanceOf)
    work_uri = URIRef(work_uri)
    # Explicitly state that work_uri is of type bf:Work
    work_graph.add((work_uri, RDF.type, bf.Work))
    # add the work to the instance graph
    instance_graph.add((instance_uri, bf.instanceOf, work_uri))
    # serialize the instance graph
    instance_xml = instance_graph.serialize(format="pretty-xml", encoding="utf-8")

    # write the instance graph to a file
    with open(filename, "wb") as file:
        file.write(instance_xml)

    # run the instance graph through the instance_xml_modifier
    instance_xml_modifier.modify_xml(filename, filename)


def remove_rdf_header():
    filename = "lc_bfxml_instance.xml"
    with open(filename, 'r') as file:
        lines = file.readlines()

    # Find the line with the opening '<rdf:RDF'
    start = next(i for i, line in enumerate(lines) if '<rdf:RDF' in line)

    # Find the line with the closing '>'
    end = next(i for i, line in enumerate(lines[start:], start=start) if '>' in line)

    # Remove all lines from start to end
    lines = lines[end+1:]

    with open(filename, 'w') as file:
        file.writelines(lines)
