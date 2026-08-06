from flask import current_app as app
from flask import render_template, redirect, url_for, request
from sqlalchemy import text
from app import db
from app.models import Producto, Categoria, Usuario, Venta, DetalleVenta, VistaProductos

@app.route("/")
def inicio():
    """Panel de administración principal."""
    return render_template("index.html")

@app.route("/admin/productos")
def admin_productos():
    """Pestaña de Productos."""
    productos = Producto.query.order_by(Producto.id_producto).all()
    categorias = Categoria.query.order_by(Categoria.nombre).all()
    return render_template("admin/productos.html", productos=productos, categorias=categorias)
# ============================================================
# CRUD - PRODUCTOS
# ============================================================

@app.route("/admin/productos/nuevo", methods=["GET", "POST"])
def admin_producto_nuevo():
    """Crear nuevo producto."""
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        descripcion = request.form.get("descripcion", "").strip()
        precio = request.form.get("precio", "").strip()
        stock = request.form.get("stock", "").strip()
        talla = request.form.get("talla", "").strip()
        color = request.form.get("color", "").strip()
        id_categoria = request.form.get("id_categoria", "").strip()
        
        # Validaciones
        if not nombre:
            return "<div class='alert alert-danger'>El nombre es obligatorio.</div>", 400
        if not precio:
            return "<div class='alert alert-danger'>El precio es obligatorio.</div>", 400
        
        try:
            precio = float(precio)
            if precio < 0:
                return "<div class='alert alert-danger'>El precio no puede ser negativo.</div>", 400
        except ValueError:
            return "<div class='alert alert-danger'>El precio debe ser un número válido.</div>", 400
        
        try:
            stock = int(stock) if stock else 0
            if stock < 0:
                return "<div class='alert alert-danger'>El stock no puede ser negativo.</div>", 400
        except ValueError:
            return "<div class='alert alert-danger'>El stock debe ser un número entero.</div>", 400
        
        id_categoria = int(id_categoria) if id_categoria else None
        
        # Crear producto
        nuevo_producto = Producto(
            nombre=nombre,
            descripcion=descripcion or None,
            precio=precio,
            stock=stock,
            talla=talla or None,
            color=color or None,
            id_categoria=id_categoria
        )
        db.session.add(nuevo_producto)
        db.session.commit()
        
        # Recargar lista
        productos = Producto.query.order_by(Producto.id_producto).all()
        categorias = Categoria.query.order_by(Categoria.nombre).all()
        return render_template("admin/productos.html", productos=productos, categorias=categorias)
    
    # GET: Mostrar formulario
    categorias = Categoria.query.order_by(Categoria.nombre).all()
    return render_template("admin/producto_form.html", producto=None, categorias=categorias)


@app.route("/admin/productos/editar/<int:id>", methods=["GET", "POST"])
def admin_producto_editar(id):
    """Editar producto existente."""
    producto = Producto.query.get_or_404(id)
    
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        descripcion = request.form.get("descripcion", "").strip()
        precio = request.form.get("precio", "").strip()
        stock = request.form.get("stock", "").strip()
        talla = request.form.get("talla", "").strip()
        color = request.form.get("color", "").strip()
        id_categoria = request.form.get("id_categoria", "").strip()
        
        if not nombre:
            return "<div class='alert alert-danger'>El nombre es obligatorio.</div>", 400
        if not precio:
            return "<div class='alert alert-danger'>El precio es obligatorio.</div>", 400
        
        try:
            precio = float(precio)
            if precio < 0:
                return "<div class='alert alert-danger'>El precio no puede ser negativo.</div>", 400
        except ValueError:
            return "<div class='alert alert-danger'>El precio debe ser un número válido.</div>", 400
        
        try:
            stock = int(stock) if stock else 0
            if stock < 0:
                return "<div class='alert alert-danger'>El stock no puede ser negativo.</div>", 400
        except ValueError:
            return "<div class='alert alert-danger'>El stock debe ser un número entero.</div>", 400
        
        id_categoria = int(id_categoria) if id_categoria else None
        
        # Actualizar
        producto.nombre = nombre
        producto.descripcion = descripcion or None
        producto.precio = precio
        producto.stock = stock
        producto.talla = talla or None
        producto.color = color or None
        producto.id_categoria = id_categoria
        db.session.commit()
        
        productos = Producto.query.order_by(Producto.id_producto).all()
        categorias = Categoria.query.order_by(Categoria.nombre).all()
        return render_template("admin/productos.html", productos=productos, categorias=categorias)
    
    # GET: Mostrar formulario con datos
    categorias = Categoria.query.order_by(Categoria.nombre).all()
    return render_template("admin/producto_form.html", producto=producto, categorias=categorias)


@app.route("/admin/productos/eliminar/<int:id>", methods=["POST"])
def admin_producto_eliminar(id):
    """Eliminar producto."""
    producto = Producto.query.get_or_404(id)
    
    # Verificar si tiene detalles de venta asociados
    if producto.detalles:
        return f"""<div class='alert alert-danger'>
            No se puede eliminar: el producto "{producto.nombre}" está asociado a {len(producto.detalles)} venta(s).
        </div>""", 400
    
    db.session.delete(producto)
    db.session.commit()
    
    productos = Producto.query.order_by(Producto.id_producto).all()
    categorias = Categoria.query.order_by(Categoria.nombre).all()
    return render_template("admin/productos.html", productos=productos, categorias=categorias)

# ============================================================
# CRUD - CATEGORÍAS
# ============================================================
@app.route("/admin/categorias")
def admin_categorias():
    """Pestaña de Categorías."""
    categorias = Categoria.query.order_by(Categoria.nombre).all()
    return render_template("admin/categorias.html", categorias=categorias)

@app.route("/admin/categorias/nueva", methods=["GET", "POST"])
def admin_categoria_nueva():
    """Crear nueva categoría."""
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        descripcion = request.form.get("descripcion", "").strip()
        
        # Validación básica
        if not nombre:
            return "<div class='alert alert-danger'>El nombre es obligatorio.</div>", 400
        
        # Verificar si ya existe
        existente = Categoria.query.filter_by(nombre=nombre).first()
        if existente:
            return "<div class='alert alert-warning'>Ya existe una categoría con ese nombre.</div>", 400
        
        # Crear categoría
        nueva_categoria = Categoria(nombre=nombre, descripcion=descripcion)
        db.session.add(nueva_categoria)
        db.session.commit()
        
        # Recargar lista de categorías
        categorias = Categoria.query.order_by(Categoria.nombre).all()
        return render_template("admin/categorias.html", categorias=categorias)
    
    # GET: Mostrar formulario
    return render_template("admin/categoria_form.html", categoria=None)


@app.route("/admin/categorias/editar/<int:id>", methods=["GET", "POST"])
def admin_categoria_editar(id):
    """Editar categoría existente."""
    categoria = Categoria.query.get_or_404(id)
    
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        descripcion = request.form.get("descripcion", "").strip()
        
        if not nombre:
            return "<div class='alert alert-danger'>El nombre es obligatorio.</div>", 400
        
        # Verificar si ya existe otra con el mismo nombre
        existente = Categoria.query.filter(Categoria.nombre == nombre, Categoria.id_categoria != id).first()
        if existente:
            return "<div class='alert alert-warning'>Ya existe otra categoría con ese nombre.</div>", 400
        
        # Actualizar
        categoria.nombre = nombre
        categoria.descripcion = descripcion
        db.session.commit()
        
        categorias = Categoria.query.order_by(Categoria.nombre).all()
        return render_template("admin/categorias.html", categorias=categorias)
    
    # GET: Mostrar formulario con datos
    return render_template("admin/categoria_form.html", categoria=categoria)


@app.route("/admin/categorias/eliminar/<int:id>", methods=["POST"])
def admin_categoria_eliminar(id):
    """Eliminar categoría."""
    categoria = Categoria.query.get_or_404(id)
    
    # Verificar si tiene productos asociados
    if categoria.productos:
        return f"""<div class='alert alert-danger'>
            No se puede eliminar: la categoría "{categoria.nombre}" tiene {len(categoria.productos)} producto(s) asociado(s).
        </div>""", 400
    
    nombre = categoria.nombre
    db.session.delete(categoria)
    db.session.commit()
    
    categorias = Categoria.query.order_by(Categoria.nombre).all()
    return render_template("admin/categorias.html", categorias=categorias)

@app.route("/admin/usuarios")
def admin_usuarios():
    """Pestaña de Usuarios."""
    usuarios = Usuario.query.order_by(Usuario.nombre).all()
    return render_template("admin/usuarios.html", usuarios=usuarios)
# ============================================================
# CRUD - USUARIOS
# ============================================================

@app.route("/admin/usuarios/nuevo", methods=["GET", "POST"])
def admin_usuario_nuevo():
    """Crear nuevo usuario."""
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        apellido = request.form.get("apellido", "").strip()
        correo = request.form.get("correo", "").strip()
        telefono = request.form.get("telefono", "").strip()
        nombre_usuario = request.form.get("nombre_usuario", "").strip()
        contrasena = request.form.get("contrasena", "").strip()
        rol = request.form.get("rol", "").strip()
        
        # Validaciones
        errores = []
        if not nombre:
            errores.append("El nombre es obligatorio.")
        if not apellido:
            errores.append("El apellido es obligatorio.")
        if not correo:
            errores.append("El correo es obligatorio.")
        if not nombre_usuario:
            errores.append("El nombre de usuario es obligatorio.")
        if not contrasena:
            errores.append("La contraseña es obligatoria.")
        if not rol:
            errores.append("El rol es obligatorio.")
        
        # Validar correo único
        if correo and Usuario.query.filter_by(correo=correo).first():
            errores.append("El correo ya está registrado.")
        
        # Validar nombre_usuario único
        if nombre_usuario and Usuario.query.filter_by(nombre_usuario=nombre_usuario).first():
            errores.append("El nombre de usuario ya existe.")
        
        if errores:
            error_html = "<div class='alert alert-danger'><ul>"
            for error in errores:
                error_html += f"<li>{error}</li>"
            error_html += "</ul></div>"
            return error_html, 400
        
        # Crear usuario
        nuevo_usuario = Usuario(
            nombre=nombre,
            apellido=apellido,
            correo=correo,
            telefono=telefono or None,
            nombre_usuario=nombre_usuario,
            contrasena=contrasena,
            rol=rol
        )
        db.session.add(nuevo_usuario)
        db.session.commit()
        
        usuarios = Usuario.query.order_by(Usuario.nombre).all()
        return render_template("admin/usuarios.html", usuarios=usuarios)
    
    # GET: Mostrar formulario
    return render_template("admin/usuario_form.html", usuario=None)


@app.route("/admin/usuarios/editar/<int:id>", methods=["GET", "POST"])
def admin_usuario_editar(id):
    """Editar usuario existente."""
    usuario = Usuario.query.get_or_404(id)
    
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        apellido = request.form.get("apellido", "").strip()
        correo = request.form.get("correo", "").strip()
        telefono = request.form.get("telefono", "").strip()
        nombre_usuario = request.form.get("nombre_usuario", "").strip()
        contrasena = request.form.get("contrasena", "").strip()
        rol = request.form.get("rol", "").strip()
        
        errores = []
        if not nombre:
            errores.append("El nombre es obligatorio.")
        if not apellido:
            errores.append("El apellido es obligatorio.")
        if not correo:
            errores.append("El correo es obligatorio.")
        if not nombre_usuario:
            errores.append("El nombre de usuario es obligatorio.")
        if not rol:
            errores.append("El rol es obligatorio.")
        
        # Validar correo único (excepto el propio usuario)
        existente_correo = Usuario.query.filter(Usuario.correo == correo, Usuario.id_usuario != id).first()
        if existente_correo:
            errores.append("El correo ya está registrado por otro usuario.")
        
        # Validar nombre_usuario único
        existente_username = Usuario.query.filter(Usuario.nombre_usuario == nombre_usuario, Usuario.id_usuario != id).first()
        if existente_username:
            errores.append("El nombre de usuario ya existe.")
        
        if errores:
            error_html = "<div class='alert alert-danger'><ul>"
            for error in errores:
                error_html += f"<li>{error}</li>"
            error_html += "</ul></div>"
            return error_html, 400
        
        # Actualizar
        usuario.nombre = nombre
        usuario.apellido = apellido
        usuario.correo = correo
        usuario.telefono = telefono or None
        usuario.nombre_usuario = nombre_usuario
        usuario.rol = rol
        
        # Solo cambiar contraseña si se proporcionó una nueva
        if contrasena:
            usuario.contrasena = contrasena
        
        db.session.commit()
        
        usuarios = Usuario.query.order_by(Usuario.nombre).all()
        return render_template("admin/usuarios.html", usuarios=usuarios)
    
    # GET: Mostrar formulario con datos
    return render_template("admin/usuario_form.html", usuario=usuario)


@app.route("/admin/usuarios/eliminar/<int:id>", methods=["POST"])
def admin_usuario_eliminar(id):
    """Eliminar usuario."""
    usuario = Usuario.query.get_or_404(id)
    
    # Verificar si tiene ventas asociadas
    if usuario.ventas:
        return f"""<div class='alert alert-danger'>
            No se puede eliminar: el usuario "{usuario.nombre_usuario}" tiene {len(usuario.ventas)} venta(s) asociada(s).
        </div>""", 400
    
    db.session.delete(usuario)
    db.session.commit()
    
    usuarios = Usuario.query.order_by(Usuario.nombre).all()
    return render_template("admin/usuarios.html", usuarios=usuarios)


@app.route("/admin/ventas")
def admin_ventas():
    """Pestaña de Ventas."""
    ventas = Venta.query.order_by(Venta.fecha.desc()).all()
    return render_template("admin/ventas.html", ventas=ventas)

# ============================================================
# CRUD - VENTAS
# ============================================================

@app.route("/admin/ventas/nueva", methods=["GET", "POST"])
def admin_venta_nueva():
    """Crear nueva venta."""
    if request.method == "POST":
        fecha = request.form.get("fecha", "").strip()
        total = request.form.get("total", "").strip()
        metodo_pago = request.form.get("metodo_pago", "").strip()
        id_usuario = request.form.get("id_usuario", "").strip()
        
        # Validaciones
        if not fecha:
            return "<div class='alert alert-danger'>La fecha es obligatoria.</div>", 400
        if not total:
            return "<div class='alert alert-danger'>El total es obligatorio.</div>", 400
        
        try:
            total = float(total)
            if total < 0:
                return "<div class='alert alert-danger'>El total no puede ser negativo.</div>", 400
        except ValueError:
            return "<div class='alert alert-danger'>El total debe ser un número válido.</div>", 400
        
        id_usuario = int(id_usuario) if id_usuario else None
        
        # Crear venta
        nueva_venta = Venta(
            fecha=fecha,
            total=total,
            metodo_pago=metodo_pago or None,
            id_usuario=id_usuario
        )
        db.session.add(nueva_venta)
        db.session.commit()
        
        ventas = Venta.query.order_by(Venta.fecha.desc()).all()
        return render_template("admin/ventas.html", ventas=ventas)
    
    # GET: Mostrar formulario
    usuarios = Usuario.query.order_by(Usuario.nombre).all()
    return render_template("admin/venta_form.html", venta=None, usuarios=usuarios)


@app.route("/admin/ventas/editar/<int:id>", methods=["GET", "POST"])
def admin_venta_editar(id):
    """Editar venta existente."""
    venta = Venta.query.get_or_404(id)
    
    if request.method == "POST":
        fecha = request.form.get("fecha", "").strip()
        total = request.form.get("total", "").strip()
        metodo_pago = request.form.get("metodo_pago", "").strip()
        id_usuario = request.form.get("id_usuario", "").strip()
        
        if not fecha:
            return "<div class='alert alert-danger'>La fecha es obligatoria.</div>", 400
        if not total:
            return "<div class='alert alert-danger'>El total es obligatorio.</div>", 400
        
        try:
            total = float(total)
            if total < 0:
                return "<div class='alert alert-danger'>El total no puede ser negativo.</div>", 400
        except ValueError:
            return "<div class='alert alert-danger'>El total debe ser un número válido.</div>", 400
        
        id_usuario = int(id_usuario) if id_usuario else None
        
        # Actualizar
        venta.fecha = fecha
        venta.total = total
        venta.metodo_pago = metodo_pago or None
        venta.id_usuario = id_usuario
        db.session.commit()
        
        ventas = Venta.query.order_by(Venta.fecha.desc()).all()
        return render_template("admin/ventas.html", ventas=ventas)
    
    # GET: Mostrar formulario con datos
    usuarios = Usuario.query.order_by(Usuario.nombre).all()
    return render_template("admin/venta_form.html", venta=venta, usuarios=usuarios)


@app.route("/admin/ventas/eliminar/<int:id>", methods=["POST"])
def admin_venta_eliminar(id):
    """Eliminar venta."""
    venta = Venta.query.get_or_404(id)
    
    # Verificar si tiene detalles asociados
    if venta.detalles:
        return f"""<div class='alert alert-danger'>
            No se puede eliminar: la venta #{venta.id_venta} tiene {len(venta.detalles)} detalle(s) asociado(s).
        </div>""", 400
    
    db.session.delete(venta)
    db.session.commit()
    
    ventas = Venta.query.order_by(Venta.fecha.desc()).all()
    return render_template("admin/ventas.html", ventas=ventas)


@app.route("/admin/detalles")
def admin_detalles():
    """Pestaña de Detalles de Venta."""
    detalles = DetalleVenta.query.order_by(DetalleVenta.id_detalle).all()
    return render_template("admin/detalles.html", detalles=detalles)

@app.route("/admin/vista-productos")
def admin_vista_productos():
    """Pestaña de Vista de Productos (solo lectura)."""
    vista = VistaProductos.query.all()
    return render_template("admin/vista_productos.html", vista=vista)