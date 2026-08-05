from app import db
from datetime import datetime

class Producto(db.Model):
    __tablename__ = 'producto'
    
    id_producto = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    talla = db.Column(db.String(10))
    color = db.Column(db.String(30))
    id_categoria = db.Column(db.Integer, db.ForeignKey('categoria.id_categoria'))
    
    # Relación con detalles de venta
    detalles_venta = db.relationship('DetalleVenta', backref='producto', lazy=True)
    
    def __repr__(self):
        return f'<Producto {self.nombre}>'
    
    def to_dict(self):
        return {
            'id_producto': self.id_producto,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'precio': self.precio,
            'stock': self.stock,
            'talla': self.talla,
            'color': self.color,
            'id_categoria': self.id_categoria,
            'categoria_nombre': self.categoria.nombre if self.categoria else None
        }