<?xml version="1.0"?>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    
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
                <link rel="stylesheet" href="http://localhost:8069/academy_online_assets/static/mapxml/v1/notebook.css"/>
                
            </head>
            
            <body>
                
                <div class="container">
                    <xsl:for-each select="notebook/activity">
                        <section>
                            <!-- <header>
                                <h2>
                                    <xsl:value-of select="name"/>
                                </h2>
                            </header> -->
                            <xsl:for-each select="block">
                                <article>
                                    <xsl:choose>
                                        <xsl:when test="name">
                                            <header>
                                                <h3>
                                                    <xsl:value-of select="name"/>
                                                </h3>
                                            </header>
                                        </xsl:when>
                                    </xsl:choose>
                                    <div class="article-content">
                                        <xsl:for-each select="division">
                                            <div class="division">
                                                <xsl:choose>
                                                    <xsl:when test="name">
                                                        <h4>
                                                            <xsl:value-of select="name"/>
                                                        </h4>
                                                    </xsl:when>
                                                </xsl:choose>
                                                <xsl:for-each select="target">
                                                    <xsl:choose>
                                                        <xsl:when test="name">
                                                            <div class="target">
                                                                <strong><xsl:value-of select="name"/>:</strong><xsl:text> </xsl:text> 
                                                                '<span> <xsl:value-of select="value"  disable-output-escaping="yes" /></span>'.
                                                            </div>
                                                        </xsl:when>
                                                        <xsl:otherwise>
                                                            <div>
                                                                <xsl:value-of select="value" disable-output-escaping="yes"/>
                                                            </div>
                                                        </xsl:otherwise>
                                                    </xsl:choose>
                                                </xsl:for-each>
                                                <xsl:for-each select="statement">
                                                    <xsl:if test="default = 'Falso'">
                                                        <div class="statement {@class}">
                                                            <xsl:apply-templates select="."/>
                                                        </div>
                                                    </xsl:if>
                                                </xsl:for-each>
                                            </div>
                                        </xsl:for-each>
                                    </div>
                                </article>
                            </xsl:for-each>
                            <xsl:choose>
                                <xsl:when test="preview">
                                    <img class="preview-inline" src="{preview}"></img>
                                </xsl:when>
                            </xsl:choose>
                        </section>
                        
                    </xsl:for-each>
                    
                    <section style="display: none">
                        <header>
                            <h2>Estadísdicas</h2>
                        </header>
                        <article>
                            <header>
                                <h3>Instrucciones</h3>
                            </header>
                            <div class="article-content">
                                <div>
                                    <strong>Mecanografía: </strong>
                                    <span><xsl:value-of
                                        select="string-length(//statement[@type = 'typing']/value)"
                                    /></span> caracteres. </div>
                                <div>
                                    <strong>Maquetación: </strong>
                                    <span><xsl:value-of select="count(//statement)"/></span>
                                    instrucciones. </div>
                            </div>
                        </article>
                    </section>
                </div>
                <!-- container -->
                
                <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
                <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"/>
                <!-- Include all compiled plugins (below), or include individual files as needed -->
                <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"/>
            </body>
        </html>
    </xsl:template>
    
    <xsl:template match="statement" name="statement">
        <span>
            <xsl:choose>
                <xsl:when test="name">
                    <strong><xsl:value-of select="name"/>: </strong>
                </xsl:when>
            </xsl:choose>
            <xsl:choose>
                <xsl:when test="value/statement">
                    <xsl:choose>
                        <xsl:when test="name">(</xsl:when>
                    </xsl:choose>
                    <xsl:for-each select="value/statement">
                        <xsl:if test="default = 'Falso'">
                            <xsl:apply-templates select=".">
                                <xsl:with-param name="islast" select="position() = last()"/>
                            </xsl:apply-templates>
                        </xsl:if>
                    </xsl:for-each>
                    <xsl:choose>
                        <xsl:when test="name">) </xsl:when>
                    </xsl:choose>
                </xsl:when>
                <xsl:otherwise>
                    <span>
                        <xsl:value-of select="value" disable-output-escaping="yes" />. </span>
                </xsl:otherwise>
            </xsl:choose>
        </span>
    </xsl:template>
    
</xsl:stylesheet>
