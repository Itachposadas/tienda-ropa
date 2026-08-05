from app import db
from datetime import datetime

class Venta(db.Model):
    __tablename__ = 'venta'
    
    id_venta = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    total = db.Column(db.Float, nullable=False)
    metodo_pago = db.Column(db.String(50))
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'), nullable=False)
    
    # Relación con detalles de venta
    detalles = db.relationship('DetalleVenta', backref='venta', lazy=True, cascade='all, delete-orphan')
    
    # Campos adicionales para el estado del pedido (si no existen en tu tabla, agregarlos)
    estado = db.Column(db.String(20), default='pendiente')
    direccion_envio = db.Column(db.String(200))
    numero_orden = db.Column(db.String(50), unique=True)
    observaciones = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Venta {self.id_venta}>'
    
    def to_dict(self):
        return {
            'id_venta': self.id_venta,
            'fecha': self.fecha.strftime('%Y-%m-%d %H:%M:%S') if self.fecha else None,
            'total': self.total,
            'metodo_pago': self.metodo_pago,
            'id_usuario': self.id_usuario,
            'estado': self.estado,
            'direccion_envio': self.direccion_envio,
            'numero_orden': self.numero_orden,
            'usuario_nombre': f"{self.usuario.nombre} {self.usuario.apellido}" if self.usuario else None
        }