from decimal import Decimal
from io import BytesIO
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from mainapp.utils.common_utils import FIXED_DELIVERY_CHARGE, calculate_line_tax, money


def _amount(value):
    return f'{money(value):,.2f}'


def _product_mrp(item):
    if item.product and item.product.price:
        return money(item.product.price)
    return money(item.price)


def build_order_invoice(order, items):
    """Return a GST-style PDF invoice for an order as bytes."""
    buffer = BytesIO()
    document = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        rightMargin=8 * mm,
        leftMargin=8 * mm,
        topMargin=8 * mm,
        bottomMargin=8 * mm,
        title=f'Invoice {order.order_number}',
        author='CREATE PASSION (OPC) PRIVATE LIMITED',
    )

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name='Tiny',
        parent=styles['Normal'],
        fontSize=7,
        leading=9,
    ))
    styles.add(ParagraphStyle(
        name='TinyBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7,
        leading=9,
    ))
    styles.add(ParagraphStyle(
        name='TinyRight',
        parent=styles['Normal'],
        fontSize=7,
        leading=9,
        alignment=TA_RIGHT,
    ))
    styles.add(ParagraphStyle(
        name='SmallRight',
        parent=styles['Normal'],
        fontSize=8,
        leading=10,
        alignment=TA_RIGHT,
    ))
    styles.add(ParagraphStyle(
        name='HeadingRight',
        parent=styles['Heading1'],
        alignment=TA_RIGHT,
        fontSize=18,
        leading=22,
    ))
    styles.add(ParagraphStyle(
        name='Address',
        parent=styles['Normal'],
        fontSize=8,
        leading=11,
        alignment=TA_LEFT,
    ))

    story = []
    customer = order.user
    bill_to = (
        '<b>CREATE PASSION (OPC) PRIVATE LIMITED</b><br/>'
        'India'
    )
    ship_to = (
        f'<b>Ship To:</b><br/>'
        f'{escape(customer.get_full_name())}<br/>'
        f'{escape(customer.email or "")}<br/>'
        f'{escape(customer.mobile or "")}<br/>'
        f'{escape(order.delivery_address).replace(chr(10), "<br/>")}'
    )

    header = Table([
        [Paragraph(bill_to, styles['Address']), Paragraph(ship_to, styles['Address'])],
    ], colWidths=[138 * mm, 138 * mm])
    header.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.7, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 7),
        ('RIGHTPADDING', (0, 0), (-1, -1), 7),
        ('TOPPADDING', (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
    ]))
    story.append(header)

    meta = Table([
        [
            Paragraph('<b>Order ID:</b>', styles['Tiny']),
            Paragraph(escape(order.order_number), styles['Tiny']),
            Paragraph('<b>Date:</b>', styles['Tiny']),
            Paragraph(order.order_date.strftime('%d %b %Y'), styles['Tiny']),
        ],
        [
            Paragraph('<b>Invoice Number:</b>', styles['Tiny']),
            Paragraph(str(order.id), styles['Tiny']),
            Paragraph('<b>Place:</b>', styles['Tiny']),
            Paragraph('India', styles['Tiny']),
        ],
    ], colWidths=[34 * mm, 104 * mm, 34 * mm, 104 * mm])
    meta.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.7, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(meta)

    rows = [[
        Paragraph('<b>S.No</b>', styles['TinyBold']),
        Paragraph('<b>Item</b>', styles['TinyBold']),
        Paragraph('<b>Size</b>', styles['TinyBold']),
        Paragraph('<b>HSN</b>', styles['TinyBold']),
        Paragraph('<b>MRP</b>', styles['TinyBold']),
        Paragraph('<b>QTY</b>', styles['TinyBold']),
        Paragraph('<b>Total</b>', styles['TinyBold']),
        Paragraph('<b>Discount</b>', styles['TinyBold']),
        Paragraph('<b>Gross<br/>Amount</b>', styles['TinyBold']),
        Paragraph('<b>CGST</b>', styles['TinyBold']),
        Paragraph('<b>SGST</b>', styles['TinyBold']),
        Paragraph('<b>Total<br/>Tax</b>', styles['TinyBold']),
        Paragraph('<b>Net Amount</b>', styles['TinyBold']),
    ]]

    totals = {
        'qty': 0,
        'total': Decimal('0.00'),
        'discount': Decimal('0.00'),
        'gross': Decimal('0.00'),
        'cgst': Decimal('0.00'),
        'sgst': Decimal('0.00'),
        'tax': Decimal('0.00'),
        'net': Decimal('0.00'),
    }

    for index, item in enumerate(items, start=1):
        qty = item.quantity
        mrp = _product_mrp(item)
        line_total = money(mrp * qty)
        gross_amount = money(item.price * qty)
        discount = money(line_total - gross_amount)
        taxes = calculate_line_tax(gross_amount)
        hsn = item.product.model_no if item.product and item.product.model_no else '-'
        product_name = item.product.name if item.product else 'Deleted Product'

        totals['qty'] += qty
        totals['total'] += line_total
        totals['discount'] += discount
        totals['gross'] += gross_amount
        totals['cgst'] += taxes['cgst']
        totals['sgst'] += taxes['sgst']
        totals['tax'] += taxes['total_tax']
        totals['net'] += taxes['net_amount']

        rows.append([
            Paragraph(str(index), styles['Tiny']),
            Paragraph(escape(product_name), styles['Tiny']),
            Paragraph(escape(item.size or '-'), styles['Tiny']),
            Paragraph(escape(str(hsn)), styles['Tiny']),
            Paragraph(_amount(mrp), styles['TinyRight']),
            Paragraph(str(qty), styles['TinyRight']),
            Paragraph(_amount(line_total), styles['TinyRight']),
            Paragraph(_amount(discount), styles['TinyRight']),
            Paragraph(_amount(gross_amount), styles['TinyRight']),
            Paragraph(_amount(taxes['cgst']), styles['TinyRight']),
            Paragraph(_amount(taxes['sgst']), styles['TinyRight']),
            Paragraph(_amount(taxes['total_tax']), styles['TinyRight']),
            Paragraph(_amount(taxes['net_amount']), styles['TinyRight']),
        ])

    rows.append([
        Paragraph('<b>Total</b>', styles['TinyBold']),
        '',
        '',
        '',
        '',
        Paragraph(f'<b>{totals["qty"]}</b>', styles['TinyRight']),
        Paragraph(f'<b>{_amount(totals["total"])}</b>', styles['TinyRight']),
        Paragraph(f'<b>{_amount(totals["discount"])}</b>', styles['TinyRight']),
        Paragraph(f'<b>{_amount(totals["gross"])}</b>', styles['TinyRight']),
        Paragraph(f'<b>{_amount(totals["cgst"])}</b>', styles['TinyRight']),
        Paragraph(f'<b>{_amount(totals["sgst"])}</b>', styles['TinyRight']),
        Paragraph(f'<b>{_amount(totals["tax"])}</b>', styles['TinyRight']),
        Paragraph(f'<b>{_amount(totals["net"])}</b>', styles['TinyRight']),
    ])

    delivery = money(FIXED_DELIVERY_CHARGE)
    final_amount = money(totals['net'] + delivery)
    rows.append([
        Paragraph('<b>Delivery Charges</b>', styles['TinyBold']),
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        Paragraph(f'<b>{_amount(delivery)}</b>', styles['TinyRight']),
    ])
    rows.append([
        Paragraph('<b>Net Amount</b>', styles['TinyBold']),
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        Paragraph(f'<b>{_amount(final_amount)}</b>', styles['TinyRight']),
    ])

    table = Table(
        rows,
        colWidths=[12 * mm, 51 * mm, 16 * mm, 15 * mm, 18 * mm, 13 * mm,
                   20 * mm, 20 * mm, 22 * mm, 18 * mm, 18 * mm, 20 * mm, 23 * mm],
        repeatRows=1,
    )
    table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.55, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F1F5F9')),
        ('SPAN', (0, -1), (11, -1)),
        ('SPAN', (0, -2), (11, -2)),
        ('SPAN', (0, -3), (4, -3)),
        ('LEFTPADDING', (0, 0), (-1, -1), 3),
        ('RIGHTPADDING', (0, 0), (-1, -1), 3),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.extend([Spacer(1, 1 * mm), table, Spacer(1, 3 * mm)])
    story.append(Paragraph(
        'This is a computer-generated invoice and does not require a signature.',
        styles['Tiny'],
    ))

    document.build(story)
    return buffer.getvalue()
