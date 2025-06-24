from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Producto
from .serializers import ProductoSerializer
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.graphics.barcode import code128

from django.http import HttpResponse
import os
from django.conf import settings

image_path = os.path.join(settings.BASE_DIR, 'static', 'jaes-logo.jpg')

@api_view(['GET'])
def lista_productos(request):
    productos = Producto.objects.all()
    serializer = ProductoSerializer(productos, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def crear_producto(request):
    serializer = ProductoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def obtener_producto(request, pk):
    try:
        producto = Producto.objects.get(pk=pk)
    except Producto.DoesNotExist:
        return Response({'error': 'Producto no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    serializer = ProductoSerializer(producto)
    return Response(serializer.data)

@api_view(['POST'])
def etiquetas_masivas(request):
    data = request.data

    # Validar que sea una lista
    if not isinstance(data, list):
        return Response({'error': 'El formato debe ser una lista.'}, status=status.HTTP_400_BAD_REQUEST)

    # Caso 1: [{id:..., checked:...}]
    if all(isinstance(item, dict) and 'id' in item and 'checked' in item for item in data):
        productos_info = [
            {
                "nombre": p.nombre,
                "sku": p.sku,
                "lote": p.lote,
                "cantidad": p.cantidad
            }
            for p in Producto.objects.filter(id__in=[item['id'] for item in data if item.get('checked')])
        ]
        return generar_pdf_etiquetas(productos_info)

    # Caso 2: [{todos:...}]
    if len(data) == 1 and isinstance(data[0], dict) and 'todos' in data[0]:
        productos = Producto.objects.all()
        productos_info = [
            {
                "nombre": p.nombre,
                "sku": p.sku,
                "lote": p.lote,
                "cantidad": p.cantidad
            }
            for p in productos
        ]
        return generar_pdf_etiquetas(productos_info)

    return Response({'error': 'Formato no permitido.'}, status=status.HTTP_400_BAD_REQUEST)


def generar_pdf_etiquetas(data):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="etiquetas.pdf"'

    c = canvas.Canvas(response, pagesize=A4)
    c.setTitle("etiquetas_producto")  # Título de la pestaña del PDF
    width, height = A4

    max_width = width * 0.2
    max_height = height * 0.2

    img = ImageReader(image_path)
    img_width, img_height = img.getSize()
    scale = min(max_width / img_width, max_height / img_height)
    draw_width = img_width * scale
    draw_height = img_height * scale

    for producto in data:
        # Centrar logo arriba
        x_img = (width - draw_width) / 2
        y_img = height - draw_height - 80  # 80 pts de margen superior
        c.drawImage(img, x_img, y_img, width=draw_width, height=draw_height)

        # Datos del producto
        filas = [
            ("Nombre:", producto.get("nombre", "")),
            ("SKU:", producto.get("sku", "")),
            ("Lote:", producto.get("lote", "")),
            ("Cantidad:", str(producto.get("cantidad", ""))),
        ]

        espacio_entre_filas = 28
        y_texto = y_img - 40  # 40 pts debajo del logo

        col1_x = width * 0.25
        col2_x = width * 0.75

        for i, (tipo, valor) in enumerate(filas):
            if i < 2:
                x = col1_x
                y_fila = y_texto - i * espacio_entre_filas
            else:
                x = col2_x
                y_fila = y_texto - (i - 2) * espacio_entre_filas

            c.setFont("Helvetica-Bold", 13)
            c.drawRightString(x - 5, y_fila, tipo)
            c.setFont("Helvetica", 13)
            c.drawString(x + 5, y_fila, valor)

        # Código de barras
        if 'sku' in producto:
            # Mucho más grande y mucho más abajo
            barcode = code128.Code128(producto['sku'], barHeight=200, barWidth=3.5, humanReadable=True)
            barcode_x = x_img + (draw_width - barcode.width) / 2
            barcode_y = y_texto - 350  # Mucho más abajo (ajusta este valor si lo necesitas)
            barcode.drawOn(c, barcode_x, barcode_y)

        c.showPage()

    c.save()
    return response

@api_view(['POST'])
def crear_productos_masivos(request):
    """
    Endpoint para crear varios productos a la vez.
    """
    serializer = ProductoSerializer(data=request.data, many=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def eliminar_producto(request, pk):
    try:
        producto = Producto.objects.get(pk=pk)
        producto.delete()
        return Response({'mensaje': 'Producto eliminado correctamente.'}, status=status.HTTP_204_NO_CONTENT)
    except Producto.DoesNotExist:
        return Response({'error': 'Producto no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

