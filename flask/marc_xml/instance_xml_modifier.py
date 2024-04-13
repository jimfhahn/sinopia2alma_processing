from lxml import etree as ET
from copy import deepcopy

# a relationship modification function for the Instance graph
def modify_xml(input_file, output_file):
    # Parse the XML file
    tree = ET.parse(input_file)
    instance_graph = tree.getroot()

    # Define namespaces
    namespaces = {'bf': 'http://id.loc.gov/ontologies/bibframe/',
                  'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
                  'rdfs': 'http://www.w3.org/2000/01/rdf-schema#'}

    # Find all bf:Instance elements
    instances = instance_graph.xpath('//bf:Instance', namespaces=namespaces)

    for instance in instances:
        instance_about = instance.attrib['{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about']

        # Find the bf:relatedTo element with the same rdf:resource attribute value
        related_to = instance_graph.xpath(f'//bf:relatedTo[@rdf:resource="{instance_about}"]', namespaces=namespaces)

        if related_to:
            # Remove the rdf:resource attribute from the bf:relatedTo element
            related_to[0].attrib.pop('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource', None)

            # Clone the bf:Instance element and append it under the bf:relatedTo element
            cloned_instance = deepcopy(instance)
            related_to[0].append(cloned_instance)

            # Remove the original bf:Instance element that was cloned
            instance.getparent().remove(instance)

    # save the modified XML to a file
    with open(output_file, 'wb') as f:
        f.write(ET.tostring(instance_graph, pretty_print=True))