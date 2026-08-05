from app import db

class VistaProductos(db.Model):
    """Modelo para la vista vista_productos (solo lectura)"""
    __tablename__ = 'vista_productos'
    __table_args__ = {'extend_existing': True}
    
    # Estos campos deben coincidir con los de tu vista
    nombre = db.Column(db.String(100), primary_key=True)  # Puede que necesites ajustar esto
    categoria = db.Column(db.String(50))
    precio = db.Column(db.Float)
    stock = db.Column(db.Integer)
    
    def to_dict(self):
        return {
            'nombre': self.nombre,
            'categoria': self.categoria,
            'precio': self.precio,
            'stock': self.stock
        }