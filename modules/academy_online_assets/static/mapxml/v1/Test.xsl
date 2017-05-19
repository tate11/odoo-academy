<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs"
    version="2.0">
    
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
                <link rel="stylesheet" href="http://guanaco:8069/academy_online_assets/static/mapxml/v1/notebook.css"/>
                
            </head>
            
            <body>
                
                <div class="container">
                    <xsl:for-each select="notebook/activity">
                        <section>
                            <header>
                                <h2>
                                    <xsl:value-of select="name"/>
                                </h2>
                            </header>
                            
                            <xsl:for-each select="//statement">
                                <xsl:if test="default = 'Falso' and not(value/statement)">
                                    <xsl:value-of select="name" disable-output-escaping="yes" />
                                    <xsl:value-of select="value" disable-output-escaping="yes" />
                                    <xsl:for-each select="ancestor-or-self::statement">
                                        <xsl:call-template name="print-step"/>
                                    </xsl:for-each>
                                    <br></br>
                                </xsl:if>
                            </xsl:for-each>
                            
                        </section>
                    </xsl:for-each>
                </div>
            </body>
        </html>
    </xsl:template>
    
    <xsl:template name="print-step">
        <xsl:text>/</xsl:text>
        <xsl:value-of select="name"/>
        <xsl:text>[</xsl:text>
        <xsl:value-of select="1+count(preceding-sibling::*)"/>
        <xsl:text>]</xsl:text>
    </xsl:template>
    
</xsl:stylesheet>
