from flask import Flask, request, render_template_string, redirect, url_for, session, jsonify, send_from_directory
from datetime import datetime
import os
import json
import re

app = Flask(__name__)
app.secret_key = "clave_secreta_taller_frenos_2025"

# ==================== FUNCIÓN PARA DETECTAR IMÁGENES ====================
def obtener_imagen_existente(nombre_base):
    extensiones = ['.jpg', '.jpeg', '.png', '.webp', '.gif']
    for ext in extensiones:
        if os.path.exists(f'static/imagenes/{nombre_base}{ext}'):
            return f'{nombre_base}{ext}'
    return None

# ==================== ARCHIVOS TXT CON UTF-8 ====================
def cargar_usuarios():
    if not os.path.exists("usuarios.txt"):
        with open("usuarios.txt", "w", encoding='utf-8') as f:
            f.write("admin,admin123,Administrador,admin@taller.com,admin\n")
            f.write("cliente,cliente456,Cliente Demo,cliente@demo.com,cliente\n")
    
    usuarios = {}
    usuarios_detalle = {}
    try:
        with open("usuarios.txt", "r", encoding='utf-8', errors='ignore') as f:
            for linea in f:
                if linea.strip():
                    partes = linea.strip().split(",")
                    if len(partes) >= 2:
                        user = partes[0]
                        pwd = partes[1]
                        nombre = partes[2] if len(partes) > 2 else user
                        email = partes[3] if len(partes) > 3 else ""
<<<<<<< HEAD
                        rol = partes[4] if len(partes) > 4 else "cliente"
=======
                        rol = partes[4] if len(partes) > 4 else "cliente"  # Por defecto cliente
>>>>>>> 53cff441a9e73117cee6103c15537e2d332d69ca
                        usuarios[user] = pwd
                        usuarios_detalle[user] = {"nombre": nombre, "email": email, "rol": rol}
    except Exception as e:
        print(f"Error cargando usuarios: {e}")
        usuarios = {"admin": "admin123", "cliente": "cliente456"}
        usuarios_detalle = {
            "admin": {"nombre": "Administrador", "email": "", "rol": "admin"},
            "cliente": {"nombre": "Cliente Demo", "email": "", "rol": "cliente"}
        }
    
    return usuarios, usuarios_detalle

def guardar_usuario(usuario, password, nombre, email, rol="cliente"):
    if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
        return False, "Email inválido"
    if not usuario or len(usuario) < 3:
        return False, "Usuario debe tener al menos 3 caracteres"
    if not password or len(password) < 4:
        return False, "Contraseña debe tener al menos 4 caracteres"
    if not nombre:
        return False, "Nombre es requerido"
    
    try:
        with open("usuarios.txt", "a", encoding='utf-8') as f:
            f.write(f"{usuario},{password},{nombre},{email},{rol}\n")
        return True, "Registro exitoso"
    except Exception as e:
        return False, f"Error al registrar: {e}"

def cargar_productos():
    if not os.path.exists("productos.txt"):
        productos_iniciales = [
<<<<<<< HEAD
=======
            # Productos con marca (para categorías normales)
>>>>>>> 53cff441a9e73117cee6103c15537e2d332d69ca
            "P001,Zapatas de Freno Delanteras,TOYOTA,Zapatas,80,10,zapata_toyota",
            "P002,Pastillas Cerámicas Premium,TOYOTA,Pastillas,120,15,pastilla_toyota",
            "P003,Bomba de Freno,TOYOTA,Bombas,200,8,bomba_toyota",
            "P004,Master de Freno,TOYOTA,Master,450,5,master_toyota",
            "P005,Manguera de Freno,TOYOTA,Mangueras,50,20,manguera_toyota",
            "P006,Zapatas de Freno Traseras,HYUNDAI,Zapatas,85,12,zapata_hyundai",
            "P007,Pastillas Cerámicas,HYUNDAI,Pastillas,125,10,pastilla_hyundai",
            "P008,Bomba de Freno,HYUNDAI,Bombas,210,7,bomba_hyundai",
            "P009,Master de Freno,HYUNDAI,Master,460,4,master_hyundai",
            "P010,Pastillas Deportivas,NISSAN,Pastillas,135,10,pastilla_nissan",
            "P011,Zapatas Traseras,NISSAN,Zapatas,90,12,zapata_nissan",
            "P012,Bomba de Freno,NISSAN,Bombas,195,6,bomba_nissan",
<<<<<<< HEAD
=======
            
            # Productos genéricos para "OTROS REPUESTOS" (sin marca específica)
>>>>>>> 53cff441a9e73117cee6103c15537e2d332d69ca
            "R001,Manguera de Freno Genérica,UNIVERSAL,Manguera,45,25,manguera_generica",
            "R002,KIT de Empaques y Jebes,UNIVERSAL,Kit,55,20,kit_empaques",
            "R003,Pistón de Caliper,UNIVERSAL,Piston,65,15,piston_caliper",
            "R004,Caliper de Freno,UNIVERSAL,Caliper,180,10,caliper_freno",
            "R005,Pasador de Muñón,UNIVERSAL,Pasador,25,30,pasador_muñon",
            "R006,Tapa de Depósito de Frenos,UNIVERSAL,Tapa,35,25,tapa_deposito",
            "R007,Rodaje y Balinera,UNIVERSAL,Rodaje,40,20,rodaje_balinera",
            "R008,Retén de Bomba de Freno,UNIVERSAL,Reten,15,40,reten_bomba",
            "R009,Jebe de Caliper,UNIVERSAL,Jebe,28,35,jebe_caliper",
            "R010,Resorte de Zapatas,UNIVERSAL,Resorte,18,45,resorte_zapatas",
            "R011,Sensor de Desgaste de Pastillas,UNIVERSAL,Sensor,42,18,sensor_desgaste",
            "R012,Grasa para Frenos de Alta Temperatura,UNIVERSAL,Grasa,22,40,grasa_frenos",
<<<<<<< HEAD
=======
            
            # Líquido de frenos (va en su propia categoría, NO en Otros)
>>>>>>> 53cff441a9e73117cee6103c15537e2d332d69ca
            "L001,Líquido de Frenos DOT 4,UNIVERSAL,Liquido,25,50,liquido_dot4",
        ]
        with open("productos.txt", "w", encoding='utf-8') as f:
            for p in productos_iniciales:
                f.write(p + "\n")
    
    productos = []
    try:
        with open("productos.txt", "r", encoding='utf-8', errors='ignore') as f:
            for linea in f:
                if linea.strip():
                    datos = linea.strip().split(",")
                    if len(datos) < 6:
                        continue
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
                        "imagen": imagen_real,
                        "nombre_base": nombre_base
                    })
    except Exception as e:
        print(f"Error cargando productos: {e}")
        productos = []
    return productos

def guardar_productos(productos):
    try:
        with open("productos.txt", "w", encoding='utf-8') as f:
            for p in productos:
                f.write(f"{p['codigo']},{p['nombre']},{p['marca']},{p['tipo']},{p['precio']},{p['stock']},{p['nombre_base']}\n")
    except Exception as e:
        print(f"Error guardando productos: {e}")

def guardar_pedido(pedido):
    try:
        with open("pedidos.txt", "a", encoding='utf-8') as f:
            f.write(json.dumps(pedido) + "\n")
    except Exception as e:
        print(f"Error guardando pedido: {e}")

def cargar_pedidos():
    if not os.path.exists("pedidos.txt"):
        return []
    pedidos = []
    try:
        with open("pedidos.txt", "r", encoding='utf-8', errors='ignore') as f:
            for linea in f:
                if linea.strip():
                    pedidos.append(json.loads(linea.strip()))
    except Exception as e:
        print(f"Error cargando pedidos: {e}")
        pedidos = []
    return pedidos

<<<<<<< HEAD
def actualizar_estado_pedido(numero, nuevo_estado):
    pedidos = cargar_pedidos()
    for p in pedidos:
        if p.get('numero') == numero:
            p['estado'] = nuevo_estado
            break
    else:
        return False
    try:
        with open("pedidos.txt", "w", encoding='utf-8') as f:
            for p in pedidos:
                f.write(json.dumps(p) + "\n")
        return True
    except:
        return False

=======
>>>>>>> 53cff441a9e73117cee6103c15537e2d332d69ca
def es_admin():
    return session.get('rol') == 'admin'

# ==================== RUTAS DE ADMINISTRACIÓN ====================
@app.route('/admin/producto', methods=['POST'])
def admin_crear_producto():
    if not es_admin():
        return jsonify({"exito": False, "mensaje": "No autorizado"}), 403
    
    data = request.json
    codigo = data.get('codigo', '').strip()
    nombre = data.get('nombre', '').strip()
    marca = data.get('marca', '').strip()
    tipo = data.get('tipo', '').strip()
    precio = data.get('precio')
    stock = data.get('stock')
    nombre_base = data.get('nombre_base', '').strip()
    
<<<<<<< HEAD
=======
    # Validaciones básicas
>>>>>>> 53cff441a9e73117cee6103c15537e2d332d69ca
    if not codigo or not nombre or not tipo:
        return jsonify({"exito": False, "mensaje": "Campos obligatorios: código, nombre, tipo"})
    try:
        precio = float(precio)
        stock = int(stock)
    except:
        return jsonify({"exito": False, "mensaje": "Precio/stock inválidos"})
    
<<<<<<< HEAD
=======
    # Verificar código único
>>>>>>> 53cff441a9e73117cee6103c15537e2d332d69ca
    productos = cargar_productos()
    if any(p['codigo'] == codigo for p in productos):
        return jsonify({"exito": False, "mensaje": "El código ya existe"})
    
<<<<<<< HEAD
=======
    # Determinar imagen
>>>>>>> 53cff441a9e73117cee6103c15537e2d332d69ca
    if not nombre_base:
        nombre_base = codigo.lower()
    imagen_real = obtener_imagen_existente(nombre_base)
    if not imagen_real:
<<<<<<< HEAD
        imagen_real = f"{nombre_base}.jpg"
=======
        imagen_real = f"{nombre_base}.jpg"  # se usará el placeholder si no existe
>>>>>>> 53cff441a9e73117cee6103c15537e2d332d69ca
    
    nuevo = {
        "codigo": codigo,
        "nombre": nombre,
        "marca": marca,
        "tipo": tipo,
        "precio": precio,
        "stock": stock,
        "imagen": imagen_real,
        "nombre_base": nombre_base
    }
    
    with open("productos.txt", "a", encoding='utf-8') as f:
        f.write(f"{codigo},{nombre},{marca},{tipo},{precio},{stock},{nombre_base}\n")
    
    return jsonify({"exito": True, "producto": nuevo})

@app.route('/admin/producto/<codigo>', methods=['PUT'])
def admin_editar_producto(codigo):
    if not es_admin():
        return jsonify({"exito": False, "mensaje": "No autorizado"}), 403
    
    data = request.json
    productos = cargar_productos()
    idx = next((i for i, p in enumerate(productos) if p['codigo'] == codigo), None)
    if idx is None:
        return jsonify({"exito": False, "mensaje": "Producto no encontrado"}), 404
    
<<<<<<< HEAD
=======
    # Actualizar campos
>>>>>>> 53cff441a9e73117cee6103c15537e2d332d69ca
    for campo in ['nombre', 'marca', 'tipo', 'precio', 'stock', 'nombre_base']:
        if campo in data:
            if campo in ('precio', 'stock'):
                try:
                    productos[idx][campo] = float(data[campo]) if campo == 'precio' else int(data[campo])
                except:
                    return jsonify({"exito": False, "mensaje": f"Valor inválido para {campo}"})
            else:
                productos[idx][campo] = data[campo]
    
<<<<<<< HEAD
=======
    # Actualizar imagen si cambió nombre_base
>>>>>>> 53cff441a9e73117cee6103c15537e2d332d69ca
    nombre_base = productos[idx]['nombre_base']
    imagen_real = obtener_imagen_existente(nombre_base)
    productos[idx]['imagen'] = imagen_real if imagen_real else f"{nombre_base}.jpg"
    
    guardar_productos(productos)
    return jsonify({"exito": True, "producto": productos[idx]})

@app.route('/admin/producto/<codigo>', methods=['DELETE'])
def admin_eliminar_producto(codigo):
    if not es_admin():
        return jsonify({"exito": False, "mensaje": "No autorizado"}), 403
    
    productos = cargar_productos()
    productos = [p for p in productos if p['codigo'] != codigo]
    if len(productos) == len(cargar_productos()):
        return jsonify({"exito": False, "mensaje": "Producto no encontrado"}), 404
    
    guardar_productos(productos)
    return jsonify({"exito": True})

<<<<<<< HEAD
# ==================== DASHBOARD DEL ADMIN ====================
@app.route('/admin/dashboard')
def admin_dashboard():
    if not es_admin():
        return redirect(url_for('index'))
    
    usuarios, _ = cargar_usuarios()
    total_usuarios = len(usuarios)
    
    productos = cargar_productos()
    total_productos = len(productos)
    
    pedidos = cargar_pedidos()
    total_pedidos = len(pedidos)
    ingresos_brutos = sum(p.get('total', 0) for p in pedidos)
    ingresos_entregados = sum(p.get('total', 0) for p in pedidos if p.get('estado') == 'entregado')
    
    pedidos_recientes = sorted(pedidos, key=lambda x: x.get('fecha', ''), reverse=True)[:10]
    
    return render_template_string(dashboard_html, 
                                  total_usuarios=total_usuarios,
                                  total_productos=total_productos,
                                  total_pedidos=total_pedidos,
                                  ingresos_brutos=ingresos_brutos,
                                  ingresos_entregados=ingresos_entregados,
                                  pedidos=pedidos_recientes,
                                  session=session)

@app.route('/admin/orden/<int:num>', methods=['PUT'])
def admin_actualizar_estado(num):
    if not es_admin():
        return jsonify({"exito": False, "mensaje": "No autorizado"}), 403
    data = request.json
    nuevo_estado = data.get('estado')
    if nuevo_estado not in ['pendiente', 'enviado', 'entregado', 'cancelado']:
        return jsonify({"exito": False, "mensaje": "Estado inválido"}), 400
    if actualizar_estado_pedido(num, nuevo_estado):
        return jsonify({"exito": True})
    else:
        return jsonify({"exito": False, "mensaje": "Pedido no encontrado"}), 404

# ==================== RUTA QUIÉNES SOMOS ====================
@app.route("/quienes-somos")
def quienes_somos():
    return render_template_string(quienes_somos_html, session=session)

=======
>>>>>>> 53cff441a9e73117cee6103c15537e2d332d69ca
# ==================== RUTAS PÚBLICAS ====================
@app.route('/imagenes/<path:filename>')
def servir_imagen(filename):
    return send_from_directory('static/imagenes', filename)

@app.route("/")
def index():
    return render_template_string(landing_html, productos=cargar_productos(), session=session)

@app.route("/login_api", methods=["POST"])
def login_api():
    data = request.json
    usuario = data.get("usuario")
    password = data.get("password")
    usuarios, usuarios_detalle = cargar_usuarios()
    if usuario in usuarios and usuarios[usuario] == password:
        session["usuario"] = usuario
        session["nombre"] = usuarios_detalle.get(usuario, {}).get("nombre", usuario)
        session["rol"] = usuarios_detalle.get(usuario, {}).get("rol", "cliente")
        return jsonify({"exito": True, "nombre": session["nombre"], "rol": session["rol"]})
    return jsonify({"exito": False, "mensaje": "Usuario o contraseña incorrectos"})

@app.route("/registro_api", methods=["POST"])
def registro_api():
    data = request.json
    usuario = data.get("usuario")
    password = data.get("password")
    nombre = data.get("nombre")
    email = data.get("email")
    
    usuarios, _ = cargar_usuarios()
    if usuario in usuarios:
        return jsonify({"exito": False, "mensaje": "El usuario ya existe"})
    
    exito, mensaje = guardar_usuario(usuario, password, nombre, email)
    if exito:
        return jsonify({"exito": True})
    return jsonify({"exito": False, "mensaje": mensaje})

@app.route("/finalizar_pedido", methods=["POST"])
def finalizar_pedido():
    if "usuario" not in session:
        return jsonify({"exito": False, "mensaje": "No autorizado"})
    
    try:
        data = request.json
        carrito = data.get("carrito", [])
        pedidos = cargar_pedidos()
        num = len(pedidos) + 1001
        total = sum(i["precio"] * i["cantidad"] for i in carrito)
        
        pedido = {
            "numero": num,
            "fecha": str(datetime.now()),
            "usuario": session["usuario"],
            "productos": carrito,
            "total": total,
            "estado": "pendiente"
        }
        guardar_pedido(pedido)
        
        productos = cargar_productos()
        for item in carrito:
            for p in productos:
                if p["codigo"] == item["codigo"]:
                    p["stock"] -= item["cantidad"]
        guardar_productos(productos)
        
        return jsonify({"exito": True, "numero": num, "total": total})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"exito": False, "error": str(e)})

@app.route("/logout")
def logout():
    session.pop("usuario", None)
    session.pop("nombre", None)
    session.pop("rol", None)
    return redirect(url_for("index"))

<<<<<<< HEAD
# ==================== HTML QUIÉNES SOMOS ====================
quienes_somos_html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quiénes Somos - FrenosPro</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body { background: #f0f2f5; font-family: 'Segoe UI', sans-serif; }
        .header {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: white;
            padding: 15px 30px;
            position: sticky;
            top: 0;
            z-index: 100;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .logo h1 { font-size: 42px; color: white; }
        .logo h1 i { color: #ff3333; margin-right: 10px; }
        .logo p { font-size: 23px; color: #ff6b6b; }
        .btn-logout {
            background: #dc3545;
            padding: 8px 15px;
            border-radius: 30px;
            text-decoration: none;
            color: white;
            font-size: 14px;
        }
        .btn-logout:hover { background: #c82333; color: white; }
        .historia-container {
            background: white;
            border-radius: 20px;
            padding: 40px;
            margin: 40px auto;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        .historia-titulo {
            color: #1a1a2e;
            font-size: 2.5rem;
            border-left: 5px solid #ff6b6b;
            padding-left: 20px;
            margin-bottom: 30px;
        }
        .historia-texto {
            font-size: 1.1rem;
            line-height: 1.8;
            color: #444;
            text-align: justify;
        }
        .mision-vision {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 20px;
            padding: 30px;
            margin-top: 30px;
            color: white;
        }
        .mision-vision h3 { margin-bottom: 20px; }
        .valores {
            margin-top: 40px;
        }
        .valor-card {
            background: #f8f9fa;
            border-radius: 15px;
            padding: 20px;
            text-align: center;
            transition: transform 0.3s;
            height: 100%;
        }
        .valor-card:hover { transform: translateY(-5px); }
        .valor-icon { font-size: 40px; color: #ff6b6b; margin-bottom: 15px; }
        .footer {
            background: #1a1a2e;
            color: white;
            text-align: center;
            padding: 30px;
            margin-top: 50px;
        }
        .btn-volver {
            background: #ff6b6b;
            color: white;
            border-radius: 30px;
            padding: 10px 25px;
            text-decoration: none;
            transition: 0.3s;
        }
        .btn-volver:hover { background: #ff5252; color: white; }
        .historia-img {
            border-radius: 20px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
            max-width: 100%;
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="container-fluid">
            <div class="d-flex justify-content-between align-items-center flex-wrap">
                <div class="logo">
                    <h1><i class="fas fa-car"></i> FrenosMaximo</h1>
                    <p>Seguridad y calidad en cada frenada</p>
                </div>
                <div class="d-flex gap-3 align-items-center">
                    <a href="/" class="btn btn-outline-light"><i class="fas fa-home"></i> Inicio</a>
                    {% if session.usuario %}
                    <div class="d-flex gap-2 align-items-center">
                        <span class="text-warning"><i class="fas fa-user"></i> {{ session.nombre }}</span>
                        <a href="/logout" class="btn-logout"><i class="fas fa-sign-out-alt"></i> Salir</a>
                    </div>
                    {% else %}
                    <button class="btn btn-outline-light" onclick="window.location.href='/'">Iniciar Sesión</button>
                    {% endif %}
                </div>
            </div>
        </div>
    </div>

    <div class="container">
        <div class="historia-container">
            <div class="row">
                <div class="col-md-6">
                    <h2 class="historia-titulo"><i class="fas fa-history"></i> Nuestra Historia</h2>
                    <div class="historia-texto">
                        <p><strong>FrenosMaximo</strong> nació en 2010 en el corazón de la ciudad, con un sueño claro: <strong>ofrecer repuestos de frenos de la más alta calidad</strong> a precios accesibles.</p>
                        <p>Todo comenzó en un pequeño taller de 30 metros cuadrados, fundado por <strong>Carlos Rodríguez</strong>, un apasionado mecánico con más de 20 años de experiencia. Lo que empezó como un negocio familiar se convirtió rápidamente en un referente en el rubro gracias a la <strong>confianza y honestidad</strong> que nos caracteriza.</p>
                        <p>Hoy, después de más de una década, <strong>FrenosMaximo</strong> es una empresa líder en venta de repuestos de frenos, atendiendo a <strong>más de 10,000 clientes satisfechos</strong> en todo el país. Contamos con un catálogo de más de 500 productos y un equipo humano dedicado a brindar la mejor asesoría.</p>
                        <p><strong>Nuestro compromiso</strong>: Que cada vehículo que circula con nuestros repuestos tenga una frenada segura y confiable. ¡Tu vida y la de tu familia son lo más importante!</p>
                    </div>
                </div>
                <div class="col-md-6 text-center">
                    <img src="/imagenes/historia.jpg" class="historia-img img-fluid" 
                         onerror="this.src='https://images.unsplash.com/photo-1487754180451-c456f719a1fc?w=600'"
                         alt="Nuestro taller">
                    <p class="text-muted mt-2"><i class="fas fa-map-marker-alt"></i> Nuestro primer taller - 2010</p>
                </div>
            </div>

            <div class="mision-vision row mt-5">
                <div class="col-md-6">
                    <h3><i class="fas fa-bullseye"></i> Misión</h3>
                    <p>Proveer repuestos de frenos de la más alta calidad, garantizando seguridad y confianza a nuestros clientes, con precios justos y atención personalizada.</p>
                </div>
                <div class="col-md-6">
                    <h3><i class="fas fa-eye"></i> Visión</h3>
                    <p>Ser la empresa líder en el mercado de repuestos de frenos, reconocida por nuestra innovación, calidad y compromiso con la seguridad vial.</p>
                </div>
            </div>

            <div class="valores">
                <h3 class="text-center mb-4"><i class="fas fa-gem"></i> Nuestros Valores</h3>
                <div class="row">
                    <div class="col-md-3 col-sm-6 mb-3">
                        <div class="valor-card">
                            <div class="valor-icon"><i class="fas fa-shield-alt"></i></div>
                            <h5>Seguridad</h5>
                            <small>Prioridad absoluta en cada producto</small>
                        </div>
                    </div>
                    <div class="col-md-3 col-sm-6 mb-3">
                        <div class="valor-card">
                            <div class="valor-icon"><i class="fas fa-handshake"></i></div>
                            <h5>Honestidad</h5>
                            <small>Transparencia con nuestros clientes</small>
                        </div>
                    </div>
                    <div class="col-md-3 col-sm-6 mb-3">
                        <div class="valor-card">
                            <div class="valor-icon"><i class="fas fa-chart-line"></i></div>
                            <h5>Mejora Continua</h5>
                            <small>Innovación constante</small>
                        </div>
                    </div>
                    <div class="col-md-3 col-sm-6 mb-3">
                        <div class="valor-card">
                            <div class="valor-icon"><i class="fas fa-users"></i></div>
                            <h5>Trabajo en Equipo</h5>
                            <small>Compromiso y colaboración</small>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="text-center mt-5">
                <a href="/" class="btn-volver"><i class="fas fa-arrow-left"></i> Volver a la tienda</a>
            </div>
        </div>
    </div>

    <div class="footer">
        <p><i class="fas fa-car"></i> FrenosPro - Tu seguridad es nuestra prioridad</p>
        <p>© 2025 - Todos los derechos reservados</p>
    </div>
</body>
</html>
"""

# ==================== HTML DEL DASHBOARD ====================
dashboard_html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Panel de Control - FrenosPro</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body { background: #f0f2f5; font-family: 'Segoe UI', sans-serif; }
        .sidebar { background: #1a1a2e; min-height: 100vh; color: white; }
        .sidebar a { color: #ccc; text-decoration: none; padding: 12px 20px; display: block; transition: 0.3s; }
        .sidebar a:hover { background: #ff6b6b; color: white; }
        .sidebar i { margin-right: 10px; }
        .main-content { padding: 20px; }
        .stat-card { background: white; border-radius: 15px; padding: 20px; margin-bottom: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .stat-number { font-size: 2.5rem; font-weight: bold; color: #ff6b6b; }
        .table-orders { background: white; border-radius: 15px; overflow: hidden; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .status-badge { padding: 5px 10px; border-radius: 20px; font-size: 12px; font-weight: bold; }
        .status-pendiente { background: #ffc107; color: #000; }
        .status-enviado { background: #17a2b8; color: #fff; }
        .status-entregado { background: #28a745; color: #fff; }
        .status-cancelado { background: #dc3545; color: #fff; }
        .btn-sm { padding: 4px 8px; font-size: 12px; }
    </style>
</head>
<body>
    <div class="container-fluid">
        <div class="row">
            <div class="col-md-2 p-0 sidebar">
                <div class="p-4">
                    <h4><i class="fas fa-chart-line"></i> FrenosPro</h4>
                    <p>Panel Admin</p>
                </div>
                <a href="/"><i class="fas fa-home"></i> Inicio</a>
                <a href="/admin/dashboard" class="active bg-primary"><i class="fas fa-tachometer-alt"></i> Dashboard</a>
                <a href="/quienes-somos"><i class="fas fa-info-circle"></i> Quiénes Somos</a>
                <a href="/logout"><i class="fas fa-sign-out-alt"></i> Cerrar sesión</a>
            </div>
            
            <div class="col-md-10 main-content">
                <div class="d-flex justify-content-between align-items-center mb-4">
                    <h2><i class="fas fa-tachometer-alt"></i> Panel de Control</h2>
                    <span class="text-muted">Bienvenido, {{ session.nombre }}</span>
                </div>
                
                <div class="row">
                    <div class="col-md-3">
                        <div class="stat-card text-center">
                            <i class="fas fa-users fa-2x text-primary"></i>
                            <div class="stat-number">{{ total_usuarios }}</div>
                            <div>Usuarios Registrados</div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="stat-card text-center">
                            <i class="fas fa-boxes fa-2x text-success"></i>
                            <div class="stat-number">{{ total_productos }}</div>
                            <div>Productos</div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="stat-card text-center">
                            <i class="fas fa-shopping-cart fa-2x text-warning"></i>
                            <div class="stat-number">{{ total_pedidos }}</div>
                            <div>Pedidos Totales</div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="stat-card text-center">
                            <i class="fas fa-dollar-sign fa-2x text-danger"></i>
                            <div class="stat-number">S/ {{ "%.2f"|format(ingresos_brutos) }}</div>
                            <div>Ingresos Brutos</div>
                            <small class="text-muted">Entregados: S/ {{ "%.2f"|format(ingresos_entregados) }}</small>
                        </div>
                    </div>
                </div>
                
                <div class="card mt-4">
                    <div class="card-header bg-white">
                        <h5><i class="fas fa-clock"></i> Últimos Pedidos</h5>
                    </div>
                    <div class="card-body p-0">
                        <div class="table-responsive">
                            <table class="table table-hover mb-0">
                                <thead class="table-light">
                                    <tr><th>N° Pedido</th><th>Fecha</th><th>Usuario</th><th>Total</th><th>Estado</th><th>Acciones</th></tr>
                                </thead>
                                <tbody>
                                    {% for p in pedidos %}
                                    <tr id="pedido-{{ p.numero }}">
                                        <td>{{ p.numero }}</td><td>{{ p.fecha[:19] }}</td><td>{{ p.usuario }}</td><td>S/ {{ "%.2f"|format(p.total) }}</td>
                                        <td><span class="status-badge status-{{ p.estado }}">{{ p.estado|capitalize }}</span></td>
                                        <td><select class="form-select form-select-sm w-auto d-inline-block estado-select" data-numero="{{ p.numero }}">
                                                <option value="pendiente" {% if p.estado == 'pendiente' %}selected{% endif %}>Pendiente</option>
                                                <option value="enviado" {% if p.estado == 'enviado' %}selected{% endif %}>Enviado</option>
                                                <option value="entregado" {% if p.estado == 'entregado' %}selected{% endif %}>Entregado</option>
                                                <option value="cancelado" {% if p.estado == 'cancelado' %}selected{% endif %}>Cancelado</option>
                                            </select>
                                        </td>
                                    </tr>
                                    {% else %}
                                    <tr><td colspan="6" class="text-center">No hay pedidos aún</td></tr>
                                    {% endfor %}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        document.querySelectorAll('.estado-select').forEach(select => {
            select.addEventListener('change', function() {
                const numero = this.dataset.numero;
                const nuevoEstado = this.value;
                fetch(`/admin/orden/${numero}`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ estado: nuevoEstado })
                })
                .then(res => res.json())
                .then(data => {
                    if (data.exito) {
                        const row = document.getElementById(`pedido-${numero}`);
                        const badgeSpan = row.querySelector('.status-badge');
                        badgeSpan.className = `status-badge status-${nuevoEstado}`;
                        badgeSpan.textContent = nuevoEstado.charAt(0).toUpperCase() + nuevoEstado.slice(1);
                        alert('✅ Estado actualizado correctamente');
                    } else {
                        alert('❌ Error al actualizar: ' + data.mensaje);
                    }
                })
                .catch(err => alert('Error de red'));
            });
        });
    </script>
</body>
</html>
"""

# ==================== HTML COMPLETO (con admin y link a Quiénes Somos) ====================
=======
# ==================== HTML COMPLETO (con admin) ====================
>>>>>>> 53cff441a9e73117cee6103c15537e2d332d69ca
landing_html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FrenosPro - Tu taller de confianza</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f0f2f5;
        }
        
        .header {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: white;
            padding: 15px 30px;
            position: sticky;
            top: 0;
            z-index: 100;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
<<<<<<< HEAD
        .logo h1 { 
            font-size: 42px; 
            color: white;
        }
        .logo h1 i {
            color: #ff3333;
            margin-right: 10px;
        }
        .logo p { 
            font-size: 23px; 
            color: #ff6b6b;
        }
=======
     .logo h1 { 
    font-size: 42px; 
    color: white;
}
.logo h1 i {
    color: #ff3333;
    margin-right: 10px;
}
.logo p { 
    font-size: 23px; 
    color: #ff6b6b;
}
>>>>>>> 53cff441a9e73117cee6103c15537e2d332d69ca
        
        .cart-icon {
            background: #ff6b6b;
            padding: 8px 15px;
            border-radius: 30px;
            cursor: pointer;
            display: inline-block;
            transition: background 0.3s;
        }
        
        .cart-icon:hover { background: #ff5252; }
        
        .btn-logout {
            background: #dc3545;
            padding: 8px 15px;
            border-radius: 30px;
            text-decoration: none;
            color: white;
            font-size: 14px;
        }
        
        .btn-logout:hover { background: #c82333; color: white; }
        
<<<<<<< HEAD
        .btn-quienes {
            background: #17a2b8;
            padding: 8px 15px;
            border-radius: 30px;
            text-decoration: none;
            color: white;
            font-size: 14px;
        }
        
        .btn-quienes:hover { background: #138496; color: white; }
        
=======
>>>>>>> 53cff441a9e73117cee6103c15537e2d332d69ca
        .buscador-container {
            background: white;
            border-radius: 50px;
            padding: 5px 15px;
            display: flex;
            align-items: center;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        
        .buscador-container input {
            border: none;
            padding: 10px;
            width: 250px;
            outline: none;
            border-radius: 50px;
        }
        
        .buscador-container button {
            background: #ff6b6b;
            border: none;
            padding: 8px 15px;
            border-radius: 50px;
            color: white;
            cursor: pointer;
            transition: background 0.3s;
        }
        
        .buscador-container button:hover { background: #ff5252; }
        
        .sidebar {
            background: white;
            border-radius: 15px;
            padding: 20px;
            position: sticky;
            top: 90px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        }
        
        .sidebar-title {
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #ff6b6b;
        }
        
        .sidebar-categoria {
            display: block;
            padding: 12px 15px;
            margin: 5px 0;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.3s;
            text-decoration: none;
            color: #333;
            font-weight: 500;
        }
        
        .sidebar-categoria:hover {
            background: #ff6b6b;
            color: white;
            transform: translateX(5px);
        }
        
        .sidebar-categoria i { margin-right: 10px; }
        
        .sidebar-categoria.active {
            background: #ff6b6b;
            color: white;
        }
        
        .contenido-principal {
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
            min-height: 500px;
        }
        
        .categoria-header {
            text-align: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 3px solid #ff6b6b;
        }
        
        .categoria-header h1 {
            font-size: 42px;
            color: #1a1a2e;
            margin-bottom: 10px;
        }
        
        .categoria-header p {
            font-size: 18px;
            color: #ff6b6b;
        }
        
        .productos-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 25px;
        }
        
        .producto-card {
            background: white;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
            transition: transform 0.3s;
            border: 1px solid #eee;
        }
        
        .producto-card:hover { transform: translateY(-5px); }
        
        .producto-imagen {
            width: 100%;
            height: 180px;
            object-fit: cover;
            background: #f5f5f5;
        }
        
        .producto-info { padding: 15px; }
        .producto-nombre { font-size: 16px; font-weight: bold; margin-bottom: 5px; }
        .producto-marca { color: #ff6b6b; font-size: 13px; margin-bottom: 5px; }
        .producto-precio { font-size: 24px; color: #1a1a2e; font-weight: bold; }
        .producto-stock { font-size: 12px; color: #666; margin: 8px 0; }
        
        .btn-comprar {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 10px;
            width: 100%;
            border-radius: 25px;
            cursor: pointer;
            transition: opacity 0.3s;
        }
        
        .btn-comprar:hover { opacity: 0.9; }
        
        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.6);
            z-index: 1000;
            justify-content: center;
            align-items: center;
        }
        
        .modal-content {
            background: white;
            width: 90%;
            max-width: 500px;
            border-radius: 20px;
            padding: 30px;
            position: relative;
        }
        
        .carrito-modal .modal-content {
            max-width: 600px;
            max-height: 80vh;
            overflow-y: auto;
        }
        
        .close-modal {
            cursor: pointer;
            font-size: 28px;
            color: #999;
            float: right;
        }
        
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
        
        .footer {
            background: #1a1a2e;
            color: white;
            text-align: center;
            padding: 30px;
            margin-top: 50px;
        }
        
        .carousel-item img {
            height: 400px;
            object-fit: cover;
        }
        
        @media (max-width: 768px) {
            .carousel-item img { height: 250px; }
            .sidebar { position: relative; top: 0; margin-bottom: 20px; }
            .producto-imagen { height: 150px; }
            .categoria-header h1 { font-size: 28px; }
            .productos-grid { grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); }
            .buscador-container input { width: 150px; }
        }
        
        .badge-stock {
            position: absolute;
            top: 10px;
            right: 10px;
            background: rgba(0,0,0,0.7);
            color: white;
            padding: 5px 10px;
            border-radius: 20px;
            font-size: 12px;
        }
        
        .marca-item {
            background: white;
            border-radius: 10px;
            padding: 8px 12px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            margin: 5px;
            display: inline-block;
            font-size: 14px;
        }
        
        .marca-item:hover {
            background: #ff6b6b;
            color: white;
            transform: scale(1.05);
        }
        
        .marca-item.active {
            background: #ff6b6b;
            color: white;
        }
        
        .sin-productos {
            text-align: center;
            padding: 60px;
            color: #999;
        }
        
        .filtro-marcas-container {
            margin-top: 20px;
            padding-top: 15px;
            border-top: 1px solid #eee;
            transition: all 0.3s ease;
        }
        
        .filtro-marcas-container.oculto {
            opacity: 0.5;
            pointer-events: none;
        }
        
        .resultado-busqueda {
            background: #fff3cd;
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 20px;
            text-align: center;
            display: none;
        }
        
        .info-otros {
            background: #e7f3ff;
            padding: 10px;
            border-radius: 10px;
            margin-top: 15px;
            font-size: 12px;
            text-align: center;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .producto-card {
            animation: fadeIn 0.5s ease;
        }

        .btn-sm {
            padding: 5px 10px;
            font-size: 0.8rem;
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="container-fluid">
            <div class="d-flex justify-content-between align-items-center flex-wrap">
                <div class="logo">
                    <h1><i class="fas fa-car"></i> FrenosMaximo</h1>
                    <p>Seguridad y calidad en cada frenada</p>
                </div>
                <div class="d-flex gap-3 align-items-center">
                    <div class="buscador-container">
                        <input type="text" id="buscadorInput" placeholder="Buscar producto..." onkeyup="buscarProducto(event)">
                        <button onclick="realizarBusqueda()"><i class="fas fa-search"></i></button>
                    </div>
<<<<<<< HEAD
                    <a href="/quienes-somos" class="btn-quienes">
                        <i class="fas fa-info-circle"></i> ¿Quiénes somos?
                    </a>
=======
>>>>>>> 53cff441a9e73117cee6103c15537e2d332d69ca
                    <div class="cart-icon" onclick="abrirCarrito()">
                        <i class="fas fa-shopping-cart"></i> <span id="cartCount">0</span>
                    </div>
                    {% if session.usuario %}
                    <div class="d-flex gap-2 align-items-center">
                        <span class="text-warning"><i class="fas fa-user"></i> {{ session.nombre }}</span>
                        <a href="/logout" class="btn-logout"><i class="fas fa-sign-out-alt"></i> Salir</a>
                    </div>
                    {% if session.get('rol') == 'admin' %}
                    <button class="btn btn-success" onclick="abrirModalAgregar()">
                        <i class="fas fa-plus-circle"></i> Agregar Producto
                    </button>
<<<<<<< HEAD
                    <a href="/admin/dashboard" class="btn btn-info">
                        <i class="fas fa-chart-line"></i> Dashboard
                    </a>
=======
>>>>>>> 53cff441a9e73117cee6103c15537e2d332d69ca
                    {% endif %}
                    {% else %}
                    <button class="btn btn-outline-light" onclick="abrirModalRegistro()">
                        <i class="fas fa-user-plus"></i> Registrarse
                    </button>
                    {% endif %}
                </div>
            </div>
        </div>
    </div>
    
    <div id="mainCarousel" class="carousel slide" data-bs-ride="carousel">
        <div class="carousel-indicators">
            <button type="button" data-bs-target="#mainCarousel" data-bs-slide-to="0" class="active"></button>
            <button type="button" data-bs-target="#mainCarousel" data-bs-slide-to="1"></button>
            <button type="button" data-bs-target="#mainCarousel" data-bs-slide-to="2"></button>
            <button type="button" data-bs-target="#mainCarousel" data-bs-slide-to="3"></button>
        </div>
        <div class="carousel-inner">
            <div class="carousel-item active">
                <img src="/imagenes/carrusel1.jpg" class="d-block w-100" 
                     onerror="this.src='https://images.unsplash.com/photo-1486262322331-3192fea0a0d3?w=1200'"
                     alt="Taller de Frenos">
                <div class="carousel-caption d-none d-md-block bg-dark bg-opacity-50 rounded p-3">
                    <h2><i class="fas fa-car"></i> Frenos de Alta Calidad</h2>
                    <p>Los mejores repuestos para tu vehículo</p>
                </div>
            </div>
            <div class="carousel-item">
                <img src="/imagenes/carrusel2.jpg" class="d-block w-100"
                     onerror="this.src='https://images.unsplash.com/photo-1487754180451-c456f719a1fc?w=1200'"
                     alt="Pastillas de freno">
                <div class="carousel-caption d-none d-md-block bg-dark bg-opacity-50 rounded p-3">
                    <h2><i class="fas fa-brake-warning"></i> Pastillas y Zapatas</h2>
                    <p>Alta durabilidad y seguridad garantizada</p>
                </div>
            </div>
            <div class="carousel-item">
                <img src="/imagenes/carrusel3.jpg" class="d-block w-100"
                     onerror="this.src='https://images.unsplash.com/photo-1625047509168-a7026f36de04?w=1200'"
                     alt="Servicio taller">
                <div class="carousel-caption d-none d-md-block bg-dark bg-opacity-50 rounded p-3">
                    <h2><i class="fas fa-wrench"></i> Servicio Especializado</h2>
                    <p>Mano de obra certificada con garantía</p>
                </div>
            </div>
            <div class="carousel-item">
                <img src="/imagenes/carrusel4.jpg" class="d-block w-100"
                     onerror="this.src='https://images.unsplash.com/photo-1619642751034-765dfdf7c58e?w=1200'"
                     alt="Mejores precios">
                <div class="carousel-caption d-none d-md-block bg-dark bg-opacity-50 rounded p-3">
                    <h2><i class="fas fa-tag"></i> Mejores Precios</h2>
                    <p>Calidad y precio, el combo perfecto</p>
                </div>
            </div>
        </div>
        <button class="carousel-control-prev" type="button" data-bs-target="#mainCarousel" data-bs-slide="prev">
            <span class="carousel-control-prev-icon"></span>
        </button>
        <button class="carousel-control-next" type="button" data-bs-target="#mainCarousel" data-bs-slide="next">
            <span class="carousel-control-next-icon"></span>
        </button>
    </div>
    
    <div class="container my-4">
        <div class="row">
            <div class="col-md-3">
                <div class="sidebar">
                    <div class="sidebar-title">
                        <i class="fas fa-filter"></i> Categorías
                    </div>
                    <div class="sidebar-categoria" data-categoria="Pastillas" onclick="cambiarCategoria('Pastillas')">
                        <i class="fas fa-brake-warning"></i> Pastillas de Freno
                    </div>
                    <div class="sidebar-categoria" data-categoria="Zapatas" onclick="cambiarCategoria('Zapatas')">
                        <i class="fas fa-car-side"></i> Zapatas de Freno
                    </div>
                    <div class="sidebar-categoria" data-categoria="Bombas" onclick="cambiarCategoria('Bombas')">
                        <i class="fas fa-oil-can"></i> Bombas de Freno
                    </div>
                    <div class="sidebar-categoria" data-categoria="Master" onclick="cambiarCategoria('Master')">
                        <i class="fas fa-microchip"></i> Master de Freno
                    </div>
                    <div class="sidebar-categoria" data-categoria="Liquido" onclick="cambiarCategoria('Liquido')">
                        <i class="fas fa-tint"></i> Líquido de Frenos
                    </div>
                    <div class="sidebar-categoria" data-categoria="Otros" onclick="cambiarCategoria('Otros')">
                        <i class="fas fa-tools"></i> Otros Repuestos
                    </div>
                    
                    <div class="filtro-marcas-container" id="filtroMarcasContainer">
                        <div class="sidebar-title mt-2">
                            <i class="fas fa-industry"></i> Filtrar por Marca
                        </div>
<<<<<<< HEAD
                        <div id="marcasLista" class="d-flex flex-wrap">
                            <div class="marca-item" onclick="filtrarPorMarca('TOYOTA')">TOYOTA</div>
                            <div class="marca-item" onclick="filtrarPorMarca('HYUNDAI')">HYUNDAI</div>
                            <div class="marca-item" onclick="filtrarPorMarca('NISSAN')">NISSAN</div>
                            <div class="marca-item" onclick="filtrarPorMarca('MAZDA')">MAZDA</div>
                            <div class="marca-item" onclick="filtrarPorMarca('CHEVROLET')">CHEVROLET</div>
                            <div class="marca-item" onclick="filtrarPorMarca('JEEP')">JEEP</div>
                            <div class="marca-item" onclick="filtrarPorMarca('MITSUBISHI')">MITSUBISHI</div>
                            <div class="marca-item" onclick="filtrarPorMarca('UNIVERSAL')">UNIVERSAL</div>
                            <div class="marca-item" onclick="filtrarPorMarca('')">Todas</div>
                        </div>
=======
                       <div id="marcasLista" class="d-flex flex-wrap">
    <div class="marca-item" onclick="filtrarPorMarca('TOYOTA')">TOYOTA</div>
    <div class="marca-item" onclick="filtrarPorMarca('HYUNDAI')">HYUNDAI</div>
    <div class="marca-item" onclick="filtrarPorMarca('NISSAN')">NISSAN</div>
    <div class="marca-item" onclick="filtrarPorMarca('MAZDA')">MAZDA</div>
    <div class="marca-item" onclick="filtrarPorMarca('CHEVROLET')">CHEVROLET</div>
    <div class="marca-item" onclick="filtrarPorMarca('JEEP')">JEEP</div>
    <div class="marca-item" onclick="filtrarPorMarca('MITSUBISHI')">MITSUBISHI</div>
    <div class="marca-item" onclick="filtrarPorMarca('UNIVERSAL')">UNIVERSAL</div>
    <div class="marca-item" onclick="filtrarPorMarca('')">Todas</div>
</div>
>>>>>>> 53cff441a9e73117cee6103c15537e2d332d69ca
                        <div id="mensajeGenerico" class="info-otros" style="display: none;">
                            <i class="fas fa-info-circle"></i> Los productos genéricos no tienen marca específica
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="col-md-9">
                <div class="contenido-principal">
                    <div class="categoria-header">
                        <h1 id="categoriaTitulo">🛑 Pastillas de Freno</h1>
                        <p id="categoriaDescripcion">Los mejores repuestos para tu vehículo</p>
                    </div>
                    <div id="resultadoBusqueda" class="resultado-busqueda"></div>
                    <div id="productosContainer" class="productos-grid">
                        <div class="text-center py-5">Cargando productos...</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <div class="footer">
        <p><i class="fas fa-car"></i> FrenosPro - Tu seguridad es nuestra prioridad</p>
        <p>© 2025 - Todos los derechos reservados</p>
    </div>
    
    <!-- Modal Registro/Login -->
    <div id="modalRegistro" class="modal">
        <div class="modal-content">
            <span class="close-modal" onclick="cerrarModalRegistro()">&times;</span>
            <h2 id="modalTitle">Iniciar Sesión</h2>
            <form id="authForm" onsubmit="return false;">
                <div id="loginForm">
                    <div class="mb-3">
                        <input type="text" id="loginUsuario" class="form-control" placeholder="Usuario" required>
                    </div>
                    <div class="mb-3">
                        <input type="password" id="loginPassword" class="form-control" placeholder="Contraseña" required>
                    </div>
                    <button type="button" class="btn btn-primary w-100" onclick="iniciarSesion()">Iniciar Sesión</button>
                </div>
                <div id="registroForm" style="display:none;">
                    <div class="mb-3">
                        <input type="text" id="regUsuario" class="form-control" placeholder="Usuario (mínimo 3 caracteres)" required>
                    </div>
                    <div class="mb-3">
                        <input type="text" id="regNombre" class="form-control" placeholder="Nombre completo" required>
                    </div>
                    <div class="mb-3">
                        <input type="email" id="regEmail" class="form-control" placeholder="Correo electrónico" required>
                    </div>
                    <div class="mb-3">
                        <input type="password" id="regPassword" class="form-control" placeholder="Contraseña (mínimo 4 caracteres)" required>
                    </div>
                    <button type="button" class="btn btn-success w-100" onclick="registrarUsuario()">Registrarse</button>
                </div>
                <div class="text-center mt-3">
                    <span id="switchText" class="text-primary" style="cursor:pointer;" onclick="cambiarForm()">¿No tienes cuenta? Regístrate aquí</span>
                </div>
                <div id="authError" class="alert alert-danger mt-3" style="display:none;"></div>
            </form>
        </div>
    </div>
    
    <!-- Modal Carrito -->
    <div id="modalCarrito" class="modal carrito-modal">
        <div class="modal-content">
            <span class="close-modal" onclick="cerrarCarrito()">&times;</span>
            <h2><i class="fas fa-shopping-cart"></i> Mi Carrito</h2>
            <div id="carritoItems"></div>
            <div id="carritoTotal" class="text-end fs-4 fw-bold mt-3"></div>
            <button class="btn btn-success w-100 mt-3" onclick="finalizarPedido()">
                <i class="fas fa-check-circle"></i> Finalizar Pedido
            </button>
        </div>
    </div>

    <!-- Modal Agregar/Editar Producto -->
    <div id="modalProducto" class="modal">
        <div class="modal-content" style="max-width:600px;">
            <span class="close-modal" onclick="cerrarModalProducto()">&times;</span>
            <h2 id="modalProductoTitulo">Agregar Producto</h2>
            <form id="formProducto" onsubmit="return false;">
                <input type="hidden" id="prodCodigoOriginal">
                <div class="mb-3">
                    <label class="form-label">Código</label>
                    <input type="text" id="prodCodigo" class="form-control" required>
                </div>
                <div class="mb-3">
                    <label class="form-label">Nombre</label>
                    <input type="text" id="prodNombre" class="form-control" required>
                </div>
                <div class="row mb-3">
                    <div class="col">
                        <label class="form-label">Marca</label>
                        <input type="text" id="prodMarca" class="form-control">
                    </div>
                    <div class="col">
                        <label class="form-label">Tipo (categoría)</label>
                        <select id="prodTipo" class="form-control" required>
                            <option value="Pastillas">Pastillas</option>
                            <option value="Zapatas">Zapatas</option>
                            <option value="Bombas">Bombas</option>
                            <option value="Master">Master</option>
                            <option value="Liquido">Líquido</option>
                            <option value="Otros">Otros (genérico)</option>
                        </select>
                    </div>
                </div>
                <div class="row mb-3">
                    <div class="col">
                        <label class="form-label">Precio (S/)</label>
                        <input type="number" id="prodPrecio" class="form-control" step="0.01" required>
                    </div>
                    <div class="col">
                        <label class="form-label">Stock</label>
                        <input type="number" id="prodStock" class="form-control" required>
                    </div>
                </div>
                <div class="mb-3">
                    <label class="form-label">Nombre base de imagen (sin extensión)</label>
                    <input type="text" id="prodImagenBase" class="form-control" placeholder="Ej: pastilla_toyota">
                    <small class="text-muted">La imagen debe estar en static/imagenes/ con ese nombre (jpg, png, etc.)</small>
                </div>
                <button type="button" class="btn btn-primary w-100" onclick="guardarProducto()">
                    <i class="fas fa-save"></i> Guardar Producto
                </button>
            </form>
        </div>
    </div>

    <!-- Modal Confirmar Eliminación -->
    <div id="modalEliminar" class="modal">
        <div class="modal-content" style="max-width:400px;">
            <span class="close-modal" onclick="cerrarModalEliminar()">&times;</span>
            <h4>¿Eliminar producto?</h4>
            <p>Estás a punto de eliminar <strong id="eliminarNombre"></strong></p>
            <div class="d-flex gap-2 justify-content-end">
                <button class="btn btn-secondary" onclick="cerrarModalEliminar()">Cancelar</button>
                <button class="btn btn-danger" id="btnConfirmarEliminar">
                    <i class="fas fa-trash"></i> Eliminar
                </button>
            </div>
        </div>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        let carrito = [];
        let productosData = {{ productos | tojson }};
        let categoriaActual = 'Pastillas';
        let marcaActiva = '';
        let busquedaActiva = '';
        let esAdmin = {{ 'true' if session.get('rol') == 'admin' else 'false' }};
        
        const categoriasConfig = {
            'Pastillas': { 
                titulo: '🛑 Pastillas de Freno', 
                descripcion: 'Pastillas de freno de alta calidad para todas las marcas',
                icono: '🛑',
                mostrarMarcas: true
            },
            'Zapatas': { 
                titulo: '🚗 Zapatas de Freno', 
                descripcion: 'Zapatas de freno duraderas y confiables',
                icono: '🚗',
                mostrarMarcas: true
            },
            'Bombas': { 
                titulo: '⚙️ Bombas de Freno', 
                descripcion: 'Bombas de freno originales y alternativas',
                icono: '⚙️',
                mostrarMarcas: true
            },
            'Master': { 
                titulo: '🔧 Master de Freno', 
                descripcion: 'Cilindros maestros para sistema de frenos',
                icono: '🔧',
                mostrarMarcas: true
            },
            'Liquido': { 
                titulo: '💧 Líquido de Frenos', 
                descripcion: 'Líquido DOT3 y DOT4 de alta calidad',
                icono: '💧',
                mostrarMarcas: true
            },
            'Otros': { 
                titulo: '🔩 Otros Repuestos', 
                descripcion: 'Repuestos y accesorios genéricos para frenos',
                icono: '🔩',
                mostrarMarcas: false
            }
        };
        
        {% if session.usuario %}
            let usuarioLogueado = true;
        {% else %}
            let usuarioLogueado = false;
        {% endif %}
        
        function cambiarCategoria(categoria) {
            categoriaActual = categoria;
            busquedaActiva = '';
            document.getElementById('buscadorInput').value = '';
            document.getElementById('resultadoBusqueda').style.display = 'none';
            
            if (categoria === 'Otros') {
                marcaActiva = '';
                document.querySelectorAll('.marca-item').forEach(el => el.classList.remove('active'));
            }
            
            document.querySelectorAll('.sidebar-categoria').forEach(el => el.classList.remove('active'));
            document.querySelector(`.sidebar-categoria[data-categoria="${categoria}"]`).classList.add('active');
            
            const config = categoriasConfig[categoria];
            document.getElementById('categoriaTitulo').innerHTML = `${config.icono} ${config.titulo.replace(config.icono, '').trim()}`;
            document.getElementById('categoriaDescripcion').innerHTML = config.descripcion;
            
            const filtroMarcas = document.getElementById('filtroMarcasContainer');
            const mensajeGenerico = document.getElementById('mensajeGenerico');
            
            if (config.mostrarMarcas) {
                filtroMarcas.classList.remove('oculto');
                mensajeGenerico.style.display = 'none';
            } else {
                filtroMarcas.classList.add('oculto');
                mensajeGenerico.style.display = 'block';
            }
            
            cargarProductosPorCategoria();
        }
        
        function realizarBusqueda() {
            const termino = document.getElementById('buscadorInput').value.toLowerCase().trim();
            busquedaActiva = termino;
            
            if (termino === '') {
                document.getElementById('resultadoBusqueda').style.display = 'none';
                cargarProductosPorCategoria();
                return;
            }
            
            let productosEncontrados = productosData.filter(p => 
                p.nombre.toLowerCase().includes(termino) || 
                p.marca.toLowerCase().includes(termino) ||
                p.tipo.toLowerCase().includes(termino)
            );
            
            if (marcaActiva && categoriaActual !== 'Otros') {
                productosEncontrados = productosEncontrados.filter(p => p.marca === marcaActiva);
            }
            
            const container = document.getElementById('productosContainer');
            const resultadoDiv = document.getElementById('resultadoBusqueda');
            
            if (productosEncontrados.length > 0) {
                resultadoDiv.innerHTML = `<i class="fas fa-search"></i> Resultados para "${termino}": ${productosEncontrados.length} producto(s) encontrado(s)`;
                resultadoDiv.style.display = 'block';
                container.innerHTML = productosEncontrados.map(p => renderProductoCard(p)).join('');
                document.getElementById('categoriaTitulo').innerHTML = `🔍 Resultados: "${termino}"`;
                document.getElementById('categoriaDescripcion').innerHTML = `Se encontraron ${productosEncontrados.length} productos`;
            } else {
                resultadoDiv.innerHTML = `<i class="fas fa-search"></i> No se encontraron resultados para "${termino}"`;
                resultadoDiv.style.display = 'block';
                container.innerHTML = `<div class="sin-productos"><i class="fas fa-search fa-3x mb-3"></i><br>No hay productos que coincidan con "${termino}"</div>`;
                document.getElementById('categoriaTitulo').innerHTML = `🔍 Búsqueda: "${termino}"`;
                document.getElementById('categoriaDescripcion').innerHTML = `No se encontraron resultados`;
            }
        }
        
        function buscarProducto(event) {
            if (event && event.key === 'Enter') {
                realizarBusqueda();
            }
        }
        
        function cargarProductosPorCategoria() {
            if (busquedaActiva !== '') return;
            
            let productosFiltrados = [];
            
            if (categoriaActual === 'Otros') {
<<<<<<< HEAD
=======
                // SOLO productos UNIVERSAL que NO sean Liquido
>>>>>>> 53cff441a9e73117cee6103c15537e2d332d69ca
                productosFiltrados = productosData.filter(p => 
                    p.marca === 'UNIVERSAL' && 
                    p.tipo !== 'Liquido'
                );
            } else {
                productosFiltrados = productosData.filter(p => p.tipo === categoriaActual);
                
                if (marcaActiva) {
                    productosFiltrados = productosFiltrados.filter(p => p.marca === marcaActiva);
                }
            }
            
            const container = document.getElementById('productosContainer');
            if (productosFiltrados.length > 0) {
                container.innerHTML = productosFiltrados.map(p => renderProductoCard(p)).join('');
            } else {
                let mensaje = '';
                if (categoriaActual === 'Otros') {
                    mensaje = `📦 No hay productos genéricos disponibles. Aquí encontrarás: Mangueras, Kits, Pistones, Calipers, Pasadores, Tapas, Rodajes, Retenes, Jebes, Resortes, Sensores y Grasas.`;
                } else {
                    mensaje = marcaActiva ? 
                        `No hay productos de ${categoriaActual} para la marca ${marcaActiva}` : 
                        `No hay productos en la categoría ${categoriaActual}`;
                }
                container.innerHTML = `<div class="sin-productos"><i class="fas fa-box-open fa-3x mb-3"></i><br>${mensaje}</div>`;
            }
        }
        
        function renderProductoCard(p) {
            const imgSrc = `/imagenes/${p.imagen}`;
            const mostrarMarca = p.marca !== 'UNIVERSAL';
            let adminBtns = '';
            if (esAdmin) {
                adminBtns = `
                    <div class="mt-2 d-flex gap-2">
                        <button class="btn btn-sm btn-outline-primary" onclick="abrirModalEditar('${p.codigo}')">
                            <i class="fas fa-edit"></i> Editar
                        </button>
                        <button class="btn btn-sm btn-outline-danger" onclick="confirmarEliminar('${p.codigo}','${p.nombre.replace(/'/g, "\\'")}')">
                            <i class="fas fa-trash"></i> Eliminar
                        </button>
                    </div>`;
            }
            
            return `
                <div class="producto-card position-relative">
                    <div class="badge-stock">📦 Stock: ${p.stock}</div>
                    <img class="producto-imagen" src="${imgSrc}" 
                         onerror="this.src='https://via.placeholder.com/300x200/667eea/white?text=${encodeURIComponent(p.nombre)}'"
                         alt="${p.nombre}">
                    <div class="producto-info">
                        <div class="producto-nombre">${p.nombre}</div>
                        ${mostrarMarca ? `<div class="producto-marca"><i class="fas fa-tag"></i> ${p.marca}</div>` : '<div class="producto-marca" style="color: #999;"><i class="fas fa-cogs"></i> Genérico</div>'}
                        <div class="producto-precio">S/ ${p.precio.toFixed(2)}</div>
                        <button class="btn-comprar mt-2" onclick="agregarAlCarrito('${p.codigo}', '${p.nombre.replace(/'/g, "\\'")}', ${p.precio})">
                            <i class="fas fa-cart-plus"></i> Agregar al carrito
                        </button>
                        ${adminBtns}
                    </div>
                </div>
            `;
        }
        
        function filtrarPorMarca(marca) {
            if (categoriaActual === 'Otros') {
                mostrarNotificacion("⚠️ Los productos genéricos no tienen marca específica", 'error');
                return;
            }
            
            marcaActiva = marca;
            busquedaActiva = '';
            document.getElementById('buscadorInput').value = '';
            document.getElementById('resultadoBusqueda').style.display = 'none';
            
            document.querySelectorAll('.marca-item').forEach(el => el.classList.remove('active'));
            if (marca) {
                const marcaElement = Array.from(document.querySelectorAll('.marca-item')).find(el => el.innerText === marca);
                if (marcaElement) marcaElement.classList.add('active');
                mostrarNotificacion(`🔧 Mostrando productos de marca ${marca}`);
            } else {
                mostrarNotificacion("📦 Mostrando todas las marcas");
            }
            cargarProductosPorCategoria();
        }
        
        function mostrarNotificacion(mensaje, tipo = 'success') {
            const notif = document.createElement('div');
            notif.className = `alert alert-${tipo === 'success' ? 'success' : 'danger'} position-fixed bottom-0 end-0 m-3`;
            notif.style.zIndex = 2000;
            notif.style.animation = 'fadeIn 0.3s ease';
            notif.innerHTML = mensaje;
            document.body.appendChild(notif);
            setTimeout(() => notif.remove(), 3000);
        }
        
        function agregarAlCarrito(codigo, nombre, precio) {
            if (!usuarioLogueado) {
                mostrarNotificacion("⚠️ Debes iniciar sesión para agregar productos al carrito", 'error');
                abrirModalRegistro();
                return;
            }
            
            let existente = carrito.find(item => item.codigo === codigo);
            if (existente) {
                existente.cantidad++;
            } else {
                carrito.push({codigo, nombre, precio, cantidad: 1});
            }
            actualizarCarritoUI();
            mostrarNotificacion(`✅ ${nombre} agregado al carrito`);
        }
        
        function actualizarCarritoUI() {
            localStorage.setItem('carrito', JSON.stringify(carrito));
            let count = carrito.reduce((s, i) => s + i.cantidad, 0);
            document.getElementById('cartCount').innerText = count;
            
            let container = document.getElementById('carritoItems');
            if (container) {
                if (carrito.length === 0) {
                    container.innerHTML = '<div class="text-center p-4">🛒 Carrito vacío</div>';
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
                                    <input type="number" value="${item.cantidad}" min="1" style="width:60px;" class="form-control form-control-sm d-inline-block w-auto" onchange="editarCantidad(${i}, this.value)">
                                    <button class="btn btn-danger btn-sm" onclick="eliminarDelCarrito(${i})"><i class="fas fa-trash"></i></button>
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
        
        function abrirCarrito() { actualizarCarritoUI(); document.getElementById('modalCarrito').style.display = 'flex'; }
        function cerrarCarrito() { document.getElementById('modalCarrito').style.display = 'none'; }
        
        function finalizarPedido() {
            if (!usuarioLogueado) {
                mostrarNotificacion("⚠️ Debes iniciar sesión para finalizar el pedido", 'error');
                cerrarCarrito();
                abrirModalRegistro();
                return;
            }
            
            if (carrito.length === 0) { 
                mostrarNotificacion("🛒 El carrito está vacío", 'error');
                return; 
            }
            
            fetch('/finalizar_pedido', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({carrito: carrito})
            }).then(r => r.json()).then(data => {
                if (data.exito) {
                    mostrarNotificacion(`✅ ¡PEDIDO REALIZADO! N° ${data.numero} - Total: S/${data.total.toFixed(2)}`);
                    carrito = []; 
                    actualizarCarritoUI(); 
                    cerrarCarrito();
                } else { 
                    mostrarNotificacion("Error al procesar el pedido", 'error');
                }
            });
        }
        
        function abrirModalRegistro() {
            document.getElementById('modalRegistro').style.display = 'flex';
            document.getElementById('authError').style.display = 'none';
        }
        
        function cerrarModalRegistro() {
            document.getElementById('modalRegistro').style.display = 'none';
        }
        
        let mostrandoLogin = true;
        
        function cambiarForm() {
            mostrandoLogin = !mostrandoLogin;
            if (mostrandoLogin) {
                document.getElementById('loginForm').style.display = 'block';
                document.getElementById('registroForm').style.display = 'none';
                document.getElementById('modalTitle').innerText = 'Iniciar Sesión';
                document.getElementById('switchText').innerHTML = '¿No tienes cuenta? Regístrate aquí';
            } else {
                document.getElementById('loginForm').style.display = 'none';
                document.getElementById('registroForm').style.display = 'block';
                document.getElementById('modalTitle').innerText = 'Registrarse';
                document.getElementById('switchText').innerHTML = '¿Ya tienes cuenta? Inicia sesión aquí';
            }
        }
        
        function iniciarSesion() {
            const usuario = document.getElementById('loginUsuario').value;
            const password = document.getElementById('loginPassword').value;
            
            fetch('/login_api', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({usuario, password})
            }).then(r => r.json()).then(data => {
                if (data.exito) {
                    mostrarNotificacion(`✅ ¡Bienvenido ${data.nombre}!`);
                    setTimeout(() => location.reload(), 1000);
                } else {
                    const errorDiv = document.getElementById('authError');
                    errorDiv.innerHTML = data.mensaje;
                    errorDiv.style.display = 'block';
                }
            });
        }
        
        function registrarUsuario() {
            const usuario = document.getElementById('regUsuario').value;
            const nombre = document.getElementById('regNombre').value;
            const email = document.getElementById('regEmail').value;
            const password = document.getElementById('regPassword').value;
            
            if (usuario.length < 3) {
                mostrarNotificacion("⚠️ Usuario debe tener al menos 3 caracteres", 'error');
                return;
            }
            if (password.length < 4) {
                mostrarNotificacion("⚠️ Contraseña debe tener al menos 4 caracteres", 'error');
                return;
            }
            if (!email.includes('@') || !email.includes('.')) {
                mostrarNotificacion("⚠️ Ingrese un email válido (ejemplo@correo.com)", 'error');
                return;
            }
            
            fetch('/registro_api', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({usuario, password, nombre, email})
            }).then(r => r.json()).then(data => {
                if (data.exito) {
                    mostrarNotificacion("✅ ¡Registro exitoso! Ahora inicia sesión");
                    cambiarForm();
                    document.getElementById('loginUsuario').value = usuario;
                    document.getElementById('loginPassword').value = '';
                } else {
                    const errorDiv = document.getElementById('authError');
                    errorDiv.innerHTML = data.mensaje;
                    errorDiv.style.display = 'block';
                }
            });
        }
        
        // Funciones para administración de productos
        function abrirModalAgregar() {
            document.getElementById('modalProductoTitulo').innerText = 'Agregar Producto';
            document.getElementById('formProducto').reset();
            document.getElementById('prodCodigoOriginal').value = '';
            document.getElementById('prodCodigo').disabled = false;
            document.getElementById('modalProducto').style.display = 'flex';
        }

        function abrirModalEditar(codigo) {
            const prod = productosData.find(p => p.codigo === codigo);
            if (!prod) return;
            document.getElementById('modalProductoTitulo').innerText = 'Editar Producto';
            document.getElementById('prodCodigoOriginal').value = prod.codigo;
            document.getElementById('prodCodigo').value = prod.codigo;
            document.getElementById('prodCodigo').disabled = true;
            document.getElementById('prodNombre').value = prod.nombre;
            document.getElementById('prodMarca').value = prod.marca;
            document.getElementById('prodTipo').value = prod.tipo;
            document.getElementById('prodPrecio').value = prod.precio;
            document.getElementById('prodStock').value = prod.stock;
            document.getElementById('prodImagenBase').value = prod.nombre_base;
            document.getElementById('modalProducto').style.display = 'flex';
        }

        function cerrarModalProducto() {
            document.getElementById('modalProducto').style.display = 'none';
        }

        function guardarProducto() {
            const codigoOriginal = document.getElementById('prodCodigoOriginal').value;
            const esEdicion = codigoOriginal !== '';
            const url = esEdicion ? `/admin/producto/${codigoOriginal}` : '/admin/producto';
            const method = esEdicion ? 'PUT' : 'POST';
            
            const data = {
                codigo: document.getElementById('prodCodigo').value,
                nombre: document.getElementById('prodNombre').value,
                marca: document.getElementById('prodMarca').value,
                tipo: document.getElementById('prodTipo').value,
                precio: document.getElementById('prodPrecio').value,
                stock: document.getElementById('prodStock').value,
                nombre_base: document.getElementById('prodImagenBase').value
            };
            
            fetch(url, {
                method: method,
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            })
            .then(r => r.json())
            .then(res => {
                if (res.exito) {
                    mostrarNotificacion(esEdicion ? '✅ Producto actualizado' : '✅ Producto creado');
                    location.reload();
                } else {
                    mostrarNotificacion('❌ ' + res.mensaje, 'error');
                }
            });
        }

        let codigoAEliminar = '';

        function confirmarEliminar(codigo, nombre) {
            codigoAEliminar = codigo;
            document.getElementById('eliminarNombre').innerText = nombre;
            document.getElementById('modalEliminar').style.display = 'flex';
        }

        function cerrarModalEliminar() {
            document.getElementById('modalEliminar').style.display = 'none';
        }

        document.getElementById('btnConfirmarEliminar').addEventListener('click', function() {
            fetch(`/admin/producto/${codigoAEliminar}`, { method: 'DELETE' })
            .then(r => r.json())
            .then(res => {
                if (res.exito) {
                    mostrarNotificacion('🗑️ Producto eliminado');
                    location.reload();
                } else {
                    mostrarNotificacion('❌ Error al eliminar', 'error');
                }
            });
            cerrarModalEliminar();
        });

<<<<<<< HEAD
=======
        // Cerrar modales al hacer clic fuera
>>>>>>> 53cff441a9e73117cee6103c15537e2d332d69ca
        window.addEventListener('click', function(e) {
            if (e.target === document.getElementById('modalProducto')) cerrarModalProducto();
            if (e.target === document.getElementById('modalEliminar')) cerrarModalEliminar();
            if (e.target === document.getElementById('modalRegistro')) cerrarModalRegistro();
            if (e.target === document.getElementById('modalCarrito')) cerrarCarrito();
        });
        
<<<<<<< HEAD
=======
        // Inicializar
>>>>>>> 53cff441a9e73117cee6103c15537e2d332d69ca
        let saved = localStorage.getItem('carrito');
        if (saved) carrito = JSON.parse(saved);
        actualizarCarritoUI();
        
        document.querySelector('.sidebar-categoria[data-categoria="Pastillas"]').classList.add('active');
        cargarProductosPorCategoria();
    </script>
</body>
</html>
    """

if __name__ == "__main__":
<<<<<<< HEAD
    port = int(os.environ.get("PORT", 8000))
=======
    port = int(os.environ.get("PORT", 8080))
>>>>>>> 53cff441a9e73117cee6103c15537e2d332d69ca
    app.run(host="0.0.0.0", port=port, debug=False)
