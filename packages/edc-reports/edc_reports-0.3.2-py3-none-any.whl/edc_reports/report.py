from abc import ABC
from io import BytesIO
from uuid import uuid4

from django.apps import apps as django_apps
from django.contrib import messages
from django.http import HttpResponse
from django.utils import timezone
from django_revision.revision import Revision
from edc_protocol import Protocol
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, _baseFontNameB, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate

from .numbered_canvas import NumberedCanvas


class Report(ABC):
    document_template = SimpleDocTemplate

    default_page = dict(
        rightMargin=0.5 * cm,
        leftMargin=0.5 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.5 * cm,
        pagesize=A4,
    )

    def __init__(self, page=None, header_line=None, filename=None, request=None, **kwargs):
        self._styles = None
        self.request = request
        self.page = page or self.default_page

        self.report_filename = filename or f"{uuid4()}.pdf"

        if not header_line:
            header_line = Protocol().institution
        self.header_line = header_line

    def get_report_story(self, **kwargs):
        return []

    def draw_footer(self, canvas, doc):
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name="header", fontSize=6, alignment=TA_CENTER))
        width, _ = A4
        canvas.setFontSize(6)
        timestamp = timezone.now().strftime("%Y-%m-%d %H:%M")
        canvas.drawRightString(width - len(timestamp) - 20, 25, f"printed on {timestamp}")
        canvas.drawString(35, 25, f"clinicedc {Revision().tag}")

    def on_first_page(self, canvas, doc):
        "Callback for onFirstPage"
        self.draw_footer(canvas, doc)

    def on_later_pages(self, canvas, doc):
        "Callback for onLaterPages"
        self.draw_footer(canvas, doc)

    def render(self, message_user=None, **kwargs):

        message_user = True if message_user is None else message_user
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="{self.report_filename}"'

        buffer = BytesIO()

        document_template = self.document_template(buffer, **self.page)

        story = self.get_report_story(**kwargs)

        document_template.build(
            story,
            onFirstPage=self.on_first_page,
            onLaterPages=self.on_later_pages,
            canvasmaker=NumberedCanvas,
        )

        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        if message_user and self.request:
            self.message_user(**kwargs)
        return response

    def message_user(self, **kwargs):
        messages.success(
            self.request,
            f"The report has been exported as a PDF. See downloads in your browser. "
            f"The filename is '{self.report_filename}'.",
            fail_silently=True,
        )

    def header_footer(self, canvas, doc):
        canvas.saveState()
        _, height = A4

        header_para = Paragraph(self.header_line, self.styles["header"])
        header_para.drawOn(canvas, doc.leftMargin, height - 15)

        dte = timezone.now().strftime("%Y-%m-%d %H:%M")
        footer_para = Paragraph(f"printed on {dte}", self.styles["footer"])
        _, h = footer_para.wrap(doc.width, doc.bottomMargin)
        footer_para.drawOn(canvas, doc.leftMargin, h)
        canvas.restoreState()

    @property
    def styles(self):
        if not self._styles:
            styles = getSampleStyleSheet()
            styles.add(ParagraphStyle(name="titleR", fontSize=8, alignment=TA_RIGHT))
            styles.add(ParagraphStyle(name="header", fontSize=6, alignment=TA_CENTER))
            styles.add(ParagraphStyle(name="footer", fontSize=6, alignment=TA_RIGHT))
            styles.add(ParagraphStyle(name="center", alignment=TA_CENTER))
            styles.add(ParagraphStyle(name="Right", alignment=TA_RIGHT))
            styles.add(ParagraphStyle(name="left", alignment=TA_LEFT))
            styles.add(
                ParagraphStyle(name="line_data", alignment=TA_LEFT, fontSize=8, leading=10)
            )
            styles.add(
                ParagraphStyle(
                    name="line_data_small", alignment=TA_LEFT, fontSize=7, leading=9
                )
            )
            styles.add(
                ParagraphStyle(
                    name="line_data_small_center",
                    alignment=TA_CENTER,
                    fontSize=7,
                    leading=8,
                )
            )
            styles.add(
                ParagraphStyle(
                    name="line_data_medium", alignment=TA_LEFT, fontSize=10, leading=12
                )
            )
            styles.add(
                ParagraphStyle(
                    name="line_data_mediumB",
                    alignment=TA_LEFT,
                    fontSize=10,
                    leading=11,
                    fontName=_baseFontNameB,
                )
            )
            styles.add(
                ParagraphStyle(
                    name="line_data_large", alignment=TA_LEFT, fontSize=11, leading=14
                )
            )
            styles.add(
                ParagraphStyle(
                    name="line_data_largest", alignment=TA_LEFT, fontSize=14, leading=18
                )
            )
            styles.add(
                ParagraphStyle(name="line_label", fontSize=7, leading=6, alignment=TA_LEFT)
            )
            styles.add(
                ParagraphStyle(name="line_label_center", fontSize=7, alignment=TA_CENTER)
            )
            styles.add(
                ParagraphStyle(name="row_header", fontSize=8, leading=8, alignment=TA_CENTER)
            )
            styles.add(
                ParagraphStyle(name="row_data", fontSize=7, leading=7, alignment=TA_CENTER)
            )
            self._styles = styles
        return self._styles
