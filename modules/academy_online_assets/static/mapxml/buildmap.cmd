@ECHO OFF


SET WATERMARK_FILE=d:\Academia\CONTROL\Recursos graficos\HeaderAndFooter-Inverse.pdf
SET STAMP=d:\Academia\CONTROL\Recursos graficos\Marca de agua (hueca).PNG
SET COVER=D:\Academia\CONTROL\Recursos graficos\Portada.pdf
SET TITLE=D:\Academia\CONTROL\Recursos graficos\titulo_simulacro_map.ps

SET XML2HTML=d:\Proyectos\academy-scripts\scripts\xml2html.py
SET PDFTK=C:\Program Files (x86)\PDFtk\bin\pdftk.exe
SET WKHTMLTOPDF=d:\Portables\Odoo\_service_\thirdparty\wkhtmltopdf.exe
SET GS=C:\Program Files\PDFCreator\Ghostscript\Bin\gswin32c.exe

SET CURRENTFOLDER=
FOR %%A IN (.) DO SET CURRENTFOLDER=%%~NA

SET UPPER=
FOR /F "skip=2 delims=" %%I IN ('tree "\%CURRENTFOLDER%"') DO IF NOT DEFINED UPPER SET "UPPER=%%~I"
SET "UPPER=%UPPER:~3%"
ECHO %UPPER%

IF NOT EXIST notebook.xml GOTO ERROR

PYTHON "%XML2HTML%" notebook.xml -o="Notebook.html"
"%WKHTMLTOPDF%" -T 37.5 -B 22.5 -L 20 -R 20 "Notebook.html"  "Notebook.pdf"

rem COPY "%TITLE%" tf.ps

(TYPE "%TITLE%" | SED -e "s/###/%UPPER%/g") > "%TMP%\tf.ps"
(TYPE "%TMP%\tf.ps" | SED -e "s/_-_/ - /g") > tf.ps
"%GS%" -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -sOutputFile=cover.pdf tf.ps "%COVER%"
"%PDFTK%" "Notebook.pdf" multibackground "%WATERMARK_FILE%" output "NotebookWM.pdf"
REM "%PDFTK%" "NotebookWM.pdf" stamp "%STAMP%" output "NotebookWMStamped.pdf"
"%GS%" -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -sOutputFile=Binder.pdf cover.pdf NotebookWM.pdf

IF EXIST binder.pdf ECHO Document ready...

GOTO FIN

:ERROR
ECHO ERROR, No se ha creado el documento.

:FIN
IF EXIST cover.pdf DEL cover.pdf
IF EXIST tf.ps DEL tf.ps
IF EXIST Notebook.html DEL Notebook.html
IF EXIST Notebook.pdf DEL Notebook.pdf
IF EXIST NotebookWM.pdf DEL NotebookWM.pdf

SET WATERMARK_FILE=
SET COVER=
SET XML2HTML=
SET PDFTK=
SET WKHTMLTOPDF=
SET GS=
SET CURRENTFOLDER=