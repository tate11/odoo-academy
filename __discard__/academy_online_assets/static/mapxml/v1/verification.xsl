<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:xd="http://www.oxygenxml.com/ns/doc/xsl"
    exclude-result-prefixes="xs xd"
    version="2.0">
    
    <xd:doc scope="stylesheet">
        <xd:desc>
            <xd:p><xd:b>Created on:</xd:b> Sep 14, 2018</xd:p>
            <xd:p><xd:b>Author:</xd:b> jorge</xd:p>
            <xd:p></xd:p>
        </xd:desc>
    </xd:doc>
    
    
    
    <xsl:template match="/">
        <html lang="en">
            <head>
                <meta charset="utf-8"/>
                <meta http-equiv="X-UA-Compatible" content="IE=edge"/>
                <meta name="viewport" content="width=device-width, initial-scale=1"/>
                
                <title>
                    <xsl:value-of select="notebook/name"/>
                </title>
                
                <link rel="stylesheet"
                    href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"
                    integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u"
                    crossorigin="anonymous"/>
                <link rel="stylesheet"
                    href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap-theme.min.css"
                    integrity="sha384-rHyoN1iRsVXV4nD0JutlnGaslCJuC7uwjduW9SVrLvRYooPp2bWYgmgJQIXwl/Sp"
                    crossorigin="anonymous"/>
                <link rel="stylesheet"
                    href="http://guanaco:8069/academy_online_assets/static/mapxml/v1/notebook.css"/>
                
                <style>
                    dd {
                        padding-left: 1cm;
                    }
                </style>
            </head>
            
            <body>
                
                <div class="container">
                    
                    <section>
                        <header><h2>Nodos principales sin clase definida</h2></header>
                        <div class="content">
                        <dl><xsl:apply-templates select="/notebook/activity/block/division/statement[not(@class)]"/></dl>
                        </div>
                    </section>
            
                    <section>
                        <header><h2>Ejercicios de Excel sin descripción</h2></header>
                        <div class="content">
                            <dl><xsl:apply-templates select="//statement[@class='list' and (not(description) or description[not(text())])]"/></dl>
                        </div>
                    </section>
                    
                </div>
        
            </body>
        </html>
        
    </xsl:template>
    
    
    
    <xsl:template match="/notebook/activity/block/division/statement[not(@class)]">
        <dt><xsl:value-of select="name"/></dt>
        <dd><xsl:call-template name="tree"></xsl:call-template></dd>
    </xsl:template>



    <xsl:template match="//statement[@class='list' and (not(description) or description[not(text())])]">
        <dt><xsl:value-of select="name"/></dt>
        <dd><xsl:call-template name="tree"></xsl:call-template></dd>
    </xsl:template>



    <xsl:template name="tree">
        <xsl:for-each select="ancestor-or-self::*">
            <xsl:text>/</xsl:text>
            <xsl:value-of select="name()" />
            <xsl:text>[</xsl:text>
            <xsl:value-of select="count(preceding-sibling::*[name() = name(current())])+1" />
            <xsl:text>]</xsl:text>
        </xsl:for-each>
    </xsl:template>
    
    
    
</xsl:stylesheet>