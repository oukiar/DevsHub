#!/usr/bin/env python
"Make some simple multipage pdf files."

from __future__ import print_function
from sys import argv

from reportlab.pdfgen import canvas

point = 1
inch = 72

TEXT = """%s    page %d of %d

a wonderful file
created with Sample_Code/makesimple.py"""


def make_pdf_file(output_filename):
    title = output_filename
    c = canvas.Canvas(output_filename, pagesize=(6 * inch, 4 * inch))
    c.setStrokeColorRGB(0,0,0)
    c.setFillColorRGB(0,0,0)
    
    
    c.setFont("Helvetica", 12 * point)
    
    
    for i in range(1, 5):
        #v = 1 * inch
        #for subtline in (TEXT % (output_filename, pn, np)).split( '\n' ):
        #    c.drawString( 1 * inch, v, subtline )
        #    v -= 12 * point
                    
        #image
        c.drawImage("test.png", 0, 0, 6 * inch, 4 * inch)
        c.showPage()
    
    c.save()

if __name__ == "__main__":
    
    make_pdf_file("test.pdf")
    print ("Wrote", "test.pdf")
