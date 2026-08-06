import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    
    app = Flask(
        __name__,
        template_folder=os.path.join(base_dir, 'templates'),
        static_folder=os.path.join(base_dir, 'static')
    )
    
    app.config.from_object('app.config.Config')
    db.init_app(app)

    with app.app_context():
        from . import routes
        from . import models
        
        if app.config.get('DB_TYPE') == 'produccion':
            db.create_all()
            from .models import Categoria
            if not Categoria.query.first():
                _crear_datos_ejemplo()
            else:
                _crear_vista_sqlite()

    return app


def _crear_vista_sqlite():
    """Crear o reemplazar la vista en SQLite si no existe."""
    from sqlalchemy import text
    try:
        db.session.execute(text("""
            CREATE VIEW IF NOT EXISTS vista_productos AS
            SELECT 
                p.nombre,
                c.nombre AS categoria,
                p.precio,
                p.stock
            FROM producto p
            LEFT JOIN categoria c ON p.id_categoria = c.id_categoria
        """))
        db.session.commit()
        print("✅ Vista 'vista_productos' verificada/creada.")
    except Exception as e:
        print(f"⚠️ Error al crear vista: {e}")


def _crear_datos_ejemplo():
    """Insertar datos iniciales en SQLite."""
    from .models import Categoria, Producto, Usuario, Venta, DetalleVenta
    from datetime import datetime
    from sqlalchemy import text
    
    # Categorías
    cats = [
        Categoria(nombre='Playeras', descripcion='Playeras de todo tipo'),
        Categoria(nombre='Pantalones', descripcion='Pantalones y jeans'),
        Categoria(nombre='Sudaderas', descripcion='Sudaderas y hoodies'),
        Categoria(nombre='Chamarras', descripcion='Chamarras y chaquetas'),
        Categoria(nombre='Vestidos', descripcion='Vestidos casuales y formales'),
        Categoria(nombre='Faldas', descripcion='Faldas de todos estilos'),
        Categoria(nombre='Shorts', descripcion='Shorts y bermudas'),
        Categoria(nombre='Tenis', descripcion='Tenis y zapatos deportivos'),
        Categoria(nombre='Accesorios', descripcion='Gorras, cinturones, etc.'),
        Categoria(nombre='Ropa deportiva', descripcion='Ropa para ejercicio'),
    ]
    db.session.add_all(cats)
    db.session.commit()
    
    # Productos
    prods = [
        Producto(nombre='Playera Nike Dri-FIT', descripcion='Playera deportiva transpirable', precio=499.99, stock=20, talla='M', color='Negro', id_categoria=1),
        Producto(nombre='Jeans Levis 501', descripcion='Jeans clásicos', precio=899.99, stock=15, talla='L', color='Azul', id_categoria=2),
        Producto(nombre='Sudadera Adidas', descripcion='Sudadera con capucha', precio=799.99, stock=12, talla='M', color='Gris', id_categoria=3),
        Producto(nombre='Chamarra Puma', descripcion='Chamarra ligera', precio=1299.99, stock=8, talla='L', color='Negro', id_categoria=4),
        Producto(nombre='Vestido Casual', descripcion='Vestido floral', precio=699.99, stock=10, talla='S', color='Floral', id_categoria=5),
        Producto(nombre='Falda Plisada', descripcion='Falda corta plisada', precio=450.00, stock=18, talla='M', color='Rosa', id_categoria=6),
        Producto(nombre='Short Deportivo', descripcion='Short para ejercicio', precio=350.00, stock=25, talla='M', color='Negro', id_categoria=7),
        Producto(nombre='Tenis Converse', descripcion='Tenis clásicos', precio=1499.99, stock=9, talla='27', color='Blanco', id_categoria=8),
        Producto(nombre='Gorra New Era', descripcion='Gorra ajustable', precio=599.99, stock=14, talla='Única', color='Negro', id_categoria=9),
        Producto(nombre='Conjunto Deportivo', descripcion='Conjunto completo', precio=999.99, stock=11, talla='L', color='Azul', id_categoria=10),
    ]
    db.session.add_all(prods)
    db.session.commit()
    
    # Usuarios
    users = [
        Usuario(nombre='Juan', apellido='Pérez', correo='juan@example.com', telefono='555-1001', nombre_usuario='juanp', contrasena='12345', rol='Administrador'),
        Usuario(nombre='María', apellido='López', correo='maria@example.com', telefono='555-1002', nombre_usuario='marial', contrasena='12345', rol='Vendedor'),
        Usuario(nombre='Carlos', apellido='García', correo='carlos@example.com', telefono='555-1003', nombre_usuario='carlosg', contrasena='12345', rol='Vendedor'),
        Usuario(nombre='Ana', apellido='Martínez', correo='ana@example.com', telefono='555-2001', nombre_usuario='anam', contrasena='12345', rol='Vendedor'),
        Usuario(nombre='Luis', apellido='Hernández', correo='luis@example.com', telefono='555-2002', nombre_usuario='luish', contrasena='12345', rol='Administrador'),
        Usuario(nombre='Sofía', apellido='Ramírez', correo='sofia@example.com', telefono='555-2003', nombre_usuario='sofiar', contrasena='12345', rol='Vendedor'),
        Usuario(nombre='Pedro', apellido='Torres', correo='pedro@example.com', telefono='555-2004', nombre_usuario='pedrot', contrasena='12345', rol='Vendedor'),
        Usuario(nombre='Fernanda', apellido='Ruiz', correo='fernanda@example.com', telefono='555-2005', nombre_usuario='ferruiz', contrasena='12345', rol='Cliente'),
        Usuario(nombre='Miguel', apellido='Flores', correo='miguel@example.com', telefono='555-2006', nombre_usuario='migf', contrasena='12345', rol='Administrador'),
        Usuario(nombre='Daniela', apellido='Castro', correo='daniela@example.com', telefono='555-2007', nombre_usuario='danic', contrasena='12345', rol='Cliente'),
    ]
    db.session.add_all(users)
    db.session.commit()
    
    # Ventas
    ventas = [
        Venta(fecha=datetime(2026, 7, 1), total=499.99, metodo_pago='Efectivo', id_usuario=1),
        Venta(fecha=datetime(2026, 7, 2), total=899.99, metodo_pago='Tarjeta', id_usuario=2),
        Venta(fecha=datetime(2026, 7, 3), total=799.99, metodo_pago='Transferencia', id_usuario=3),
    ]
    db.session.add_all(ventas)
    db.session.commit()
    
    # Detalles
    detalles = [
        DetalleVenta(id_venta=1, id_producto=1, cantidad=1, precio_unitario=499.99, subtotal=499.99),
        DetalleVenta(id_venta=2, id_producto=2, cantidad=1, precio_unitario=899.99, subtotal=899.99),
        DetalleVenta(id_venta=3, id_producto=3, cantidad=1, precio_unitario=799.99, subtotal=799.99),
    ]
    db.session.add_all(detalles)
    db.session.commit()
    
    # Crear vista
    _crear_vista_sqlite()
    
    print("Datos de ejemplo creados en SQLite.")