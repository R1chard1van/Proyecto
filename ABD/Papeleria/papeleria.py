import sys
import mysql.connector
from PyQt6.QtWidgets import QMessageBox, QLabel, QApplication, QMainWindow, QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout
from PyQt6.QtCore import Qt

# Conectar a la base de datos MySQL
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="872004",
        database="PapeleriaDB"
    )

def load_products(table_widget):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Productos")
    rows = cursor.fetchall()
    table_widget.setRowCount(len(rows))
    for i, row in enumerate(rows):
        for j, cell in enumerate(row):
            table_widget.setItem(i, j, QTableWidgetItem(str(cell)))
    conn.close()

def add_product(name, description, price, stock, category):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Productos (nombre, descripcion, precio, stock, categoria)
        VALUES (%s, %s, %s, %s, %s)
    """, (name, description, price, stock, category))
    conn.commit()
    conn.close()

def update_product(product_id, name, description, price, stock, category):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE Productos
        SET nombre = %s, descripcion = %s, precio = %s, stock = %s, categoria = %s
        WHERE id_producto = %s
    """, (name, description, price, stock, category, product_id))
    conn.commit()
    conn.close()

def delete_product(product_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Productos WHERE id_producto = %s", (product_id,))
    conn.commit()
    conn.close()

class CRUDWindow(QMainWindow):
    def __init__(self, main_menu, title):
        super().__init__()
        self.main_menu = main_menu
        self.setWindowTitle(title)
        self.setGeometry(150, 150, 800, 600)
    
    def add_back_button(self, layout):
        back_btn = QPushButton("← Regresar al Menú Principal")
        back_btn.setStyleSheet("""
            QPushButton {
                padding: 8px;
                font-weight: bold;
                background-color: #2196F3;
                color: white;
            }
        """)
        back_btn.clicked.connect(self.go_back)
        layout.addWidget(back_btn)
    
    def go_back(self):
        self.close()
        self.main_menu.show()

class ProductApp(CRUDWindow): 
    def __init__(self, main_menu):
        super().__init__(main_menu, "Gestión de Productos")  
        self.init_ui()
    
    def init_ui(self):
        main_layout = QVBoxLayout()

        form_layout = QFormLayout()
        self.name_input = QLineEdit()
        self.description_input = QLineEdit()
        self.price_input = QLineEdit()
        self.stock_input = QLineEdit()
        self.category_input = QLineEdit()

        form_layout.addRow("Nombre:", self.name_input)
        form_layout.addRow("Descripción:", self.description_input)
        form_layout.addRow("Precio:", self.price_input)
        form_layout.addRow("Stock:", self.stock_input)
        form_layout.addRow("Categoría:", self.category_input)

        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Agregar")
        self.update_button = QPushButton("Actualizar")
        self.delete_button = QPushButton("Eliminar")

        self.add_button.clicked.connect(self.add_product)
        self.update_button.clicked.connect(self.update_product)
        self.delete_button.clicked.connect(self.delete_product)

        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.delete_button)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Nombre", "Descripción", "Precio", "Stock", "Categoría"])
        load_products(self.table)

        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.table)
        
        self.add_back_button(main_layout) 

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def add_product(self):
        name = self.name_input.text()
        description = self.description_input.text()
        price = float(self.price_input.text())
        stock = int(self.stock_input.text())
        category = self.category_input.text()
        add_product(name, description, price, stock, category)
        load_products(self.table)  

    def update_product(self):
        row = self.table.currentRow()
        if row >= 0:
            product_id = self.table.item(row, 0).text()
            name = self.name_input.text()
            description = self.description_input.text()
            price = float(self.price_input.text())
            stock = int(self.stock_input.text())
            category = self.category_input.text()
            update_product(product_id, name, description, price, stock, category)
            load_products(self.table) 

    def delete_product(self):
        row = self.table.currentRow()
        if row >= 0:
            product_id = self.table.item(row, 0).text()
            delete_product(product_id)
            load_products(self.table)  

def load_suppliers(table_widget):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Proveedores")
    rows = cursor.fetchall()
    table_widget.setRowCount(len(rows))
    for i, row in enumerate(rows):
        for j, cell in enumerate(row):
            table_widget.setItem(i, j, QTableWidgetItem(str(cell)))
    conn.close()

def add_supplier(name, phone, email, address):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Proveedores (nombre, telefono, email, direccion)
        VALUES (%s, %s, %s, %s)
    """, (name, phone, email, address))
    conn.commit()
    conn.close()

def update_supplier(supplier_id, name, phone, email, address):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE Proveedores
        SET nombre = %s, telefono = %s, email = %s, direccion = %s
        WHERE id_proveedor = %s
    """, (name, phone, email, address, supplier_id))
    conn.commit()
    conn.close()

def delete_supplier(supplier_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Proveedores WHERE id_proveedor = %s", (supplier_id,))
    conn.commit()
    conn.close()

class SupplierApp(CRUDWindow):
    def __init__(self, main_menu):
        super().__init__(main_menu, "Gestión de Proveedores")
        self.selected_id = None 
        self.init_ui()
    
    def init_ui(self):
        main_layout = QVBoxLayout()

        form_layout = QFormLayout()
        self.name_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.email_input = QLineEdit()
        self.address_input = QLineEdit()

        form_layout.addRow("Nombre:", self.name_input)
        form_layout.addRow("Teléfono:", self.phone_input)
        form_layout.addRow("Email:", self.email_input)
        form_layout.addRow("Dirección:", self.address_input)

        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Agregar")
        self.update_button = QPushButton("Actualizar")
        self.delete_button = QPushButton("Eliminar")

        self.add_button.clicked.connect(self.add_supplier)
        self.update_button.clicked.connect(self.update_supplier)
        self.delete_button.clicked.connect(self.delete_supplier)

        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.delete_button)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Nombre", "Teléfono", "Email", "Dirección"])
        self.table.cellClicked.connect(self.load_inputs_from_table) 
        load_suppliers(self.table) 

        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.table)
        
        self.add_back_button(main_layout) 

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def load_inputs_from_table(self, row, column):
        self.selected_id = self.table.item(row, 0).text()
        self.name_input.setText(self.table.item(row, 1).text())
        self.phone_input.setText(self.table.item(row, 2).text())
        self.email_input.setText(self.table.item(row, 3).text())
        self.address_input.setText(self.table.item(row, 4).text())

    def add_supplier(self):
        name = self.name_input.text()
        phone = self.phone_input.text()
        email = self.email_input.text()
        address = self.address_input.text()
        add_supplier(name, phone, email, address)
        load_suppliers(self.table)

    def update_supplier(self):
        if hasattr(self, 'selected_id'):
            supplier_id = self.selected_id
            name = self.name_input.text()
            phone = self.phone_input.text()
            email = self.email_input.text()
            address = self.address_input.text()
            update_supplier(supplier_id, name, phone, email, address)
            load_suppliers(self.table)

    def delete_supplier(self):
        if hasattr(self, 'selected_id'):
            supplier_id = self.selected_id
            delete_supplier(supplier_id)
            load_suppliers(self.table)
            self.name_input.clear()
            self.phone_input.clear()
            self.email_input.clear()
            self.address_input.clear()

def load_clients(table_widget):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Clientes")
    rows = cursor.fetchall()
    table_widget.setRowCount(len(rows))
    for i, row in enumerate(rows):
        for j, cell in enumerate(row):
            table_widget.setItem(i, j, QTableWidgetItem(str(cell)))
    conn.close()

def add_client(name, phone, email, address):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Clientes (nombre, telefono, email, direccion)
        VALUES (%s, %s, %s, %s)
    """, (name, phone, email, address))
    conn.commit()
    conn.close()

def update_client(client_id, name, phone, email, address):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE Clientes
        SET nombre = %s, telefono = %s, email = %s, direccion = %s
        WHERE id_cliente = %s
    """, (name, phone, email, address, client_id))
    conn.commit()
    conn.close()

def delete_client(client_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Clientes WHERE id_cliente = %s", (client_id,))
    conn.commit()
    conn.close()

class ClientApp(CRUDWindow):
    def __init__(self, main_menu):
        super().__init__(main_menu, "Gestión de Clientes")
        self.init_ui()
    
    def init_ui(self):
        main_layout = QVBoxLayout()

        form_layout = QFormLayout()
        self.name_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.email_input = QLineEdit()
        self.address_input = QLineEdit()

        form_layout.addRow("Nombre:", self.name_input)
        form_layout.addRow("Teléfono:", self.phone_input)
        form_layout.addRow("Email:", self.email_input)
        form_layout.addRow("Dirección:", self.address_input)

        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Agregar")
        self.update_button = QPushButton("Actualizar")
        self.delete_button = QPushButton("Eliminar")

        self.add_button.clicked.connect(self.add_client)
        self.update_button.clicked.connect(self.update_client)
        self.delete_button.clicked.connect(self.delete_client)

        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.delete_button)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Nombre", "Teléfono", "Email", "Dirección"])
        self.table.cellClicked.connect(self.load_client_data)
        load_clients(self.table)

        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.table)
        
        self.add_back_button(main_layout)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)
    
    def load_client_data(self, row, column):
        self.selected_id = self.table.item(row, 0).text()
        self.name_input.setText(self.table.item(row, 1).text())
        self.phone_input.setText(self.table.item(row, 2).text())
        self.email_input.setText(self.table.item(row, 3).text())
        self.address_input.setText(self.table.item(row, 4).text())
    
    def add_client(self):
        add_client(
            self.name_input.text(),
            self.phone_input.text(),
            self.email_input.text(),
            self.address_input.text()
        )
        load_clients(self.table)
    
    def update_client(self):
        if hasattr(self, 'selected_id'):
            update_client(
                self.selected_id,
                self.name_input.text(),
                self.phone_input.text(),
                self.email_input.text(),
                self.address_input.text()
            )
            load_clients(self.table)
    
    def delete_client(self):
        if hasattr(self, 'selected_id'):
            delete_client(self.selected_id)
            load_clients(self.table)
            self.clear_inputs()
    
    def clear_inputs(self):
        self.name_input.clear()
        self.phone_input.clear()
        self.email_input.clear()
        self.address_input.clear()

def cargar_ventas(table_widget):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Ventas")
    rows = cursor.fetchall()
    table_widget.setRowCount(len(rows))
    for i, row in enumerate(rows):
        for j, cell in enumerate(row):
            table_widget.setItem(i, j, QTableWidgetItem(str(cell)))
    conn.close()

def agregar_venta(id_cliente, total, fecha):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Ventas (id_cliente, total, fecha)
        VALUES (%s, %s, %s)
    """, (id_cliente, total, fecha))
    conn.commit()
    conn.close()

def actualizar_venta(id_venta, id_cliente, total, fecha):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE Ventas
        SET id_cliente = %s, total = %s, fecha = %s
        WHERE id_venta = %s
    """, (id_cliente, total, fecha, id_venta))
    conn.commit()
    conn.close()

def eliminar_venta(id_venta):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Ventas WHERE id_venta = %s", (id_venta,))
    conn.commit()
    conn.close()

class VentasApp(CRUDWindow):
    def __init__(self, main_menu):
        super().__init__(main_menu, "CRUD Ventas - Papelería")
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        form_layout = QFormLayout()
        self.id_cliente_input = QLineEdit()
        self.total_input = QLineEdit()
        self.fecha_input = QLineEdit()

        form_layout.addRow("ID Cliente:", self.id_cliente_input)
        form_layout.addRow("Total:", self.total_input)
        form_layout.addRow("Fecha:", self.fecha_input)

        button_layout = QHBoxLayout()

        self.agregar_button = QPushButton("Agregar")
        self.actualizar_button = QPushButton("Actualizar")
        self.eliminar_button = QPushButton("Eliminar")

        self.agregar_button.clicked.connect(self.agregar_venta)
        self.actualizar_button.clicked.connect(self.actualizar_venta)
        self.eliminar_button.clicked.connect(self.eliminar_venta)

        button_layout.addWidget(self.agregar_button)
        button_layout.addWidget(self.actualizar_button)
        button_layout.addWidget(self.eliminar_button)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID Venta", "ID Cliente", "Fecha", "Total"])
        self.table.cellClicked.connect(self.cargar_inputs_desde_tabla)

        cargar_ventas(self.table)

        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.table)
        
        self.add_back_button(main_layout)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)
    
    
    def cargar_inputs_desde_tabla(self, row, column):
        self.selected_id = self.table.item(row, 0).text()
        self.id_cliente_input.setText(self.table.item(row, 1).text())
        self.total_input.setText(self.table.item(row, 2).text())
        self.fecha_input.setText(self.table.item(row, 3).text())

    def agregar_venta(self):
        id_cliente = self.id_cliente_input.text()
        total = float(self.total_input.text())
        fecha = self.fecha_input.text()
        agregar_venta(id_cliente, total, fecha)
        cargar_ventas(self.table)

    def actualizar_venta(self):
        if hasattr(self, 'selected_id'):
            id_venta = self.selected_id
            id_cliente = self.id_cliente_input.text()
            total = float(self.total_input.text())
            fecha = self.fecha_input.text()
            actualizar_venta(id_venta, id_cliente, total, fecha)
            cargar_ventas(self.table)

    def eliminar_venta(self):
        if hasattr(self, 'selected_id'):
            id_venta = self.selected_id
            eliminar_venta(id_venta)
            cargar_ventas(self.table)
            self.id_cliente_input.clear()
            self.total_input.clear()
            self.fecha_input.clear()

def cargar_detalles_venta(table_widget):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Detalles_Venta")
    rows = cursor.fetchall()
    table_widget.setRowCount(len(rows))
    for i, row in enumerate(rows):
        for j, cell in enumerate(row):
            table_widget.setItem(i, j, QTableWidgetItem(str(cell)))
    conn.close()

def agregar_detalle_venta(id_venta, id_producto, cantidad, precio_unitario):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Detalles_Venta (id_venta, id_producto, cantidad, subtotal)
        VALUES (%s, %s, %s, %s)
    """, (id_venta, id_producto, cantidad, precio_unitario))
    conn.commit()
    conn.close()

def actualizar_detalle_venta(id_detalle, id_venta, id_producto, cantidad, precio_unitario):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE Detalles_Venta
        SET id_venta = %s, id_producto = %s, cantidad = %s, subtotal = %s
        WHERE id_detalle = %s
    """, (id_venta, id_producto, cantidad, precio_unitario, id_detalle))
    conn.commit()
    conn.close()

def eliminar_detalle_venta(id_detalle):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Detalles_Venta WHERE id_detalle = %s", (id_detalle,))
    conn.commit()
    conn.close()

class DetallesVentaApp(CRUDWindow):
    def __init__(self, main_menu):
        super().__init__(main_menu, "Gestión de Detalles de Venta")
        self.init_ui()
    
    def init_ui(self):
        main_layout = QVBoxLayout()

        form_layout = QFormLayout()
        self.id_venta_input = QLineEdit()
        self.id_producto_input = QLineEdit()
        self.cantidad_input = QLineEdit()
        self.precio_unitario_input = QLineEdit()

        form_layout.addRow("ID Venta:", self.id_venta_input)
        form_layout.addRow("ID Producto:", self.id_producto_input)
        form_layout.addRow("Cantidad:", self.cantidad_input)
        form_layout.addRow("Precio Unitario:", self.precio_unitario_input)

        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Agregar")
        self.update_button = QPushButton("Actualizar")
        self.delete_button = QPushButton("Eliminar")

        self.add_button.clicked.connect(self.add_detalle)
        self.update_button.clicked.connect(self.update_detalle)
        self.delete_button.clicked.connect(self.delete_detalle)

        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.delete_button)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID Detalle", "ID Venta", "ID Producto", "Cantidad", "Subtotal"])
        self.table.cellClicked.connect(self.load_inputs_from_table)
        cargar_detalles_venta(self.table)

        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.table)
        
        self.add_back_button(main_layout)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def load_inputs_from_table(self, row, column):
        self.selected_id = self.table.item(row, 0).text()
        self.id_venta_input.setText(self.table.item(row, 1).text())
        self.id_producto_input.setText(self.table.item(row, 2).text())
        self.cantidad_input.setText(self.table.item(row, 3).text())
        self.precio_unitario_input.setText(self.table.item(row, 4).text())

    def add_detalle(self):
        id_venta = self.id_venta_input.text()
        id_producto = self.id_producto_input.text()
        cantidad = int(self.cantidad_input.text())
        precio_unitario = float(self.precio_unitario_input.text())
        agregar_detalle_venta(id_venta, id_producto, cantidad, precio_unitario)
        cargar_detalles_venta(self.table)

    def update_detalle(self):
        if hasattr(self, 'selected_id'):
            id_detalle = self.selected_id
            id_venta = self.id_venta_input.text()
            id_producto = self.id_producto_input.text()
            cantidad = int(self.cantidad_input.text())
            precio_unitario = float(self.precio_unitario_input.text())
            actualizar_detalle_venta(id_detalle, id_venta, id_producto, cantidad, precio_unitario)
            cargar_detalles_venta(self.table)

    def delete_detalle(self):
        if hasattr(self, 'selected_id'):
            id_detalle = self.selected_id
            eliminar_detalle_venta(id_detalle)
            cargar_detalles_venta(self.table)
            self.clear_inputs()
    
    def clear_inputs(self):
        self.id_venta_input.clear()
        self.id_producto_input.clear()
        self.cantidad_input.clear()
        self.precio_unitario_input.clear()

def cargar_compras(table_widget):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Compras")
    rows = cursor.fetchall()
    table_widget.setRowCount(len(rows))
    for i, row in enumerate(rows):
        for j, cell in enumerate(row):
            table_widget.setItem(i, j, QTableWidgetItem(str(cell)))
    conn.close()

def agregar_compra(id_proveedor, fecha, total):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Compras (id_proveedor, fecha, total)
        VALUES (%s, %s, %s)
    """, (id_proveedor, fecha, total))
    conn.commit()
    conn.close()

def actualizar_compra(id_compra, id_proveedor, fecha, total):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE Compras
        SET id_proveedor = %s, fecha = %s, total = %s
        WHERE id_compra = %s
    """, (id_proveedor, fecha, total, id_compra))
    conn.commit()
    conn.close()

def eliminar_compra(id_compra):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Compras WHERE id_compra = %s", (id_compra,))
    conn.commit()
    conn.close()

class ComprasApp(CRUDWindow):
    def __init__(self, main_menu):
        super().__init__(main_menu, "Gestión de Compras - Papelería")
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        form_layout = QFormLayout()
        
        self.id_proveedor_input = QLineEdit()
        self.fecha_input = QLineEdit()
        self.total_input = QLineEdit()
        self.fecha_input.setPlaceholderText("AAAA-MM-DD")

        form_layout.addRow("ID Proveedor:", self.id_proveedor_input)
        form_layout.addRow("Fecha:", self.fecha_input)
        form_layout.addRow("Total:", self.total_input)

        button_layout = QHBoxLayout()
        
        self.agregar_button = QPushButton("Agregar")
        self.actualizar_button = QPushButton("Actualizar")
        self.eliminar_button = QPushButton("Eliminar")

        self.agregar_button.clicked.connect(self.agregar_compra)
        self.actualizar_button.clicked.connect(self.actualizar_compra)
        self.eliminar_button.clicked.connect(self.eliminar_compra)

        button_layout.addWidget(self.agregar_button)
        button_layout.addWidget(self.actualizar_button)
        button_layout.addWidget(self.eliminar_button)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID Compra", "ID Proveedor", "Fecha", "Total"])
        self.table.cellClicked.connect(self.cargar_inputs_desde_tabla)

        cargar_compras(self.table)

        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.table)
        
        self.add_back_button(main_layout)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def cargar_inputs_desde_tabla(self, row, column):
        self.selected_id = self.table.item(row, 0).text()
        self.id_proveedor_input.setText(self.table.item(row, 1).text())
        self.fecha_input.setText(self.table.item(row, 2).text())
        self.total_input.setText(self.table.item(row, 3).text())

    def agregar_compra(self):
        id_proveedor = self.id_proveedor_input.text()
        fecha = self.fecha_input.text()
        total = float(self.total_input.text())
        agregar_compra(id_proveedor, fecha, total)
        cargar_compras(self.table)

    def actualizar_compra(self):
        if hasattr(self, 'selected_id'):
            id_compra = self.selected_id
            id_proveedor = self.id_proveedor_input.text()
            fecha = self.fecha_input.text()
            total = float(self.total_input.text())
            actualizar_compra(id_compra, id_proveedor, fecha, total)
            cargar_compras(self.table)

    def eliminar_compra(self):
        if hasattr(self, 'selected_id'):
            id_compra = self.selected_id
            eliminar_compra(id_compra)
            cargar_compras(self.table)
            self.id_proveedor_input.clear()
            self.fecha_input.clear()
            self.total_input.clear()

def cargar_detalles_compra(table_widget):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Detalles_Compra")
    rows = cursor.fetchall()
    table_widget.setRowCount(len(rows))
    for i, row in enumerate(rows):
        for j, cell in enumerate(row):
            table_widget.setItem(i, j, QTableWidgetItem(str(cell)))
    conn.close()

def agregar_detalle_compra(id_compra, id_producto, cantidad, precio_unitario):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Detalles_Compra (id_compra, id_producto, cantidad, precio_unitario)
        VALUES (%s, %s, %s, %s)
    """, (id_compra, id_producto, cantidad, precio_unitario))
    conn.commit()
    conn.close()

def actualizar_detalle_compra(id_detalle, id_compra, id_producto, cantidad, precio_unitario):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE Detalles_Compra
        SET id_compra = %s, id_producto = %s, cantidad = %s, precio_unitario = %s
        WHERE id_detalle = %s
    """, (id_compra, id_producto, cantidad, precio_unitario, id_detalle))
    conn.commit()
    conn.close()

def eliminar_detalle_compra(id_detalle):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Detalles_Compra WHERE id_detalle = %s", (id_detalle,))
    conn.commit()
    conn.close()

class DetallesCompraApp(CRUDWindow):
    def __init__(self, main_menu):
        super().__init__(main_menu, "Gestión de Detalles de Compra")
        self.init_ui()
    
    def init_ui(self):
        main_layout = QVBoxLayout()

        form_layout = QFormLayout()
        self.id_compra_input = QLineEdit()
        self.id_producto_input = QLineEdit()
        self.cantidad_input = QLineEdit()
        self.precio_unitario_input = QLineEdit()

        form_layout.addRow("ID Compra:", self.id_compra_input)
        form_layout.addRow("ID Producto:", self.id_producto_input)
        form_layout.addRow("Cantidad:", self.cantidad_input)
        form_layout.addRow("Precio Unitario:", self.precio_unitario_input)

        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Agregar")
        self.update_button = QPushButton("Actualizar")
        self.delete_button = QPushButton("Eliminar")

        self.add_button.clicked.connect(self.add_detalle)
        self.update_button.clicked.connect(self.update_detalle)
        self.delete_button.clicked.connect(self.delete_detalle)

        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.delete_button)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID Detalle", "ID Compra", "ID Producto", "Cantidad", "precio unitario"])
        self.table.cellClicked.connect(self.load_inputs_from_table)
        cargar_detalles_compra(self.table)

        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.table)
        
        self.add_back_button(main_layout)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def load_inputs_from_table(self, row, column):
        self.selected_id = self.table.item(row, 0).text()
        self.id_compra_input.setText(self.table.item(row, 1).text())
        self.id_producto_input.setText(self.table.item(row, 2).text())
        self.cantidad_input.setText(self.table.item(row, 3).text())
        self.precio_unitario_input.setText(self.table.item(row, 4).text())

    def add_detalle(self):
        id_compra = self.id_compra_input.text()
        id_producto = self.id_producto_input.text()
        cantidad = int(self.cantidad_input.text())
        precio_unitario = float(self.precio_unitario_input.text())
        agregar_detalle_compra(id_compra, id_producto, cantidad, precio_unitario)
        cargar_detalles_compra(self.table)

    def update_detalle(self):
        if hasattr(self, 'selected_id'):
            id_detalle = self.selected_id
            id_compra = self.id_compra_input.text()
            id_producto = self.id_producto_input.text()
            cantidad = int(self.cantidad_input.text())
            precio_unitario = float(self.precio_unitario_input.text())
            actualizar_detalle_compra(id_detalle, id_compra, id_producto, cantidad, precio_unitario)
            cargar_detalles_compra(self.table)

    def delete_detalle(self):
        if hasattr(self, 'selected_id'):
            id_detalle = self.selected_id
            eliminar_detalle_compra(id_detalle)
            cargar_detalles_compra(self.table)
            self.clear_inputs()
    
    def clear_inputs(self):
        self.id_compra_input.clear()
        self.id_producto_input.clear()
        self.cantidad_input.clear()
        self.precio_unitario_input.clear()

       
class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Menú Principal - Papelería")
        self.setGeometry(100, 100, 400, 550) 
        self.init_ui()
        
        self.product_window = ProductApp(self)
        self.supplier_window = SupplierApp(self)  
        self.client_window = ClientApp(self)
        self.ventas_window = VentasApp(self)
        self.compras_window = ComprasApp(self)
        self.detalles_venta_window = DetallesVentaApp(self)
        self.detalles_compra_window = DetallesCompraApp(self)

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)
        
        title = QLabel("Sistema de Papelería")
        title.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                color: #333;
                padding-bottom: 20px;
            }
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        button_style = """
            QPushButton {
                padding: 12px;
                font-size: 14px;
                min-width: 250px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """
        btn_productos = QPushButton("Gestión de Productos")
        btn_productos.setStyleSheet(button_style)  

        btn_proveedores = QPushButton("Gestión de Proveedores")
        btn_proveedores.setStyleSheet(button_style)

        btn_clientes = QPushButton("Gestión de Clientes")
        btn_clientes.setStyleSheet(button_style) 

        btn_ventas = QPushButton("Ventas")
        btn_ventas.setStyleSheet(button_style)

        btn_compras = QPushButton("Compras")
        btn_compras.setStyleSheet(button_style)

        btn_detalles_venta = QPushButton("Detalles de Ventas")
        btn_detalles_venta.clicked.connect(self.show_detalles_venta)

        btn_detalles_compra = QPushButton("Detalles de Compras")
        btn_detalles_compra.clicked.connect(self.show_detalles_compra)


        for btn in [btn_productos, btn_proveedores, btn_clientes, btn_ventas, btn_compras, btn_detalles_venta, btn_detalles_compra]:
            btn.setStyleSheet(button_style)
        
        btn_productos.clicked.connect(self.show_products)
        btn_proveedores.clicked.connect(self.show_suppliers)
        btn_clientes.clicked.connect(self.show_clients)
        btn_ventas.clicked.connect(self.show_ventas)
        btn_compras.clicked.connect(self.show_compras)
        btn_detalles_venta.clicked.connect(self.show_detalles_venta)
        btn_detalles_compra.clicked.connect(self.show_detalles_compra)
        
        
        layout.addWidget(btn_productos)
        layout.addWidget(btn_proveedores)
        layout.addWidget(btn_clientes)
        layout.addWidget(btn_ventas)
        layout.addWidget(btn_compras)
        layout.addWidget(btn_detalles_venta)
        layout.addWidget(btn_detalles_compra)
        
        exit_btn = QPushButton("🚪 Salir del Sistema")
        exit_btn.setStyleSheet("""
            QPushButton {
                padding: 12px;
                background-color: #f44336;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
        """)
        exit_btn.clicked.connect(self.close)
        layout.addWidget(exit_btn)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def show_products(self):
        self.hide()
        self.product_window.show()

    def show_suppliers(self): 
        self.hide()
        self.supplier_window.show()
    
    def show_clients(self): 
        self.hide()
        self.client_window.show()

    def show_ventas(self):
        self.hide()
        self.ventas_window.show()

    def show_compras(self):
        self.hide()
        self.compras_window.show()
    def show_detalles_venta(self):
        self.hide()
        self.detalles_venta_window.show()
        
    def show_detalles_compra(self):
        self.hide()
        self.detalles_compra_window.show()           
 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    main_menu = MainMenu()
    main_menu.show()
    
    sys.exit(app.exec())
