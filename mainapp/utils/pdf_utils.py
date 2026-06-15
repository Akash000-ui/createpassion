from io import BytesIO
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


def build_order_invoice(order, items):
    """Return a PDF invoice for an order as bytes."""
    buffer = BytesIO()
    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=16 * mm,
        bottomMargin=16 * mm,
        title=f'Invoice {order.order_number}',
        author='CREATE PASSION (OPC) PRIVATE LIMITED',
    )

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name='InvoiceTitle',
        parent=styles['Title'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#111827'),
        alignment=TA_RIGHT,
    ))
    styles.add(ParagraphStyle(
        name='SmallMuted',
        parent=styles['Normal'],
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#6B7280'),
    ))
    styles.add(ParagraphStyle(
        name='Address',
        parent=styles['Normal'],
        fontSize=9,
        leading=13,
    ))
    styles.add(ParagraphStyle(
        name='Amount',
        parent=styles['Normal'],
        fontSize=9,
        alignment=TA_RIGHT,
    ))
    styles.add(ParagraphStyle(
        name='TableText',
        parent=styles['Normal'],
        fontSize=9,
        leading=12,
        alignment=TA_LEFT,
    ))

    story = []
    header = Table([
        [
            Paragraph(
                '<b>CREATE PASSION</b><br/>'
                '<font size="8">(OPC) PRIVATE LIMITED</font>',
                styles['Heading2'],
            ),
            Paragraph('INVOICE', styles['InvoiceTitle']),
        ],
    ], colWidths=[105 * mm, 51 * mm])
    header.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LINEBELOW', (0, 0), (-1, -1), 1.5, colors.HexColor('#C9A84C')),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.extend([header, Spacer(1, 8 * mm)])

    customer = order.user
    customer_name = escape(customer.get_full_name())
    customer_email = escape(customer.email or '')
    customer_mobile = escape(customer.mobile or '')
    invoice_meta = Table([
        [
            Paragraph(
                '<b>Bill To</b><br/>'
                f'{customer_name}<br/>'
                f'{customer_email}<br/>'
                f'{customer_mobile}',
                styles['Address'],
            ),
            Paragraph(
                f'<b>Invoice No:</b> {order.order_number}<br/>'
                f'<b>Order Date:</b> {order.order_date.strftime("%d %b %Y, %I:%M %p")}<br/>'
                f'<b>Status:</b> {order.status}<br/>'
                '<b>Payment:</b> Wallet',
                styles['Address'],
            ),
        ],
    ], colWidths=[90 * mm, 66 * mm])
    invoice_meta.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8F7F3')),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#E5E7EB')),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 9),
    ]))
    story.extend([invoice_meta, Spacer(1, 7 * mm)])

    rows = [[
        Paragraph('<b>Product</b>', styles['TableText']),
        Paragraph('<b>Size</b>', styles['TableText']),
        Paragraph('<b>Qty</b>', styles['Amount']),
        Paragraph('<b>Unit Price</b>', styles['Amount']),
        Paragraph('<b>Amount</b>', styles['Amount']),
    ]]
    for item in items:
        product_name = escape(item.product.name if item.product else 'Deleted Product')
        rows.append([
            Paragraph(product_name, styles['TableText']),
            Paragraph(item.size or '-', styles['TableText']),
            Paragraph(str(item.quantity), styles['Amount']),
            Paragraph(f'Rs. {item.price:.2f}', styles['Amount']),
            Paragraph(f'Rs. {item.get_item_total():.2f}', styles['Amount']),
        ])

    item_table = Table(
        rows,
        colWidths=[66 * mm, 19 * mm, 15 * mm, 28 * mm, 28 * mm],
        repeatRows=1,
    )
    item_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#111827')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#D1D5DB')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#FAFAFA')]),
        ('TOPPADDING', (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.extend([item_table, Spacer(1, 6 * mm)])

    totals = Table([
        ['Subtotal', f'Rs. {order.subtotal:.2f}'],
        ['Delivery Charge', 'FREE' if order.delivery_charge == 0 else f'Rs. {order.delivery_charge:.2f}'],
        ['Total Paid', f'Rs. {order.total_amount:.2f}'],
    ], colWidths=[45 * mm, 35 * mm], hAlign='RIGHT')
    totals.setStyle(TableStyle([
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('FONTSIZE', (0, -1), (-1, -1), 11),
        ('LINEABOVE', (0, -1), (-1, -1), 1, colors.HexColor('#111827')),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.extend([totals, Spacer(1, 8 * mm)])

    story.extend([
        Paragraph('<b>Delivery Address</b>', styles['Heading4']),
        Paragraph(
            escape(order.delivery_address).replace('\n', '<br/>'),
            styles['Address'],
        ),
        Spacer(1, 8 * mm),
        Paragraph(
            'This is a computer-generated invoice and does not require a signature.',
            styles['SmallMuted'],
        ),
    ])

    document.build(story)
    return buffer.getvalue()
