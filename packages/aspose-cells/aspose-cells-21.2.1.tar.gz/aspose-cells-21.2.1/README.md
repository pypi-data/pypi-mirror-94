# Python Excel API
Aspose.Cells for Python via Java is a scalable and feature-rich API to process Excel spreadsheets using Python. API offers Excel file creation, manipulation, conversion, & rendering. Developers can format worksheets, rows, columns or cells to the most granular level, create & manipulate chart & pivot tables, render worksheets, charts and specific data ranges to PDF & images, add & calculate Excel's builtin and custom formulas and much more - all without any dependency on Microsoft Office or Excel application.

## Python Spreadsheet API Features
- Create Excel files via API.
- Create & refresh Pivot Tables & charts.
- Create & manipulate sparklines & conditional formatting.
- Convert charts to images or PDF.
- Manage comments & hyperlinks.
- Set complex formulas & calculate results via API.
- Set protection on workbook, worksheet, cell, column or row.
- Create & manipulate named ranges.
- Populate worksheets through Smart Markers.
- Convert worksheets to PDF, XPS & SVG formats.
- Inter-convert files to popular Excel formats.

## Read & Write Excel Files
**Microsoft Excel:** XLS, XLSX, XLSB, XLTX, XLTM, XLSM, XML
**OpenOffice:** ODS
**Text:** CSV, Tab-Delimited, TXT
**Web:** HTML, MHTML

## Save Excel Files As 
**Fixed Layout:** PDF, XPS
**Images:** JPEG, PNG, BMP, SVG, TIFF, GIF, EMF

## Create Excel File from Scratch using Python
``` python
import jpype
import asposecells
jpype.startJVM()
from asposecells.api import Workbook, FileFormatType

workbook = Workbook(FileFormatType.XLSX)
workbook.getWorksheets().get(0).getCells().get("A1").putValue("Hello World")
workbook.save("output.xlsx")

jpype.shutdownJVM()
```
## Create Excel Chart & Convert to Image via Python
``` python
import jpype
import asposecells
jpype.startJVM()
from asposecells.api import Workbook, Chart, ChartType, ImageOrPrintOptions

workbook = Workbook()
sheet = workbook.getWorksheets().get(0)
cells = sheet.getCells()
cells.get(0, 1).putValue("Income")
cells.get(1, 0).putValue("Company A")
cells.get(2, 0).putValue("Company B")
cells.get(3, 0).putValue("Company C")
cells.get(1, 1).putValue(10000)
cells.get(2, 1).putValue(20000)
cells.get(3, 1).putValue(30000)
chartIndex = sheet.getCharts().add(ChartType.COLUMN, 9, 9, 21, 15)
chart = sheet.getCharts().get(chartIndex)
chart.getNSeries().add("B2:B4", True)
chart.getNSeries().setCategoryData("A2:A4")
aSeries = chart.getNSeries().get(0)
aSeries.setName("=B1")
chart.setShowLegend(True)
chart.getTitle().setText("Income Analysis")

options = ImageOrPrintOptions()
options.setHorizontalResolution(300)
options.setVerticalResolution(300)
chart.toImage("chart.png", options)

jpype.shutdownJVM()
```
[Product Page](https://products.aspose.com/cells/python-java) | [Documentation](https://docs.aspose.com/display/cellspythonjava/Home) | [Blog](https://blog.aspose.com/category/cells/) | [API Reference](https://apireference.aspose.com/python/cells) | [Code Samples](https://github.com/aspose-cells/Aspose.Cells-for-Java) | [Free Support](https://forum.aspose.com/c/cells) | [Temporary License](https://purchase.aspose.com/temporary-license) | [EULA](https://company.aspose.com/legal/eula)
