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
            load_products(self.table)  # Actualizar la tabla

    def delete_product(self):
        row = self.table.currentRow()
        if row >= 0:
            product_id = self.table.item(row, 0).text()
            delete_product(product_id)
            load_products(self.table)  # Actualizar la tabla

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProductApp()
    window.show()
    sys.exit(app.exec())
