from django.urls import path
from .views import lista_productos, crear_producto, obtener_producto, etiquetas_masivas, crear_productos_masivos, eliminar_producto

urlpatterns = [
    path('productos/', lista_productos, name='lista_productos'),
    path('productos/add/', crear_producto, name='crear_producto'),
    path('productos/add-masivo/', crear_productos_masivos, name='crear_productos_masivos'),
    path('productos/<int:pk>/', obtener_producto, name='obtener_producto'),
    path('productos/<int:pk>/delete/', eliminar_producto, name='eliminar_producto'),
    path('etiquetas/masivas/', etiquetas_masivas, name='etiquetas_masivas'),
]