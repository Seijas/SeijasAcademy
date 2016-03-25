import os
from reportlab.platypus import Paragraph, Image, SimpleDocTemplate, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

import time
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

class Informes:

    def __init__(self, option):
        if option:
            self.new_registration()
        else:
            self.monthly_bill()

    @staticmethod
    def new_registration():

        c = canvas.Canvas("new_registration.pdf", pagesize=A4)
        c.drawString(50, 800, "La Academia de Seijas")
        c.drawString(400, 50, time.ctime())
        c.drawString(460, 100, "Daniel Seijas")
        c.save()

    def monthly_bill(self):
        print("Dos")

Informes(1)