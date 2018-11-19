<?xml version="1.1"?>

<!--
- [ ] Border style list should begin at zero
- [ ] Border art list should begin at zero
- [ ] Probar márgenes: Interior y Exterior
- [ ] Probar: Varias páginas y Hojas por folleto
- [ ] Probar: Color de subrayado
- [ ] Probar unidades en las sangrías y espaciados
- [ ] No agregar espacios entre párrafos del mismo estilo
- [ ] Números negativos no pueden ser cargados en el test
- [ ] Distancia del borde de la hoja a la sangría
- [ ] Distancia del borde de la hoja a la sangría especial
- [ ] Distancia del borde de la hoja a la viñeta, ...
- [ ] Verificar cómo afecta «[1]» en cada caso
--> 

<xsl:stylesheet version="2.0" xmlns="http://www.w3.org/1999/xhtml"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:fn="http://www.w3.org/2005/xpath-functions" 
    xmlns:regexp="http://exslt.org/regular-expressions" 
    xmlns:math="http://exslt.org/math"
    extension-element-prefixes="math">

   <!-- <xsl:output method="text" omit-xml-declaration="yes" indent="no"/>-->


    <xsl:decimal-format name="uk" decimal-separator="." grouping-separator=","/>
    <xsl:decimal-format name="es" decimal-separator="," grouping-separator="."/>
    <xsl:variable name="wordactivity" select="//notebook/activity[name='PRUEBA DE MAQUETACIÓN']" />



    <xsl:template match="/">
        <pre>
        
        
        
        <!-- CONFIGURACIÓN DE PÁGINA
             - Tema
             - Nombre del formato de papel
             - Ancho del papel
             - Altura del papel
             - Margen superior, derecho, inferior, izquierdo, interior y exterior 
             - Margen de encuadernación
             - Posición del margen interno
             - Margen del encabezado
             - Margen del pie de página
             - Orientación del papel
             - Alineación vertical
             - Inicio de la primera sección
             - Varias páginas
             - Páginas por folleto
             - [ ] Pares e impares diferentes y Primera página diferente
        - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - --> 
        
        <xsl:variable name="statementset" select="$wordactivity/block/division/statement[@class = 'page-format']" />
         
        <!-- CONFIGURACIÓN DE PÁGINA : : Tema -->         
        <xsl:variable name="statementvalue" select="$statementset/value/statement[name = 'Tema']/value" />
        <xsl:if test="$statementvalue">
            <xsl:variable name="order" select="floor(math:random() * 50)"/>
            > Diseño de página / Tema
            1. ¿Cuál es el tema establecido para el documento?
                a) <xsl:value-of select="$statementvalue"/>
                b) <xsl:call-template name="themelist">
                        <xsl:with-param name="invalid" select="$statementvalue"/>
                        <xsl:with-param name="order" select="$order"/>
                   </xsl:call-template>
                c) <xsl:call-template name="themelist">
                        <xsl:with-param name="invalid" select="$statementvalue"/>
                        <xsl:with-param name="order" select="$order + 1"/>
                   </xsl:call-template>
                d) <xsl:call-template name="themelist">
                        <xsl:with-param name="invalid" select="$statementvalue"/>
                        <xsl:with-param name="order" select="$order + 2"/>
                   </xsl:call-template> 
        </xsl:if>

        <!-- CONFIGURACIÓN DE PÁGINA : Papel : ...  - - - - - - - - - - - - - - - - - --> 
        <xsl:variable name="statementsubset" select="$statementset/value/statement[name = 'Papel']" />

        <!-- CONFIGURACIÓN DE PÁGINA : Papel : Tamaño de papel -->    
        <xsl:variable name="statementvalue" select="$statementsubset/value/statement[name='Tamaño del papel']/value" />
        <xsl:if test="$statementvalue">
            <xsl:variable name="order" select="floor(math:random() * 49)"/>
            > Diseño de página / Configurar página [ALT + C + C] / Papel / Tamaño del papel
            1. ¿Cuál es el tamaño del papel establecido para la impresión del documento?
                a) <xsl:value-of select="$statementvalue"/>
                b) <xsl:call-template name="papersizelist">
                        <xsl:with-param name="invalid" select="$statementvalue"/>
                        <xsl:with-param name="order" select="$order"/>
                   </xsl:call-template>
                c) <xsl:call-template name="papersizelist">
                        <xsl:with-param name="invalid" select="$statementvalue"/>
                        <xsl:with-param name="order" select="$order + 1"/>
                   </xsl:call-template>
                d) <xsl:call-template name="papersizelist">
                        <xsl:with-param name="invalid" select="$statementvalue"/>
                        <xsl:with-param name="order" select="$order + 2"/>
                   </xsl:call-template> 
        </xsl:if>

        <!-- CONFIGURACIÓN DE PÁGINA : Papel : Ancho -->    
        <xsl:variable name="statementvalue" select="number(replace(replace($statementsubset/value/statement[name = 'Ancho']/value, ' cm', ''), ',', '.'))"/>
        <xsl:if test="$statementvalue">
            > Diseño de página / Configurar página [ALT + C + C] / Papel / Ancho
            1. ¿Cuál es el ancho de página establecido para el documento?
                a) <xsl:value-of select="format-number($statementvalue, '#.##0,00 cm', 'es')"/>
                b) <xsl:value-of select="format-number($statementvalue + ((floor(math:random() * 100) div 100)), '0,00 cm', 'es')"/>
                c) <xsl:value-of select="format-number($statementvalue - ((floor(math:random() * 100) div 100)), '0,00 cm', 'es')"/>
                d) <xsl:value-of select="format-number($statementvalue + ((floor(math:random() * 100) div 100)), '0,00 cm', 'es')"/> 
        </xsl:if>

        <!-- CONFIGURACIÓN DE PÁGINA : Papel : Alto -->    
        <xsl:variable name="statementvalue" select="number(replace(replace($statementsubset/value/statement[name = 'Alto']/value, ' cm', ''), ',', '.'))"/>
        <xsl:if test="$statementvalue">
            > Diseño de página / Configurar página [ALT + C + C] / Papel / Alto
            1. ¿Cuál es la altura de página establecida para el documento?
                a) <xsl:value-of select="format-number($statementvalue, '#.##0,00 cm', 'es')"/>
                b) <xsl:value-of select="format-number($statementvalue + ((floor(math:random() * 100) div 100)), '0,00 cm', 'es')"/>
                c) <xsl:value-of select="format-number($statementvalue - ((floor(math:random() * 100) div 100)), '0,00 cm', 'es')"/>
                d) <xsl:value-of select="format-number($statementvalue + ((floor(math:random() * 100) div 100)), '0,00 cm', 'es')"/> 
        </xsl:if>

        <!-- CONFIGURACIÓN DE PÁGINA : Margen : ... - - - - - - - - - - - - - - - - - --> 
        <xsl:variable name="statementsubset" select="$statementset/value/statement[name = 'Margen']" />

        <!-- CONFIGURACIÓN DE PÁGINA : Margen : Superior -->    
        <xsl:variable name="statementvalue" select="number(replace(replace(//$statementsubset/value/statement[name = 'Superior']/value, ' cm', ''), ',', '.'))"/>
        <xsl:if test="$statementvalue">
            > Diseño de página / Configurar página [ALT + C + C] / Márgenes / Superior
            1. ¿Cuál es el margen superior establecido para el documento?
                a) <xsl:value-of select="format-number($statementvalue, '#.##0,00 cm', 'es')"/>
                b) <xsl:value-of select="format-number($statementvalue + ((floor(math:random() * 100) div 100)), '0,00 cm', 'es')"/>
                c) <xsl:value-of select="format-number($statementvalue - ((floor(math:random() * 100) div 100)), '0,00 cm', 'es')"/>
                d) <xsl:value-of select="format-number($statementvalue + ((floor(math:random() * 100) div 100)), '0,00 cm', 'es')"/> 
        </xsl:if>

        <!-- CONFIGURACIÓN DE PÁGINA : Margen : Derecho -->    
        <xsl:variable name="statementvalue" select="number(replace(replace(//$statementsubset/value/statement[name = 'Derecho']/value, ' cm', ''), ',', '.'))"/>
        <xsl:if test="$statementvalue">
            > Diseño de página / Configurar página [ALT + C + C] / Márgenes / Derecho
            1. ¿Cuál es el margen derecho establecido para el documento?
                a) <xsl:value-of select="format-number($statementvalue, '#.##0,00 cm', 'es')"/>
                b) <xsl:value-of select="format-number($statementvalue + ((floor(math:random() * 100) div 100)), '0,00 cm', 'es')"/>
                c) <xsl:value-of select="format-number($statementvalue - ((floor(math:random() * 100) div 100)), '0,00 cm', 'es')"/>
                d) <xsl:value-of select="format-number($statementvalue + ((floor(math:random() * 100) div 100)), '0,00 cm', 'es')"/> 
        </xsl:if>

        <!-- CONFIGURACIÓN DE PÁGINA : Margen : Inferior -->    
        <xsl:variable name="statementvalue" select="number(replace(replace($statementsubset/value/statement[name = 'Inferior']/value, ' cm', ''), ',', '.'))"/>
        <xsl:if test="$statementvalue">
            > Diseño de página / Configurar página [ALT + C + C] / Márgenes / Inferior
            1. ¿Cuál es el margen inferior establecido para el documento?
                a) <xsl:value-of select="format-number($statementvalue, '#.##0,00 cm', 'es')"/>
                b) <xsl:value-of select="format-number($statementvalue + ((floor(math:random() * 100) div 100)), '0,00 cm', 'es')"/>
                c) <xsl:value-of select="format-number($statementvalue - ((floor(math:random() * 100) div 100)), '0,00 cm', 'es')"/>
                d) <xsl:value-of select="format-number($statementvalue + ((floor(math:random() * 100) div 100)), '0,00 cm', 'es')"/> 
        </xsl:if>

        <!-- CONFIGURACIÓN DE PÁGINA : Margen : Izquierdo -->    
        <xsl:variable name="statementvalue" select="number(replace(replace($statementsubset/value/statement[name = 'Izquierdo']/value, ' cm', ''), ',', '.'))"/>
        <xsl:if test="$statementvalue">
            > Diseño de página / Configurar página [ALT + C + C] / Márgenes / Izquierdo
            1. ¿Cuál es el margen izquierdo establecido para el documento?
                a) <xsl:value-of select="format-number($statementvalue, '#.##0,00 cm', 'es')"/>
                b) <xsl:value-of select="format-number($statementvalue + ((floor(math:random() * 100) div 100)), '0,00 cm', 'es')"/>
                c) <xsl:value-of select="format-number($statementvalue - ((floor(math:random() * 100) div 100)), '0,00 cm', 'es')"/>
                d) <xsl:value-of select="format-number($statementvalue + ((floor(math:random() * 100) div 100)), '0,00 cm', 'es')"/> 
        </xsl:if>

        <!-- CONFIGURACIÓN DE PÁGINA : Margen : Interior -->    
        <xsl:variable name="statementvalue" select="number(replace(replace(//$statementsubset/value/statement[name = 'Interior']/value, ' cm', ''), ',', '.'))"/>
        <xsl:if test="$statementvalue">
            > Diseño de página / Configurar página [ALT + C + C] / Márgenes / Interior (Sólo con márgenes simétricos)
            1. ¿Cuál es el margen interior establecido para el documento?
                a) <xsl:value-of select="format-number($statementvalue, '#.##0,00 cm', 'es')"/>
                b) <xsl:value-of select="format-number($statementvalue + ((floor(math:random() * 100) div 100)), '0,00 cm', 'es')"/>
                c) <xsl:value-of select="format-number($statementvalue - ((floor(math:random() * 100) div 100)), '0,00 cm', 'es')"/>
                d) <xsl:value-of select="format-number($statementvalue + ((floor(math:random() * 100) div 100)), '0,00 cm', 'es')"/> 
        </xsl:if>

        <!-- CONFIGURACIÓN DE PÁGINA : Margen : Exterior -->    
        <xsl:variable name="statementvalue" select="number(replace(replace(//$statementsubset/value/statement[name = 'Exterior']/value, ' cm', ''), ',', '.'))"/>
        <xsl:if test="$statementvalue">
            > Diseño de página / Configurar página [ALT + C + C] / Márgenes / Exterior (Sólo con márgenes simétricos)
            1. ¿Cuál es el margen exterior establecido para el documento?
                a) <xsl:value-of select="format-number($statementvalue, '#.##0,00 cm', 'es')"/>
                b) <xsl:value-of select="format-number($statementvalue + ((floor(math:random() * 100) div 100)), '0,00 cm', 'es')"/>
                c) <xsl:value-of select="format-number($statementvalue - ((floor(math:random() * 100) div 100)), '0,00 cm', 'es')"/>
                d) <xsl:value-of select="format-number($statementvalue + ((floor(math:random() * 100) div 100)), '0,00 cm', 'es')"/> 
        </xsl:if>
        <!-- CONFIGURACIÓN DE PÁGINA : Margen : Encuadernación -->    
        <xsl:variable name="statementvalue" select="number(replace(replace($statementsubset/value/statement[name = 'Encuadernación']/value, ' cm', ''), ',', '.'))"/>
        <xsl:if test="$statementvalue">
            > Diseño de página / Configurar página [ALT + C + C] / Márgenes / Encuadernación
            1. ¿Cuál es el margen de encuadernación establecido para el documento?
                a) <xsl:value-of select="format-number($statementvalue, '#.##0,00 cm', 'es')"/>
                b) <xsl:value-of select="format-number($statementvalue + ((floor(math:random() * 100) div 100)), '0,00 cm', 'es')"/>
                c) <xsl:value-of select="format-number($statementvalue - ((floor(math:random() * 100) div 100)), '0,00 cm', 'es')"/>
                d) <xsl:value-of select="format-number($statementvalue + ((floor(math:random() * 100) div 100)), '0,00 cm', 'es')"/> 
        </xsl:if>
        
        <!-- CONFIGURACIÓN DE PÁGINA : Margen : Posición del margen interno -->    
        <xsl:variable name="statementvalue" select="$statementsubset/value/statement[name = 'Posición del margen interno']/value"/>
        <xsl:if test="$statementvalue">
            > Diseño de página / Configurar página [ALT + C + C] / Márgenes / Posición del margen interno
            1. ¿Cuál es la posición del margen interno establecida para el documento?
                a) <xsl:value-of select="$statementvalue"/>
                b) <xsl:choose>
                    <xsl:when test="$statementvalue = 'Arriba'">Izquierda</xsl:when>
                    <xsl:otherwise>Arriba</xsl:otherwise>
                </xsl:choose>
                c) Derecha
                d) Abajo
        </xsl:if>
        
        <!-- CONFIGURACIÓN DE PÁGINA : Margen : Encabezado, desde el borde -->    
        <xsl:variable name="statementvalue" select="number(replace(replace($statementsubset/value/statement[name = 'Encabezado, desde el borde']/value, ' cm', ''), ',', '.'))"/>
        <xsl:if test="$statementvalue">
            > Diseño de página / Configurar página [ALT + C + C] / Diseño / Encabezado
            1. ¿Cuál es la distancia desde el texto establecida para encabezado de página del documento?
                a) <xsl:value-of select="format-number($statementvalue, '#.##0,00 cm', 'es')"/>
                b) <xsl:value-of select="format-number($statementvalue + ((floor(math:random() * 100) div 100)), '0,00 cm', 'es')"/>
                c) <xsl:value-of select="format-number($statementvalue - ((floor(math:random() * 100) div 100)), '0,00 cm', 'es')"/>
                d) <xsl:value-of select="format-number($statementvalue + ((floor(math:random() * 100) div 100)), '0,00 cm', 'es')"/> 
        </xsl:if>
        
        <!-- CONFIGURACIÓN DE PÁGINA : Margen : Pie de página, desde el borde -->    
        <xsl:variable name="statementvalue" select="number(replace(replace($statementsubset/value/statement[name = 'Pie de página, desde el borde']/value, ' cm', ''), ',', '.'))"/>
        <xsl:if test="$statementvalue">
              > Diseño de página / Configurar página [ALT + C + C] / Diseño / Pie de página
            1. ¿Cuál es la distancia desde el texto establecida para el pie de página del documento?
                a) <xsl:value-of select="format-number($statementvalue, '#.##0,00 cm', 'es')"/>
                b) <xsl:value-of select="format-number($statementvalue + ((floor(math:random() * 100) div 100)), '0,00 cm', 'es')"/>
                c) <xsl:value-of select="format-number($statementvalue - ((floor(math:random() * 100) div 100)), '0,00 cm', 'es')"/>
                d) <xsl:value-of select="format-number($statementvalue + ((floor(math:random() * 100) div 100)), '0,00 cm', 'es')"/> 
        </xsl:if>
        
        <!-- CONFIGURACIÓN DE PÁGINA : Margen : Orientación -->    
        <xsl:variable name="statementvalue" select="$statementset/value/statement[name = 'Orientación']/value"/>
        <xsl:if test="$statementvalue">
            > Diseño de página / Configurar página [ALT + C + C] / Márgenes / Orientación
            1. ¿Cuál es la orientación de página establecida para el documento?
                a) <xsl:value-of select="$statementvalue"/>
                b) <xsl:choose><xsl:when test="$statementvalue = 'Vertical'">Horizontal</xsl:when><xsl:otherwise>Vertical</xsl:otherwise></xsl:choose>
                c) Centrada
                d) <xsl:value-of select="format-number(((45 + floor(math:random() * 31500) div 100)), '0,00º', 'es')"/> 
        </xsl:if>

        <!-- CONFIGURACIÓN DE PÁGINA : : Alineación vertical -->    
        <xsl:variable name="statementvalue" select="$statementset/value/statement[name = 'Alineación vertical']/value"/>
        <xsl:if test="$statementvalue">
            > Diseño de página / Configurar página [ALT + C + C] / Diseño / Alineación vertical
            1. ¿Cuál es la alineación vertical de página establecida para el documento?
                a) <xsl:value-of select="$statementvalue"/>
                b) <xsl:choose><xsl:when test="$statementvalue= 'Vertical'">Horizontal</xsl:when><xsl:otherwise>Vertical</xsl:otherwise></xsl:choose>
                c) Centrada
                d) <xsl:value-of select="format-number(((45 + floor(math:random() * 31500) div 100)), '0,00º', 'es')"/> 
        </xsl:if>

            <!-- CONFIGURACIÓN DE PÁGINA : : Varias páginas -->    
        <xsl:variable name="statementvalue" select="$statementset/value/statement[name = 'Varias páginas']/value"/>
        <xsl:if test="$statementvalue">
            > Diseño de página / Configurar página [ALT + C + C] / Márgenes / Varias páginas
            1. ¿Cuál de las siguientes afirmaciones es correcta?
                b) <xsl:choose>
                        <xsl:when test="$statementvalue = 'Márgenes simétricos'">La configuración de página establecida para el documento es la adecuada para imprimir con márgenes simétricos</xsl:when>
                        <xsl:when test="$statementvalue = 'Dos páginas por hoja'">La configuración de página establecida para el documento es la adecuada imprimir dos páginas en cada hoja de papel</xsl:when>
                        <xsl:when test="$statementvalue = 'Formato libro'">La configuración de página establecida para el documento es la adecuada para crear folletos determinando en número de hojas por folleto</xsl:when>
                        <xsl:otherwise>Manteniendo el resto de opciones de configuración de página establecidas para el documento, es posible variar la posición del margen interno</xsl:otherwise>
                   </xsl:choose>
                b) <xsl:choose>
                        <xsl:when test="$statementvalue = 'Márgenes simétricos'">Manteniendo el resto de opciones de configuración de página establecidas para el documento, es posible variar la posición del margen interno</xsl:when>
                        <xsl:otherwise>La configuración de página establecida para el documento es la adecuada para imprimir con márgenes simétricos</xsl:otherwise>
                   </xsl:choose>
                c) <xsl:choose>
                        <xsl:when test="$statementvalue = 'Dos páginas por hoja'">Manteniendo el resto de opciones de configuración de página establecidas para el documento, es posible variar la posición del margen interno</xsl:when>
                        <xsl:otherwise>La configuración de página establecida para el documento es la adecuada imprimir dos páginas en cada hoja de papel</xsl:otherwise>
                   </xsl:choose>
                b) <xsl:choose>
                        <xsl:when test="$statementvalue = 'Formato libro'">Manteniendo el resto de opciones de configuración de página establecidas para el documento, es posible variar la posición del margen interno</xsl:when>
                        <xsl:otherwise>La configuración de página establecida para el documento es la adecuada para crear folletos determinando en número de hojas por folleto</xsl:otherwise>
                   </xsl:choose>
        </xsl:if>
            
            <!-- CONFIGURACIÓN DE PÁGINA : : Hojas por folleto -->    
        <xsl:variable name="statementvalue" select="$statementset/value/statement[name = 'Hojas por folleto' and default='Falso']/value"/>
        <xsl:if test="$statementvalue">
            > Diseño de página / Configurar página [ALT + C + C] / Márgenes / Varias páginas (Sólo con Formato libro)
            1. ¿Cuál es el número de hojas por folleto establecido para el documento?
                a) <xsl:value-of select="$statementvalue"/>
                b) <xsl:choose>
                        <xsl:when test="$statementvalue = 'Todas'">1</xsl:when>
                        <xsl:otherwise>Todas</xsl:otherwise>
                   </xsl:choose>
                c) <xsl:choose>
                        <xsl:when test="$statementvalue = 'Automático'">2</xsl:when>
                        <xsl:otherwise>Automático</xsl:otherwise>
                   </xsl:choose>
                d) <xsl:choose>
                        <xsl:when test="$statementvalue = 'Todas' or $statementvalue = 'Automático' or $statementvalue = '40'">4</xsl:when>
                        <xsl:otherwise><xsl:value-of select="$statementvalue + 4"/></xsl:otherwise>
                   </xsl:choose> 
        </xsl:if>
            
        <!-- CONFIGURACIÓN DE PÁGINA : : Empezar sección -->    
        <xsl:variable name="statementvalue" select="$statementset/value/statement[name = 'Empezar sección']/value"/>
        <xsl:if test="$statementvalue">
            > Diseño de página / Configurar página [ALT + C + C] / Diseño / Empezar sección
            1. ¿Cómo está establecido el inicio de la primera sección del documento?
                a) <xsl:value-of select="$statementvalue"/>
                b) <xsl:choose>
                       <xsl:when test="$statementvalue = 'Página par'">Columna nueva</xsl:when>
                       <xsl:otherwise>Página par</xsl:otherwise>
                   </xsl:choose>
                c) <xsl:choose>
                       <xsl:when test="$statementvalue = 'Página nueva'">Columna nueva</xsl:when>
                       <xsl:otherwise>Página nueva</xsl:otherwise>
                   </xsl:choose>
                d) <xsl:choose>
                       <xsl:when test="$statementvalue = 'Página impar'">Columna nueva</xsl:when>
                       <xsl:otherwise>Página impar</xsl:otherwise>
                   </xsl:choose> 
        </xsl:if>
            
            

        <!-- BORDE DE PÁGINA
             - Ancho
             - Estilo
             - Arte
             - Color
             - Márgenes: superior, derecho, inferior, izquierdo
        - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - --> 
        
        <xsl:variable name="statementset" select="$wordactivity/block/division[statement[@class = 'page-format']]/statement[@class = 'borders-format' and (value/statement[name = 'Valor' and (value = 'Cuadro' or value = 'Sombra')])]" />

        <!-- BORDE DE PÁGINA : : Ancho -->    
        <xsl:variable name="statementvalue" select="number(replace(replace($statementset/value/statement[name='Ancho']/value, ' puntos', ''), ',', '.'))"/>
        <xsl:if test="$statementvalue">
            > Diseño de página / Bordes de página [ALT + F + B] / Borde de página / Ancho
            1. ¿Cuál es el grosor del borde de página establecido para el documento?
                a) <xsl:value-of select="format-number($statementvalue, '0,00 pto', 'es')"/>
                b) <xsl:value-of select="format-number(((floor(math:random() * 3100) div 100)), '0,00 pto', 'es')"/>
                c) <xsl:value-of select="format-number(((floor(math:random() * 3100) div 100)), '0,00 pto', 'es')"/>
                d) <xsl:value-of select="format-number(((floor(math:random() * 3100) div 100)), '0,00 pto', 'es')"/> 
        </xsl:if>
        
        <!-- BORDE DE PÁGINA : : Estilo -->    
        <xsl:variable name="borderstyle" select="$statementset/value/statement[name='Estilo']/value"/>
        <xsl:if test="$borderstyle">
            <xsl:variable name="order" select="floor(math:random() * 162)"/>
            > Diseño de página / Bordes de página [ALT + F + B] / Borde de página / Estilo
            1. ¿Cuál es el estilo seleccionado para el borde de página del documento?
                a) <xsl:value-of select="substring-before($borderstyle, ' (')"/>
                b) <xsl:call-template name="borderstylelist">
                       <xsl:with-param name="invalid" select="substring-before($borderstyle, ' (')"/>
                        <xsl:with-param name="order" select="$order"/>
                   </xsl:call-template>
                c) <xsl:call-template name="borderstylelist">
                       <xsl:with-param name="invalid" select="substring-before($borderstyle, ' (')"/>
                        <xsl:with-param name="order" select="$order + 1"/>
                   </xsl:call-template>
                d) <xsl:call-template name="borderstylelist">
                       <xsl:with-param name="invalid" select="substring-before($borderstyle, ' (')"/>
                        <xsl:with-param name="order" select="$order + 2"/>
                   </xsl:call-template> 
        </xsl:if>

        <!-- BORDE DE PÁGINA : : Arte -->    
        <xsl:variable name="borderart" select="$statementset/value/statement[name='Arte']/value"/>
        <xsl:if test="$borderart">
            <xsl:variable name="order" select="floor(math:random() * 162)"/>
            > Diseño de página / Bordes de página [ALT + F + B] / Borde de página / Arte
            1. ¿Cuál es el arte seleccionado para el borde de página del documento?
                a) <xsl:value-of select="substring-before($borderart, ' (')"/>
                b) <xsl:call-template name="borderartlist">
                       <xsl:with-param name="invalid" select="substring-before($borderart, ' (')"/>
                        <xsl:with-param name="order" select="$order"/>
                   </xsl:call-template>
                c) <xsl:call-template name="borderartlist">
                       <xsl:with-param name="invalid" select="substring-before($borderart, ' (')"/>
                        <xsl:with-param name="order" select="$order + 1"/>
                   </xsl:call-template>
                d) <xsl:call-template name="borderartlist">
                       <xsl:with-param name="invalid" select="substring-before($borderart, ' (')"/>
                        <xsl:with-param name="order" select="$order + 2"/>
                   </xsl:call-template> 
        </xsl:if>
            
        <!-- BORDE DE PÁGINA : : Color -->    
        <xsl:variable name="bordercolor" select="$statementset/value/statement[name='Color']/value"/>
        <xsl:if test="$bordercolor">
            > Diseño de página / Bordes de página [ALT + F + B] / Borde de página / Color
            1. ¿Cuál es el color del borde de página establecido para el documento?
                a) <xsl:value-of select="$bordercolor"/>
                b) RGB(<xsl:value-of select="string-join((format-number(floor(math:random() * 255), '0'), format-number(floor(math:random() * 255), '0'), format-number(floor(math:random() * 255), '0')), ',')"/>)
                b) HSL(<xsl:value-of select="string-join((format-number(floor(math:random() * 255), '0'), format-number(floor(math:random() * 255), '0'), format-number(floor(math:random() * 255), '0')), ',')"/>)
                d) Todas las anteriores son correctas
        </xsl:if>
        
        <!-- BORDE DE PÁGINA : Margen : ... - - - - - - - - - - - - - - - - - --> 
        <xsl:variable name="statementsubset" select="$statementset/value/statement[name = 'Margen' and default = 'Falso']"/>
        
        <!-- BORDE DE PÁGINA : Margen : Superior -->    
        <xsl:variable name="statementvalue" select="number(replace(replace($statementsubset/value/statement[name = 'Superior' and default = 'Falso']/value, ' puntos', ''), ',', '.'))"/>
        <xsl:if test="$statementvalue">
            > Diseño de página / Bordes de página [ALT + F + B] / Borde de página / Opciones... / Superior
            1. ¿Cuál la distancia establecida para el margen entre el borde superior de la página y el texto?
                a) <xsl:value-of select="format-number($statementvalue, '0,00 pto', 'es')"/>
                b) <xsl:value-of select="format-number(((floor(math:random() * 3100) div 100)), '0,00 pto', 'es')"/>
                c) <xsl:value-of select="format-number(((floor(math:random() * 3100) div 100)), '0,00 pto', 'es')"/>
                d) <xsl:value-of select="format-number(((floor(math:random() * 3100) div 100)), '0,00 pto', 'es')"/> 
        </xsl:if>
        
        <!-- BORDE DE PÁGINA : Margen : Derecho -->    
        <xsl:variable name="statementvalue" select="number(replace(replace($statementsubset/value/statement[name = 'Derecha' and default = 'Falso']/value, ' puntos', ''), ',', '.'))"/>
        <xsl:if test="$statementvalue">
            > Diseño de página / Bordes de página [ALT + F + B] / Borde de página / Opciones... / Derecho
            1. ¿Cuál la distancia establecida para el margen entre el borde derecho de la página y el texto?
                a) <xsl:value-of select="format-number($statementvalue, '0,00 pto', 'es')"/>
                b) <xsl:value-of select="format-number(((floor(math:random() * 3100) div 100)), '0,00 pto', 'es')"/>
                c) <xsl:value-of select="format-number(((floor(math:random() * 3100) div 100)), '0,00 pto', 'es')"/>
                d) <xsl:value-of select="format-number(((floor(math:random() * 3100) div 100)), '0,00 pto', 'es')"/> 
        </xsl:if>

        <!-- BORDE DE PÁGINA : Margen : Inferior -->    
        <xsl:variable name="statementvalue" select="number(replace(replace($statementsubset/value/statement[name = 'Inferior' and default = 'Falso']/value, ' puntos', ''), ',', '.'))"/>
        <xsl:if test="$statementvalue">
            > Diseño de página / Bordes de página [ALT + F + B] / Borde de página / Opciones... / Inferior
            1. ¿Cuál la distancia establecida para el margen entre el borde inferior de la página y el texto?
                a) <xsl:value-of select="format-number($statementvalue, '0,00 pto', 'es')"/>
                b) <xsl:value-of select="format-number(((floor(math:random() * 3100) div 100)), '0,00 pto', 'es')"/>
                c) <xsl:value-of select="format-number(((floor(math:random() * 3100) div 100)), '0,00 pto', 'es')"/>
                d) <xsl:value-of select="format-number(((floor(math:random() * 3100) div 100)), '0,00 pto', 'es')"/> 
        </xsl:if>
        
        <!-- BORDE DE PÁGINA : Margen : Izquierdo -->    
        <xsl:variable name="statementvalue" select="number(replace(replace($statementsubset/value/statement[name = 'Izquierda' and default = 'Falso']/value, ' puntos', ''), ',', '.'))"/>
        <xsl:if test="$statementvalue">
            > Diseño de página / Bordes de página [ALT + F + B] / Borde de página / Opciones... / Izquierdo
            1. ¿Cuál la distancia establecida para el margen entre el borde izquierdo de la página y el texto?
                a) <xsl:value-of select="format-number($statementvalue, '0,00 pto', 'es')"/>
                b) <xsl:value-of select="format-number(((floor(math:random() * 3100) div 100)), '0,00 pto', 'es')"/>
                c) <xsl:value-of select="format-number(((floor(math:random() * 3100) div 100)), '0,00 pto', 'es')"/>
                d) <xsl:value-of select="format-number(((floor(math:random() * 3100) div 100)), '0,00 pto', 'es')"/> 
        </xsl:if>
        
        

        <!-- FUENTE
             - [x] Tipo
             - [x] Estilo
             - [x] Tamaño
             - [x] Color
             - [ ] Efectos
             - Espaciado de caracteres
             - Posición
             - Escala
        - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - --> 
        
        <xsl:variable name="divisionset" select="$wordactivity/block/division[statement[@class = 'font-format' and default='Falso'] and target/value]" />
        
        <xsl:variable name="targetset" select="$divisionset/target[1]" />
        <xsl:variable name="statementset" select="$divisionset/statement[@class='font-format' and default='Falso'][1]" />
            
        <!-- FUENTE : Fuente  -->    
        <xsl:variable name="matchnumber" select="ceiling(math:random() * count($statementset))"/>    
        <xsl:if test="$matchnumber > 0">
            <xsl:variable name="target" select="normalize-space(replace($targetset[$matchnumber]/value, '[\r\n]', ''))"/>
            <xsl:variable name="statementvalue" select="$statementset[$matchnumber]/value/statement[name='Fuente']/value"/>
            <xsl:variable name="order" select="floor(math:random() * 163)"/>
            > Inicio / Fuente / Fuente [ALT + F + E] / Fuente / Fuente
            1. ¿Cuál es el tipo de letra empleado en el párrafo «<xsl:value-of select="$target"/>»?   
                a) <xsl:value-of select="$statementvalue"/>
                b) <xsl:call-template name="fontfamilylist">
                       <xsl:with-param name="invalid" select="substring-before($statementvalue, ' (')"/>
                        <xsl:with-param name="order" select="$order"/>
                   </xsl:call-template>
                c) <xsl:call-template name="fontfamilylist">
                       <xsl:with-param name="invalid" select="substring-before($statementvalue, ' (')"/>
                        <xsl:with-param name="order" select="$order + 1"/>
                   </xsl:call-template>
                d) <xsl:call-template name="fontfamilylist">
                       <xsl:with-param name="invalid" select="substring-before($statementvalue, ' (')"/>
                        <xsl:with-param name="order" select="$order + 2"/>
                   </xsl:call-template> 
        </xsl:if>
        
        <!-- FUENTE : Estilo de fuente -->    
        <xsl:variable name="matchnumber" select="ceiling(math:random() * count($statementset))"/>    
        <xsl:if test="$matchnumber > 0">
            <xsl:variable name="target" select="normalize-space(replace($targetset[$matchnumber]/value, '[\r\n]', ''))"/>
            <xsl:variable name="statementvalue" select="$statementset[$matchnumber]/value/statement[name='Estilo de fuente']/value"/>
            > Inicio / Fuente / Fuente [ALT + F + E] / Fuente / Estilo de fuente
            1. ¿Cuál es el estilo de fuente empleado en el párrafo «<xsl:value-of select="$target"/>»?   
                a) <xsl:value-of select="$statementvalue"/>
                b) <xsl:choose>
                       <xsl:when test="$statementvalue = 'Negrita'">Normal</xsl:when>
                       <xsl:otherwise>Negrita</xsl:otherwise>
                   </xsl:choose>
                c) <xsl:choose>
                       <xsl:when test="$statementvalue = 'Cursiva'">Normal</xsl:when>
                       <xsl:otherwise>Cursiva</xsl:otherwise>
                   </xsl:choose>
                d) <xsl:choose>
                       <xsl:when test="$statementvalue = 'Negrita cursiva'">Normal</xsl:when>
                       <xsl:otherwise>Negrita cursiva</xsl:otherwise>
                   </xsl:choose> 
        </xsl:if>       
        
        <!-- FUENTE : Tamaño -->    
        <xsl:variable name="matchnumber" select="ceiling(math:random() * count($statementset))"/>    
        <xsl:if test="$matchnumber > 0">
            <xsl:variable name="target" select="normalize-space(replace($targetset[$matchnumber]/value, '[\r\n]', ''))"/>
            <xsl:variable name="statementvalue" select="number(replace(replace($statementset[$matchnumber]/value/statement[name='Tamaño']/value, ',', '.'), 'puntos', ''))"/>
            > Inicio / Fuente / Fuente [ALT + F + E] / Fuente / Tamaño
            1. ¿Cuál es el tamaño de letra empleado en el párrafo «<xsl:value-of select="$target"/>»?   
                a) <xsl:value-of select="format-number($statementvalue, '0,00', 'es')"/> puntos
                b) <xsl:value-of select="format-number($statementvalue + 0.5, '#.##0,00', 'es')"/> puntos
                c) <xsl:value-of select="format-number($statementvalue, '#.##0,00', 'es')"/> píxeles
                d) <xsl:value-of select="format-number($statementvalue - 0.5, '#.##0,00', 'es')"/> píxeles
            </xsl:if>
        
        <!-- FUENTE : Color -->    
        <xsl:variable name="matchnumber" select="ceiling(math:random() * count($statementset))"/>    
        <xsl:if test="$matchnumber > 0">
            <xsl:variable name="target" select="normalize-space(replace($targetset[$matchnumber]/value, '[\r\n]', ''))"/>
            <xsl:variable name="statementvalue" select="$statementset[$matchnumber]/value/statement[name='Color']/value"/>
            > Inicio / Fuente / Fuente [ALT + F + E] / Fuente / Color
            1. ¿Cuál es el color de letra empleado en el párrafo «<xsl:value-of select="$target"/>»?   
                a) <xsl:value-of select="$statementvalue"/>
                b) RGB(<xsl:value-of select="string-join((format-number(floor(math:random() * 255), '0'), format-number(floor(math:random() * 255), '0'), format-number(floor(math:random() * 255), '0')), ',')"/>)
                b) HSL(<xsl:value-of select="string-join((format-number(floor(math:random() * 255), '0'), format-number(floor(math:random() * 255), '0'), format-number(floor(math:random() * 255), '0')), ',')"/>)
                d) Todas las anteriores son correctas
        </xsl:if> 
            
        <!-- FUENTE : Subrayado -->    
        <xsl:variable name="matchnumber" select="ceiling(math:random() * count($statementset))"/>    
        <xsl:if test="$matchnumber > 0">
            <xsl:variable name="target" select="normalize-space(replace($targetset[$matchnumber]/value, '[\r\n]', ''))"/>
            <xsl:variable name="statementvalue" select="$statementset[$matchnumber]/value/statement[name='Subrayado']/value"/>
            <xsl:variable name="order" select="floor(math:random() * 14)"/>
            > Inicio / Fuente / Fuente [ALT + F + E] / Fuente / Subrayado
            1. ¿Cuál es el estilo de subrayado empleado en el párrafo «<xsl:value-of select="$target"/>»?   
                a) <xsl:value-of select="$statementvalue"/>
                b) <xsl:call-template name="underlinestylelist">
                       <xsl:with-param name="invalid" select="substring-before($statementvalue, ' (')"/>
                        <xsl:with-param name="order" select="$order"/>
                   </xsl:call-template>
                c) <xsl:call-template name="underlinestylelist">
                       <xsl:with-param name="invalid" select="substring-before($statementvalue, ' (')"/>
                        <xsl:with-param name="order" select="$order + 1"/>
                   </xsl:call-template>
                d) <xsl:call-template name="underlinestylelist">
                       <xsl:with-param name="invalid" select="substring-before($statementvalue, ' (')"/>
                        <xsl:with-param name="order" select="$order + 2"/>
                   </xsl:call-template> 
        </xsl:if> 
            
        <!-- FUENTE : Color de subrayado -->    
        <xsl:variable name="matchnumber" select="ceiling(math:random() * count($statementset))"/>    
        <xsl:if test="$matchnumber > 0 and not($statementset[$matchnumber]/value/statement[name='Subrayado']/value = '(Ninguno)')">
            <xsl:variable name="target" select="normalize-space(replace($targetset[$matchnumber]/value, '[\r\n]', ''))"/>
            <xsl:variable name="statementvalue" select="$statementset[$matchnumber]/value/statement[name='Color de subrayado']/value"/>
            > Inicio / Fuente / Fuente [ALT + F + E] / Fuente / Color de subrayado
            1. ¿Cuál es el color de subrayado empleado en el párrafo «<xsl:value-of select="$target"/>»?   
                a) <xsl:value-of select="$statementvalue"/>
                b) RGB(<xsl:value-of select="string-join((format-number(floor(math:random() * 255), '0'), format-number(floor(math:random() * 255), '0'), format-number(floor(math:random() * 255), '0')), ',')"/>)
                b) HSL(<xsl:value-of select="string-join((format-number(floor(math:random() * 255), '0'), format-number(floor(math:random() * 255), '0'), format-number(floor(math:random() * 255), '0')), ',')"/>)
                d) Todas las anteriores son correctas
        </xsl:if>  

        <!-- FUENTE : Escala  -->    
        <xsl:variable name="matchnumber" select="ceiling(math:random() * count($statementset))"/>    
        <xsl:if test="$matchnumber > 0">
            <xsl:variable name="target" select="normalize-space(replace($targetset[$matchnumber]/value, '[\r\n]', ''))"/>
            <xsl:variable name="statementvalue" select="number(replace($statementset[$matchnumber]/value/statement[name='Escala']/value, '%', ''))"/>
            > Inicio / Fuente / Fuente [ALT + F + E] / Avanzado / Escala
            1. ¿Cuál es el valor establecido para la escala de carácter empleado en el párrafo «<xsl:value-of select="$target"/>»?   
                a) <xsl:value-of select="format-number($statementvalue, '0,00', 'es')"/>%
                b) <xsl:value-of select="format-number($statementvalue + 0.5, '#.##0,00', 'es')"/>%
                c) <xsl:value-of select="format-number($statementvalue + 5.5, '#.##0,00', 'es')"/>%
                d) <xsl:value-of select="format-number($statementvalue - 0.5, '#.##0,00', 'es')"/>%
        </xsl:if>  
        
        <!-- FUENTE : Espaciado  -->    
        <xsl:variable name="matchnumber" select="ceiling(math:random() * count($statementset))"/>    
        <xsl:if test="$matchnumber > 0">
            <xsl:variable name="target" select="normalize-space(replace($targetset[$matchnumber]/value, '[\r\n]', ''))"/>
            <xsl:variable name="statementvalue" select="$statementset[$matchnumber]/value/statement[name='Espaciado']/value"/>
            <xsl:variable name="space" select="substring-before($statementvalue, ' en ')"/>
            <xsl:variable name="in" select="number(replace(replace(substring-after($statementvalue, ' en '), ',', '.'), ' puntos', ''))"/>
            > Inicio / Fuente / Fuente [ALT + F + E] / Avanzado / Espaciado
            1. ¿Cuál es el espaciado de carácter empleado en el párrafo «<xsl:value-of select="$target"/>»?   
                a) <xsl:value-of select="$space"/> en <xsl:value-of select="format-number($in, '0,00', 'es')"/> puntos
                b) <xsl:choose>
                       <xsl:when test="$space = 'Expandido'">Comprimido</xsl:when>
                       <xsl:otherwise>Expandido</xsl:otherwise>
                   </xsl:choose> en <xsl:value-of select="format-number($in, '#.##0,00', 'es')"/> puntos
                c) <xsl:value-of select="$space"/> en <xsl:value-of select="format-number($in + ((math:random() *5) div 100), '#.##0,00', 'es')"/> puntos
                d) <xsl:choose>
                       <xsl:when test="$space = 'Expandido'">Comprimido</xsl:when>
                       <xsl:otherwise>Expandido</xsl:otherwise>
                   </xsl:choose> en <xsl:value-of select="format-number($in + ((math:random() *5) div 100), '#.##0,00', 'es')"/> puntos
        </xsl:if>  

        <!-- FUENTE : Espaciado  -->    
        <xsl:variable name="matchnumber" select="ceiling(math:random() * count($statementset))"/>    
        <xsl:if test="$matchnumber > 0">
            <xsl:variable name="target" select="normalize-space(replace($targetset[$matchnumber]/value, '[\r\n]', ''))"/>
            <xsl:variable name="statementvalue" select="$statementset[$matchnumber]/value/statement[name='Posición']/value"/>
            <xsl:variable name="space" select="substring-before($statementvalue, ' en ')"/>
            <xsl:variable name="in" select="number(replace(replace(substring-after($statementvalue, ' en '), ',', '.'), ' puntos', ''))"/>
            > Inicio / Fuente / Fuente [ALT + F + E] / Avanzado / Posición
            1. ¿Cuál es la posición de carácter establecida para el párrafo «<xsl:value-of select="$target"/>»?   
                a) <xsl:value-of select="$space"/> en <xsl:value-of select="format-number($in, '0,00', 'es')"/> puntos
                b) <xsl:choose>
                       <xsl:when test="$space = 'Elevado'">Disminuido</xsl:when>
                       <xsl:otherwise>Elevado</xsl:otherwise>
                   </xsl:choose> en <xsl:value-of select="format-number($in, '#.##0,00', 'es')"/> puntos
                c) <xsl:value-of select="$space"/> en <xsl:value-of select="format-number($in + ((math:random() *5) div 100), '#.##0,00', 'es')"/> puntos
                d) <xsl:choose>
                       <xsl:when test="$space = 'Elevado'">Disminuido</xsl:when>
                       <xsl:otherwise>Elevado</xsl:otherwise>
                   </xsl:choose> en <xsl:value-of select="format-number($in + ((math:random() *5) div 100), '#.##0,00', 'es')"/> puntos
        </xsl:if>  



        <!-- PÁRRAFO
             - [x] Alineación
             - [x] Nivel de esquema
             - [x] Sangría izquierda
             - [x] Sangría derecha
             - [x] Sangría especial
             - [x] Espaciado anterior
             - [x] Espaciado posterior
             - [ ] Interlineado
             - [ ] Salto de página anterior
             - [ ] Control de viudas y huérfanas
             - [ ] Conservar líneas juntas
             - [ ] Conservar con el siguiente
             - [ ] No dividir con guiones
             - [ ] Suplrimir números de línea
        - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - --> 
        <xsl:variable name="divisionset" select="$wordactivity/block/division[statement[@class = 'paragraph-format' and default='Falso'] and target/value]" />
        
        <xsl:variable name="targetset" select="$divisionset/target[1]" />
        <xsl:variable name="statementset" select="$divisionset/statement[@class='paragraph-format' and default='Falso'][1]" />
            
        <!-- PÁRRAFO : Alineación  -->    
        <xsl:variable name="matchnumber" select="ceiling(math:random() * count($statementset))"/>    
        <xsl:if test="$matchnumber > 0">
            <xsl:variable name="target" select="normalize-space(replace($targetset[$matchnumber]/value, '[\r\n]', ''))"/>
            <xsl:variable name="statementvalue" select="$statementset[$matchnumber]/value/statement[name='Alineación']/value"/>
            > Inicio / Párrafo / Párrafo [ALT + F + P] / Sangría y espacio / Alineación
            1. ¿Cuál es la alineación de párrafo establecida para el párrafo «<xsl:value-of select="$target"/>» existente en el documento?
                a) <xsl:value-of select="$statementvalue"/>  
                b) <xsl:choose>
                    <xsl:when test="$statementvalue = 'Centrada'">Izquierda</xsl:when>
                    <xsl:otherwise>Centrada</xsl:otherwise>
                </xsl:choose>
                c) <xsl:choose>
                    <xsl:when test="$statementvalue = 'Derecha'">Izquierda</xsl:when>
                    <xsl:otherwise>Derecha</xsl:otherwise>
                </xsl:choose>
                d) <xsl:choose>
                    <xsl:when test="$statementvalue = 'Justificada'">Izquierda</xsl:when>
                    <xsl:otherwise>Justificada</xsl:otherwise>
                </xsl:choose> 
        </xsl:if>
            
       <!-- PÁRRAFO : Nivel de esquema  -->    
        <xsl:variable name="matchnumber" select="ceiling(math:random() * count($statementset))"/>    
        <xsl:if test="$matchnumber > 0">
            <xsl:variable name="target" select="normalize-space(replace($targetset[$matchnumber]/value, '[\r\n]', ''))"/>
            <xsl:variable name="statementvalue" select="$statementset[$matchnumber]/value/statement[name='Nivel de esquema']/value"/>
            > Inicio / Párrafo / Párrafo [ALT + F + P] / Sangría y espacio / Nivel de esquema
            1. ¿Cuál es el nivel de esquema establecido para el párrafo «<xsl:value-of select="$target"/>» existente en el documento?
                a) <xsl:value-of select="$statementvalue"/>  
                b) <xsl:choose>
                    <xsl:when test="$statementvalue = 'Nivel 1'">Texto independiente</xsl:when>
                    <xsl:otherwise>Nivel 1</xsl:otherwise>
                </xsl:choose>
                c) <xsl:choose>
                    <xsl:when test="$statementvalue = 'Nivel 2'">Texto independiente</xsl:when>
                    <xsl:otherwise>Nivel 2</xsl:otherwise>
                </xsl:choose>
                d) <xsl:choose>
                    <xsl:when test="$statementvalue = 'Nivel 3'">Texto independiente</xsl:when>
                    <xsl:otherwise>Nivel 3</xsl:otherwise>
                </xsl:choose> 
        </xsl:if>
                     
        <!-- PÁRRAFO : Sangrías : Izquierda  -->   
        <xsl:variable name="matchnumber" select="ceiling(math:random() * count($statementset))"/>    
        <xsl:if test="$matchnumber > 0">
            <xsl:variable name="target" select="normalize-space(replace($targetset[$matchnumber]/value, '[\r\n]', ''))"/>
            <xsl:variable name="statementvalue" select="$statementset[$matchnumber]/value/statement[name='Sangrías']/value/statement[name='Izquierda']/value"/>
            <xsl:variable name="distance" select="number(replace(substring-before($statementvalue, ' '), ',', '.'))"/>
            <xsl:variable name="unit" select="substring-after($statementvalue, ' ')"/>
            > Inicio / Párrafo / Párrafo [ALT + F + P] / Sangría y espacio / Izquierda
            1. ¿Cuál es el valor establecido para la sangría izquierda del párrafo «<xsl:value-of select="$target"/>» existente en el documento?
                a) <xsl:value-of select="format-number($distance, concat('0,00 ', $unit), 'es')"/>
                b) <xsl:value-of select="format-number($distance + ((floor(math:random() * 100) div 100)), concat('0,00 ', $unit), 'es')"/>
                c) <xsl:value-of select="format-number($distance - ((floor(math:random() * 100) div 100)), concat('0,00 ', $unit), 'es')"/>
                d) <xsl:value-of select="format-number($distance + ((floor(math:random() * 100) div 100)), concat('0,00 ', $unit), 'es')"/> 
        </xsl:if>
            
        <!-- PÁRRAFO : Sangrías : Derecha  -->      
        <xsl:variable name="matchnumber" select="ceiling(math:random() * count($statementset))"/>    
        <xsl:if test="$matchnumber > 0">
            <xsl:variable name="target" select="normalize-space(replace($targetset[$matchnumber]/value, '[\r\n]', ''))"/>
            <xsl:variable name="statementvalue" select="$statementset[$matchnumber]/value/statement[name='Sangrías']/value/statement[name='Derecha']/value"/>
            <xsl:variable name="distance" select="number(replace(substring-before($statementvalue, ' '), ',', '.'))"/>
            <xsl:variable name="unit" select="substring-after($statementvalue, ' ')"/>            
            > Inicio / Párrafo / Párrafo [ALT + F + P] / Sangría y espacio / Derecha
            1. ¿Cuál es el valor establecido para la sangría derecha del párrafo «<xsl:value-of select="$target"/>» existente en el documento?
                a) <xsl:value-of select="format-number($distance, concat('0,00 ', $unit), 'es')"/>
                b) <xsl:value-of select="format-number($distance + ((floor(math:random() * 100) div 100)), concat('0,00 ', $unit), 'es')"/>
                c) <xsl:value-of select="format-number($distance - ((floor(math:random() * 100) div 100)), concat('0,00 ', $unit), 'es')"/>
                d) <xsl:value-of select="format-number($distance + ((floor(math:random() * 100) div 100)), concat('0,00 ', $unit), 'es')"/> 
        </xsl:if>
            
        <!-- PÁRRAFO : Sangrías : Especial  -->    
        <xsl:variable name="matchnumber" select="ceiling(math:random() * count($statementset))"/>    
        <xsl:if test="$matchnumber > 0 and not($statementset[$matchnumber]/value/statement[name='Sangrías']/value/statement[name='Especial']/value = '(Ninguno)')">
            <xsl:variable name="target" select="normalize-space(replace($targetset[$matchnumber]/value, '[\r\n]', ''))"/>
            <xsl:variable name="statementvalue" select="$statementset[$matchnumber]/value/statement[name='Sangrías']/value/statement[name='Especial']/value"/>
            <xsl:variable name="indenttype" select="substring-before($statementvalue, ' en ')"/>
            <xsl:variable name="indentvalue" select="substring-after($statementvalue, ' en ')"/>
            <xsl:variable name="distance" select="number(replace(substring-before($indentvalue, ' '), ',', '.'))"/>
            <xsl:variable name="unit" select="substring-after($indentvalue, ' ')"/>
            > Inicio / Párrafo / Párrafo [ALT + F + P] / Sangría y espacio / Especial
            1. ¿Cuál es el valor establecido para la sangría especial del párrafo «<xsl:value-of select="$target"/>» existente en el documento?
                a) <xsl:value-of select="$indenttype"/> en <xsl:value-of select="format-number($distance, concat('0,00 ', $unit), 'es')"/>
                b) <xsl:value-of select="$indenttype"/> en <xsl:value-of select="format-number($distance + ((floor(math:random() * 100) div 100)), concat('0,00 ', $unit), 'es')"/>
                c) <xsl:choose>
                       <xsl:when test="$indenttype = 'Francesa'">Primera línea</xsl:when>
                       <xsl:otherwise>Francesa</xsl:otherwise>
                   </xsl:choose> en <xsl:value-of select="format-number($distance + ((floor(math:random() * 100) div 100)), concat('0,00 ', $unit), 'es')"/>
                d) <xsl:choose>
                       <xsl:when test="$indenttype = 'Francesa'">Primera línea</xsl:when>
                       <xsl:otherwise>Francesa</xsl:otherwise>
                   </xsl:choose> en <xsl:value-of select="format-number($distance + ((floor(math:random() * 100) div 100)), concat('0,00 ', $unit), 'es')"/> 
        </xsl:if>
        
        <!-- PÁRRAFO : Espaciados : Anterior -->      
        <xsl:variable name="matchnumber" select="ceiling(math:random() * count($statementset))"/>    
        <xsl:if test="$matchnumber > 0">
            <xsl:variable name="target" select="normalize-space(replace($targetset[$matchnumber]/value, '[\r\n]', ''))"/>
            <xsl:variable name="statementvalue" select="$statementset[$matchnumber]/value/statement[name='Espaciados']/value/statement[name='Anterior']/value"/>
            <xsl:variable name="distance">
                <xsl:choose>
                    <xsl:when test="$statementvalue='Automático'"><xsl:value-of select="number('0')" /></xsl:when>
                    <xsl:otherwise><xsl:value-of select="number(replace(substring-before($statementvalue, ' '), ',', '.'))"/></xsl:otherwise>
                </xsl:choose>
            </xsl:variable>
            <xsl:variable name="unit">
                <xsl:choose>
                    <xsl:when test="$statementvalue='Automático'">pto</xsl:when>
                    <xsl:otherwise><xsl:value-of select="substring-after($statementvalue, ' ')"/></xsl:otherwise>
                </xsl:choose>
            </xsl:variable>
            > Inicio / Párrafo / Párrafo [ALT + F + P] / Sangría y espacio / Anterior
            1. ¿Cuál es el valor establecido para el espaciado anterior del párrafo «<xsl:value-of select="$target"/>» existente en el documento?
                a) <xsl:choose>
                       <xsl:when test="$statementvalue = 'Automático'">Automático</xsl:when>
                       <xsl:otherwise><xsl:value-of select="format-number($distance, concat('0,00 ', $unit), 'es')"/></xsl:otherwise>
                   </xsl:choose> 
                b) <xsl:value-of select="format-number($distance + ((floor(math:random() * 100) div 100)), concat('0,00 ', $unit), 'es')"/>
                c) <xsl:value-of select="format-number($distance + ((floor(math:random() * 100) div 100)), concat('0,00 ', $unit), 'es')"/>
                d) <xsl:value-of select="format-number($distance + ((floor(math:random() * 100) div 100)), concat('0,00 ', $unit), 'es')"/> 
        </xsl:if>            
       
        <!-- PÁRRAFO : Espaciados : Posterior -->      
        <xsl:variable name="matchnumber" select="ceiling(math:random() * count($statementset))"/>    
        <xsl:if test="$matchnumber > 0">
            <xsl:variable name="target" select="normalize-space(replace($targetset[$matchnumber]/value, '[\r\n]', ''))"/>
            <xsl:variable name="statementvalue" select="$statementset[$matchnumber]/value/statement[name='Espaciados']/value/statement[name='Posterior']/value"/>
            <xsl:variable name="distance">
                <xsl:choose>
                    <xsl:when test="$statementvalue='Automático'"><xsl:value-of select="number('0')" /></xsl:when>
                    <xsl:otherwise><xsl:value-of select="number(replace(substring-before($statementvalue, ' '), ',', '.'))"/></xsl:otherwise>
                </xsl:choose>
            </xsl:variable>
            <xsl:variable name="unit">
                <xsl:choose>
                    <xsl:when test="$statementvalue='Automático'">pto</xsl:when>
                    <xsl:otherwise><xsl:value-of select="substring-after($statementvalue, ' ')"/></xsl:otherwise>
                </xsl:choose>
            </xsl:variable>
            > Inicio / Párrafo / Párrafo [ALT + F + P] / Sangría y espacio / Posterior
            1. ¿Cuál es el valor establecido para el espaciado posterior del párrafo «<xsl:value-of select="$target"/>» existente en el documento?
                a) <xsl:choose>
                       <xsl:when test="$statementvalue = 'Automático'">Automático</xsl:when>
                       <xsl:otherwise><xsl:value-of select="format-number($distance, concat('0,00 ', $unit), 'es')"/></xsl:otherwise>
                   </xsl:choose> 
                b) <xsl:value-of select="format-number($distance + ((floor(math:random() * 100) div 100)), concat('0,00 ', $unit), 'es')"/>
                c) <xsl:value-of select="format-number($distance + ((floor(math:random() * 100) div 100)), concat('0,00 ', $unit), 'es')"/>
                d) <xsl:value-of select="format-number($distance + ((floor(math:random() * 100) div 100)), concat('0,00 ', $unit), 'es')"/> 
        </xsl:if>            

        <!-- PÁRRAFO : Espaciados : Interlineado -->      
        <xsl:variable name="matchnumber" select="ceiling(math:random() * count($statementset))"/>    
        <xsl:if test="$matchnumber > 0">
            <xsl:variable name="target" select="normalize-space(replace($targetset[$matchnumber]/value, '[\r\n]', ''))"/>
            <xsl:variable name="statementvalue" select="$statementset[$matchnumber]/value/statement[name='Espaciados']/value/statement[name='Interlineado']/value"/>
            > Inicio / Párrafo / Párrafo [ALT + F + P] / Sangría y espacio / Interlineado
            1. ¿Cuál es el valor establecido para el interlineado del párrafo «<xsl:value-of select="$target"/>» existente en el documento?
                a) <xsl:value-of select="$statementvalue"/>
                b) <xsl:value-of select="format-number(((floor(math:random() * 100) div 100)), 'Múltiple en 0,00', 'es')"/>
                c) <xsl:value-of select="format-number(((floor(math:random() * 100) div 100)), 'Mínimo en 0,00 pto', 'es')"/>
                d) <xsl:value-of select="format-number(((floor(math:random() * 100) div 100)), 'Exacto en 0,00 pto', 'es')"/> 
        </xsl:if>           

        <!-- PÁRRAFO : Líneas y saltos de página -->      
        <xsl:variable name="matchnumber" select="ceiling(math:random() * count($statementset))"/>    
        <xsl:if test="$matchnumber > 0">
            <xsl:variable name="target" select="normalize-space(replace($targetset[$matchnumber]/value, '[\r\n]', ''))"/>
            <xsl:variable name="statementname">
                <xsl:variable name="order" select="ceiling(math:random() * 3)"/>
                <xsl:choose>
                    <xsl:when test="$order = 1">Control de viudas y huérfanas</xsl:when>
                    <xsl:when test="$order = 2">No dividir con guiones</xsl:when>
                    <xsl:otherwise>Suprimir números de línea</xsl:otherwise>
                </xsl:choose> 
            </xsl:variable>
            > Inicio / Párrafo / Párrafo [ALT + F + P] / Líneas y saltos de página / ...
            1. ¿Cuál de las siguientes afirmaciones sobre el párrafo «<xsl:value-of select="$target"/>» existente en el documento, NO es cierta?
                a) La opción <xsl:value-of select="fn:lower-case($statementname)"/><xsl:if test="$statementset[$matchnumber]/value/statement[name=$statementname]/value = 'Sí'"> no</xsl:if> está activa
                b) <xsl:value-of select="normalize-space(concat('La opción conservar con el siguiente ', replace(fn:lower-case($statementset[$matchnumber]/value/statement[name='Conservar con el siguiente']/value), 'sí', ''), ' está activa'))" />
                c) <xsl:value-of select="normalize-space(concat('La opción conservar líneas juntas ', replace(fn:lower-case($statementset[$matchnumber]/value/statement[name='Conservar líneas juntas']/value), 'sí', ''), ' está activa'))" />
                d) <xsl:value-of select="normalize-space(concat('La opción salto de página anterior ', replace(fn:lower-case($statementset[$matchnumber]/value/statement[name='Salto de página anterior']/value), 'sí', ''), ' está activa'))" /> 
        </xsl:if>           



        <!-- BORDE DE PÁRRAFO
             - Ancho
             - Estilo
             - Arte
             - Color
             - Márgenes: superior, derecho, inferior, izquierdo
        - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - --> 
        
        <xsl:variable name="divisionset" select="$wordactivity/block/division[statement[@class='borders-format' and default = 'Falso'] and target/value]" />

        <xsl:variable name="statementset" select="$divisionset/(statement[@class='borders-format' and default = 'Falso'][1])"/>
        <xsl:variable name="targetset" select="$divisionset/(target[1])"/>

        <!-- BORDE DE PÁRRAFO : : Ancho -->    
        <xsl:variable name="matchnumber" select="ceiling(math:random() * count($statementset))"/> 
        <xsl:variable name="targetvalue" select="normalize-space(replace($targetset[$matchnumber], '[\r\n]', ' '))"/>
        <xsl:variable name="statementvalue" select="number(replace(replace($statementset[$matchnumber]/value/statement[name='Ancho']/value, ' puntos', ''), ',', '.'))"/>
        <xsl:if test="$statementvalue">
            > Inicio / Párrafo / Bordes y sombreado [ALT + F + B] / Bordes / Ancho
            1. ¿Cuál es el grosor del borde establecido para el párrafo «<xsl:value-of select="$targetvalue"/>» existente en el documento?
                a) <xsl:value-of select="format-number($statementvalue, '0,00 pto', 'es')"/>
                b) <xsl:value-of select="format-number(((floor(math:random() * 3100) div 100)), '0,00 pto', 'es')"/>
                c) <xsl:value-of select="format-number(((floor(math:random() * 3100) div 100)), '0,00 pto', 'es')"/>
                d) <xsl:value-of select="format-number(((floor(math:random() * 3100) div 100)), '0,00 pto', 'es')"/> 
        </xsl:if>
        
        <!-- BORDE DE PÁRRAFO : : Estilo -->    
        <xsl:variable name="matchnumber" select="ceiling(math:random() * count($statementset))"/> 
        <xsl:variable name="targetvalue" select="normalize-space(replace($targetset[$matchnumber], '[\r\n]', ' '))"/>
        <xsl:variable name="borderstyle" select="$statementset[$matchnumber]/value/statement[name='Estilo']/value"/>
        <xsl:if test="$borderstyle">
            <xsl:variable name="order" select="floor(math:random() * 162)"/>
            > Inicio / Párrafo / Bordes y sombreado [ALT + F + B] / Bordes / Estilo
            1. ¿Cuál es el estilo del borde establecido para el párrafo «<xsl:value-of select="$targetvalue"/>» existente en el documento?
                a) <xsl:value-of select="substring-before($borderstyle, ' (')"/>
                b) <xsl:call-template name="borderstylelist">
                       <xsl:with-param name="invalid" select="substring-before($borderstyle, ' (')"/>
                        <xsl:with-param name="order" select="$order"/>
                   </xsl:call-template>
                c) <xsl:call-template name="borderstylelist">
                       <xsl:with-param name="invalid" select="substring-before($borderstyle, ' (')"/>
                        <xsl:with-param name="order" select="$order + 1"/>
                   </xsl:call-template>
                d) <xsl:call-template name="borderstylelist">
                       <xsl:with-param name="invalid" select="substring-before($borderstyle, ' (')"/>
                        <xsl:with-param name="order" select="$order + 2"/>
                   </xsl:call-template> 
        </xsl:if>

        <!-- BORDE DE PÁRRAFO : : Color -->    
        <xsl:variable name="matchnumber" select="ceiling(math:random() * count($statementset))"/> 
        <xsl:variable name="targetvalue" select="normalize-space(replace($targetset[$matchnumber], '[\r\n]', ' '))"/>
        <xsl:variable name="bordercolor" select="$statementset[$matchnumber]/value/statement[name='Color']/value"/>
        <xsl:if test="$bordercolor">
            > Inicio / Párrafo / Bordes y sombreado [ALT + F + B] / Bordes / Color
            1. ¿Cuál es el color del borde establecido para el párrafo «<xsl:value-of select="$targetvalue"/>» existente en el documento?
                a) <xsl:value-of select="$bordercolor"/>
                b) RGB(<xsl:value-of select="string-join((format-number(floor(math:random() * 255), '0'), format-number(floor(math:random() * 255), '0'), format-number(floor(math:random() * 255), '0')), ',')"/>)
                b) HSL(<xsl:value-of select="string-join((format-number(floor(math:random() * 255), '0'), format-number(floor(math:random() * 255), '0'), format-number(floor(math:random() * 255), '0')), ',')"/>)
                d) Todas las anteriores son correctas
        </xsl:if>
        
        <!-- BORDE DE PÁRRAFO : Margen : ... - - - - - - - - - - - - - - - - - --> 
        <xsl:variable name="statementsubset" select="$statementset/value/statement[name = 'Desde el texto' and default = 'Falso']"/>
        
        <!-- BORDE DE PÁRRAFO : Margen : Superior -->    
        <xsl:variable name="matchnumber" select="ceiling(math:random() * count($statementset))"/> 
        <xsl:variable name="targetvalue" select="normalize-space(replace($targetset[$matchnumber], '[\r\n]', ' '))"/>
        <xsl:variable name="statementvalue" select="number(replace(replace($statementsubset[$matchnumber]/value/statement[name = 'Superior' and default = 'Falso']/value, ' puntos', ''), ',', '.'))"/>
        <xsl:if test="$statementvalue">
            > Inicio / Párrafo / Bordes y sombreado [ALT + F + B] / Bordes / Opciones... / Superior
            1. ¿Cuál la distancia establecida para el margen entre el borde superior del párrafo «<xsl:value-of select="$targetvalue"/>» y el texto?
                a) <xsl:value-of select="format-number($statementvalue, '0,00 pto', 'es')"/>
                b) <xsl:value-of select="format-number(((floor(math:random() * 3100) div 100)), '0,00 pto', 'es')"/>
                c) <xsl:value-of select="format-number(((floor(math:random() * 3100) div 100)), '0,00 pto', 'es')"/>
                d) <xsl:value-of select="format-number(((floor(math:random() * 3100) div 100)), '0,00 pto', 'es')"/> 
        </xsl:if>
        
        <!-- BORDE DE PÁRRAFO : Margen : Derecho -->    
        <xsl:variable name="matchnumber" select="ceiling(math:random() * count($statementset))"/> 
        <xsl:variable name="targetvalue" select="normalize-space(replace($targetset[$matchnumber], '[\r\n]', ' '))"/>
        <xsl:variable name="statementvalue" select="number(replace(replace($statementsubset[$matchnumber]/value/statement[name = 'Derecha' and default = 'Falso']/value, ' puntos', ''), ',', '.'))"/>
        <xsl:if test="$statementvalue">
            > Inicio / Párrafo / Bordes y sombreado [ALT + F + B] / Bordes / Opciones... / Derecho
            1. ¿Cuál la distancia establecida para el margen entre el borde derecho del párrafo «<xsl:value-of select="$targetvalue"/>» y el texto?
                a) <xsl:value-of select="format-number($statementvalue, '0,00 pto', 'es')"/>
                b) <xsl:value-of select="format-number(((floor(math:random() * 3100) div 100)), '0,00 pto', 'es')"/>
                c) <xsl:value-of select="format-number(((floor(math:random() * 3100) div 100)), '0,00 pto', 'es')"/>
                d) <xsl:value-of select="format-number(((floor(math:random() * 3100) div 100)), '0,00 pto', 'es')"/> 
        </xsl:if>

        <!-- BORDE DE PÁRRAFO : Margen : Inferior -->    
        <xsl:variable name="matchnumber" select="ceiling(math:random() * count($statementset))"/> 
        <xsl:variable name="targetvalue" select="normalize-space(replace($targetset[$matchnumber], '[\r\n]', ' '))"/>
        <xsl:variable name="statementvalue" select="number(replace(replace($statementsubset[$matchnumber]/value/statement[name = 'Inferior' and default = 'Falso']/value, ' puntos', ''), ',', '.'))"/>
        <xsl:if test="$statementvalue">
            > Inicio / Párrafo / Bordes y sombreado [ALT + F + B] / Bordes / Opciones... / Inferior
            1. ¿Cuál la distancia establecida para el margen entre el borde inferior del párrafo «<xsl:value-of select="$targetvalue"/>» y el texto?
                a) <xsl:value-of select="format-number($statementvalue, '0,00 pto', 'es')"/>
                b) <xsl:value-of select="format-number(((floor(math:random() * 3100) div 100)), '0,00 pto', 'es')"/>
                c) <xsl:value-of select="format-number(((floor(math:random() * 3100) div 100)), '0,00 pto', 'es')"/>
                d) <xsl:value-of select="format-number(((floor(math:random() * 3100) div 100)), '0,00 pto', 'es')"/> 
        </xsl:if>
        
        <!-- BORDE DE PÁRRAFO : Margen : Izquierdo -->    
        <xsl:variable name="matchnumber" select="ceiling(math:random() * count($statementset))"/> 
        <xsl:variable name="targetvalue" select="normalize-space(replace($targetset[$matchnumber], '[\r\n]', ' '))"/>
        <xsl:variable name="statementvalue" select="number(replace(replace($statementsubset[$matchnumber]/value/statement[name = 'Izquierda' and default = 'Falso']/value, ' puntos', ''), ',', '.'))"/>
        <xsl:if test="$statementvalue">
            > Inicio / Párrafo / Bordes y sombreado [ALT + F + B] / Bordes / Opciones... / Izquierdo
            1. ¿Cuál la distancia establecida para el margen entre el borde izquierdo del párrafo «<xsl:value-of select="$targetvalue"/>» y el texto?
                a) <xsl:value-of select="format-number($statementvalue, '0,00 pto', 'es')"/>
                b) <xsl:value-of select="format-number(((floor(math:random() * 3100) div 100)), '0,00 pto', 'es')"/>
                c) <xsl:value-of select="format-number(((floor(math:random() * 3100) div 100)), '0,00 pto', 'es')"/>
                d) <xsl:value-of select="format-number(((floor(math:random() * 3100) div 100)), '0,00 pto', 'es')"/> 
        </xsl:if>



        <!-- SOMBREADO
            - Relleno
            - Trama
            - Color
        - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - --> 
        <xsl:variable name="divisionset" select="$wordactivity/block/division[statement[@class = 'shading-format' and default='Falso'] and target/value]" />
        
        <xsl:variable name="targetset" select="$divisionset/target[1]" />
        <xsl:variable name="statementset" select="$divisionset/statement[@class='shading-format' and default='Falso'][1]" />
            
        <!-- SOMBREADO : Relleno -->    
        <xsl:variable name="matchnumber" select="ceiling(math:random() * count($statementset))"/> 
        <xsl:variable name="targetvalue" select="normalize-space(replace($targetset[$matchnumber], '[\r\n]', ' '))"/>
        <xsl:variable name="statementvalue" select="$statementset[$matchnumber]/value/statement[name='Relleno' and default='Falso']/value"/>
        <xsl:if test="$statementvalue">
            > Inicio / Párrafo / Bordes y sombreado [ALT + F + B] / Sombreado / Relleno
            1. ¿Cuál es el color de relleno establecido para el párrafo «<xsl:value-of select="$targetvalue"/>» existente en el documento?
                a) <xsl:value-of select="$statementvalue"/>
                b) RGB(<xsl:value-of select="string-join((format-number(floor(math:random() * 255), '0'), format-number(floor(math:random() * 255), '0'), format-number(floor(math:random() * 255), '0')), ',')"/>)
                b) HSL(<xsl:value-of select="string-join((format-number(floor(math:random() * 255), '0'), format-number(floor(math:random() * 255), '0'), format-number(floor(math:random() * 255), '0')), ',')"/>)
                d) Todas las anteriores son correctas
        </xsl:if>

        <!-- SOMBREADO : Trama -->    
        <xsl:variable name="matchnumber" select="ceiling(math:random() * count($statementset))"/> 
        <xsl:variable name="targetvalue" select="normalize-space(replace($targetset[$matchnumber], '[\r\n]', ' '))"/>
        <xsl:variable name="statementvalue" select="$statementset[$matchnumber]/value/statement[name='Trama' and default='Falso']/value"/>
        <xsl:if test="$statementvalue">
            <xsl:variable name="order" select="floor(math:random() * 49)"/>
            > Inicio / Párrafo / Bordes y sombreado [ALT + F + B] / Sombreado / Estilo
            1. ¿Cuál es el estilo de trama establecido para el párrafo «<xsl:value-of select="$targetvalue"/>» existente en el documento?
                a) <xsl:value-of select="$statementvalue"/>
                b) <xsl:call-template name="texturelist">
                        <xsl:with-param name="invalid" select="$statementvalue"/>
                        <xsl:with-param name="order" select="$order"/>
                   </xsl:call-template>
                c) <xsl:call-template name="texturelist">
                        <xsl:with-param name="invalid" select="$statementvalue"/>
                        <xsl:with-param name="order" select="$order + 1"/>
                   </xsl:call-template>
                d) <xsl:call-template name="texturelist">
                        <xsl:with-param name="invalid" select="$statementvalue"/>
                        <xsl:with-param name="order" select="$order + 2"/>
                   </xsl:call-template> 
        </xsl:if>
            
        <!-- SOMBREADO : Color -->    
        <xsl:variable name="matchnumber" select="ceiling(math:random() * count($statementset))"/> 
        <xsl:variable name="targetvalue" select="normalize-space(replace($targetset[$matchnumber], '[\r\n]', ' '))"/>
        <xsl:variable name="statementvalue" select="$statementset[$matchnumber]/value/statement[name='Color' and default='Falso']/value"/>
        <xsl:if test="$statementvalue">
            > Inicio / Párrafo / Bordes y sombreado [ALT + F + B] / Sombreado / Color
            1. ¿Cuál es el color de trama establecido para el párrafo «<xsl:value-of select="$targetvalue"/>» existente en el documento?
                a) <xsl:value-of select="$statementvalue"/>
                b) RGB(<xsl:value-of select="string-join((format-number(floor(math:random() * 255), '0'), format-number(floor(math:random() * 255), '0'), format-number(floor(math:random() * 255), '0')), ',')"/>)
                b) HSL(<xsl:value-of select="string-join((format-number(floor(math:random() * 255), '0'), format-number(floor(math:random() * 255), '0'), format-number(floor(math:random() * 255), '0')), ',')"/>)
                d) Todas las anteriores son correctas
        </xsl:if>
       
       
        <!-- TABULACIONES
            - Posición
            - Alineción
            - Relleno
        - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - --> 
        <xsl:variable name="divisionset" select="$wordactivity/block/division[statement[@class = 'tabstops-format' and default='Falso'] and target/value]" />
        
        <xsl:variable name="targetset" select="$divisionset/target[1]" />
        <xsl:variable name="statementset" select="$divisionset/statement[@class='tabstops-format' and default='Falso'][1]" />
            
        <!-- TABULACIONES : Posición -->    
        <xsl:variable name="matchnumber" select="ceiling(math:random() * count($statementset))"/> 
        <xsl:variable name="order" select="ceiling(math:random() * count($statementset[$matchnumber]/value/statement[@class='tabstop-format']))"/> 
        <xsl:if test="$matchnumber > 0">
            <xsl:variable name="target" select="normalize-space(replace($targetset[$matchnumber]/value, '[\r\n]', ''))"/>
            <xsl:variable name="statementvalue" select="number(replace(replace($statementset[$matchnumber]/value/statement[@class='tabstop-format'][$order]/value/statement[name='Posición']/value, ' cm', ' '), ',', '.'))"/>
            > Inicio / Párrafo / Párrafo / Tabulaciones [ALT + F + T] / (Seleccionar la tabulación correspondiente) / Posición
            1. ¿Cuál es la posición de la <xsl:value-of select="$order"/>ª marca de tabulación del párrafo «<xsl:value-of select="$target"/>» existente en el documento?
                a) <xsl:value-of select="format-number($statementvalue, '0,00 cm', 'es')"/>
                b) <xsl:value-of select="format-number($statementvalue + ((floor(math:random() * 100) div 100)), '0,00 cm', 'es')"/>
                c) <xsl:value-of select="format-number($statementvalue - ((floor(math:random() * 100) div 100)), '0,00 cm', 'es')"/>
                d) <xsl:value-of select="format-number($statementvalue + ((floor(math:random() * 100) div 100)), '0,00 cm', 'es')"/> 
        </xsl:if>
            
        <!-- TABULACIONES : Alineación -->    
        <xsl:variable name="matchnumber" select="ceiling(math:random() * count($statementset))"/> 
        <xsl:variable name="order" select="ceiling(math:random() * count($statementset[$matchnumber]/value/statement[@class='tabstop-format']))"/> 
        <xsl:if test="$matchnumber > 0">
            <xsl:variable name="target" select="normalize-space(replace($targetset[$matchnumber]/value, '[\r\n]', ''))"/>
            <xsl:variable name="statementvalue" select="$statementset[$matchnumber]/value/statement[@class='tabstop-format'][$order]/value/statement[name='Alineación']/value"/>
            > Inicio / Párrafo / Párrafo / Tabulaciones [ALT + F + T] / (Seleccionar la tabulación correspondiente) / Alineación
            1. ¿Cuál es la alineación de la <xsl:value-of select="$order"/>ª marca de tabulación del párrafo «<xsl:value-of select="$target"/>» existente en el documento?
                a) <xsl:value-of select="$statementvalue"/>
                b) <xsl:choose>
                       <xsl:when test="$statementvalue = 'Centrada'">Barra</xsl:when>
                       <xsl:otherwise>Centrada</xsl:otherwise>
                   </xsl:choose>
                c) <xsl:choose>
                       <xsl:when test="$statementvalue = 'Derecha'">Barra</xsl:when>
                       <xsl:otherwise>Derecha</xsl:otherwise>
                   </xsl:choose>
                d) <xsl:choose>
                       <xsl:when test="$statementvalue = 'Decimal'">Barra</xsl:when>
                       <xsl:otherwise>Decimal</xsl:otherwise>
                   </xsl:choose> 
        </xsl:if>
            
        <!-- TABULACIONES : Relleno -->    
        <xsl:variable name="matchnumber" select="ceiling(math:random() * count($statementset))"/> 
        <xsl:variable name="order" select="ceiling(math:random() * count($statementset[$matchnumber]/value/statement[@class='tabstop-format']))"/> 
        <xsl:if test="$matchnumber > 0">
            <xsl:variable name="target" select="normalize-space(replace($targetset[$matchnumber]/value, '[\r\n]', ''))"/>
            <xsl:variable name="statementvalue" select="replace($statementset[$matchnumber]/value/statement[@class='tabstop-format'][$order]/value/statement[name='Relleno']/value, 'Espacios', 'Ninguno')"/>
            > Inicio / Párrafo / Párrafo / Tabulaciones [ALT + F + T] / (Seleccionar la tabulación correspondiente) / Relleno
            1. ¿Cuál es el relleno de la <xsl:value-of select="$order"/>ª marca de tabulación del párrafo «<xsl:value-of select="$target"/>» existente en el documento?
                a) <xsl:value-of select="$statementvalue"/>
                b) <xsl:choose>
                       <xsl:when test="$statementvalue = 'Puntos'">Ninguno</xsl:when>
                       <xsl:otherwise>Puntos</xsl:otherwise>
                   </xsl:choose>
                c) <xsl:choose>
                       <xsl:when test="$statementvalue = 'Guiones'">Ninguno</xsl:when>
                       <xsl:otherwise>Guiones</xsl:otherwise>
                   </xsl:choose>
                d) <xsl:choose>
                       <xsl:when test="$statementvalue = 'Caracteres de subrayado'">Ninguno</xsl:when>
                       <xsl:otherwise>Caracteres de subrayado</xsl:otherwise>
                   </xsl:choose> 
        </xsl:if>

         
         
        <!-- COLUMNAS
            - Número de columnas
            - Ancho
            - Espacio
            - Línea entre columnas, columnas de igual ancho
        - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - --> 
        <xsl:variable name="divisionset" select="$wordactivity/block/division[statement[name='Más columnas' and default='Falso']]" />
        
        <xsl:variable name="targetset" select="$divisionset/target[1]" />
        <xsl:variable name="statementset" select="$divisionset/statement[name='Más columnas' and default='Falso'][1]" />
        
        <!-- COLUMNAS : Número de columnas -->    
        <xsl:variable name="matchnumber" select="ceiling(math:random() * count($statementset))"/> 
        <xsl:if test="$matchnumber > 0">
            <xsl:variable name="statementvalue" select="number($statementset[$matchnumber]/value/statement[name='Número de columnas']/value)"/>
            <xsl:variable name="blockorder">
                <xsl:choose>
                    <xsl:when test="$matchnumber = 1">primer</xsl:when>
                    <xsl:when test="$matchnumber = 3">tercer</xsl:when>
                    <xsl:otherwise><xsl:value-of select="format-number($matchnumber, '0º', 'es')"/></xsl:otherwise>
                </xsl:choose>
            </xsl:variable>
            > Diseño de página / Más columnas [ALT + F + C] / Número de columnas
            1. ¿Cuántas columnas han sido establecidas para el <xsl:value-of select="$blockorder"/> bloque de columnas del documento?
                a) <xsl:value-of select="format-number($statementvalue, '0', 'es')"/>
                b) <xsl:value-of select="format-number($statementvalue + 1, '0', 'es')"/>
                c) <xsl:value-of select="format-number($statementvalue + 2, '0', 'es')"/>
                d) <xsl:value-of select="format-number($statementvalue + 3, '0', 'es')"/> 
        </xsl:if>
            
        <!-- COLUMNAS : Ancho -->    
        <xsl:variable name="matchnumber" select="ceiling(math:random() * count($statementset))"/> 
        <xsl:if test="$matchnumber > 0">
            <xsl:variable name="statementsubset" select="$statementset[$matchnumber]/value/statement[starts-with(name,'Ancho')]"/>
            <xsl:variable name="order" select="ceiling(math:random() * count($statementsubset))"/>
            <xsl:variable name="statementvalue" select="number(replace(replace($statementsubset[$order]/value, ',', '.'), ' cm', ''))"/>
            <xsl:variable name="blockorder">
                <xsl:choose>
                    <xsl:when test="$matchnumber = 1">primer</xsl:when>
                    <xsl:when test="$matchnumber = 3">tercer</xsl:when>
                    <xsl:otherwise><xsl:value-of select="format-number($matchnumber, '0º', 'es')"/></xsl:otherwise>
                </xsl:choose>
            </xsl:variable>
            > Diseño de página / Más columnas [ALT + F + C] / Ancho (de la columna correspondiente, salvo que esté marcado «Columnas de igual ancho» en cuyo caso el ancho es igual para todas)
            1. ¿Cuál es el ancho establecido para la <xsl:value-of select="$order"/>ª columna del <xsl:value-of select="$blockorder"/> bloque de columnas del documento?
                a) <xsl:value-of select="format-number($statementvalue, '0,00 cm', 'es')"/>
                b) <xsl:value-of select="format-number($statementvalue + ((floor(math:random() * 100) div 100)), '0,00 cm', 'es')"/>
                c) <xsl:value-of select="format-number($statementvalue - ((floor(math:random() * 100) div 100)), '0,00 cm', 'es')"/>
                d) <xsl:value-of select="format-number($statementvalue + ((floor(math:random() * 100) div 100)), '0,00 cm', 'es')"/> 
        </xsl:if>

        <!-- COLUMNAS : Espaciado -->    
        <xsl:variable name="matchnumber" select="ceiling(math:random() * count($statementset))"/> 
        <xsl:if test="$matchnumber > 0">
            <xsl:variable name="statementsubset" select="$statementset[$matchnumber]/value/statement[starts-with(name,'Espaciado')]"/>
            <xsl:variable name="order" select="ceiling(math:random() * count($statementsubset))"/>
            <xsl:variable name="statementvalue" select="number(replace(replace($statementsubset[$order]/value, ',', '.'), ' cm', ''))"/>
            <xsl:variable name="blockorder">
                <xsl:choose>
                    <xsl:when test="$matchnumber = 1">primer</xsl:when>
                    <xsl:when test="$matchnumber = 3">tercer</xsl:when>
                    <xsl:otherwise><xsl:value-of select="format-number($matchnumber, '0º', 'es')"/></xsl:otherwise>
                </xsl:choose>
            </xsl:variable>
            <xsl:variable name="spaceorder">
                <xsl:choose>
                    <xsl:when test="$matchnumber = 1">primer</xsl:when>
                    <xsl:when test="$matchnumber = 3">tercer</xsl:when>
                    <xsl:otherwise><xsl:value-of select="format-number($order, '0º', 'es')"/></xsl:otherwise>
                </xsl:choose>
            </xsl:variable>
            > Diseño de página / Más columnas [ALT + F + C] / Espaciado (el que corresponda, salvo que esté marcado «Columnas de igual ancho» en cuyo caso el espacido es común para todas)
            1. ¿Cuál es el valor establecido para el <xsl:value-of select="$spaceorder"/> espaciado entre columnas del <xsl:value-of select="$blockorder"/> bloque de columnas del documento?
                a) <xsl:value-of select="format-number($statementvalue, '0,00 cm', 'es')"/>
                b) <xsl:value-of select="format-number($statementvalue + ((floor(math:random() * 100) div 100)), '0,00 cm', 'es')"/>
                c) <xsl:value-of select="format-number($statementvalue - ((floor(math:random() * 100) div 100)), '0,00 cm', 'es')"/>
                d) <xsl:value-of select="format-number($statementvalue + ((floor(math:random() * 100) div 100)), '0,00 cm', 'es')"/> 
        </xsl:if>
            
        <!-- COLUMNAS : ... -->    
        <xsl:variable name="matchnumber" select="ceiling(math:random() * count($statementset))"/> 
        <xsl:if test="$matchnumber > 0">
            <xsl:variable name="blockorder">
                <xsl:choose>
                    <xsl:when test="$matchnumber = 1">primer</xsl:when>
                    <xsl:when test="$matchnumber = 3">tercer</xsl:when>
                    <xsl:otherwise><xsl:value-of select="format-number($matchnumber, '0º', 'es')"/></xsl:otherwise>
                </xsl:choose>
            </xsl:variable>
            <xsl:variable name="option" select="math:random()"/>
            <xsl:variable name="answera">
                <xsl:choose>
                    <xsl:when test="$option >= 0.5">
                        <xsl:variable name="value" select="$statementset[$matchnumber]/value/statement[name='Columnas de igual ancho']/value"/>
                        <xsl:choose>
                            <xsl:when test="$value = 'Sí'">Las columnas no son de igual ancho</xsl:when>
                            <xsl:otherwise>Las columnas son de igual ancho</xsl:otherwise>
                        </xsl:choose>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:variable name="value" select="$statementset[$matchnumber]/value/statement[name='Línea entre columnas']/value"/>
                        <xsl:choose>
                            <xsl:when test="$value = 'Sí'">No hay línea entre las columnas</xsl:when>
                            <xsl:otherwise>Hay una línea entre las columnas</xsl:otherwise>
                        </xsl:choose>
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:variable>
            <xsl:variable name="answerb">
                <xsl:choose>
                    <xsl:when test="$option >= 0.5">
                        <xsl:variable name="value" select="$statementset[$matchnumber]/value/statement[name='Línea entre columnas']/value"/>
                        <xsl:choose>
                            <xsl:when test="$value = 'No'">No hay línea entre las columnas</xsl:when>
                            <xsl:otherwise>Hay una línea entre las columnas</xsl:otherwise>
                        </xsl:choose>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:variable name="value" select="$statementset[$matchnumber]/value/statement[name='Columnas de igual ancho']/value"/>
                        <xsl:choose>
                            <xsl:when test="$value = 'No'">Las columnas no son de igual ancho</xsl:when>
                            <xsl:otherwise>Las columnas son de igual ancho</xsl:otherwise>
                        </xsl:choose>
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:variable>
            > Diseño de página / Más columnas [ALT + F + C] / ...
            1. ¿Cuál de las siguientes afirmaciones sobre el <xsl:value-of select="$blockorder"/> bloque de columnas del documento NO es cierta?
                a) <xsl:value-of select="$answera"/>
                b) <xsl:value-of select="$answerb"/>
                c) La suma de los anchos de columna y los espacios que hay entre ellas da como resultado la distancia entre los márgenes izquierdo y derecho establecidos para la sección
                d) El posible acceder a la configuración de columnas empleando la ficha Diseño de página de la cinta de opciones
        </xsl:if>  
        
            
            
        <!-- NÚMEROS DE LÍNEA
            - Iniciar en
            - Desde el texto
            - Intervalo
            - Numeración
        - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - --> 
        <xsl:variable name="statementset" select="$wordactivity/block/division/statement[@class='line-numbering' and default='Falso']" />
        
        <!-- NÚMEROS DE LÍNEA : Iniciar en -->    
        <xsl:if test="$statementset">
            <xsl:variable name="statementvalue" select="number($statementset[1]/value/statement[name='Iniciar en']/value)"/>
            > Diseño de página / Configurar página [ALT + C + C] / Diseño / Números de línea / Iniciar en
            1. ¿Cuál es el valor establecido para el inicio de la numeración de líneas del documento?
                a) <xsl:value-of select="$statementvalue"/>
                b) <xsl:value-of select="$statementvalue + 1"/>
                c) <xsl:value-of select="$statementvalue - 1"/>
                d) <xsl:value-of select="$statementvalue + ceiling(math:random())"/> 
        </xsl:if>

        <!-- NÚMEROS DE LÍNEA : Desde el texto -->   
        <xsl:if test="$statementset">
            <xsl:variable name="statementvalue" select="number(replace(replace($statementset[1]/value/statement[name='Desde el texto']/value, ',', '.'), ' cm', ''))"/>
            > Diseño de página / Configurar página [ALT + C + C] / Diseño / Números de línea / Iniciar en
            1. ¿Cuál es la distancia establecida entre la numeración de líneas y el texto del documento?
                a) <xsl:value-of select="format-number($statementvalue, '0,00 cm', 'es')"/>
                b) <xsl:value-of select="format-number($statementvalue + ((floor(math:random() * 100) div 100)), '0,00 cm', 'es')"/>
                c) <xsl:value-of select="format-number($statementvalue - ((floor(math:random() * 100) div 100)), '0,00 cm', 'es')"/>
                d) <xsl:value-of select="format-number($statementvalue + ((floor(math:random() * 100) div 100)), '0,00 cm', 'es')"/> 
        </xsl:if>        
            
        <!-- NÚMEROS DE LÍNEA : Intervalo -->    
        <xsl:if test="$statementset">
            <xsl:variable name="statementvalue" select="number($statementset[1]/value/statement[name='Intervalo']/value)"/>
            > Diseño de página / Configurar página [ALT + C + C] / Diseño / Números de línea / Intervalo
            1. ¿Cuál es el intervalo establecido para la numeración de líneas del documento?
                a) <xsl:value-of select="$statementvalue"/>
                b) <xsl:value-of select="$statementvalue + 1"/>
                c) <xsl:value-of select="$statementvalue - 1"/>
                d) <xsl:value-of select="$statementvalue + ceiling(math:random())"/> 
        </xsl:if>

        <!-- NÚMEROS DE LÍNEA : Numeración -->   
        <xsl:if test="$statementset">
            <xsl:variable name="statementvalue" select="$statementset[1]/value/statement[name='Numeración']/value"/>
            > Diseño de página / Configurar página [ALT + C + C] / Diseño / Números de línea / Numeración
            1. ¿Cuál es el valor establecido para la opción «Numeración» correspondiente a la numeración de líneas del documento?
                a) <xsl:value-of select="$statementvalue"/>
                b) <xsl:choose>
                       <xsl:when test="$statementvalue = 'Reiniciar en cada página'">Reiniciar en cada documento</xsl:when>
                       <xsl:otherwise>Reiniciar en cada página</xsl:otherwise>
                   </xsl:choose>
                c) <xsl:choose>
                       <xsl:when test="$statementvalue = 'Reiniciar en cada sección'">Reiniciar en cada documento</xsl:when>
                       <xsl:otherwise>Reiniciar en cada sección</xsl:otherwise>
                   </xsl:choose>
                d) <xsl:choose>
                       <xsl:when test="$statementvalue = 'Continua'">Reiniciar en cada documento</xsl:when>
                       <xsl:otherwise>Continua</xsl:otherwise>
                   </xsl:choose> 
        </xsl:if>


       
        <!-- MARCA DE AGUA
             - Escala
             - Idioma
             - Texto
             - Fuente
             - Tamaño
             - Color
             - Decolorar, Semitransparente, Distribución
        - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - --> 
        
        <xsl:variable name="statementset" select="$wordactivity/block/division/statement[@class = 'watermark-format']" />
         
        <!-- MARCA DE AGUA : : Escala -->         
        <xsl:variable name="statementvalue" select="number(replace(replace($statementset[1]/value/statement[name='Escala' and default='Falso']/value, 'Automático', '0'), '%', ''))"/>
        <xsl:if test="$statementvalue">
            > Diseño de página / Marcas de agua personalizadas / Escala
            1. ¿Cuál es el valor de la escala establecida para la marca de agua empleada en el documento?
                a) <xsl:choose>
                    <xsl:when test="$statementvalue = 0">Automático</xsl:when>
                    <xsl:otherwise><xsl:value-of select="format-number($statementvalue, '0,00', 'es')"/>%</xsl:otherwise>
                </xsl:choose>
                b) <xsl:value-of select="format-number($statementvalue + 5, '#.##0,00', 'es')"/>%
                c) <xsl:value-of select="format-number($statementvalue + 10, '#.##0,00', 'es')"/>%
                d) <xsl:value-of select="format-number($statementvalue - 5, '#.##0,00', 'es')"/>%
        </xsl:if>
              
        <!-- MARCA DE AGUA : Idioma -->          
        <xsl:variable name="statementvalue" select="$statementset[1]/value/statement[name='Idioma' and default='Falso']/value"/>
        <xsl:if test="$statementvalue">
            > Diseño de página / Marcas de agua personalizadas / Idioma
            1. ¿Cuál es el idioma establecido para la para la marca de agua empleada en el documento?
                a) <xsl:value-of select="$statementvalue"/>%
                b) <xsl:choose>
                       <xsl:when test="$statementvalue = 'Gallego'">Bable</xsl:when>
                       <xsl:otherwise>Gallego</xsl:otherwise>
                   </xsl:choose>
                c) <xsl:choose>
                       <xsl:when test="$statementvalue = 'Catalán'">Bable</xsl:when>
                       <xsl:otherwise>Catalán</xsl:otherwise>
                   </xsl:choose>
                d) <xsl:choose>
                       <xsl:when test="$statementvalue = 'Euskera'">Bable</xsl:when>
                       <xsl:otherwise>Euskera</xsl:otherwise>
                   </xsl:choose> 
        </xsl:if>
         
        <!-- MARCA DE AGUA : Texto -->          
        <xsl:variable name="statementvalue" select="$statementset[1]/value/statement[name='Texto' and default='Falso']/value"/>
        <xsl:if test="$statementvalue">
            > Diseño de página / Marcas de agua personalizadas / Texto
            1. ¿Cuál es el texto establecido para la para la marca de agua empleada en el documento?
                a) <xsl:value-of select="$statementvalue"/>
                b) <xsl:choose>
                       <xsl:when test="$statementvalue = 'Borrador'">Urgente</xsl:when>
                       <xsl:otherwise>Borrador</xsl:otherwise>
                   </xsl:choose>
                c) <xsl:choose>
                       <xsl:when test="$statementvalue = 'Copia'">Urgente</xsl:when>
                       <xsl:otherwise>Copia</xsl:otherwise>
                   </xsl:choose>
                d) <xsl:choose>
                       <xsl:when test="$statementvalue = 'Original'">Urgente</xsl:when>
                       <xsl:otherwise>Original</xsl:otherwise>
                   </xsl:choose> 
        </xsl:if>
            
        <!-- MARCA DE AGUA : Fuente  -->    
        <xsl:variable name="statementvalue" select="$statementset[1]/value/statement[name='Fuente' and default='Falso']/value"/>   
        <xsl:if test="$statementvalue">
            > Diseño de página / Marcas de agua personalizadas / Fuente
            1. ¿Cuál es el tipo de letra establecido para la para la marca de agua empleada en el documento?  
                a) <xsl:value-of select="$statementvalue"/>
                b) <xsl:call-template name="fontfamilylist">
                       <xsl:with-param name="invalid" select="substring-before($statementvalue, ' (')"/>
                        <xsl:with-param name="order" select="$order"/>
                   </xsl:call-template>
                c) <xsl:call-template name="fontfamilylist">
                       <xsl:with-param name="invalid" select="substring-before($statementvalue, ' (')"/>
                        <xsl:with-param name="order" select="$order + 1"/>
                   </xsl:call-template>
                d) <xsl:call-template name="fontfamilylist">
                       <xsl:with-param name="invalid" select="substring-before($statementvalue, ' (')"/>
                        <xsl:with-param name="order" select="$order + 2"/>
                   </xsl:call-template>  
        </xsl:if>
            
        <!-- MARCA DE AGUA : Tamaño --> 
        <xsl:variable name="statementvalue" select="number(replace(replace(replace($statementset[1]/value/statement[name='Tamaño' and default='Falso']/value, 'Automático', '0'), ',', '.'), 'puntos', ''))"/>
        <xsl:if test="$statementvalue or $statementvalue = 0">
            > Diseño de página / Marcas de agua personalizadas / Tamaño
            1. ¿Cuál es el tamaño de letra establecido para la para la marca de agua empleada en el documento?
                a) <xsl:choose>
                    <xsl:when test="$statementvalue = 0">Automático</xsl:when>
                    <xsl:otherwise><xsl:value-of select="format-number($statementvalue, '0,00', 'es')"/> puntos</xsl:otherwise>
                </xsl:choose>
                b) <xsl:value-of select="format-number(fn:max(($statementvalue, 6)) + 0.5, '#.##0,00', 'es')"/> puntos
                c) <xsl:value-of select="format-number(fn:max(($statementvalue, 6)), '#.##0,00', 'es')"/> píxeles
                d) <xsl:value-of select="format-number(fn:max(($statementvalue, 6)) - 0.5, '#.##0,00', 'es')"/> píxeles
        </xsl:if>
            
        <!-- MARCA DE AGUA : Color -->         
        <xsl:variable name="statementvalue" select="$statementset[1]/value/statement[name='Color' and default='Falso']/value"/>
        <xsl:if test="$statementvalue">
            > Diseño de página / Marcas de agua personalizadas / Color
            1. ¿Cuál es el color de letra establecido para la para la marca de agua empleada en el documento?
                a) <xsl:value-of select="$statementvalue"/>
                b) RGB(<xsl:value-of select="string-join((format-number(floor(math:random() * 255), '0'), format-number(floor(math:random() * 255), '0'), format-number(floor(math:random() * 255), '0')), ',')"/>)
                b) HSL(<xsl:value-of select="string-join((format-number(floor(math:random() * 255), '0'), format-number(floor(math:random() * 255), '0'), format-number(floor(math:random() * 255), '0')), ',')"/>)
                d) Todas las anteriores son correctas
        </xsl:if>
            
        <xsl:if test="$statementset">            
            <!-- MARCA DE AGUA: ... -->
            <xsl:variable name="wmtype">
                <xsl:choose>
                <xsl:when test="$statementset[1]/value/statement[name='Seleccionar imagen' and default='Falso']/value">marca de agua de imagen</xsl:when>
                <xsl:otherwise>marca de agua de texto</xsl:otherwise>
                </xsl:choose>        
            </xsl:variable><!--Decolorar, Semitransparente, Distribución-->
            <xsl:variable name="wmdiscolour">
                <xsl:choose>
                    <xsl:when test="$statementset[1]/value/statement[name='Decolorar' and default='Falso']/value = 'Sí'">La opción «Decolorar» NO ha sido establecida para la marca de agua</xsl:when>
                    <xsl:otherwise>La opción «Decolorar» ha sido establecida para la marca de agua</xsl:otherwise>
                </xsl:choose>
            </xsl:variable>
            <xsl:variable name="wmsemitransparent">
                <xsl:choose>
                    <xsl:when test="$statementset[1]/value/statement[name='Semitransparente' and default='Falso']/value = 'Sí'">La opción «Semitransparente» NO ha sido establecida para la marca de agua</xsl:when>
                    <xsl:otherwise>La opción «Semitransparente» ha sido establecida para la marca de agua</xsl:otherwise>
                </xsl:choose>
            </xsl:variable>
            <xsl:variable name="wmdistribution">
                <xsl:choose>
                    <xsl:when test="$statementset[1]/value/statement[name='Distribución' and default='Falso']/value = 'Horizontal'">El valor para la «Distribución» de la marca de agua ha sido establecido a «Vertical»</xsl:when>
                    <xsl:otherwise>El valor para la «Distribución» de la marca de agua ha sido establecido a «Horizontal»</xsl:otherwise>
                </xsl:choose>
            </xsl:variable>
            > Diseño de página / Marcas de agua personalizadas / ...
            1.- ¿Cuál de las siguientes afirmaciones sobre la marcade agua establecida para el documento no es cierta?
                a) Se ha aplicado una <xsl:value-of select="$wmtype"/> al documento
                b) <xsl:value-of select="$wmdiscolour"/>
                b) <xsl:value-of select="$wmsemitransparent"/>
                b) <xsl:value-of select="$wmdistribution"/>
     </xsl:if>
    
     <!--
         
     - [x] Estilo de número
     - [ ] Incluir número de nivel desde
     - [x] Formato de número
     - [x] Fuente del símbolo
     - [x] Alineación de los números
     - [x] Alineación
     - [x] Sangría de texto en
     - [x] Número seguido de
     - [x] Agregar tabulación en
     - [x] Iniciar en
     - [ ] Reiniciar la lista después de
     - [x] Vincular nivel al estilo
     -->
    
        <xsl:variable name="divisionset" select="$wordactivity/block[name='Lista ordenada']/division[statement[@class='level-format']][1]"/>
        
        <xsl:variable name="matchnumber" select="ceiling(math:random() * count($divisionset))"/>
        <xsl:variable name="levelset" select="$divisionset[$matchnumber]/statement[@class='level-format' and default='Falso']"/>
        <xsl:variable name="statementsubset" select="$levelset[ceiling(math:random() * count($levelset))]"/>
        <xsl:variable name="statementvalue" select="$statementsubset/value/statement[name='Estilo de número']/value"/>
        <xsl:variable name="order" select="ceiling(math:random()* 12)"/>
        <xsl:if test="$statementvalue">
            1. ¿Cuál es el estilo de número aplicado al nivel <xsl:value-of select="$statementsubset/value/statement[name='Nivel']/value"/> de la <xsl:value-of select="$matchnumber"/>ª lista multinivel existente en el documento?
                a) <xsl:value-of select="$statementvalue"/>
                b) <xsl:call-template name="levellist">
                       <xsl:with-param name="order" select="$order"></xsl:with-param>
                       <xsl:with-param name="invalid" select="$statementvalue"></xsl:with-param>
                   </xsl:call-template>
                c) <xsl:call-template name="levellist">
                       <xsl:with-param name="order" select="$order+1"></xsl:with-param>
                       <xsl:with-param name="invalid" select="$statementvalue"></xsl:with-param>
                   </xsl:call-template>
                d) <xsl:call-template name="levellist">
                       <xsl:with-param name="order" select="$order+2"></xsl:with-param>
                       <xsl:with-param name="invalid" select="$statementvalue"></xsl:with-param>
                   </xsl:call-template>
        </xsl:if>
            
        <xsl:variable name="divisionset" select="$wordactivity/block[name='Lista ordenada']/division[statement[@class='level-format']][1]"/>
        
        <xsl:variable name="matchnumber" select="ceiling(math:random() * count($divisionset))"/>
        <xsl:variable name="levelset" select="$divisionset[$matchnumber]/statement[@class='level-format' and default='Falso']"/>
        <xsl:variable name="statementsubset" select="$levelset[ceiling(math:random() * count($levelset))]"/>
        <xsl:variable name="statementvalue" select="$statementsubset/value/statement[name='Formato de número']/value"/>
        <xsl:variable name="numstyle" select="$statementsubset/value/statement[name='Estilo de número']/value"/>
        <xsl:variable name="order" select="ceiling(math:random()* 12)"/>
        <xsl:if test="$statementvalue and $numstyle <> 'Nueva viñeta' and $numstyle='Nueva imagen'>
            1. ¿Cuál es el formato de número aplicado al nivel <xsl:value-of select="$statementsubset/value/statement[name='Nivel']/value"/> de la <xsl:value-of select="$matchnumber"/>ª lista multinivel existente en el documento?
                a) <xsl:value-of select="$statementvalue"/>
                b) <xsl:choose>
                       <xsl:when test="fn:string-length($statementvalue) > 1"><xsl:value-of select="substring($statementvalue, 1, fn:string-length($statementvalue) - 1)"/></xsl:when>
                       <xsl:otherwise>~ 1 ~</xsl:otherwise>
                   </xsl:choose>
                b) <xsl:choose>
                       <xsl:when test="fn:string-length($statementvalue) > 1"><xsl:value-of select="substring($statementvalue, 2, fn:string-length($statementvalue) - 1)"/></xsl:when>
                       <xsl:otherwise>→ 1 ←</xsl:otherwise>
                   </xsl:choose>
                c) {a}
            
     1. ¿Cuál es la fuente del símbolo para la viñeta establecida para el nivel <xsl:value-of select="$statementsubset/value/statement[name='Nivel']/value"/> de la <xsl:value-of select="$matchnumber"/>ª lista multinivel existente en el documento?
     1. ¿Cuál es la alineación de número establecida para el nivel <xsl:value-of select="$statementsubset/value/statement[name='Nivel']/value"/> de la <xsl:value-of select="$matchnumber"/>ª lista multinivel existente en el documento?
     1. ¿Cuál es la posición establecida para el número del nivel <xsl:value-of select="$statementsubset/value/statement[name='Nivel']/value"/> de la <xsl:value-of select="$matchnumber"/>ª lista multinivel existente en el documento?
     1. ¿Cuál es la sangría de texto establecida para el nivel <xsl:value-of select="$statementsubset/value/statement[name='Nivel']/value"/> de la <xsl:value-of select="$matchnumber"/>ª lista multinivel existente en el documento?
     1. ¿Cuál es posición de la tabulación establecida para el nivel <xsl:value-of select="$statementsubset/value/statement[name='Nivel']/value"/> de la <xsl:value-of select="$matchnumber"/>ª lista multinivel existente en el documento?
     1. ¿Qué hay entre el número del nivel  <xsl:value-of select="$statementsubset/value/statement[name='Nivel']/value"/> de la <xsl:value-of select="$matchnumber"/>ª lista multinivel existente en el documento y el texto que le sigue?
     1. ¿Cuál es valor inicial establecido para la numeración del nivel <xsl:value-of select="$statementsubset/value/statement[name='Nivel']/value"/> de la <xsl:value-of select="$matchnumber"/>ª lista multinivel existente en el documento?
     1. ¿Cuál es el estilo vinculado al nivel <xsl:value-of select="$statementsubset/value/statement[name='Nivel']/value"/> de la <xsl:value-of select="$matchnumber"/>ª lista multinivel existente en el documento?

            
    
</pre>

    </xsl:template>
    
    
    
    
    
    
    <xsl:template name="themelist">
        <xsl:param name="order"/>
        <xsl:param name="invalid"/>
        <xsl:choose>
            <xsl:when test="$order = floor(0) and $invalid != 'Adyacencia'">Adyacencia</xsl:when>
            <xsl:when test="$order = floor(1) and $invalid != 'Alta costura'">Alta costura</xsl:when>
            <xsl:when test="$order = floor(2) and $invalid != 'Angulos'">Angulos</xsl:when>
            <xsl:when test="$order = floor(3) and $invalid != 'Aspecto'">Aspecto</xsl:when>
            <xsl:when test="$order = floor(4) and $invalid != 'Austin'">Austin</xsl:when>
            <xsl:when test="$order = floor(5) and $invalid != 'Boticario'">Boticario</xsl:when>
            <xsl:when test="$order = floor(6) and $invalid != 'Brío'">Brío</xsl:when>
            <xsl:when test="$order = floor(7) and $invalid != 'Cartone'">Cartone</xsl:when>
            <xsl:when test="$order = floor(8) and $invalid != 'Chincheta'">Chincheta</xsl:when>
            <xsl:when test="$order = floor(9) and $invalid != 'Civil'">Civil</xsl:when>
            <xsl:when test="$order = floor(10) and $invalid != 'Claridad'">Claridad</xsl:when>
            <xsl:when test="$order = floor(11) and $invalid != 'Compuesto'">Compuesto</xsl:when>
            <xsl:when test="$order = floor(12) and $invalid != 'Concurrencia'">Concurrencia</xsl:when>
            <xsl:when test="$order = floor(13) and $invalid != 'Cuaderno'">Cuaderno</xsl:when>
            <xsl:when test="$order = floor(14) and $invalid != 'Cuadricula'">Cuadricula</xsl:when>
            <xsl:when test="$order = floor(15) and $invalid != 'Decatur'">Decatur</xsl:when>
            <xsl:when test="$order = floor(16) and $invalid != 'Ejecutivo'">Ejecutivo</xsl:when>
            <xsl:when test="$order = floor(17) and $invalid != 'Elemental'">Elemental</xsl:when>
            <xsl:when test="$order = floor(18) and $invalid != 'Equidad'">Equidad</xsl:when>
            <xsl:when test="$order = floor(19) and $invalid != 'Esencial'">Esencial</xsl:when>
            <xsl:when test="$order = floor(20) and $invalid != 'Etiqueta'">Etiqueta</xsl:when>
            <xsl:when test="$order = floor(21) and $invalid != 'Feria comercial'">Feria comercial</xsl:when>
            <xsl:when test="$order = floor(22) and $invalid != 'Flujo'">Flujo</xsl:when>
            <xsl:when test="$order = floor(23) and $invalid != 'Forma de onda'">Forma de onda</xsl:when>
            <xsl:when test="$order = floor(24) and $invalid != 'Fundición'">Fundición</xsl:when>
            <xsl:when test="$order = floor(25) and $invalid != 'Horizonte'">Horizonte</xsl:when>
            <xsl:when test="$order = floor(26) and $invalid != 'Intermedio'">Intermedio</xsl:when>
            <xsl:when test="$order = floor(27) and $invalid != 'Invierno'">Invierno</xsl:when>
            <xsl:when test="$order = floor(28) and $invalid != 'Kilter'">Kilter</xsl:when>
            <xsl:when test="$order = floor(29) and $invalid != 'Macro'">Macro</xsl:when>
            <xsl:when test="$order = floor(30) and $invalid != 'Metro'">Metro</xsl:when>
            <xsl:when test="$order = floor(31) and $invalid != 'Mirador'">Mirador</xsl:when>
            <xsl:when test="$order = floor(32) and $invalid != 'Módulo'">Módulo</xsl:when>
            <xsl:when test="$order = floor(33) and $invalid != 'Mylar'">Mylar</xsl:when>
            <xsl:when test="$order = floor(34) and $invalid != 'Office'">Office</xsl:when>
            <xsl:when test="$order = floor(35) and $invalid != 'Opulento'">Opulento</xsl:when>
            <xsl:when test="$order = floor(36) and $invalid != 'Origen'">Origen</xsl:when>
            <xsl:when test="$order = floor(37) and $invalid != 'Otoño'">Otoño</xsl:when>
            <xsl:when test="$order = floor(38) and $invalid != 'Paja'">Paja</xsl:when>
            <xsl:when test="$order = floor(39) and $invalid != 'Papel'">Papel</xsl:when>
            <xsl:when test="$order = floor(40) and $invalid != 'Papel periódico'">Papel periódico</xsl:when>
            <xsl:when test="$order = floor(41) and $invalid != 'Perspectiva'">Perspectiva</xsl:when>
            <xsl:when test="$order = floor(42) and $invalid != 'Primavera'">Primavera</xsl:when>
            <xsl:when test="$order = floor(43) and $invalid != 'SOHO'">SOHO</xsl:when>
            <xsl:when test="$order = floor(44) and $invalid != 'Solsticio'">Solsticio</xsl:when>
            <xsl:when test="$order = floor(45) and $invalid != 'Técnico'">Técnico</xsl:when>
            <xsl:when test="$order = floor(46) and $invalid != 'Thermal'">Thermal</xsl:when>
            <xsl:when test="$order = floor(47) and $invalid != 'Transmisión de listas'">Transmisión de listas</xsl:when>
            <xsl:when test="$order = floor(48) and $invalid != 'Urban Pop'">Urban Pop</xsl:when>
            <xsl:when test="$order = floor(49) and $invalid != 'Urbano'">Urbano</xsl:when>
            <xsl:when test="$order = floor(50) and $invalid != 'Verano'">Verano</xsl:when>
            <xsl:when test="$order = floor(51) and $invalid != 'Vértice'">Vértice</xsl:when>
            <xsl:when test="$order = floor(52) and $invalid != 'Viajes'">Viajes</xsl:when>
            <xsl:otherwise>El tiempo</xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template name="papersizelist">
        <xsl:param name="order"/>
        <xsl:param name="invalid"/>
        <xsl:choose>
            <xsl:when test="$order = floor(0) and $invalid != 'A0'">A0</xsl:when>
            <xsl:when test="$order = floor(1) and $invalid != 'A1'">A1</xsl:when>
            <xsl:when test="$order = floor(2) and $invalid != 'A2'">A2</xsl:when>
            <xsl:when test="$order = floor(3) and $invalid != 'A3'">A3</xsl:when>
            <xsl:when test="$order = floor(4) and $invalid != 'A4'">A4</xsl:when>
            <xsl:when test="$order = floor(5) and $invalid != 'A5'">A5</xsl:when>
            <xsl:when test="$order = floor(6) and $invalid != 'A6'">A6</xsl:when>
            <xsl:when test="$order = floor(7) and $invalid != 'A7'">A7</xsl:when>
            <xsl:when test="$order = floor(8) and $invalid != 'A8'">A8</xsl:when>
            <xsl:when test="$order = floor(9) and $invalid != 'B0'">B0</xsl:when>
            <xsl:when test="$order = floor(10) and $invalid != 'B1'">B1</xsl:when>
            <xsl:when test="$order = floor(11) and $invalid != 'B2'">B2</xsl:when>
            <xsl:when test="$order = floor(12) and $invalid != 'B3'">B3</xsl:when>
            <xsl:when test="$order = floor(13) and $invalid != 'B4'">B4</xsl:when>
            <xsl:when test="$order = floor(14) and $invalid != 'B5'">B5</xsl:when>
            <xsl:when test="$order = floor(15) and $invalid != 'B6'">B6</xsl:when>
            <xsl:when test="$order = floor(16) and $invalid != 'B7'">B7</xsl:when>
            <xsl:when test="$order = floor(17) and $invalid != 'B8'">B8</xsl:when>
            <xsl:when test="$order = floor(18) and $invalid != 'C0'">C0</xsl:when>
            <xsl:when test="$order = floor(19) and $invalid != 'C1'">C1</xsl:when>
            <xsl:when test="$order = floor(20) and $invalid != 'C2'">C2</xsl:when>
            <xsl:when test="$order = floor(21) and $invalid != 'C3'">C3</xsl:when>
            <xsl:when test="$order = floor(22) and $invalid != 'C4'">C4</xsl:when>
            <xsl:when test="$order = floor(23) and $invalid != 'C5'">C5</xsl:when>
            <xsl:when test="$order = floor(24) and $invalid != 'C6'">C6</xsl:when>
            <xsl:when test="$order = floor(25) and $invalid != 'C7'">C7</xsl:when>
            <xsl:when test="$order = floor(26) and $invalid != 'C8'">C8</xsl:when>
            <xsl:when test="$order = floor(27) and $invalid != 'Sábana'">Sábana</xsl:when>
            <xsl:when test="$order = floor(28) and $invalid != 'Berliner'">Berliner</xsl:when>
            <xsl:when test="$order = floor(29) and $invalid != 'Tabloide'">Tabloide</xsl:when>
            <xsl:when test="$order = floor(30) and $invalid != 'Compacto'">Compacto</xsl:when>
            <xsl:when test="$order = floor(31) and $invalid != 'Arch A'">Arch A</xsl:when>
            <xsl:when test="$order = floor(32) and $invalid != 'Arch B'">Arch B</xsl:when>
            <xsl:when test="$order = floor(33) and $invalid != 'Arch C'">Arch C</xsl:when>
            <xsl:when test="$order = floor(34) and $invalid != 'Arch D'">Arch D</xsl:when>
            <xsl:when test="$order = floor(35) and $invalid != 'Arch E'">Arch E</xsl:when>
            <xsl:when test="$order = floor(36) and $invalid != 'Arch E1'">Arch E1</xsl:when>
            <xsl:when test="$order = floor(37) and $invalid != 'Estamento'">Estamento</xsl:when>
            <xsl:when test="$order = floor(38) and $invalid != 'Carta'">Carta</xsl:when>
            <xsl:when test="$order = floor(39) and $invalid != 'Oficio'">Oficio</xsl:when>
            <xsl:when test="$order = floor(40) and $invalid != 'Junior'">Junior</xsl:when>
            <xsl:when test="$order = floor(41) and $invalid != 'Ledger'">Ledger</xsl:when>
            <xsl:when test="$order = floor(42) and $invalid != 'RA0'">RA0</xsl:when>
            <xsl:when test="$order = floor(43) and $invalid != 'RA1'">RA1</xsl:when>
            <xsl:when test="$order = floor(44) and $invalid != 'RA2'">RA2</xsl:when>
            <xsl:when test="$order = floor(45) and $invalid != 'RA3'">RA3</xsl:when>
            <xsl:when test="$order = floor(46) and $invalid != 'RA4'">RA4</xsl:when>
            <xsl:when test="$order = floor(47) and $invalid != 'SRA0'">SRA0</xsl:when>
            <xsl:when test="$order = floor(48) and $invalid != 'SRA1'">SRA1</xsl:when>
            <xsl:when test="$order = floor(49) and $invalid != 'SRA2'">SRA2</xsl:when>
            <xsl:when test="$order = floor(50) and $invalid != 'SRA3'">SRA3</xsl:when>
            <xsl:when test="$order = floor(51) and $invalid != 'SRA4'">SRA4</xsl:when>
            <xsl:otherwise>Higiénico</xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template name="borderstylelist">
        <xsl:param name="order"/>
        <xsl:param name="invalid"/>
        <xsl:choose>
            <xsl:when test="$order = floor(1) and $invalid != 'Línea continua sencilla'">Línea continua sencilla</xsl:when>
            <xsl:when test="$order = floor(2) and $invalid != 'Punteado'">Punteado</xsl:when>
            <xsl:when test="$order = floor(3) and $invalid != 'Rayado (espacio pequeño)'">Rayado (espacio pequeño)</xsl:when>
            <xsl:when test="$order = floor(4) and $invalid != 'Rayado (espacio grande)'">Rayado (espacio grande)</xsl:when>
            <xsl:when test="$order = floor(5) and $invalid != 'Guion punto'">Guion punto</xsl:when>
            <xsl:when test="$order = floor(6) and $invalid != 'Guion punto punto'">Guion punto punto</xsl:when>
            <xsl:when test="$order = floor(7) and $invalid != 'Doble'">Doble</xsl:when>
            <xsl:when test="$order = floor(8) and $invalid != 'Triple línea sólida'">Triple línea sólida</xsl:when>
            <xsl:when test="$order = floor(9) and $invalid != 'Diferencia pequeña fino-grueso'">Diferencia pequeña fino-grueso</xsl:when>
            <xsl:when test="$order = floor(10) and $invalid != 'Diferencia pequeña grueso-fino'">Diferencia pequeña grueso-fino</xsl:when>
            <xsl:when test="$order = floor(11) and $invalid != 'Diferencia pequeña fino-grueso-fino'">Diferencia pequeña fino-grueso-fino</xsl:when>
            <xsl:when test="$order = floor(12) and $invalid != 'Diferencia mediana fino-grueso'">Diferencia mediana fino-grueso</xsl:when>
            <xsl:when test="$order = floor(13) and $invalid != 'Diferencia mediana grueso-fino'">Diferencia mediana grueso-fino</xsl:when>
            <xsl:when test="$order = floor(14) and $invalid != 'Diferencia mediana fino-grueso-fino'">Diferencia mediana fino-grueso-fino</xsl:when>
            <xsl:when test="$order = floor(15) and $invalid != 'Diferencia grande fino-grueso'">Diferencia grande fino-grueso</xsl:when>
            <xsl:when test="$order = floor(16) and $invalid != 'Diferencia grande grueso-fino'">Diferencia grande grueso-fino</xsl:when>
            <xsl:when test="$order = floor(17) and $invalid != 'Diferencia grande fino-grueso-fino'">Diferencia grande fino-grueso-fino</xsl:when>
            <xsl:when test="$order = floor(18) and $invalid != 'Ondulado sencillo'">Ondulado sencillo</xsl:when>
            <xsl:when test="$order = floor(19) and $invalid != 'Doble subrayado ondulado'">Doble subrayado ondulado</xsl:when>
            <xsl:when test="$order = floor(20) and $invalid != 'Guion-punto (trazo)'">Guion-punto (trazo)</xsl:when>
            <xsl:when test="$order = floor(21) and $invalid != 'Relieve 3D'">Relieve 3D</xsl:when>
            <xsl:when test="$order = floor(22) and $invalid != 'Grabado 3D'">Grabado 3D</xsl:when>
            <xsl:when test="$order = floor(23) and $invalid != 'Exterior'">Exterior</xsl:when>
            <xsl:when test="$order = floor(24) and $invalid != 'Interior'">Interior</xsl:when>
            <xsl:otherwise>Sin borde</xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template name="borderartlist">
        <xsl:param name="order"/>
        <xsl:param name="invalid"/>
        <xsl:choose>
            <xsl:when test="$order = floor(1) and $invalid != 'Borde de manzanas'">Borde de manzanas</xsl:when>
            <xsl:when test="$order = floor(2) and $invalid != 'Borde de bizcochos'">Borde de bizcochos</xsl:when>
            <xsl:when test="$order = floor(3) and $invalid != 'Borde de porciones de pastel'">Borde de porciones de pastel</xsl:when>
            <xsl:when test="$order = floor(4) and $invalid != 'Borde de maíz dulce'">Borde de maíz dulce</xsl:when>
            <xsl:when test="$order = floor(5) and $invalid != 'Borde de helados'">Borde de helados</xsl:when>
            <xsl:when test="$order = floor(6) and $invalid != 'Borde de botellas de champán'">Borde de botellas de champán</xsl:when>
            <xsl:when test="$order = floor(7) and $invalid != 'Borde de vasos de fiesta'">Borde de vasos de fiesta</xsl:when>
            <xsl:when test="$order = floor(8) and $invalid != 'Borde de árboles de Navidad'">Borde de árboles de Navidad</xsl:when>
            <xsl:when test="$order = floor(9) and $invalid != 'Borde de árboles'">Borde de árboles</xsl:when>
            <xsl:when test="$order = floor(10) and $invalid != 'Borde de palmeras de colores'">Borde de palmeras de colores</xsl:when>
            <xsl:when test="$order = floor(11) and $invalid != 'Borde de globos de tres colores'">Borde de globos de tres colores</xsl:when>
            <xsl:when test="$order = floor(12) and $invalid != 'Borde de globos de aire caliente'">Borde de globos de aire caliente</xsl:when>
            <xsl:when test="$order = floor(13) and $invalid != 'Borde de regalos sorpresa'">Borde de regalos sorpresa</xsl:when>
            <xsl:when test="$order = floor(14) and $invalid != 'Borde de confeti con serpentinas'">Borde de confeti con serpentinas</xsl:when>
            <xsl:when test="$order = floor(15) and $invalid != 'Borde de corazones'">Borde de corazones</xsl:when>
            <xsl:when test="$order = floor(16) and $invalid != 'Borde de globos de corazón'">Borde de globos de corazón</xsl:when>
            <xsl:when test="$order = floor(17) and $invalid != 'Borde de estrellas en 3D'">Borde de estrellas en 3D</xsl:when>
            <xsl:when test="$order = floor(18) and $invalid != 'Borde de estrellas sombreadas'">Borde de estrellas sombreadas</xsl:when>
            <xsl:when test="$order = floor(19) and $invalid != 'Borde de estrellas'">Borde de estrellas</xsl:when>
            <xsl:when test="$order = floor(20) and $invalid != 'Borde de soles'">Borde de soles</xsl:when>
            <xsl:when test="$order = floor(21) and $invalid != 'Borde número 2 de Tierra'">Borde número 2 de Tierra</xsl:when>
            <xsl:when test="$order = floor(22) and $invalid != 'Borde número 1 de Tierra'">Borde número 1 de Tierra</xsl:when>
            <xsl:when test="$order = floor(23) and $invalid != 'Borde de gente con sombreros'">Borde de gente con sombreros</xsl:when>
            <xsl:when test="$order = floor(24) and $invalid != 'Borde de sombreros'">Borde de sombreros</xsl:when>
            <xsl:when test="$order = floor(25) and $invalid != 'Borde de lápices'">Borde de lápices</xsl:when>
            <xsl:when test="$order = floor(26) and $invalid != 'Borde de paquetes'">Borde de paquetes</xsl:when>
            <xsl:when test="$order = floor(27) and $invalid != 'Borde de relojes'">Borde de relojes</xsl:when>
            <xsl:when test="$order = floor(28) and $invalid != 'Borde e petardos'">Borde e petardos</xsl:when>
            <xsl:when test="$order = floor(29) and $invalid != 'Borde de anillos'">Borde de anillos</xsl:when>
            <xsl:when test="$order = floor(30) and $invalid != 'Borde de marcadores de mapas'">Borde de marcadores de mapas</xsl:when>
            <xsl:when test="$order = floor(31) and $invalid != 'Borde de confeti'">Borde de confeti</xsl:when>
            <xsl:when test="$order = floor(32) and $invalid != 'Borde de mariposas'">Borde de mariposas</xsl:when>
            <xsl:when test="$order = floor(33) and $invalid != 'Borde de mariquitas'">Borde de mariquitas</xsl:when>
            <xsl:when test="$order = floor(34) and $invalid != 'Borde de peces'">Borde de peces</xsl:when>
            <xsl:when test="$order = floor(35) and $invalid != 'Borde de pájaros en vuelo'">Borde de pájaros en vuelo</xsl:when>
            <xsl:when test="$order = floor(36) and $invalid != 'Borde de gatos asustados'">Borde de gatos asustados</xsl:when>
            <xsl:when test="$order = floor(37) and $invalid != 'Borde de murciélagos'">Borde de murciélagos</xsl:when>
            <xsl:when test="$order = floor(38) and $invalid != 'Borde de rosas'">Borde de rosas</xsl:when>
            <xsl:when test="$order = floor(39) and $invalid != 'Borde de rosas rojas'">Borde de rosas rojas</xsl:when>
            <xsl:when test="$order = floor(40) and $invalid != 'Borde de poinsettias'">Borde de poinsettias</xsl:when>
            <xsl:when test="$order = floor(41) and $invalid != 'Borde de acebo'">Borde de acebo</xsl:when>
            <xsl:when test="$order = floor(42) and $invalid != 'Borde de flores diminutas'">Borde de flores diminutas</xsl:when>
            <xsl:when test="$order = floor(43) and $invalid != 'Borde de pensamientos'">Borde de pensamientos</xsl:when>
            <xsl:when test="$order = floor(44) and $invalid != 'Borde de flores moderno número 2'">Borde de flores moderno número 2</xsl:when>
            <xsl:when test="$order = floor(45) and $invalid != 'Borde de flores moderno'">Borde de flores moderno</xsl:when>
            <xsl:when test="$order = floor(46) and $invalid != 'Borde de flores blancas'">Borde de flores blancas</xsl:when>
            <xsl:when test="$order = floor(47) and $invalid != 'Borde de viñas'">Borde de viñas</xsl:when>
            <xsl:when test="$order = floor(48) and $invalid != 'Borde de margaritas'">Borde de margaritas</xsl:when>
            <xsl:when test="$order = floor(49) and $invalid != 'Borde de xilografía de flores'">Borde de xilografía de flores</xsl:when>
            <xsl:when test="$order = floor(50) and $invalid != 'Borde de arcos de colores'">Borde de arcos de colores</xsl:when>
            <xsl:when test="$order = floor(51) and $invalid != 'Borde de abanicos'">Borde de abanicos</xsl:when>
            <xsl:when test="$order = floor(52) and $invalid != 'Borde de película'">Borde de película</xsl:when>
            <xsl:when test="$order = floor(53) and $invalid != 'Borde número 1 de relámpagos'">Borde número 1 de relámpagos</xsl:when>
            <xsl:when test="$order = floor(54) and $invalid != 'Borde de brújulas'">Borde de brújulas</xsl:when>
            <xsl:when test="$order = floor(55) and $invalid != 'Borde de D dobles'">Borde de D dobles</xsl:when>
            <xsl:when test="$order = floor(56) and $invalid != 'Borde de onda clásica'">Borde de onda clásica</xsl:when>
            <xsl:when test="$order = floor(57) and $invalid != 'Borde de cuadrados sombreados'">Borde de cuadrados sombreados</xsl:when>
            <xsl:when test="$order = floor(58) and $invalid != 'Borde de líneas retorcidas número 1'">Borde de líneas retorcidas número 1</xsl:when>
            <xsl:when test="$order = floor(59) and $invalid != 'Borde de línea ondulada'">Borde de línea ondulada</xsl:when>
            <xsl:when test="$order = floor(60) and $invalid != 'Borde de cuadrantes'">Borde de cuadrantes</xsl:when>
            <xsl:when test="$order = floor(61) and $invalid != 'Borde de barra de cuadros de colores'">Borde de barra de cuadros de colores</xsl:when>
            <xsl:when test="$order = floor(62) and $invalid != 'Borde de remolinos'">Borde de remolinos</xsl:when>
            <xsl:when test="$order = floor(63) and $invalid != 'Borde de alfileres de anotación número 1'">Borde de alfileres de anotación número 1</xsl:when>
            <xsl:when test="$order = floor(64) and $invalid != 'Borde de alfileres de anotación número 2'">Borde de alfileres de anotación número 2</xsl:when>
            <xsl:when test="$order = floor(65) and $invalid != 'Borde de calabazas número 1'">Borde de calabazas número 1</xsl:when>
            <xsl:when test="$order = floor(66) and $invalid != 'Borde de huevos de color negro'">Borde de huevos de color negro</xsl:when>
            <xsl:when test="$order = floor(67) and $invalid != 'Borde de cupidos'">Borde de cupidos</xsl:when>
            <xsl:when test="$order = floor(68) and $invalid != 'Borde de globos de corazón en tonos de gris'">Borde de globos de corazón en tonos de gris</xsl:when>
            <xsl:when test="$order = floor(69) and $invalid != 'Borde de monigotes'">Borde de monigotes</xsl:when>
            <xsl:when test="$order = floor(70) and $invalid != 'Borde de chupetes'">Borde de chupetes</xsl:when>
            <xsl:when test="$order = floor(71) and $invalid != 'Borde de sonajeros'">Borde de sonajeros</xsl:when>
            <xsl:when test="$order = floor(72) and $invalid != 'Borde de cabañas'">Borde de cabañas</xsl:when>
            <xsl:when test="$order = floor(73) and $invalid != 'Borde de casas originales'">Borde de casas originales</xsl:when>
            <xsl:when test="$order = floor(74) and $invalid != 'Borde de estrellas negras'">Borde de estrellas negras</xsl:when>
            <xsl:when test="$order = floor(75) and $invalid != 'Borde de copos de nieve'">Borde de copos de nieve</xsl:when>
            <xsl:when test="$order = floor(76) and $invalid != 'Borde de copos de nieve de fantasía'">Borde de copos de nieve de fantasía</xsl:when>
            <xsl:when test="$order = floor(77) and $invalid != 'Borde de cohetes'">Borde de cohetes</xsl:when>
            <xsl:when test="$order = floor(78) and $invalid != 'Borde Seattle'">Borde Seattle</xsl:when>
            <xsl:when test="$order = floor(79) and $invalid != 'Borde de notas musicales'">Borde de notas musicales</xsl:when>
            <xsl:when test="$order = floor(80) and $invalid != 'Borde de palmeras negras'">Borde de palmeras negras</xsl:when>
            <xsl:when test="$order = floor(81) and $invalid != 'Borde de hojas de arce'">Borde de hojas de arce</xsl:when>
            <xsl:when test="$order = floor(82) and $invalid != 'Borde de clips'">Borde de clips</xsl:when>
            <xsl:when test="$order = floor(83) and $invalid != 'Borde de huellas de pájaro costero'">Borde de huellas de pájaro costero</xsl:when>
            <xsl:when test="$order = floor(84) and $invalid != 'Borde de gente'">Borde de gente</xsl:when>
            <xsl:when test="$order = floor(85) and $invalid != 'Borde de gente saludando'">Borde de gente saludando</xsl:when>
            <xsl:when test="$order = floor(86) and $invalid != 'Borde número 2 de cuadros eclipsados'">Borde número 2 de cuadros eclipsados</xsl:when>
            <xsl:when test="$order = floor(87) and $invalid != 'Borde hipnótico'">Borde hipnótico</xsl:when>
            <xsl:when test="$order = floor(88) and $invalid != 'Borde de rombos en tonos de gris'">Borde de rombos en tonos de gris</xsl:when>
            <xsl:when test="$order = floor(89) and $invalid != 'Borde de arcos decorativos'">Borde de arcos decorativos</xsl:when>
            <xsl:when test="$order = floor(90) and $invalid != 'Borde de bloques decorativos'">Borde de bloques decorativos</xsl:when>
            <xsl:when test="$order = floor(91) and $invalid != 'Borde de círculos y líneas'">Borde de círculos y líneas</xsl:when>
            <xsl:when test="$order = floor(92) and $invalid != 'Borde de papiro'">Borde de papiro</xsl:when>
            <xsl:when test="$order = floor(93) and $invalid != 'Borde de carpintería'">Borde de carpintería</xsl:when>
            <xsl:when test="$order = floor(94) and $invalid != 'Borde de trenzas entrelazadas'">Borde de trenzas entrelazadas</xsl:when>
            <xsl:when test="$order = floor(95) and $invalid != 'Borde de cinta de opciones entrelazadas'">Borde de cinta de opciones entrelazadas</xsl:when>
            <xsl:when test="$order = floor(96) and $invalid != 'Borde de ángulos entrelazados'">Borde de ángulos entrelazados</xsl:when>
            <xsl:when test="$order = floor(97) and $invalid != 'Borde de festones en forma de arco'">Borde de festones en forma de arco</xsl:when>
            <xsl:when test="$order = floor(98) and $invalid != 'Borde de safari'">Borde de safari</xsl:when>
            <xsl:when test="$order = floor(99) and $invalid != 'Borde de nudos celtas'">Borde de nudos celtas</xsl:when>
            <xsl:when test="$order = floor(100) and $invalid != 'Borde de laberinto loco'">Borde de laberinto loco</xsl:when>
            <xsl:when test="$order = floor(101) and $invalid != 'Borde número 1 de cuadros eclipsados'">Borde número 1 de cuadros eclipsados</xsl:when>
            <xsl:when test="$order = floor(102) and $invalid != 'Borde de pájaros'">Borde de pájaros</xsl:when>
            <xsl:when test="$order = floor(103) and $invalid != 'Borde de tazas de té'">Borde de tazas de té</xsl:when>
            <xsl:when test="$order = floor(104) and $invalid != 'Borde de noroeste'">Borde de noroeste</xsl:when>
            <xsl:when test="$order = floor(105) and $invalid != 'Borde Mexicano'">Borde Mexicano</xsl:when>
            <xsl:when test="$order = floor(106) and $invalid != 'Borde tribal número 6'">Borde tribal número 6</xsl:when>
            <xsl:when test="$order = floor(107) and $invalid != 'Borde tribal número 4'">Borde tribal número 4</xsl:when>
            <xsl:when test="$order = floor(108) and $invalid != 'Borde tribal número 3'">Borde tribal número 3</xsl:when>
            <xsl:when test="$order = floor(109) and $invalid != 'Borde tribal número 2'">Borde tribal número 2</xsl:when>
            <xsl:when test="$order = floor(110) and $invalid != 'Borde tribal número 5'">Borde tribal número 5</xsl:when>
            <xsl:when test="$order = floor(111) and $invalid != 'Borde de efectos ópticos en X'">Borde de efectos ópticos en X</xsl:when>
            <xsl:when test="$order = floor(112) and $invalid != 'Borde de triángulos divertidos'">Borde de triángulos divertidos</xsl:when>
            <xsl:when test="$order = floor(113) and $invalid != 'Borde de pirámides'">Borde de pirámides</xsl:when>
            <xsl:when test="$order = floor(114) and $invalid != 'Borde de pirámides exterior'">Borde de pirámides exterior</xsl:when>
            <xsl:when test="$order = floor(115) and $invalid != 'Borde de confeti usando tonos de gris'">Borde de confeti usando tonos de gris</xsl:when>
            <xsl:when test="$order = floor(116) and $invalid != 'Borde de contorno de confeti'">Borde de contorno de confeti</xsl:when>
            <xsl:when test="$order = floor(117) and $invalid != 'Borde de confeti blanco'">Borde de confeti blanco</xsl:when>
            <xsl:when test="$order = floor(118) and $invalid != 'Borde de mosaico'">Borde de mosaico</xsl:when>
            <xsl:when test="$order = floor(119) and $invalid != 'Borde número 2 de relámpagos'">Borde número 2 de relámpagos</xsl:when>
            <xsl:when test="$order = floor(120) and $invalid != 'Borde de carne de gallina'">Borde de carne de gallina</xsl:when>
            <xsl:when test="$order = floor(121) and $invalid != 'Borde de bombillas'">Borde de bombillas</xsl:when>
            <xsl:when test="$order = floor(122) and $invalid != 'Borde degradado'">Borde degradado</xsl:when>
            <xsl:when test="$order = floor(123) and $invalid != 'Borde de fiesta de triángulos'">Borde de fiesta de triángulos</xsl:when>
            <xsl:when test="$order = floor(124) and $invalid != 'Borde de líneas retorcidas número 2'">Borde de líneas retorcidas número 2</xsl:when>
            <xsl:when test="$order = floor(125) and $invalid != 'Borde de lunas'">Borde de lunas</xsl:when>
            <xsl:when test="$order = floor(126) and $invalid != 'Borde de elipses'">Borde de elipses</xsl:when>
            <xsl:when test="$order = floor(127) and $invalid != 'Borde de rombos dobles'">Borde de rombos dobles</xsl:when>
            <xsl:when test="$order = floor(128) and $invalid != 'Borde de eslabones de cadena'">Borde de eslabones de cadena</xsl:when>
            <xsl:when test="$order = floor(129) and $invalid != 'Borde de triángulos'">Borde de triángulos</xsl:when>
            <xsl:when test="$order = floor(130) and $invalid != 'Borde tribal número 1'">Borde tribal número 1</xsl:when>
            <xsl:when test="$order = floor(131) and $invalid != 'Borde de marquesina dentada'">Borde de marquesina dentada</xsl:when>
            <xsl:when test="$order = floor(132) and $invalid != 'Borde de dientes de tiburón'">Borde de dientes de tiburón</xsl:when>
            <xsl:when test="$order = floor(133) and $invalid != 'Borde de sierra'">Borde de sierra</xsl:when>
            <xsl:when test="$order = floor(134) and $invalid != 'Borde de sierra en gris'">Borde de sierra en gris</xsl:when>
            <xsl:when test="$order = floor(135) and $invalid != 'Borde de sello'">Borde de sello</xsl:when>
            <xsl:when test="$order = floor(136) and $invalid != 'Borde de tiras entrelazadas'">Borde de tiras entrelazadas</xsl:when>
            <xsl:when test="$order = floor(137) and $invalid != 'Borde en zigzag'">Borde en zigzag</xsl:when>
            <xsl:when test="$order = floor(138) and $invalid != 'Borde de punto de cruz'">Borde de punto de cruz</xsl:when>
            <xsl:when test="$order = floor(139) and $invalid != 'Borde de gemas'">Borde de gemas</xsl:when>
            <xsl:when test="$order = floor(140) and $invalid != 'Borde de círculos y rectángulos'">Borde de círculos y rectángulos</xsl:when>
            <xsl:when test="$order = floor(141) and $invalid != 'Borde de triángulos'">Borde de triángulos</xsl:when>
            <xsl:when test="$order = floor(142) and $invalid != 'Borde de insectos'">Borde de insectos</xsl:when>
            <xsl:when test="$order = floor(143) and $invalid != 'Borde de punto en zigzag'">Borde de punto en zigzag</xsl:when>
            <xsl:when test="$order = floor(144) and $invalid != 'Borde tipo tablero de ajedrez'">Borde tipo tablero de ajedrez</xsl:when>
            <xsl:when test="$order = floor(145) and $invalid != 'Borde de barra de cuadros negros'">Borde de barra de cuadros negros</xsl:when>
            <xsl:when test="$order = floor(146) and $invalid != 'Borde de marquesina'">Borde de marquesina</xsl:when>
            <xsl:when test="$order = floor(147) and $invalid != 'Borde básico de puntos blancos'">Borde básico de puntos blancos</xsl:when>
            <xsl:when test="$order = floor(148) and $invalid != 'Borde básico de línea media gruesa'">Borde básico de línea media gruesa</xsl:when>
            <xsl:when test="$order = floor(149) and $invalid != 'Borde básico de línea exterior gruesa'">Borde básico de línea exterior gruesa</xsl:when>
            <xsl:when test="$order = floor(150) and $invalid != 'Borde básico de línea interior gruesa'">Borde básico de línea interior gruesa</xsl:when>
            <xsl:when test="$order = floor(151) and $invalid != 'Borde básico de líneas finas'">Borde básico de líneas finas</xsl:when>
            <xsl:when test="$order = floor(152) and $invalid != 'Borde básico de guiones blancos'">Borde básico de guiones blancos</xsl:when>
            <xsl:when test="$order = floor(153) and $invalid != 'Borde básico de cuadrados blancos'">Borde básico de cuadrados blancos</xsl:when>
            <xsl:when test="$order = floor(154) and $invalid != 'Borde básico de cuadros negros'">Borde básico de cuadros negros</xsl:when>
            <xsl:when test="$order = floor(155) and $invalid != 'Borde básico de guiones negros'">Borde básico de guiones negros</xsl:when>
            <xsl:when test="$order = floor(156) and $invalid != 'Borde básico de puntos negros'">Borde básico de puntos negros</xsl:when>
            <xsl:when test="$order = floor(157) and $invalid != 'Borde de estrellas en lo alto'">Borde de estrellas en lo alto</xsl:when>
            <xsl:when test="$order = floor(158) and $invalid != 'Borde de título para certificado'">Borde de título para certificado</xsl:when>
            <xsl:when test="$order = floor(159) and $invalid != 'Borde hecho a mano número 1'">Borde hecho a mano número 1</xsl:when>
            <xsl:when test="$order = floor(160) and $invalid != 'Borde hecho a mano número 2'">Borde hecho a mano número 2</xsl:when>
            <xsl:when test="$order = floor(161) and $invalid != 'Borde de papel rasgado'">Borde de papel rasgado</xsl:when>
            <xsl:when test="$order = floor(162) and $invalid != 'Borde de papel rasgado negro'">Borde de papel rasgado negro</xsl:when>
            <xsl:when test="$order = floor(163) and $invalid != 'Borde de línea de recorte con guiones'">Borde de línea de recorte con guiones</xsl:when>
            <xsl:when test="$order = floor(164) and $invalid != 'Borde de línea de recorte con puntos'">Borde de línea de recorte con puntos</xsl:when>
            <xsl:otherwise>Borde relleno de queso</xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template name="fontfamilylist">
        <xsl:param name="order"/>
        <xsl:param name="invalid"/>
        <xsl:choose>
            <xsl:when test="$order = floor(0) and $invalid != 'Abadi MT Condensed Light'">Abadi MT Condensed Light</xsl:when>
            <xsl:when test="$order = floor(1) and $invalid != 'Aharoni'">Aharoni</xsl:when>
            <xsl:when test="$order = floor(2) and $invalid != 'Aldhabi'">Aldhabi</xsl:when>
            <xsl:when test="$order = floor(3) and $invalid != 'Andalus'">Andalus</xsl:when>
            <xsl:when test="$order = floor(4) and $invalid != 'Angsana New'">Angsana New</xsl:when>
            <xsl:when test="$order = floor(5) and $invalid != 'AngsanaUPC'">AngsanaUPC</xsl:when>
            <xsl:when test="$order = floor(6) and $invalid != 'Aparajita'">Aparajita</xsl:when>
            <xsl:when test="$order = floor(7) and $invalid != 'Arabic Typesetting'">Arabic Typesetting</xsl:when>
            <xsl:when test="$order = floor(8) and $invalid != 'Arial'">Arial</xsl:when>
            <xsl:when test="$order = floor(9) and $invalid != 'Arial Black'">Arial Black</xsl:when>
            <xsl:when test="$order = floor(10) and $invalid != 'Arial Nova'">Arial Nova</xsl:when>
            <xsl:when test="$order = floor(11) and $invalid != 'Batang'">Batang</xsl:when>
            <xsl:when test="$order = floor(12) and $invalid != 'BatangChe'">BatangChe</xsl:when>
            <xsl:when test="$order = floor(13) and $invalid != 'Book Antiqua'">Book Antiqua</xsl:when>
            <xsl:when test="$order = floor(14) and $invalid != 'Browallia New'">Browallia New</xsl:when>
            <xsl:when test="$order = floor(15) and $invalid != 'BrowalliaUPC'">BrowalliaUPC</xsl:when>
            <xsl:when test="$order = floor(16) and $invalid != 'Calibri'">Calibri</xsl:when>
            <xsl:when test="$order = floor(17) and $invalid != 'Calibri Light'">Calibri Light</xsl:when>
            <xsl:when test="$order = floor(18) and $invalid != 'Calisto MT'">Calisto MT</xsl:when>
            <xsl:when test="$order = floor(19) and $invalid != 'Cambria'">Cambria</xsl:when>
            <xsl:when test="$order = floor(20) and $invalid != 'Cambria Math'">Cambria Math</xsl:when>
            <xsl:when test="$order = floor(21) and $invalid != 'Candara'">Candara</xsl:when>
            <xsl:when test="$order = floor(22) and $invalid != 'Century Gothic'">Century Gothic</xsl:when>
            <xsl:when test="$order = floor(23) and $invalid != 'Comic Sans MS'">Comic Sans MS</xsl:when>
            <xsl:when test="$order = floor(24) and $invalid != 'Consolas'">Consolas</xsl:when>
            <xsl:when test="$order = floor(25) and $invalid != 'Constantia'">Constantia</xsl:when>
            <xsl:when test="$order = floor(26) and $invalid != 'Copperplate Gothic Bold'">Copperplate Gothic Bold</xsl:when>
            <xsl:when test="$order = floor(27) and $invalid != 'Copperplate Gothic Light'">Copperplate Gothic Light</xsl:when>
            <xsl:when test="$order = floor(28) and $invalid != 'Corbel'">Corbel</xsl:when>
            <xsl:when test="$order = floor(29) and $invalid != 'Cordia New'">Cordia New</xsl:when>
            <xsl:when test="$order = floor(30) and $invalid != 'CordiaUPC'">CordiaUPC</xsl:when>
            <xsl:when test="$order = floor(31) and $invalid != 'Courier New'">Courier New</xsl:when>
            <xsl:when test="$order = floor(32) and $invalid != 'DaunPenh'">DaunPenh</xsl:when>
            <xsl:when test="$order = floor(33) and $invalid != 'David'">David</xsl:when>
            <xsl:when test="$order = floor(34) and $invalid != 'Dengxian'">Dengxian</xsl:when>
            <xsl:when test="$order = floor(35) and $invalid != 'DFKai-SB'">DFKai-SB</xsl:when>
            <xsl:when test="$order = floor(36) and $invalid != 'DilleniaUPC'">DilleniaUPC</xsl:when>
            <xsl:when test="$order = floor(37) and $invalid != 'DokChampa'">DokChampa</xsl:when>
            <xsl:when test="$order = floor(38) and $invalid != 'Dotum'">Dotum</xsl:when>
            <xsl:when test="$order = floor(39) and $invalid != 'DotumChe'">DotumChe</xsl:when>
            <xsl:when test="$order = floor(40) and $invalid != 'Ebrima'">Ebrima</xsl:when>
            <xsl:when test="$order = floor(41) and $invalid != 'Estrangelo Edessa'">Estrangelo Edessa</xsl:when>
            <xsl:when test="$order = floor(42) and $invalid != 'EucrosiaUPC'">EucrosiaUPC</xsl:when>
            <xsl:when test="$order = floor(43) and $invalid != 'Euphemia'">Euphemia</xsl:when>
            <xsl:when test="$order = floor(44) and $invalid != 'FangSong'">FangSong</xsl:when>
            <xsl:when test="$order = floor(45) and $invalid != 'Franklin Gothic Medium'">Franklin Gothic Medium</xsl:when>
            <xsl:when test="$order = floor(46) and $invalid != 'FrankRuehl'">FrankRuehl</xsl:when>
            <xsl:when test="$order = floor(47) and $invalid != 'FreesiaUPC'">FreesiaUPC</xsl:when>
            <xsl:when test="$order = floor(48) and $invalid != 'Gabriola'">Gabriola</xsl:when>
            <xsl:when test="$order = floor(49) and $invalid != 'Gadugi'">Gadugi</xsl:when>
            <xsl:when test="$order = floor(50) and $invalid != 'Gautami'">Gautami</xsl:when>
            <xsl:when test="$order = floor(51) and $invalid != 'Georgia'">Georgia</xsl:when>
            <xsl:when test="$order = floor(52) and $invalid != 'Georgia Pro'">Georgia Pro</xsl:when>
            <xsl:when test="$order = floor(53) and $invalid != 'Gill Sans Nova'">Gill Sans Nova</xsl:when>
            <xsl:when test="$order = floor(54) and $invalid != 'Gisha'">Gisha</xsl:when>
            <xsl:when test="$order = floor(55) and $invalid != 'Gulim'">Gulim</xsl:when>
            <xsl:when test="$order = floor(56) and $invalid != 'GulimChe'">GulimChe</xsl:when>
            <xsl:when test="$order = floor(57) and $invalid != 'Gungsuh'">Gungsuh</xsl:when>
            <xsl:when test="$order = floor(58) and $invalid != 'GungsuhChe'">GungsuhChe</xsl:when>
            <xsl:when test="$order = floor(59) and $invalid != 'Impact'">Impact</xsl:when>
            <xsl:when test="$order = floor(60) and $invalid != 'IrisUPC'">IrisUPC</xsl:when>
            <xsl:when test="$order = floor(61) and $invalid != 'Iskoola Pota'">Iskoola Pota</xsl:when>
            <xsl:when test="$order = floor(62) and $invalid != 'JasmineUPC'">JasmineUPC</xsl:when>
            <xsl:when test="$order = floor(63) and $invalid != 'Javanese Text'">Javanese Text</xsl:when>
            <xsl:when test="$order = floor(64) and $invalid != 'KaiTi'">KaiTi</xsl:when>
            <xsl:when test="$order = floor(65) and $invalid != 'Kalinga'">Kalinga</xsl:when>
            <xsl:when test="$order = floor(66) and $invalid != 'Kartika'">Kartika</xsl:when>
            <xsl:when test="$order = floor(67) and $invalid != 'Khmer UI'">Khmer UI</xsl:when>
            <xsl:when test="$order = floor(68) and $invalid != 'KodchiangUPC'">KodchiangUPC</xsl:when>
            <xsl:when test="$order = floor(69) and $invalid != 'Kokila'">Kokila</xsl:when>
            <xsl:when test="$order = floor(70) and $invalid != 'Lao UI'">Lao UI</xsl:when>
            <xsl:when test="$order = floor(71) and $invalid != 'Latha'">Latha</xsl:when>
            <xsl:when test="$order = floor(72) and $invalid != 'Leelawadee'">Leelawadee</xsl:when>
            <xsl:when test="$order = floor(73) and $invalid != 'Leelawadee UI'">Leelawadee UI</xsl:when>
            <xsl:when test="$order = floor(74) and $invalid != 'Levenim MT'">Levenim MT</xsl:when>
            <xsl:when test="$order = floor(75) and $invalid != 'LilyUPC'">LilyUPC</xsl:when>
            <xsl:when test="$order = floor(76) and $invalid != 'Lucida Console'">Lucida Console</xsl:when>
            <xsl:when test="$order = floor(77) and $invalid != 'Lucida Handwriting Italic'">Lucida Handwriting Italic</xsl:when>
            <xsl:when test="$order = floor(78) and $invalid != 'Lucida Sans Unicode'">Lucida Sans Unicode</xsl:when>
            <xsl:when test="$order = floor(79) and $invalid != 'Malgun Gothic'">Malgun Gothic</xsl:when>
            <xsl:when test="$order = floor(80) and $invalid != 'Mangal'">Mangal</xsl:when>
            <xsl:when test="$order = floor(81) and $invalid != 'Manny ITC'">Manny ITC</xsl:when>
            <xsl:when test="$order = floor(82) and $invalid != 'Marlett'">Marlett</xsl:when>
            <xsl:when test="$order = floor(83) and $invalid != 'Meiryo'">Meiryo</xsl:when>
            <xsl:when test="$order = floor(84) and $invalid != 'Meiryo UI'">Meiryo UI</xsl:when>
            <xsl:when test="$order = floor(85) and $invalid != 'Microsoft Himalaya'">Microsoft Himalaya</xsl:when>
            <xsl:when test="$order = floor(86) and $invalid != 'Microsoft JhengHei'">Microsoft JhengHei</xsl:when>
            <xsl:when test="$order = floor(87) and $invalid != 'Microsoft JhengHei UI'">Microsoft JhengHei UI</xsl:when>
            <xsl:when test="$order = floor(88) and $invalid != 'Microsoft New Tai Lue'">Microsoft New Tai Lue</xsl:when>
            <xsl:when test="$order = floor(89) and $invalid != 'Microsoft PhagsPa'">Microsoft PhagsPa</xsl:when>
            <xsl:when test="$order = floor(90) and $invalid != 'Microsoft Sans Serif'">Microsoft Sans Serif</xsl:when>
            <xsl:when test="$order = floor(91) and $invalid != 'Microsoft Tai Le'">Microsoft Tai Le</xsl:when>
            <xsl:when test="$order = floor(92) and $invalid != 'Microsoft Uighur'">Microsoft Uighur</xsl:when>
            <xsl:when test="$order = floor(93) and $invalid != 'Microsoft YaHei'">Microsoft YaHei</xsl:when>
            <xsl:when test="$order = floor(94) and $invalid != 'Microsoft YaHei UI'">Microsoft YaHei UI</xsl:when>
            <xsl:when test="$order = floor(95) and $invalid != 'Microsoft Yi Baiti'">Microsoft Yi Baiti</xsl:when>
            <xsl:when test="$order = floor(96) and $invalid != 'MingLiU, PMingLiU'">MingLiU, PMingLiU</xsl:when>
            <xsl:when test="$order = floor(97) and $invalid != 'MingLiU-ExtB, PMingLiU-ExtB'">MingLiU-ExtB, PMingLiU-ExtB</xsl:when>
            <xsl:when test="$order = floor(98) and $invalid != 'MingLiU_HKSCS'">MingLiU_HKSCS</xsl:when>
            <xsl:when test="$order = floor(99) and $invalid != 'MingLiU_HKSCS-ExtB'">MingLiU_HKSCS-ExtB</xsl:when>
            <xsl:when test="$order = floor(100) and $invalid != 'Miriam, Miriam Fixed'">Miriam, Miriam Fixed</xsl:when>
            <xsl:when test="$order = floor(101) and $invalid != 'Mongolian Baiti'">Mongolian Baiti</xsl:when>
            <xsl:when test="$order = floor(102) and $invalid != 'MoolBoran'">MoolBoran</xsl:when>
            <xsl:when test="$order = floor(103) and $invalid != 'MS Gothic, MS PGothic'">MS Gothic, MS PGothic</xsl:when>
            <xsl:when test="$order = floor(104) and $invalid != 'MS Mincho, MS PMincho'">MS Mincho, MS PMincho</xsl:when>
            <xsl:when test="$order = floor(105) and $invalid != 'MS UI Gothic'">MS UI Gothic</xsl:when>
            <xsl:when test="$order = floor(106) and $invalid != 'MV Boli'">MV Boli</xsl:when>
            <xsl:when test="$order = floor(107) and $invalid != 'Myanmar Text'">Myanmar Text</xsl:when>
            <xsl:when test="$order = floor(108) and $invalid != 'Narkisim'">Narkisim</xsl:when>
            <xsl:when test="$order = floor(109) and $invalid != 'Neue Haas Grotesk Text Pro'">Neue Haas Grotesk Text Pro</xsl:when>
            <xsl:when test="$order = floor(110) and $invalid != 'News Gothic MT'">News Gothic MT</xsl:when>
            <xsl:when test="$order = floor(111) and $invalid != 'Nirmala UI'">Nirmala UI</xsl:when>
            <xsl:when test="$order = floor(112) and $invalid != 'NSimSun'">NSimSun</xsl:when>
            <xsl:when test="$order = floor(113) and $invalid != 'Nyala'">Nyala</xsl:when>
            <xsl:when test="$order = floor(114) and $invalid != 'Palatino Linotype'">Palatino Linotype</xsl:when>
            <xsl:when test="$order = floor(115) and $invalid != 'Plantagenet Cherokee'">Plantagenet Cherokee</xsl:when>
            <xsl:when test="$order = floor(116) and $invalid != 'Raavi'">Raavi</xsl:when>
            <xsl:when test="$order = floor(117) and $invalid != 'Rockwell Nova'">Rockwell Nova</xsl:when>
            <xsl:when test="$order = floor(118) and $invalid != 'Rod'">Rod</xsl:when>
            <xsl:when test="$order = floor(119) and $invalid != 'Sakkal Majalla'">Sakkal Majalla</xsl:when>
            <xsl:when test="$order = floor(120) and $invalid != 'Sanskrit Text'">Sanskrit Text</xsl:when>
            <xsl:when test="$order = floor(121) and $invalid != 'Segoe MDL2 Assets'">Segoe MDL2 Assets</xsl:when>
            <xsl:when test="$order = floor(122) and $invalid != 'Segoe Print'">Segoe Print</xsl:when>
            <xsl:when test="$order = floor(123) and $invalid != 'Segoe Script'">Segoe Script</xsl:when>
            <xsl:when test="$order = floor(124) and $invalid != 'Segoe UI v5.00[3]'">Segoe UI v5.00[3]</xsl:when>
            <xsl:when test="$order = floor(125) and $invalid != 'Segoe UI v5.00 (top) and v5.27 (bottom)'">Segoe UI v5.00 (top) and v5.27 (bottom)</xsl:when>
            <xsl:when test="$order = floor(126) and $invalid != 'Segoe UI v5.01[4]'">Segoe UI v5.01[4]</xsl:when>
            <xsl:when test="$order = floor(127) and $invalid != 'Segoe UI v5.27[5]'">Segoe UI v5.27[5]</xsl:when>
            <xsl:when test="$order = floor(128) and $invalid != 'Segoe UI v5.35'">Segoe UI v5.35</xsl:when>
            <xsl:when test="$order = floor(129) and $invalid != 'Segoe UI Emoji'">Segoe UI Emoji</xsl:when>
            <xsl:when test="$order = floor(130) and $invalid != 'Segoe UI Historic[6]'">Segoe UI Historic[6]</xsl:when>
            <xsl:when test="$order = floor(131) and $invalid != 'Segoe UI Symbol'">Segoe UI Symbol</xsl:when>
            <xsl:when test="$order = floor(132) and $invalid != 'Shonar Bangla'">Shonar Bangla</xsl:when>
            <xsl:when test="$order = floor(133) and $invalid != 'Shruti'">Shruti</xsl:when>
            <xsl:when test="$order = floor(134) and $invalid != 'SimHei'">SimHei</xsl:when>
            <xsl:when test="$order = floor(135) and $invalid != 'SimKai'">SimKai</xsl:when>
            <xsl:when test="$order = floor(136) and $invalid != 'Simplified Arabic'">Simplified Arabic</xsl:when>
            <xsl:when test="$order = floor(137) and $invalid != 'SimSun'">SimSun</xsl:when>
            <xsl:when test="$order = floor(138) and $invalid != 'SimSun-ExtB'">SimSun-ExtB</xsl:when>
            <xsl:when test="$order = floor(139) and $invalid != 'Sitka Banner'">Sitka Banner</xsl:when>
            <xsl:when test="$order = floor(140) and $invalid != 'Sitka Display'">Sitka Display</xsl:when>
            <xsl:when test="$order = floor(141) and $invalid != 'Sitka Heading'">Sitka Heading</xsl:when>
            <xsl:when test="$order = floor(142) and $invalid != 'Sitka Small'">Sitka Small</xsl:when>
            <xsl:when test="$order = floor(143) and $invalid != 'Sitka Subheading'">Sitka Subheading</xsl:when>
            <xsl:when test="$order = floor(144) and $invalid != 'Sitka Text'">Sitka Text</xsl:when>
            <xsl:when test="$order = floor(145) and $invalid != 'Sylfaen'">Sylfaen</xsl:when>
            <xsl:when test="$order = floor(146) and $invalid != 'Symbol'">Symbol</xsl:when>
            <xsl:when test="$order = floor(147) and $invalid != 'Tahoma'">Tahoma</xsl:when>
            <xsl:when test="$order = floor(148) and $invalid != 'Times New Roman'">Times New Roman</xsl:when>
            <xsl:when test="$order = floor(149) and $invalid != 'Traditional Arabic'">Traditional Arabic</xsl:when>
            <xsl:when test="$order = floor(150) and $invalid != 'Trebuchet MS'">Trebuchet MS</xsl:when>
            <xsl:when test="$order = floor(151) and $invalid != 'Tunga'">Tunga</xsl:when>
            <xsl:when test="$order = floor(152) and $invalid != 'Urdu Typesetting'">Urdu Typesetting</xsl:when>
            <xsl:when test="$order = floor(153) and $invalid != 'Utsaah'">Utsaah</xsl:when>
            <xsl:when test="$order = floor(154) and $invalid != 'Vani'">Vani</xsl:when>
            <xsl:when test="$order = floor(155) and $invalid != 'Verdana'">Verdana</xsl:when>
            <xsl:when test="$order = floor(156) and $invalid != 'Verdana Pro'">Verdana Pro</xsl:when>
            <xsl:when test="$order = floor(157) and $invalid != 'Vijaya'">Vijaya</xsl:when>
            <xsl:when test="$order = floor(158) and $invalid != 'Vrinda'">Vrinda</xsl:when>
            <xsl:when test="$order = floor(159) and $invalid != 'Webdings'">Webdings</xsl:when>
            <xsl:when test="$order = floor(160) and $invalid != 'Westminster'">Westminster</xsl:when>
            <xsl:when test="$order = floor(161) and $invalid != 'Wingdings'">Wingdings</xsl:when>
            <xsl:when test="$order = floor(162) and $invalid != 'Yu Gothic'">Yu Gothic</xsl:when>
            <xsl:when test="$order = floor(163) and $invalid != 'Yu Gothic UI'">Yu Gothic UI</xsl:when>
            <xsl:when test="$order = floor(164) and $invalid != 'Yu Mincho'">Yu Mincho</xsl:when>
            <xsl:when test="$order = floor(165) and $invalid != 'See also[edit]'">See also[edit]</xsl:when>
            <xsl:otherwise>Biscordel</xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    
    <xsl:template name="underlinestylelist">
        <xsl:param name="order"/>
        <xsl:param name="invalid"/>
        <xsl:choose>
            <xsl:when test="$order = floor(0) and $invalid != 'Sólo palabras'">Sólo palabras</xsl:when>
            <xsl:when test="$order = floor(1) and $invalid != 'Simple'">Simple</xsl:when>
            <xsl:when test="$order = floor(2) and $invalid != 'Doble'">Doble</xsl:when>
            <xsl:when test="$order = floor(3) and $invalid != 'Grueso'">Grueso</xsl:when>
            <xsl:when test="$order = floor(4) and $invalid != 'Punteado'">Punteado</xsl:when>
            <xsl:when test="$order = floor(5) and $invalid != 'Punteado grueso'">Punteado grueso</xsl:when>
            <xsl:when test="$order = floor(6) and $invalid != 'Guiones'">Guiones</xsl:when>
            <xsl:when test="$order = floor(7) and $invalid != 'Grueso de guiones'">Grueso de guiones</xsl:when>
            <xsl:when test="$order = floor(8) and $invalid != 'Guiones largos'">Guiones largos</xsl:when>
            <xsl:when test="$order = floor(9) and $invalid != 'Grueso de guiones largos'">Grueso de guiones largos</xsl:when>
            <xsl:when test="$order = floor(10) and $invalid != 'Punto-guión'">Punto-guión</xsl:when>
            <xsl:when test="$order = floor(11) and $invalid != 'Grueso punto-guión'">Grueso punto-guión</xsl:when>
            <xsl:when test="$order = floor(12) and $invalid != 'Punto-punto-guión'">Punto-punto-guión</xsl:when>
            <xsl:when test="$order = floor(13) and $invalid != 'Grueso punto-punto-guión'">Grueso punto-punto-guión</xsl:when>
            <xsl:when test="$order = floor(14) and $invalid != 'Ondulado'">Ondulado</xsl:when>
            <xsl:when test="$order = floor(15) and $invalid != 'Grueso ondulado'">Grueso ondulado</xsl:when>
            <xsl:when test="$order = floor(16) and $invalid != 'Doble ondulado'">Doble ondulado</xsl:when>
            <xsl:otherwise>(Ninguno)</xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    
    <xsl:template name="texturelist">
        <xsl:param name="order"/>
        <xsl:param name="invalid"/>
        <xsl:choose>
            <xsl:when test="$order = floor(0) and $invalid != '10%'">10%</xsl:when>
            <xsl:when test="$order = floor(1) and $invalid != '12,5%'">12,5%</xsl:when>
            <xsl:when test="$order = floor(2) and $invalid != '15%'">15%</xsl:when>
            <xsl:when test="$order = floor(3) and $invalid != '17,5%'">17,5%</xsl:when>
            <xsl:when test="$order = floor(4) and $invalid != '20%'">20%</xsl:when>
            <xsl:when test="$order = floor(5) and $invalid != '22,5%'">22,5%</xsl:when>
            <xsl:when test="$order = floor(6) and $invalid != '25%'">25%</xsl:when>
            <xsl:when test="$order = floor(7) and $invalid != '27,5%'">27,5%</xsl:when>
            <xsl:when test="$order = floor(8) and $invalid != '2,5%'">2,5%</xsl:when>
            <xsl:when test="$order = floor(9) and $invalid != '30%'">30%</xsl:when>
            <xsl:when test="$order = floor(10) and $invalid != '32,5%'">32,5%</xsl:when>
            <xsl:when test="$order = floor(11) and $invalid != '35%'">35%</xsl:when>
            <xsl:when test="$order = floor(12) and $invalid != '37,5%'">37,5%</xsl:when>
            <xsl:when test="$order = floor(13) and $invalid != '40%'">40%</xsl:when>
            <xsl:when test="$order = floor(14) and $invalid != '42,5%'">42,5%</xsl:when>
            <xsl:when test="$order = floor(15) and $invalid != '45%'">45%</xsl:when>
            <xsl:when test="$order = floor(16) and $invalid != '47,5%'">47,5%</xsl:when>
            <xsl:when test="$order = floor(17) and $invalid != '50%'">50%</xsl:when>
            <xsl:when test="$order = floor(18) and $invalid != '52,5%'">52,5%</xsl:when>
            <xsl:when test="$order = floor(19) and $invalid != '55%'">55%</xsl:when>
            <xsl:when test="$order = floor(20) and $invalid != '57,5%'">57,5%</xsl:when>
            <xsl:when test="$order = floor(21) and $invalid != '5%'">5%</xsl:when>
            <xsl:when test="$order = floor(22) and $invalid != '60%'">60%</xsl:when>
            <xsl:when test="$order = floor(23) and $invalid != '62,5%'">62,5%</xsl:when>
            <xsl:when test="$order = floor(24) and $invalid != '65%'">65%</xsl:when>
            <xsl:when test="$order = floor(25) and $invalid != '67,5%'">67,5%</xsl:when>
            <xsl:when test="$order = floor(26) and $invalid != '70%'">70%</xsl:when>
            <xsl:when test="$order = floor(27) and $invalid != '72,5%'">72,5%</xsl:when>
            <xsl:when test="$order = floor(28) and $invalid != '75%'">75%</xsl:when>
            <xsl:when test="$order = floor(29) and $invalid != '77,5%'">77,5%</xsl:when>
            <xsl:when test="$order = floor(30) and $invalid != '7,5%'">7,5%</xsl:when>
            <xsl:when test="$order = floor(31) and $invalid != '80%'">80%</xsl:when>
            <xsl:when test="$order = floor(32) and $invalid != '82,5%'">82,5%</xsl:when>
            <xsl:when test="$order = floor(33) and $invalid != '85%'">85%</xsl:when>
            <xsl:when test="$order = floor(34) and $invalid != '87,5%'">87,5%</xsl:when>
            <xsl:when test="$order = floor(35) and $invalid != '90%'">90%</xsl:when>
            <xsl:when test="$order = floor(36) and $invalid != '92,5%'">92,5%</xsl:when>
            <xsl:when test="$order = floor(37) and $invalid != '95%'">95%</xsl:when>
            <xsl:when test="$order = floor(38) and $invalid != '97,5%'">97,5%</xsl:when>
            <xsl:when test="$order = floor(39) and $invalid != 'Cruzado horizontal'">Cruzado horizontal</xsl:when>
            <xsl:when test="$order = floor(40) and $invalid != 'Cruzado horizontal oscuro'">Cruzado horizontal oscuro</xsl:when>
            <xsl:when test="$order = floor(41) and $invalid != 'Cruzado diagonal oscuro'">Cruzado diagonal oscuro</xsl:when>
            <xsl:when test="$order = floor(42) and $invalid != 'Diagonal hacia abajo oscuro'">Diagonal hacia abajo oscuro</xsl:when>
            <xsl:when test="$order = floor(43) and $invalid != 'Diagonal hacia arriba oscuro'">Diagonal hacia arriba oscuro</xsl:when>
            <xsl:when test="$order = floor(44) and $invalid != 'Horizontal oscuro'">Horizontal oscuro</xsl:when>
            <xsl:when test="$order = floor(45) and $invalid != 'Vertical oscuro'">Vertical oscuro</xsl:when>
            <xsl:when test="$order = floor(46) and $invalid != 'Diagonal cruzado'">Diagonal cruzado</xsl:when>
            <xsl:when test="$order = floor(47) and $invalid != 'Diagonal hacia abajo'">Diagonal hacia abajo</xsl:when>
            <xsl:when test="$order = floor(48) and $invalid != 'Diagonal hacia arriba'">Diagonal hacia arriba</xsl:when>
            <xsl:when test="$order = floor(49) and $invalid != 'Horizontal'">Horizontal</xsl:when>
            <xsl:when test="$order = floor(50) and $invalid != 'Sólido (100%)'">Sólido (100%)</xsl:when>
            <xsl:when test="$order = floor(51) and $invalid != 'Vertical'">Vertical</xsl:when>
            <xsl:otherwise>Claro</xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template name="levellist">
        <xsl:param name="order"/>
        <xsl:param name="invalid"/>
        <xsl:choose>
            <xsl:when test="$order = floor(0) and $invalid != '1, 2, 3,...'">1, 2, 3,...</xsl:when>
            <xsl:when test="$order = floor(1) and $invalid != 'I, II, III,...'">I, II, III,...</xsl:when>
            <xsl:when test="$order = floor(2) and $invalid != 'A, B, C,...'">A, B, C,...</xsl:when>
            <xsl:when test="$order = floor(3) and $invalid != 'a, b, c,...'">a, b, c,...</xsl:when>
            <xsl:when test="$order = floor(4) and $invalid != 'i, ii, iii,...'">i, ii, iii,...</xsl:when>
            <xsl:when test="$order = floor(5) and $invalid != '1°, 2°, 3°,...'">1°, 2°, 3°,...</xsl:when>
            <xsl:when test="$order = floor(6) and $invalid != 'Uno, Dos, Tres,...'">Uno, Dos, Tres,...</xsl:when>
            <xsl:when test="$order = floor(7) and $invalid != 'Primero, Segundo, Tercero ...'">Primero, Segundo, Tercero ...</xsl:when>
            <xsl:when test="$order = floor(8) and $invalid != '01, 02, 03,...'">01, 02, 03,...</xsl:when>
            <xsl:when test="$order = floor(9) and $invalid != '001, 002, 003,...'">001, 002, 003,...</xsl:when>
            <xsl:when test="$order = floor(10) and $invalid != '0001, 0002, 0003,...'">0001, 0002, 0003,...</xsl:when>
            <xsl:when test="$order = floor(11) and $invalid != '00001, 00002, 00003,...'">00001, 00002, 00003,...</xsl:when>
            <xsl:when test="$order = floor(12) and $invalid != 'Nueva viñeta'">Nueva viñeta</xsl:when>
            <xsl:when test="$order = floor(13) and $invalid != 'Nueva imagen'">Nueva imagen</xsl:when>
            <xsl:otherwise>(ninguno)</xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
</xsl:stylesheet>
