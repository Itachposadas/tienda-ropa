from app import db

class DetalleVenta(db.Model):
    __tablename__ = 'detalle_venta'
    
    id_detalle = db.Column(db.Integer, primary_key=True)
    id_venta = db.Column(db.Integer, db.ForeignKey('venta.id_venta'), nullable=False)
    id_producto = db.Column(db.Integer, db.ForeignKey('producto.id_producto'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)
    
    def __repr__(self):
        return f'<DetalleVenta {self.id_detalle}>'
    
    def to_dict(self):
        return {
            'id_detalle': self.id_detalle,
            'id_venta': self.id_venta,
            'id_producto': self.id_producto,
            'cantidad': self.cantidad,
            'precio_unitario': self.precio_unitario,
            'subtotal': self.subtotal,
            'producto_nombre': self.producto.nombre if self.producto else None
        }