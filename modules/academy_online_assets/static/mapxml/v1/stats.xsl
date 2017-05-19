<?xml version="1.0"?>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <xsl:template match="/">
        <html>
            <head>
                <title>
                    <xsl:value-of select="//notebook/name"/>
                </title>
                <style>i { color: #CCCCCC; }</style>
            </head>

            <body>
                <h1>
                    <xsl:value-of select="//notebook/name"/>
                </h1>
                <p>Mecanografia: <xsl:value-of
                    select="string-length(//block[name='Mecanografía']/division/target/value)"/>/<i>1.274</i></p>

                <h2>Instrucciones:</h2>

                <p>Totales <xsl:value-of
                        select="count(//statement[default = 'Falso' and not(value/statement)])"/>
                    <ul>
                        <li>Word: <xsl:value-of
                                select="count(//statement[default = 'Falso' and not(value/statement)]) - count(//statement[default = 'Falso' and not(value/statement) and @class = 'list'])"
                            />/<i>185</i></li>
                        <li>Excel: <xsl:value-of
                                select="count(//statement[default = 'Falso' and @class = 'list'])"
                            />/<i>20</i></li>
                    </ul>
                </p>

                <p>Instruccion 185 en <ul>
                        <li>Bloque: <xsl:value-of
                                select="(//statement[default = 'Falso' and not(value/statement)])[185]/ancestor-or-self::block/name"
                            /></li>
                        <xsl:choose>
                            <xsl:when
                                test="(//statement[default = 'Falso' and not(value/statement)])[185]/ancestor-or-self::division/name">
                                <li>División: <xsl:value-of
                                        select="(//statement[default = 'Falso' and not(value/statement)])[185]/ancestor-or-self::division/name"
                                    /></li>
                            </xsl:when>
                        </xsl:choose>
                        <li>Instrucion: <xsl:value-of
                                select="(//statement[default = 'Falso' and not(value/statement)])[185]/name"
                            />: <xsl:value-of
                                select="(//statement[default = 'Falso' and not(value/statement)])[185]/value"
                            /></li>
                    </ul>
                </p>

            </body>
        </html>
    </xsl:template>

</xsl:stylesheet>
