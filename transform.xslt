<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="2.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:mh="https://zeticon.mediahaven.com/metadata/20.3/mh/"
    xmlns:mhs="https://zeticon.mediahaven.com/metadata/20.3/mhs/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <xsl:output method="xml" encoding="UTF-8" byte-order-mark="no" indent="yes"/>
    <xsl:param name="pid" />
    <xsl:param name="s3_object_key" />
    <xsl:param name="s3_bucket" />
    <xsl:template match="/">
        <mhs:Sidecar xmlns:mhs="https://zeticon.mediahaven.com/metadata/20.3/mhs/"
            xmlns:mh="https://zeticon.mediahaven.com/metadata/20.3/mh/" version="20.3">
            <xsl:apply-templates select="//mhs:Dynamic"/>
            <mhs:Descriptive>
                <mh:Title>Essence: pid: <xsl:value-of select = "$pid" /></mh:Title>
                <mh:Description>Main fragment for essence:
    - filename: <xsl:value-of select = "$s3_object_key" />
    - CP: vrt</mh:Description>
            </mhs:Descriptive>
        </mhs:Sidecar>
    </xsl:template>

    <xsl:template match="mhs:Dynamic">
        <xsl:copy>
            <object_use>archive_master</object_use>
            <object_level>file</object_level>
            <ie_type>n/a</ie_type>
            <s3_bucket><xsl:value-of select = "$s3_bucket" /></s3_bucket>
            <s3_domain>s3.viaa.be</s3_domain>
            <s3_object_owner>Pieter Adams+or-rf5kf25</s3_object_owner>
            <s3_object_key><xsl:value-of select = "$s3_object_key" /></s3_object_key>
            <xsl:apply-templates select="*[self::PID | self::CP | self::CP_id]"/>
            <xsl:for-each select="*[not(self::PID | self::CP | self::CP_id | self::object_use | self::object_level | self::ie_type | self::s3_bucket | self::s3_domain | self::s3_object_owner | self::s3_object_key)]">
                <xsl:copy>
                  <xsl:attribute name="strategy">OVERWRITE</xsl:attribute>
                  <xsl:apply-templates select="@*"/>
                </xsl:copy>
            </xsl:for-each>
       </xsl:copy>
    </xsl:template>

    <!--Identity template copies content forward, needed for a deep copy while adding new elements -->
    <xsl:template match="@*|node()">
        <xsl:copy>
            <xsl:apply-templates select="@*|node()"/>
        </xsl:copy>
    </xsl:template>
    
</xsl:stylesheet>
