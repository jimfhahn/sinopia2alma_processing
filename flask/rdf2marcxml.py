from saxonche import PySaxonProcessor
import lxml.etree as ET
from marc_xml.lc_bfxml_work import lc_bfxml_work, remove_last_line
from marc_xml.lc_bfxml_instance import lc_bfxml_instance, remove_rdf_header
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

@app.route('/rdf2marcxml', methods=['POST'])
def rdf2marcxml():
    instance_uri = request.form.get('instance_uri')
    #quality check the file
    if instance_uri is None:
        #return 500 error
        return "No data received", 500
    lc_bfxml_work(instance_uri)  
    remove_last_line() 
    lc_bfxml_instance(instance_uri) 
    remove_rdf_header() 
    # combine the two files, work first
    with open("bfxml_work.xml", "r") as work_file:
        work = work_file.read()
    with open("lc_bfxml_instance.xml", "r") as instance_file:
        instance = instance_file.read()
    #save as a file
    with open("LoC_Work_Instance.xml", "w") as combined_file:
        combined_file.write(work + instance)

    # add the sinopiabf namespace to the combined file
    with open("LoC_Work_Instance.xml", "r") as file:
        filedata = file.read()
    filedata = filedata.replace('<rdf:RDF', '<rdf:RDF xmlns:sinopiabf="http://sinopia.io/vocabulary/bf/"')
    with open("LoC_Work_Instance.xml", "w") as file:
        file.write(filedata)

    # apply "pre-transform-normalize.xsl" for normalization
    dom = ET.parse("LoC_Work_Instance.xml")
    xslt = ET.parse("marc_xml/xsl/pre-transform-normalize.xsl")
    transform = ET.XSLT(xslt)
    newdom = transform(dom)
    with open("LoC_Work_Instance_Normalized.xml", "w") as f:
        f.write(str(newdom))    

    # use PySaxonProcessor to appy bibframe2marc.xsl to LoC_Work_Instance_Normalized.xml
    with PySaxonProcessor(license=False) as proc:
        xsltproc = proc.new_xslt30_processor()
        document = proc.parse_xml(xml_file_name="LoC_Work_Instance_Normalized.xml")
        executable = xsltproc.compile_stylesheet(stylesheet_file="bibframe2marc.xsl")
        output = executable.transform_to_string(xdm_node=document)
        #save as a file
        with open("marc.xml", "w") as f:
            f.write(output)
    return output, 200

if __name__ == "__main__":
    app.run(debug=True)