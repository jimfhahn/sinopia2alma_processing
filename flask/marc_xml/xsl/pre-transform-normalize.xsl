<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:sinopiabf="http://sinopia.io/vocabulary/bf/"
  xmlns:bflc="http://id.loc.gov/ontologies/bflc/"
  xmlns:bf="http://id.loc.gov/ontologies/bibframe/"
  xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <xsl:output method="xml" indent="yes"/>
  
  <!-- Identity transform -->
  <xsl:template match="@*|node()">
    <xsl:copy>
      <xsl:apply-templates select="@*|node()"/>
    </xsl:copy>
  </xsl:template>

  <!-- Match sinopiabf:nonfiling and replace it with bflc:nonSortNum -->
  <xsl:template match="sinopiabf:nonfiling">
    <bflc:nonSortNum rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">
      <xsl:value-of select="."/>
    </bflc:nonSortNum>
  </xsl:template>

  <!-- Match bf:creationDate and add rdf:datatype attribute -->
  <xsl:template match="bf:creationDate">
    <bf:creationDate rdf:datatype="http://www.w3.org/2001/XMLSchema#date">
      <xsl:value-of select="."/>
    </bf:creationDate>
  </xsl:template>

<!-- Match bflc:PrimaryContribution and replace it with bf:PrimaryContribution -->
<xsl:template match="bflc:PrimaryContribution">
  <bf:PrimaryContribution>
    <xsl:apply-templates select="@*|node()"/>
  </bf:PrimaryContribution>
</xsl:template>

<!-- the following will make sure edtf does not have trailing slash if it is present  -->

<xsl:template match="bf:date/@rdf:datatype" xmlns:bf="http://id.loc.gov/ontologies/bibframe/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <xsl:attribute name="rdf:datatype" namespace="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
    <xsl:choose>
      <xsl:when test="contains(., 'http://id.loc.gov/datatypes/edtf/')">
        <xsl:value-of select="concat('http://id.loc.gov/datatypes/edtf', substring-after(., 'http://id.loc.gov/datatypes/edtf/'))"/>
      </xsl:when>
      <xsl:otherwise>
        <xsl:value-of select="."/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:attribute>
</xsl:template>


</xsl:stylesheet>