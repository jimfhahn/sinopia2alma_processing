from lxml import etree as ET
from copy import deepcopy


# a relationship modification function for the Work graph
def modify_xml(input_file, output_file):
    # Parse the XML file
    tree = ET.parse(input_file)
    work_graph = tree.getroot()

    # Define namespaces
    namespaces = {'bf': 'http://id.loc.gov/ontologies/bibframe/',
                  'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
                  'rdfs': 'http://www.w3.org/2000/01/rdf-schema#'}

    # Find all bf:Work elements
    works = work_graph.xpath('//bf:Work', namespaces=namespaces)

    for work in works:
        work_about = work.attrib['{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about']

        # Find the bf:relatedTo element with the same rdf:resource attribute value
        related_to = work_graph.xpath(f'//bf:relatedTo[@rdf:resource="{work_about}"]', namespaces=namespaces)

        if related_to:
            # Remove the rdf:resource attribute from the bf:relatedTo element
            related_to[0].attrib.pop('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource', None)

            # Clone the bf:Work element and append it under the bf:relatedTo element
            cloned_work = deepcopy(work)
            related_to[0].append(cloned_work)

            # Remove the original bf:Work element that was cloned
            work.getparent().remove(work)

    # save the modified XML to a file
    with open(output_file, 'wb') as f:
        f.write(ET.tostring(work_graph, pretty_print=True))