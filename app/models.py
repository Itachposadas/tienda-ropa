from app import db
from datetime import datetime

# ============================================================
# MODELOS - Mapeo de tablas existentes en MariaDB
# NO crean ni modifican tablas, solo las reflejan.
# ============================================================

class Categoria(db.Model):
    __tablename__ = 'categoria'
    __table_args__ = {'extend_existing': True}

    id_categoria = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    
    # Relación con productos
    productos = db.relationship('Producto', backref='categoria', lazy=True)
    
    def __repr__(self):
        return f'<Categoria {self.nombre}>'


class Producto(db.Model):
    __tablename__ = 'producto'
    __table_args__ = {'extend_existing': True}

    id_producto = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    talla = db.Column(db.String(10), nullable=True)
    color = db.Column(db.String(50), nullable=True)
    id_categoria = db.Column(db.Integer, db.ForeignKey('categoria.id_categoria'), nullable=True)
    
    # Relación con detalles de venta
    detalles = db.relationship('DetalleVenta', backref='producto', lazy=True)
    
    def __repr__(self):
        return f'<Producto {self.nombre} - ${self.precio}>'


class Usuario(db.Model):
    __tablename__ = 'usuario'
    __table_args__ = {'extend_existing': True}

    id_usuario = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), unique=True, nullable=False)
    telefono = db.Column(db.String(20), nullable=True)
    nombre_usuario = db.Column(db.String(50), unique=True, nullable=False)
    contrasena = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(20), default='cliente')  # cliente, admin, etc.
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relación con ventas
    ventas = db.relationship('Venta', backref='usuario', lazy=True)
    
    def __repr__(self):
        return f'<Usuario {self.nombre_usuario} - {self.rol}>'


class Venta(db.Model):
    __tablename__ = 'venta'
    __table_args__ = {'extend_existing': True}

    id_venta = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    total = db.Column(db.Float, nullable=False)
    metodo_pago = db.Column(db.String(50), nullable=True)  # efectivo, tarjeta, etc.
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'), nullable=True)
    
    # Relación con detalles de venta
    detalles = db.relationship('DetalleVenta', backref='venta', lazy=True)
    
    def __repr__(self):
        return f'<Venta {self.id_venta} - ${self.total}>'


class DetalleVenta(db.Model):
    __tablename__ = 'detalle_venta'
    __table_args__ = {'extend_existing': True}

    id_detalle = db.Column(db.Integer, primary_key=True)
    id_venta = db.Column(db.Integer, db.ForeignKey('venta.id_venta'), nullable=False)
    id_producto = db.Column(db.Integer, db.ForeignKey('producto.id_producto'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)
    
    def __repr__(self):
        return f'<DetalleVenta {self.id_detalle} - Prod:{self.id_producto}>'


# ============================================================
# VISTA - Solo lectura, no se puede modificar
# ============================================================

class VistaProductos(db.Model):
    __tablename__ = 'vista_productos'
    __table_args__ = {'extend_existing': True}
    
    # Las vistas no tienen primary key real, usamos un identificador único
    nombre = db.Column(db.String(100))
    categoria = db.Column(db.String(100))
    precio = db.Column(db.Float)
    stock = db.Column(db.Integer)
    
    # SQLAlchemy necesita una primary key, usamos nombre como "clave" virtual
    __mapper_args__ = {
        'primary_key': [nombre]
    }
    
    def __repr__(self):
        return f'<VistaProductos {self.nombre} - {self.categoria}>'