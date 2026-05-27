from flask import Flask, request, render_template_string, redirect, url_for, session, jsonify, send_from_directory
from datetime import datetime
import os
import json

app = Flask(__name__)
app.secret_key = "clave_secreta_taller_frenos_2024"

# ==================== FUNCIÓN PARA DETECTAR IMÁGENES ====================
def obtener_imagen_existente(nombre_base):
    """Busca la imagen automáticamente en cualquier formato"""
    extensiones = ['.jpg', '.jpeg', '.png', '.webp', '.gif']
    for ext in extensiones:
        if os.path.exists(f'static/imagenes/{nombre_base}{ext}'):
            return f'{nombre_base}{ext}'
    return None

# ==================== ARCHIVOS TXT ====================
def cargar_usuarios():
    if not os.path.exists("usuarios.txt"):
        with open("usuarios.txt", "w") as f:
            f.write("admin,admin123\ncliente,cliente456\n")
    usuarios = {}
    with open("usuarios.txt", "r") as f:
        for linea in f:
            if linea.strip():
                user, pwd = linea.strip().split(",")
                usuarios[user] = pwd
    return usuarios

def cargar_productos():
    # Si NO existe productos.txt, lo creamos con los datos iniciales
    if not os.path.exists("productos.txt"):
        productos_iniciales = [
            "P001,Zapatas de Freno,TOYOTA,Zapatas,80,10,zapata_toyota",
            "P002,Pastillas Cerámicas,TOYOTA,Pastillas,120,15,pastilla_toyota",
            "P003,Bomba de Freno,TOYOTA,Bombas,200,8,bomba_toyota",
            "P004,Master de Freno,TOYOTA,Master,450,5,master_toyota",
            "P005,Manguera de Freno,TOYOTA,Mangueras,50,20,manguera",
            "P006,Zapatas de Freno,HYUNDAI,Zapatas,85,12,zapata_hyundai",
            "P007,Pastillas Cerámicas,HYUNDAI,Pastillas,125,10,pastilla_hyundai",
            "P008,Bomba de Freno,HYUNDAI,Bombas,210,7,bomba_hyundai",
            "P009,Master de Freno,HYUNDAI,Master,460,4,master_hyundai",
            "P010,Jebe de Caliper,TOYOTA,Jebes,35,25,jebe",
            "P011,KIT de Empaques,NISSAN,Kit,45,15,kit",
            "P012,Líquido de Frenos,UNIVERSAL,Liquido,25,30,liquido"
        ]
        with open("productos.txt", "w") as f:
            for p in productos_iniciales:
                f.write(p + "\n")
    
    productos = []
    with open("productos.txt", "r") as f:
        for linea in f:
            if linea.strip():
                datos = linea.strip().split(",")
                nombre_base = datos[6] if len(datos) > 6 else "default"
                imagen_real = obtener_imagen_existente(nombre_base)
                if imagen_real is None:
                    imagen_real = f"{nombre_base}.jpg"
                
                productos.append({
                    "codigo": datos[0],
                    "nombre": datos[1],
                    "marca": datos[2],
                    "tipo": datos[3],
                    "precio": float(datos[4]),
                    "stock": int(datos[5]),
                    "imagen": imagen_real
                })
    return productos

def guardar_productos(productos):
    with open("productos.txt", "w") as f:
        for p in productos:
            nombre_base = p['imagen'].split('.')[0] if '.' in p['imagen'] else p['imagen']
            f.write(f"{p['codigo']},{p['nombre']},{p['marca']},{p['tipo']},{p['precio']},{p['stock']},{nombre_base}\n")

def guardar_factura(factura):
    with open("facturas.txt", "a") as f:
        f.write(json.dumps(factura) + "\n")

def cargar_facturas():
    if not os.path.exists("facturas.txt"):
        return []
    facturas = []
    with open("facturas.txt", "r") as f:
        for linea in f:
            if linea.strip():
                facturas.append(json.loads(linea.strip()))
    return facturas

# Ruta para servir imágenes
@app.route('/imagenes/<path:filename>')
def servir_imagen(filename):
    return send_from_directory('static/imagenes', filename)

# ==================== HTML ====================
login_html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Taller de Frenos - Login</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .login-container {
            background: rgba(255,255,255,0.95);
            border-radius: 30px;
            padding: 40px;
            width: 400px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            text-align: center;
        }
        .logo { font-size: 60px; margin-bottom: 10px; }
        h1 { color: #1a1a2e; }
        input {
            width: 100%;
            padding: 15px;
            margin: 10px 0;
            border: 2px solid #e0e0e0;
            border-radius: 15px;
            font-size: 16px;
        }
        button {
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
            color: white;
            border: none;
            border-radius: 15px;
            font-size: 18px;
            cursor: pointer;
        }
        .mensaje { color: #ff6b6b; margin-top: 15px; }
        .demo {
            margin-top: 20px;
            padding: 15px;
            background: #f5f5f5;
            border-radius: 10px;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <div class="logo">🔧</div>
        <h1>Taller de Frenos</h1>
        <p style="color:#666; margin-bottom:30px;">Seguridad y calidad en cada frenada</p>
        <form method="POST">
            <input type="text" name="usuario" placeholder="👤 Usuario" required>
            <input type="password" name="password" placeholder="🔒 Contraseña" required>
            <button type="submit">🚗 Ingresar</button>
        </form>
        <div class="mensaje">{{ mensaje }}</div>
        <div class="demo">
            <strong>📝 Cuentas de prueba:</strong><br>
            admin / admin123 | cliente / cliente456
        </div>
    </div>
</body>
</html>
"""

index_html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Taller de Frenos - Productos</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f5f5f5; }
        
        .header {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: white;
            padding: 15px 30px;
            position: sticky;
            top: 0;
            z-index: 100;
        }
        .header-content {
            max-width: 1400px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .logo h1 { font-size: 24px; }
        .logo p { font-size: 12px; color: #ff6b6b; }
        .cart-icon {
            background: #ff6b6b;
            padding: 10px 20px;
            border-radius: 30px;
            cursor: pointer;
            display: inline-block;
            margin-right: 15px;
        }
        .cerrar-sesion {
            background: #dc3545;
            padding: 10px 20px;
            border-radius: 30px;
            text-decoration: none;
            color: white;
        }
        
        .carrusel {
            position: relative;
            background: #1a1a2e;
            text-align: center;
            overflow: hidden;
        }
        .slide {
            display: none;
            position: relative;
            animation: fadeIn 0.5s ease;
        }
        .slide.active {
            display: block;
        }
        .slide img {
            width: 100%;
            height: 450px;
            object-fit: cover;
        }
        .slide-caption {
            position: absolute;
            bottom: 20%;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(0,0,0,0.7);
            padding: 20px 40px;
            border-radius: 15px;
            text-align: center;
            color: white;
            min-width: 300px;
        }
        .slide-caption h2 {
            font-size: 32px;
            margin-bottom: 10px;
        }
        .slide-caption p {
            font-size: 18px;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: scale(1.05); }
            to { opacity: 1; transform: scale(1); }
        }
        .carrusel-btn {
            position: absolute;
            top: 50%;
            transform: translateY(-50%);
            background: rgba(0,0,0,0.5);
            color: white;
            border: none;
            padding: 15px 25px;
            cursor: pointer;
            border-radius: 50px;
            font-size: 20px;
            transition: all 0.3s;
            z-index: 10;
        }
        .carrusel-btn:hover {
            background: #ff6b6b;
        }
        .btn-prev {
            left: 20px;
        }
        .btn-next {
            right: 20px;
        }
        .indicators {
            position: absolute;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            gap: 10px;
            z-index: 10;
        }
        .indicator {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: rgba(255,255,255,0.5);
            cursor: pointer;
            transition: all 0.3s;
        }
        .indicator.active {
            background: #ff6b6b;
            width: 25px;
            border-radius: 10px;
        }
        
        .filtros {
            max-width: 1400px;
            margin: 30px auto;
            padding: 20px;
            background: white;
            border-radius: 15px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }
        .filtros select, .filtros input {
            padding: 10px 15px;
            border: 1px solid #ddd;
            border-radius: 25px;
            flex: 1;
            min-width: 120px;
        }
        .filtros button {
            background: #ff6b6b;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 25px;
            cursor: pointer;
        }
        
        .productos {
            max-width: 1400px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 25px;
            padding: 20px;
        }
        .producto-card {
            background: white;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
            transition: transform 0.3s;
        }
        .producto-card:hover { transform: translateY(-5px); }
        .producto-imagen {
            width: 100%;
            height: 200px;
            object-fit: cover;
        }
        .producto-info { padding: 15px; }
        .producto-nombre { font-size: 16px; font-weight: bold; }
        .producto-marca { color: #ff6b6b; font-size: 13px; margin: 5px 0; }
        .producto-precio { font-size: 24px; color: #1a1a2e; font-weight: bold; }
        .producto-stock { font-size: 12px; color: #666; margin: 8px 0; }
        .btn-agregar {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 10px;
            width: 100%;
            border-radius: 25px;
            cursor: pointer;
        }
        
        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.6);
            z-index: 1000;
        }
        .modal-content {
            background: white;
            width: 90%;
            max-width: 600px;
            margin: 50px auto;
            border-radius: 20px;
            padding: 20px;
            max-height: 80%;
            overflow-y: auto;
        }
        .modal-header {
            display: flex;
            justify-content: space-between;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #f0f0f0;
        }
        .cerrar { cursor: pointer; font-size: 24px; }
        .carrito-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px;
            border-bottom: 1px solid #eee;
        }
        .btn-eliminar {
            background: #dc3545;
            color: white;
            border: none;
            padding: 5px 10px;
            border-radius: 5px;
            cursor: pointer;
        }
        .facturar-btn {
            background: #28a745;
            color: white;
            border: none;
            padding: 12px;
            width: 100%;
            border-radius: 10px;
            font-size: 16px;
            margin-top: 15px;
            cursor: pointer;
        }
        
        @media (max-width: 768px) {
            .productos { grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); }
            .slide-caption h2 { font-size: 20px; }
            .slide-caption p { font-size: 12px; }
            .slide-caption { padding: 10px 20px; min-width: 200px; }
            .slide img { height: 300px; }
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="header-content">
            <div class="logo">
                <h1>🔧 Taller de Frenos</h1>
                <p>🚗 Seguridad y calidad en cada frenada</p>
            </div>
            <div>
                <span class="cart-icon" onclick="abrirCarrito()">🛒 Carrito (<span id="cartCount">0</span>)</span>
                <a href="/logout" class="cerrar-sesion">🚪 Salir</a>
            </div>
        </div>
    </div>

    <div class="carrusel" id="carrusel">
        <div class="slide active">
            <img src="/imagenes/carrusel1.jpg" 
                 onerror="this.src='https://images.unsplash.com/photo-1486262322331-3192fea0a0d3?w=1200'"
                 alt="Taller de Frenos">
            <div class="slide-caption">
                <h2> Frenos de Alta Calidad</h2>
                <p>Los mejores repuestos para tu vehículo</p>
            </div>
        </div>
        <div class="slide">
            <img src="/imagenes/carrusel2.jpg" 
                 onerror="this.src='https://images.unsplash.com/photo-1487754180451-c456f719a1fc?w=1200'"
                 alt="Pastillas de freno">
            <div class="slide-caption">
                <h2> Pastillas y Zapatas</h2>
                <p>Alta durabilidad y seguridad garantizada</p>
            </div>
        </div>
        <div class="slide">
            <img src="/imagenes/carrusel3.jpg" 
                 onerror="this.src='https://images.unsplash.com/photo-1625047509168-a7026f36de04?w=1200'"
                 alt="Servicio taller">
            <div class="slide-caption">
                <h2>️ Servicio Especializado</h2>
                <p>Mano de obra certificada con garantía</p>
            </div>
        </div>
        <div class="slide">
            <img src="/imagenes/carrusel4.jpg" 
                 onerror="this.src='https://images.unsplash.com/photo-1619642751034-765dfdf7c58e?w=1200'"
                 alt="Mejores precios">
            <div class="slide-caption">
                <h2>💰 Mejores Precios</h2>
                <p>Calidad y precio, el combo perfecto</p>
            </div>
        </div>
        
        <button class="carrusel-btn btn-prev" onclick="cambiarSlide(-1)">◀</button>
        <button class="carrusel-btn btn-next" onclick="cambiarSlide(1)">▶</button>
        
        <div class="indicators" id="indicators">
            <div class="indicator active" onclick="irSlide(0)"></div>
            <div class="indicator" onclick="irSlide(1)"></div>
            <div class="indicator" onclick="irSlide(2)"></div>
            <div class="indicator" onclick="irSlide(3)"></div>
        </div>
    </div>

    <div class="filtros">
        <select id="filtroMarca">
            <option value="">Todas las Marcas</option>
            <option>TOYOTA</option><option>HYUNDAI</option><option>KIA</option>
            <option>NISSAN</option><option>MAZDA</option><option>CHEVROLET</option>
            <option>JEEP</option><option>MITSUBISHI</option><option>UNIVERSAL</option>
        </select>
        <select id="filtroTipo">
            <option value="">Todos los Tipos</option>
            <option>Zapatas</option><option>Pastillas</option><option>Bombas</option>
            <option>Master</option><option>Mangueras</option><option>Jebes</option>
            <option>Kit</option><option>Liquido</option>
        </select>
        <input type="text" id="filtroBusqueda" placeholder="🔍 Buscar producto...">
        <button onclick="filtrarProductos()">Buscar</button>
        <button onclick="agregarManoObra()">🔧 Mano de Obra (S/150)</button>
    </div>

    <div class="productos" id="productosContainer">
        {% for p in productos %}
        <div class="producto-card" data-marca="{{ p.marca }}" data-tipo="{{ p.tipo }}" data-nombre="{{ p.nombre }}">
            <img class="producto-imagen" src="/imagenes/{{ p.imagen }}" 
                 onerror="this.src='https://via.placeholder.com/300x200/667eea/white?text={{ p.nombre | replace(' ', '+') }}'"
                 alt="{{ p.nombre }}">
            <div class="producto-info">
                <div class="producto-nombre">{{ p.nombre }}</div>
                <div class="producto-marca">🏷️ {{ p.marca }} | {{ p.tipo }}</div>
                <div class="producto-precio"> S/ {{ "%.2f"|format(p.precio) }}</div>
                <div class="producto-stock">📦 Stock: {{ p.stock }} unidades</div>
                <button class="btn-agregar" onclick="agregarAlCarrito('{{ p.codigo }}', '{{ p.nombre }}', {{ p.precio }})">
                    🛒 Agregar
                </button>
            </div>
        </div>
        {% endfor %}
    </div>

    <div id="modalCarrito" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <h2>🛒 Mi Carrito</h2>
                <span class="cerrar" onclick="cerrarCarrito()">&times;</span>
            </div>
            <div id="carritoItems"></div>
            <div id="carritoTotal" style="font-size: 22px; font-weight: bold; text-align: right; margin-top: 15px;"></div>
            <button class="facturar-btn" onclick="facturar()">💳 Facturar</button>
        </div>
    </div>

    <script>
        let carrito = [];
        let slideActual = 0;
        const slides = document.querySelectorAll('.slide');
        const indicators = document.querySelectorAll('.indicator');
        
        function actualizarIndicadores() {
            indicators.forEach((ind, i) => {
                if (i === slideActual) {
                    ind.classList.add('active');
                } else {
                    ind.classList.remove('active');
                }
            });
        }
        
        function cambiarSlide(direccion) {
            slides[slideActual].classList.remove('active');
            slideActual = (slideActual + direccion + slides.length) % slides.length;
            slides[slideActual].classList.add('active');
            actualizarIndicadores();
        }
        
        function irSlide(index) {
            slides[slideActual].classList.remove('active');
            slideActual = index;
            slides[slideActual].classList.add('active');
            actualizarIndicadores();
        }
        
        setInterval(() => cambiarSlide(1), 5000);
        
        function agregarAlCarrito(codigo, nombre, precio) {
            let existente = carrito.find(item => item.codigo === codigo);
            if (existente) existente.cantidad++;
            else carrito.push({codigo, nombre, precio, cantidad: 1});
            actualizarCarritoUI();
            mostrarNotificacion(`✅ ${nombre} agregado`);
        }
        
        function mostrarNotificacion(mensaje) {
            let notif = document.createElement('div');
            notif.textContent = mensaje;
            notif.style.cssText = `position: fixed; bottom: 20px; right: 20px; background: #28a745; color: white; padding: 10px 15px; border-radius: 8px; z-index: 2000; animation: fadeIn 0.3s;`;
            document.body.appendChild(notif);
            setTimeout(() => notif.remove(), 2000);
        }
        
        function agregarManoObra() {
            let existente = carrito.find(item => item.codigo === "MANO_OBRA");
            if (existente) existente.cantidad++;
            else carrito.push({codigo: "MANO_OBRA", nombre: "🔧 Mano de Obra", precio: 150, cantidad: 1});
            actualizarCarritoUI();
            mostrarNotificacion("🔧 Mano de obra agregada (S/150)");
        }
        
        function actualizarCarritoUI() {
            localStorage.setItem('carrito', JSON.stringify(carrito));
            let count = carrito.reduce((s, i) => s + i.cantidad, 0);
            document.getElementById('cartCount').innerText = count;
            
            let container = document.getElementById('carritoItems');
            if (container) {
                if (carrito.length === 0) {
                    container.innerHTML = '<div style="text-align:center;padding:30px;">🛒 Carrito vacío</div>';
                } else {
                    container.innerHTML = '';
                    carrito.forEach((item, i) => {
                        container.innerHTML += `
                            <div class="carrito-item">
                                <div style="flex:2;">
                                    <strong>${item.nombre}</strong><br>
                                    <small>S/${item.precio} c/u</small>
                                </div>
                                <div>
                                    <input type="number" value="${item.cantidad}" min="1" style="width:50px;" onchange="editarCantidad(${i}, this.value)">
                                    <button class="btn-eliminar" onclick="eliminarDelCarrito(${i})">🗑️</button>
                                </div>
                                <div><strong>S/${(item.precio * item.cantidad).toFixed(2)}</strong></div>
                            </div>
                        `;
                    });
                }
                let total = carrito.reduce((s, i) => s + (i.precio * i.cantidad), 0);
                document.getElementById('carritoTotal').innerHTML = `Total: S/${total.toFixed(2)}`;
            }
        }
        
        function editarCantidad(i, cant) {
            if (cant <= 0) eliminarDelCarrito(i);
            else carrito[i].cantidad = parseInt(cant);
            actualizarCarritoUI();
        }
        
        function eliminarDelCarrito(i) { carrito.splice(i, 1); actualizarCarritoUI(); }
        function abrirCarrito() { actualizarCarritoUI(); document.getElementById('modalCarrito').style.display = 'block'; }
        function cerrarCarrito() { document.getElementById('modalCarrito').style.display = 'none'; }
        
        function facturar() {
            if (carrito.length === 0) { alert("Carrito vacío"); return; }
            let nombre = prompt("Nombre completo:");
            if (!nombre) return;
            let ruc = prompt("RUC (opcional):", "Sin RUC");
            fetch('/facturar', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({carrito, nombre, ruc: ruc || "Sin RUC"})
            }).then(r => r.json()).then(data => {
                if (data.exito) {
                    alert(`✅ ¡FACTURA EMITIDA!\n\nN° Factura: ${data.numero}\nTotal: S/${data.total.toFixed(2)}`);
                    carrito = []; actualizarCarritoUI(); cerrarCarrito();
                } else { alert("Error al facturar"); }
            });
        }
        
        function filtrarProductos() {
            let marca = document.getElementById('filtroMarca').value;
            let tipo = document.getElementById('filtroTipo').value;
            let busqueda = document.getElementById('filtroBusqueda').value.toLowerCase();
            document.querySelectorAll('.producto-card').forEach(p => {
                let mostrar = true;
                if (marca && p.dataset.marca !== marca) mostrar = false;
                if (tipo && p.dataset.tipo !== tipo) mostrar = false;
                if (busqueda && !p.dataset.nombre.toLowerCase().includes(busqueda)) mostrar = false;
                p.style.display = mostrar ? 'block' : 'none';
            });
        }
        
        let saved = localStorage.getItem('carrito');
        if (saved) carrito = JSON.parse(saved);
        actualizarCarritoUI();
        
        window.onclick = function(e) {
            if (e.target === document.getElementById('modalCarrito')) cerrarCarrito();
        }
    </script>
</body>
</html>
"""
# ==================== RUTAS FLASK ====================
intentos = 0

@app.route("/", methods=["GET", "POST"])
def login():
    global intentos
    if intentos >= 3:
        return "<h1>Sistema Bloqueado</h1><a href='/'>Volver</a>"
    if request.method == "POST":
        usuario = request.form["usuario"]
        password = request.form["password"]
        usuarios = cargar_usuarios()
        if usuario in usuarios and usuarios[usuario] == password:
            session["usuario"] = usuario
            intentos = 0
            return redirect(url_for("index"))
        else:
            intentos += 1
            return render_template_string(login_html, mensaje="❌ Usuario/contraseña incorrectos")
    return render_template_string(login_html, mensaje="")

@app.route("/index")
def index():
    if "usuario" not in session:
        return redirect(url_for("login"))
    return render_template_string(index_html, productos=cargar_productos())

@app.route("/facturar", methods=["POST"])
def facturar():
    data = request.json
    carrito = data.get("carrito", [])
    nombre = data.get("nombre", "")
    ruc = data.get("ruc", "")
    facturas = cargar_facturas()
    num = len(facturas) + 1001
    total = sum(i["precio"] * i["cantidad"] for i in carrito)
    factura = {"numero": num, "fecha": str(datetime.now()), "nombre": nombre, "ruc": ruc, "productos": carrito, "total": total}
    guardar_factura(factura)
    
    productos = cargar_productos()
    for item in carrito:
        for p in productos:
            if p["codigo"] == item["codigo"]:
                p["stock"] -= item["cantidad"]
    guardar_productos(productos)
    return jsonify({"exito": True, "numero": num, "total": total})

@app.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)
