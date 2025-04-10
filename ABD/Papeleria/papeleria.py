import sys
import mysql.connector
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout
from PyQt6.QtCore import Qt

# Conectar a la base de datos MySQL
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="872004",
        database="PapeleriaDB"
    )

# Función para cargar los productos en la tabla
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

# Función para agregar un producto
def add_product(name, description, price, stock, category):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Productos (nombre, descripcion, precio, stock, categoria)
        VALUES (%s, %s, %s, %s, %s)
    """, (name, description, price, stock, category))
    conn.commit()
    conn.close()

# Función para actualizar un producto
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

# Función para eliminar un producto
def delete_product(product_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Productos WHERE id_producto = %s", (product_id,))
    conn.commit()
    conn.close()

# Interfaz gráfica
class ProductApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CRUD Productos - Papelería")
        self.setGeometry(100, 100, 600, 400)
        self.init_ui()

    def init_ui(self):
        # Layout principal
        main_layout = QVBoxLayout()

        # Formulario para agregar o actualizar productos
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

        # Botones para agregar, actualizar, eliminar
        button_layout = QHBoxLayout()

        self.add_button = QPushButton("Agregar")
        self.add_button.clicked.connect(self.add_product)
        self.update_button = QPushButton("Actualizar")
        self.update_button.clicked.connect(self.update_product)
        self.delete_button = QPushButton("Eliminar")
        self.delete_button.clicked.connect(self.delete_product)

        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.delete_button)

        # Tabla para mostrar los productos
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Nombre", "Descripción", "Precio", "Stock", "Categoría"])

        # Cargar los productos al iniciar
        load_products(self.table)

        # Agregar todo al layout principal
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.table)

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
        load_products(self.table)  # Actualizar la tabla

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

class SupplierApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CRUD Proveedores - Papelería")
        self.setGeometry(150, 150, 600, 400)
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # Formulario
        form_layout = QFormLayout()
        self.name_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.email_input = QLineEdit()
        self.address_input = QLineEdit()

        form_layout.addRow("Nombre:", self.name_input)
        form_layout.addRow("Teléfono:", self.phone_input)
        form_layout.addRow("Email:", self.email_input)
        form_layout.addRow("Dirección:", self.address_input)

        # Botones
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

        # Tabla
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Nombre", "Teléfono", "Email", "Dirección"])
        self.table.cellClicked.connect(self.load_inputs_from_table)

        load_suppliers(self.table)

        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.table)

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

class ClientApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CRUD Clientes - Papelería")
        self.setGeometry(200, 200, 600, 400)
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # Formulario
        form_layout = QFormLayout()
        self.name_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.email_input = QLineEdit()
        self.address_input = QLineEdit()

        form_layout.addRow("Nombre:", self.name_input)
        form_layout.addRow("Teléfono:", self.phone_input)
        form_layout.addRow("Email:", self.email_input)
        form_layout.addRow("Dirección:", self.address_input)

        # Botones
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

        # Tabla
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Nombre", "Teléfono", "Email", "Dirección"])
        self.table.cellClicked.connect(self.load_inputs_from_table)

        load_clients(self.table)

        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.table)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def load_inputs_from_table(self, row, column):
        self.selected_id = self.table.item(row, 0).text()
        self.name_input.setText(self.table.item(row, 1).text())
        self.phone_input.setText(self.table.item(row, 2).text())
        self.email_input.setText(self.table.item(row, 3).text())
        self.address_input.setText(self.table.item(row, 4).text())

    def add_client(self):
        name = self.name_input.text()
        phone = self.phone_input.text()
        email = self.email_input.text()
        address = self.address_input.text()
        add_client(name, phone, email, address)
        load_clients(self.table)

    def update_client(self):
        if hasattr(self, 'selected_id'):
            client_id = self.selected_id
            name = self.name_input.text()
            phone = self.phone_input.text()
            email = self.email_input.text()
            address = self.address_input.text()
            update_client(client_id, name, phone, email, address)
            load_clients(self.table)

    def delete_client(self):
        if hasattr(self, 'selected_id'):
            client_id = self.selected_id
            delete_client(client_id)
            load_clients(self.table)
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

# Función para agregar una venta
def agregar_venta(id_cliente, total, fecha):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Ventas (id_cliente, total, fecha)
        VALUES (%s, %s, %s)
    """, (id_cliente, total, fecha))
    conn.commit()
    conn.close()

# Función para actualizar una venta
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

# Función para eliminar una venta
def eliminar_venta(id_venta):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Ventas WHERE id_venta = %s", (id_venta,))
    conn.commit()
    conn.close()

# Clase para la interfaz gráfica del CRUD de Ventas
class VentasApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CRUD Ventas - Papelería")
        self.setGeometry(250, 250, 600, 400)
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # Formulario
        form_layout = QFormLayout()
        self.id_cliente_input = QLineEdit()
        self.total_input = QLineEdit()
        self.fecha_input = QLineEdit()

        form_layout.addRow("ID Cliente:", self.id_cliente_input)
        form_layout.addRow("Total:", self.total_input)
        form_layout.addRow("Fecha:", self.fecha_input)

        # Botones
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

        # Tabla
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID Venta", "ID Cliente", "Total", "Fecha"])
        self.table.cellClicked.connect(self.cargar_inputs_desde_tabla)

        cargar_ventas(self.table)

        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.table)

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

if __name__ == "__main__":
    app = QApplication(sys.argv)

    product_window = ProductApp()
    product_window.show()

    supplier_window = SupplierApp()
    supplier_window.show()

    client_window = ClientApp()
    client_window.show()

    ventana_venta = VentasApp()
    ventana_venta.show()

    sys.exit(app.exec())
