<?xml version="1.0"?>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:variable name="stabilisers" select="//notebook/@stabilisers"/>

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

            </head>

            <body>

                <div class="container">
                    <xsl:for-each select="notebook/activity">
                        <xsl:choose>
                            <xsl:when test="preview">
                                <img class="preview" src="{preview}"/>
                            </xsl:when>
                        </xsl:choose>
                        <section>
                            <header>
                                <h2>
                                    <xsl:value-of select="name"/>
                                </h2>
                            </header>
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
                                                  <xsl:apply-templates select="."/>
                                                </xsl:for-each>

                                                <xsl:for-each select="statement">
                                                  <!-- <xsl:sort select="name" /> -->
                                                  <xsl:if test="default = 'Falso'">
                                                  <div class="row">
                                                  <xsl:choose>
                                                  <xsl:when
                                                  test="$stabilisers = 'true' and description and not(string-length(description) > 12)">
                                                  <div class="col-xs-10 statement {@class}">
                                                  <xsl:apply-templates select=".">
                                                  <!-- <xsl:sort select="name" /> -->
                                                  </xsl:apply-templates>
                                                  </div>
                                                  <div class="col-xs-2 statement text-right">
                                                  <small class="label label-info">
                                                  <xsl:value-of select="description"/>
                                                  </small>
                                                  </div>
                                                  </xsl:when>
                                                  <xsl:otherwise>
                                                  <div class="col-xs-12 statement {@class}">
                                                  <xsl:apply-templates select=".">
                                                  <!-- <xsl:sort select="name" /> -->
                                                  </xsl:apply-templates>
                                                  </div>
                                                  <xsl:if test="$stabilisers and description">
                                                  <div class="col-xs-12">
                                                  <div class="" style="word-break: break-all;">
                                                  <small class="label label-info">
                                                  <xsl:value-of select="description"/>
                                                  </small>
                                                  </div>
                                                  </div>
                                                  </xsl:if>
                                                  </xsl:otherwise>
                                                  </xsl:choose>
                                                  </div>
                                                  </xsl:if>
                                                </xsl:for-each>
                                            </div>
                                        </xsl:for-each>
                                    </div>
                                </article>
                            </xsl:for-each>
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
                                            select="string-length(//target[@class = 'typing']/value)"
                                        /></span> caracteres. </div>
                                <div>
                                    <strong>Totales: </strong>
                                    <span><xsl:value-of
                                            select="count(//statement[default = 'Falso' and not(value/statement)])"
                                        /></span> instrucciones. </div>

                                <div>
                                    <strong>Word: </strong>
                                    <span><xsl:value-of
                                            select="count(//statement[default = 'Falso' and not(value/statement)]) - count(//statement[default = 'Falso' and not(value/statement) and @class = 'list'])"
                                        /></span> instrucciones. </div>

                                <div>
                                    <strong>Excel: </strong>
                                    <span><xsl:value-of
                                            select="count(//statement[default = 'Falso' and @class = 'list'])"
                                        /></span> instrucciones. </div>

                                <div>
                                    <strong>Instrucción 185 en </strong>
                                    <strong>bloque </strong>«<xsl:value-of
                                        select="(//statement[default = 'Falso' and not(value/statement)])[185]/ancestor-or-self::block/name"
                                    />» <xsl:choose>
                                        <xsl:when
                                            test="(//statement[default = 'Falso' and not(value/statement)])[185]/ancestor-or-self::division/name">
                                            <strong>, división </strong>«<xsl:value-of
                                                select="(//statement[default = 'Falso' and not(value/statement)])[185]/ancestor-or-self::division/name"
                                            />» </xsl:when>
                                    </xsl:choose>
                                    <strong>, instrución </strong>«<xsl:value-of
                                        select="(//statement[default = 'Falso' and not(value/statement)])[185]/name"
                                    />: <xsl:value-of
                                        select="(//statement[default = 'Falso' and not(value/statement)])[185]/value"
                                    />». </div>

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

    <xsl:template match="target" name="target">
        <xsl:choose>
            <xsl:when test="name">
                <div class="target  {@class}">
                    <strong><xsl:value-of select="name"/>:</strong><xsl:text> </xsl:text> '<span>
                        <xsl:value-of select="value" disable-output-escaping="yes"/></span>'. </div>
            </xsl:when>
            <xsl:otherwise>
                <div class="{@class}">
                    <xsl:value-of select="value" disable-output-escaping="yes"/>
                </div>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="statement" name="statement">
        <span class="statement {@class}">
            <xsl:choose>
                <xsl:when test="name">
                    <xsl:choose>
                        <xsl:when test="@class">
                            <xsl:if test="not(@class = 'list')">
                                <strong><xsl:value-of select="name"/>: </strong>
                            </xsl:if>
                            <xsl:if test="@class = 'list' and not(value/statement)">
                                <strong><xsl:value-of select="name"/> </strong>
                            </xsl:if>
                            <xsl:if test="@class = 'list' and value/statement">
                                <strong><xsl:value-of select="name"/>&#160;</strong>
                            </xsl:if>
                        </xsl:when>
                        <xsl:otherwise>
                            <strong><xsl:value-of select="name"/>: </strong>
                        </xsl:otherwise>
                    </xsl:choose>
                </xsl:when>
            </xsl:choose>

            <xsl:choose>
                <xsl:when test="not(@class = 'list') and (value/statement or value/target)">
                    <xsl:choose>
                        <xsl:when test="name and not(@class = 'tab')">(</xsl:when>
                    </xsl:choose>

                    <xsl:for-each select="value/target">
                        <xsl:apply-templates select="."/>&#160; </xsl:for-each>

                    <xsl:for-each select="value/statement">
                        <!-- <xsl:sort select="name" /> -->
                        <xsl:if test="default = 'Falso'">
                            <xsl:apply-templates select=".">
                                <xsl:with-param name="islast" select="position() = last()"/>
                                <!-- <xsl:sort select="name" /> -->
                            </xsl:apply-templates>
                        </xsl:if>
                    </xsl:for-each>
                    <xsl:choose>
                        <xsl:when test="name and not(@class = 'tab')">) </xsl:when>
                    </xsl:choose>
                </xsl:when>
                <xsl:when test="@class = 'list' and value/statement">
                    <span><xsl:value-of select="value/text()"/>:</span>
                    <span class="ul">
                        <xsl:for-each select="value/statement">
                            <span class="li"><strong><xsl:value-of select="name"
                                        /></strong>&#160;<span><xsl:value-of select="value"
                                /></span>.</span>
                        </xsl:for-each>
                    </span>
                </xsl:when>
                <xsl:otherwise>
                    <span>

                        <xsl:choose>
                            <xsl:when
                                test="name = 'Arte' and ancestor::statement[@class = 'borders-format']">
                                <xsl:call-template name="art_style_preview"/>
                            </xsl:when>
                        </xsl:choose>
                        
                        <xsl:choose>
                            <xsl:when
                                test="name = 'Estilo' and ancestor::statement[@class = 'borders-format']">
                                <xsl:call-template name="border_style_preview"/>
                            </xsl:when>
                        </xsl:choose>
                        
                        <xsl:choose>
                            <xsl:when
                                test="(name = 'Subrayado' and ancestor::statement[@class = 'font-format']) or (name = 'Estilo de línea' and ancestor::statement[name = 'Subrayado'])">
                                <xsl:call-template name="undeline_style_preview"/>
                            </xsl:when>
                        </xsl:choose>
                        
                        <xsl:value-of select="value" disable-output-escaping="yes"/>. </span>
                </xsl:otherwise>
            </xsl:choose>
        </span>
    </xsl:template>


    <xsl:template name="undeline_style_preview">
        <xsl:choose>
            <xsl:when test="normalize-space(value)='Normal'">
                <span class="underline-style-preview">
                    <img style="margin-top: 0px"
                        src="http://localhost:8069/academy_online_assets/static/mapxml/v1/underline-styles.png"
                    />
                </span>
            </xsl:when>

            <xsl:when test="normalize-space(value)='Simple'">
                <span class="underline-style-preview">
                    <img style="margin-top: 0px"
                        src="http://localhost:8069/academy_online_assets/static/mapxml/v1/underline-styles.png"
                    />
                </span>
            </xsl:when>
            <xsl:when test="normalize-space(value)='Doble'">
                <span class="underline-style-preview">
                    <img style="margin-top: -9px"
                        src="http://localhost:8069/academy_online_assets/static/mapxml/v1/underline-styles.png"
                    />
                </span>
            </xsl:when>
            <xsl:when test="normalize-space(value)='Grueso'">
                <span class="underline-style-preview">
                    <img style="margin-top: -18px"
                        src="http://localhost:8069/academy_online_assets/static/mapxml/v1/underline-styles.png"
                    />
                </span>
            </xsl:when>
            <xsl:when test="normalize-space(value)='Punteado'">
                <span class="underline-style-preview">
                    <img style="margin-top: -27px"
                        src="http://localhost:8069/academy_online_assets/static/mapxml/v1/underline-styles.png"
                    />
                </span>
            </xsl:when>
            <xsl:when test="normalize-space(value)='Punteado grueso'">
                <span class="underline-style-preview">
                    <img style="margin-top: -36px"
                        src="http://localhost:8069/academy_online_assets/static/mapxml/v1/underline-styles.png"
                    />
                </span>
            </xsl:when>
            <xsl:when test="normalize-space(value)='Guiones'">
                <span class="underline-style-preview">
                    <img style="margin-top: -45px"
                        src="http://localhost:8069/academy_online_assets/static/mapxml/v1/underline-styles.png"
                    />
                </span>
            </xsl:when>
            <xsl:when test="normalize-space(value)='Grueso de guiones'">
                <span class="underline-style-preview">
                    <img style="margin-top: -54px"
                        src="http://localhost:8069/academy_online_assets/static/mapxml/v1/underline-styles.png"
                    />
                </span>
            </xsl:when>
            <xsl:when test="normalize-space(value)='Guiones largos'">
                <span class="underline-style-preview">
                    <img style="margin-top: -63px"
                        src="http://localhost:8069/academy_online_assets/static/mapxml/v1/underline-styles.png"
                    />
                </span>
            </xsl:when>
            <xsl:when test="normalize-space(value)='Grueso de guiones largos'">
                <span class="underline-style-preview">
                    <img style="margin-top: -72px"
                        src="http://localhost:8069/academy_online_assets/static/mapxml/v1/underline-styles.png"
                    />
                </span>
            </xsl:when>
            <xsl:when test="normalize-space(value)='Punto-guión'">
                <span class="underline-style-preview">
                    <img style="margin-top: -81px"
                        src="http://localhost:8069/academy_online_assets/static/mapxml/v1/underline-styles.png"
                    />
                </span>
            </xsl:when>
            <xsl:when test="normalize-space(value)='Grueso punto-guión'">
                <span class="underline-style-preview">
                    <img style="margin-top: -90px"
                        src="http://localhost:8069/academy_online_assets/static/mapxml/v1/underline-styles.png"
                    />
                </span>
            </xsl:when>
            <xsl:when test="normalize-space(value)='Punto-punto-guión'">
                <span class="underline-style-preview">
                    <img style="margin-top: -99px"
                        src="http://localhost:8069/academy_online_assets/static/mapxml/v1/underline-styles.png"
                    />
                </span>
            </xsl:when>
            <xsl:when test="normalize-space(value)='Grueso punto-punto-guión'">
                <span class="underline-style-preview">
                    <img style="margin-top: -108px"
                        src="http://localhost:8069/academy_online_assets/static/mapxml/v1/underline-styles.png"
                    />
                </span>
            </xsl:when>
            <xsl:when test="normalize-space(value)='Ondulado'">
                <span class="underline-style-preview">
                    <img style="margin-top: -117px"
                        src="http://localhost:8069/academy_online_assets/static/mapxml/v1/underline-styles.png"
                    />
                </span>
            </xsl:when>
            <xsl:when test="normalize-space(value)='Grueso ondulado'">
                <span class="underline-style-preview">
                    <img style="margin-top: -126px"
                        src="http://localhost:8069/academy_online_assets/static/mapxml/v1/underline-styles.png"
                    />
                </span>
            </xsl:when>
            <xsl:when test="normalize-space(value)='Doble ondulado'">
                <span class="underline-style-preview">
                    <img style="margin-top: -135px"
                        src="http://localhost:8069/academy_online_assets/static/mapxml/v1/underline-styles.png"
                    />
                </span>
            </xsl:when>
        </xsl:choose>
    </xsl:template>


    <xsl:template name="border_style_preview">
        <xsl:choose>
            <xsl:when test="normalize-space(value)='Línea continua sencilla (La opción nº 1 en la lista)'">
                <span class="border-style-preview">
                    <img style="margin-top: 0px"
                        src="http://localhost:8069/academy_online_assets/static/mapxml/v1/border-styles.png"
                    />
                </span>
            </xsl:when>

            <xsl:when test="normalize-space(value)='Punteado (La opción nº 2 en la lista)'">
                <span class="border-style-preview">
                    <img style="margin-top: -26px"
                        src="http://localhost:8069/academy_online_assets/static/mapxml/v1/border-styles.png"
                    />
                </span>
            </xsl:when>

            <xsl:when test="normalize-space(value)='Rayado (espacio pequeño) (La opción nº 3 en la lista)'">
                <span class="border-style-preview">
                    <img style="margin-top: -52px"
                        src="http://localhost:8069/academy_online_assets/static/mapxml/v1/border-styles.png"
                    />
                </span>
            </xsl:when>

            <xsl:when test="normalize-space(value)='Rayado (espacio grande) (La opción nº 4 en la lista)'">
                <span class="border-style-preview">
                    <img style="margin-top: -78px"
                        src="http://localhost:8069/academy_online_assets/static/mapxml/v1/border-styles.png"
                    />
                </span>
            </xsl:when>

            <xsl:when test="normalize-space(value)='Guion punto (La opción nº 5 en la lista)'">
                <span class="border-style-preview">
                    <img style="margin-top: -104px"
                        src="http://localhost:8069/academy_online_assets/static/mapxml/v1/border-styles.png"
                    />
                </span>
            </xsl:when>

            <xsl:when test="normalize-space(value)='Guion punto punto (La opción nº 6 en la lista)'">
                <span class="border-style-preview">
                    <img style="margin-top: -130px"
                        src="http://localhost:8069/academy_online_assets/static/mapxml/v1/border-styles.png"
                    />
                </span>
            </xsl:when>

            <xsl:when test="normalize-space(value)='Doble (La opción nº 7 en la lista)'">
                <span class="border-style-preview">
                    <img style="margin-top: -156px"
                        src="http://localhost:8069/academy_online_assets/static/mapxml/v1/border-styles.png"
                    />
                </span>
            </xsl:when>

            <xsl:when test="normalize-space(value)='Triple línea sólida (La opción nº 8 en la lista)'">
                <span class="border-style-preview">
                    <img style="margin-top: -182px"
                        src="http://localhost:8069/academy_online_assets/static/mapxml/v1/border-styles.png"
                    />
                </span>
            </xsl:when>

            <xsl:when test="normalize-space(value)='Diferencia pequeña fino-grueso (La opción nº 9 en la lista)'">
                <span class="border-style-preview">
                    <img style="margin-top: -208px"
                        src="http://localhost:8069/academy_online_assets/static/mapxml/v1/border-styles.png"
                    />
                </span>
            </xsl:when>

            <xsl:when test="normalize-space(value)='Diferencia pequeña grueso-fino (La opción nº 10 en la lista)'">
                <span class="border-style-preview">
                    <img style="margin-top: -234px"
                        src="http://localhost:8069/academy_online_assets/static/mapxml/v1/border-styles.png"
                    />
                </span>
            </xsl:when>

            <xsl:when
                test="normalize-space(value)='Diferencia pequeña fino-grueso-fino (La opción nº 11 en la lista)'">
                <span class="border-style-preview">
                    <img style="margin-top: -260px"
                        src="http://localhost:8069/academy_online_assets/static/mapxml/v1/border-styles.png"
                    />
                </span>
            </xsl:when>

            <xsl:when test="normalize-space(value)='Diferencia mediana fino-grueso (La opción nº 12 en la lista)'">
                <span class="border-style-preview">
                    <img style="margin-top: -286px"
                        src="http://localhost:8069/academy_online_assets/static/mapxml/v1/border-styles.png"
                    />
                </span>
            </xsl:when>

            <xsl:when test="normalize-space(value)='Diferencia mediana grueso-fino (La opción nº 13 en la lista)'">
                <span class="border-style-preview">
                    <img style="margin-top: -312px"
                        src="http://localhost:8069/academy_online_assets/static/mapxml/v1/border-styles.png"
                    />
                </span>
            </xsl:when>

            <xsl:when
                test="normalize-space(value)='Diferencia mediana fino-grueso-fino (La opción nº 14 en la lista)'">
                <span class="border-style-preview">
                    <img style="margin-top: -338px"
                        src="http://localhost:8069/academy_online_assets/static/mapxml/v1/border-styles.png"
                    />
                </span>
            </xsl:when>

            <xsl:when test="normalize-space(value)='Diferencia grande fino-grueso (La opción nº 15 en la lista)'">
                <span class="border-style-preview">
                    <img style="margin-top: -364px"
                        src="http://localhost:8069/academy_online_assets/static/mapxml/v1/border-styles.png"
                    />
                </span>
            </xsl:when>

            <xsl:when test="normalize-space(value)='Diferencia grande grueso-fino (La opción nº 16 en la lista)'">
                <span class="border-style-preview">
                    <img style="margin-top: -390px"
                        src="http://localhost:8069/academy_online_assets/static/mapxml/v1/border-styles.png"
                    />
                </span>
            </xsl:when>

            <xsl:when
                test="normalize-space(value)='Diferencia grande fino-grueso-fino (La opción nº 17 en la lista)'">
                <span class="border-style-preview">
                    <img style="margin-top: -416px"
                        src="http://localhost:8069/academy_online_assets/static/mapxml/v1/border-styles.png"
                    />
                </span>
            </xsl:when>

            <xsl:when test="normalize-space(value)='Ondulado sencillo (La opción nº 18 en la lista)'">
                <span class="border-style-preview">
                    <img style="margin-top: -442    px"
                        src="http://localhost:8069/academy_online_assets/static/mapxml/v1/border-styles.png"
                    />
                </span>
            </xsl:when>

            <xsl:when test="normalize-space(value)='Doble subrayado ondulado (La opción nº 19 en la lista)'">
                <span class="border-style-preview">
                    <img style="margin-top: -468px"
                        src="http://localhost:8069/academy_online_assets/static/mapxml/v1/border-styles.png"
                    />
                </span>
            </xsl:when>

            <xsl:when test="normalize-space(value)='Guion-punto (trazo) (La opción nº 20 en la lista)'">
                <span class="border-style-preview">
                    <img style="margin-top: -494px"
                        src="http://localhost:8069/academy_online_assets/static/mapxml/v1/border-styles.png"
                    />
                </span>
            </xsl:when>

            <xsl:when test="normalize-space(value)='Relieve 3D (La opción nº 21 en la lista)'">
                <span class="border-style-preview">
                    <img style="margin-top: -520px"
                        src="http://localhost:8069/academy_online_assets/static/mapxml/v1/border-styles.png"
                    />
                </span>
            </xsl:when>

            <xsl:when test="normalize-space(value)='Grabado 3D (La opción nº 22 en la lista)'">
                <span class="border-style-preview">
                    <img style="margin-top: -546px"
                        src="http://localhost:8069/academy_online_assets/static/mapxml/v1/border-styles.png"
                    />
                </span>
            </xsl:when>

            <xsl:when test="normalize-space(value)='Exterior (La opción nº 23 en la lista)'">
                <span class="border-style-preview">
                    <img style="margin-top: -598px"
                        src="http://localhost:8069/academy_online_assets/static/mapxml/v1/border-styles.png"
                    />
                </span>
            </xsl:when>

            <xsl:when test="normalize-space(value)='Interior (La opción nº 24 en la lista)'">
                <span class="border-style-preview">
                    <img style="margin-top: -624px"
                        src="http://localhost:8069/academy_online_assets/static/mapxml/v1/border-styles.png"
                    />
                </span>
            </xsl:when>

        </xsl:choose>
    </xsl:template>


    <xsl:template name="art_style_preview">
        <xsl:choose>
            
            <xsl:when test="normalize-space(value)='Borde de manzanas (el 1º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: 0px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de bizcochos (el 2º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -26px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de porciones de pastel (el 3º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -52px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de maíz dulce (el 4º de la lista desplegable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -78px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de helados (el 5º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -104px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de botellas de champán (el 6º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -130px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de vasos de fiesta (el 7º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -156px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de árboles de Navidad (el 8º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -182px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de árboles (el 9º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -208px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de palmeras de colores (el 10º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -234px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de globos de tres colores (el 11º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -260px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de globos de aire caliente (el 12º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -286px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de regalos sorpresa (el 13º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -312px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de confeti con serpentinas (el 14º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -338px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de corazones (el 15º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -364px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de globos de corazón (el 16º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -390px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de estrellas en 3D (el 17º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -416px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de estrellas sombreadas (el 18º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -442px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de estrellas (el 19º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -468px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de soles (el 20º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -494px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde número 2 de Tierra (el 21º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -520px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde número 1 de Tierra (el 22º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -546px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de gente con sombreros (el 23º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -572px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de sombreros (el 24º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -598px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de lápices (el 25º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -624px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de paquetes (el 26º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -650px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de relojes (el 27º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -676px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde e petardos (el 28º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -702px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de anillos (el 29º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -728px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de marcadores de mapas (el 30º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -754px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de confeti (el 31º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -780px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de mariposas (el 32º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -806px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de mariquitas (el 33º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -832px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de peces (el 34º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -858px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de pájaros en vuelo (el 35º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -884px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de gatos asustados (el 36º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -910px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de murciélagos (el 37º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -936px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de rosas (el 38º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -962px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de rosas rojas (el 39º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -988px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de poinsettias (el 40º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -1014px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de acebo (el 41º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -1040px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de flores diminutas (el 42º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -1066px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de pensamientos (el 43º de la lista desplegable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -1092px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de flores moderno número 2 (el 44º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -1118px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de flores moderno (el 45º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -1144px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de flores blancas (el 46º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -1170px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de viñas (el 47º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -1196px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de margaritas (el 48º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -1222px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de xilografía de flores (el 49º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -1248px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de arcos de colores (el 50º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -1274px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de abanicos (el 51º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -1300px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de película (el 52º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -1326px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde número 1 de relámpagos (el 53º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -1352px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de brújulas (el 54º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -1378px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de D dobles (el 55º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -1404px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de onda clásica (el 56º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -1430px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de cuadrados sombreados (el 57º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -1456px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de líneas retorcidas número 1 (el 58º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -1482px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de línea ondulada (el 59º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -1508px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de cuadrantes (el 60º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -1534px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de barra de cuadros de colores (el 61º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -1560px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de remolinos (el 62º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -1586px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de alfileres de anotación número 1 (el 63º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -1612px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de alfileres de anotación número 2 (el 64º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -1638px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de calabazas número 1 (el 65º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -1664px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de huevos de color negro (el 66º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -1690px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de cupidos (el 67º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -1716px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de globos de corazón en tonos de gris (el 68º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -1742px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de monigotes (el 69º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -1768px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de chupetes (el 70º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -1794px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de sonajeros (el 71º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -1820px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de cabañas (el 72º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -1846px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de casas originales (el 73º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -1872px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de estrellas negras (el 74º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -1898px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de copos de nieve (el 75º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -1924px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de copos de nieve de fantasía (el 76º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -1950px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de cohetes (el 77º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -1976px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde Seattle (el 78º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -2002px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de notas musicales (el 79º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -2028px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de palmeras negras (el 80º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -2054px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de hojas de arce (el 81º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -2080px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de clips (el 82º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -2106px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de huellas de pájaro costero (el 83º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -2132px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de gente (el 84º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -2158px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de gente saludando (el 85º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -2184px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde número 2 de cuadros eclipsados (el 86º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -2210px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde hipnótico (el 87º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -2236px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de rombos en tonos de gris (el 88º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -2262px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de arcos decorativos (el 89º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -2288px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de bloques decorativos (el 90º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -2314px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de círculos y líneas (el 91º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -2340px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de papiro (el 92º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -2366px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de carpintería (el 93º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -2392px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de trenzas entrelazadas (el 94º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -2418px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de cinta de opciones entrelazadas (el 95º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -2444px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de ángulos entrelazados (el 96º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -2470px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de festones en forma de arco (el 97º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -2496px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de safari (el 98º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -2522px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de nudos celtas (el 99º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -2548px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de laberinto loco (el 100º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -2574px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde número 1 de cuadros eclipsados (el 101º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -2600px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de pájaros (el 102º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -2626px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de tazas de té (el 103º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -2652px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de noroeste (el 104º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -2678px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde Mexicano (el 105º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -2704px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde tribal número 6 (el 106º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -2730px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde tribal número 4 (el 107º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -2756px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde tribal número 3 (el 108º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -2782px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde tribal número 2 (el 109º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -2808px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde tribal número 5 (el 110º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -2834px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de efectos ópticos en X (el 111º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -2860px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de triángulos divertidos (el 112º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -2886px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de pirámides (el 113º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -2912px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de pirámides exterior (el 114º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -2938px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de confeti usando tonos de gris (el 115º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -2964px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de contorno de confeti (el 116º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -2990px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de confeti blanco (el 117º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -3016px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de mosaico (el 118º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -3042px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde número 2 de relámpagos (el 119º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -3068px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de carne de gallina (el 120º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -3094px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de bombillas (el 121º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -3120px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde degradado (el 122º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -3146px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de fiesta de triángulos (el 123º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -3172px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de líneas retorcidas número 2 (el 124º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -3198px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de lunas (el 125º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -3224px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de elipses (el 126º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -3250px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de rombos dobles (el 127º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -3276px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de eslabones de cadena (el 128º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -3302px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de triángulos (el 129º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -3328px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde tribal número 1 (el 130º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -3354px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de marquesina dentada (el 131º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -3380px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de dientes de tiburón (el 132º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -3406px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de sierra (el 133º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -3432px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de sierra en gris (el 134º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -3458px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de sello (el 135º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -3484px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de tiras entrelazadas (el 136º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -3510px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde en zigzag (el 137º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -3536px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de punto de cruz (el 138º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -3562px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de gemas (el 139º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -3588px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de círculos y rectángulos (el 140º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -3614px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de triángulos (el 141º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -3640px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de insectos (el 142º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -3666px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de punto en zigzag (el 143º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -3692px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde tipo tablero de ajedrez (el 144º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -3718px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de barra de cuadros negros (el 145º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -3744px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de marquesina (el 146º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -3770px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde básico de puntos blancos (el 147º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -3796px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde básico de línea media gruesa (el 148º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -3822px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde básico de línea exterior gruesa (el 149º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -3848px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde básico de línea interior gruesa (el 150º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -3874px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde básico de líneas finas (el 151º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -3900px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde básico de guiones blancos (el 152º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -3926px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde básico de cuadrados blancos (el 153º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -3952px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde básico de cuadros negros (el 154º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -3978px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde básico de guiones negros (el 155º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -4004px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde básico de puntos negros (el 156º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -4030px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de estrellas en lo alto (el 157º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -4056px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de título para certificado (el 158º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -4082px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde hecho a mano número 1 (el 159º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -4108px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde hecho a mano número 2 (el 160º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -4134px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de papel rasgado (el 161º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -4160px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de papel rasgado negro (el 162º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -4186px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de línea de recorte con guiones (el 163º de la lista despleglable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -4212px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>
            
            <xsl:when test="normalize-space(value)='Borde de línea de recorte con puntos (el 164º de la lista desplegable)'">
                <span class="art-style-preview">
                    <img style="margin-top: -4238px" src="http://localhost:8069/academy_online_assets/static/mapxml/v1/art-styles.png" />
                </span>
            </xsl:when>

        </xsl:choose>
    </xsl:template>

</xsl:stylesheet>
