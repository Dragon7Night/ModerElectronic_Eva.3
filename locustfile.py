import re
import random
from locust import HttpUser, task, between

# Comando para ejecutar las pruebas de rendimiento:
# locust -f locustfile.py

# Acceder a la interfaz web de Locust
# http://localhost:8089

# Acceder a la interfaz web de Silk
# http://localhost:8000/silk/


class UsuarioPublico(HttpUser):
    """
    Usuario que navega como cliente no autenticado.
    Simula navegación básica: home, catálogo y detalle de productos.
    """

    wait_time = between(1, 3)  # tiempo de espera entre requests

    def on_start(self):
        """Se ejecuta cuando un usuario simulado comienza.

        Aquí obtenemos la lista de IDs de productos desde el catálogo.
        """
        self.product_ids = []
        try:
            response = self.client.get("/productos/catalogo-producto/", name="catalogo_inicial")
            if response.status_code == 200:
                # Busca URLs tipo /productos/producto/123/
                ids = re.findall(r"/productos/producto/(\d+)/", response.text)
                self.product_ids = list({int(i) for i in ids})
        except Exception as e:
            # En Locust no queremos romper todo por un error, solo loguear
            print("Error al obtener catálogo inicial:", e)

        if not self.product_ids:
            # Para evitar errores más adelante
            self.product_ids = [1]

    @task(3)
    def ver_home(self):
        self.client.get("/", name="home")

    @task(5)
    def ver_catalogo(self):
        self.client.get("/productos/catalogo-producto/", name="catalogo")

    @task(4)
    def ver_detalle_producto(self):
        if not self.product_ids:
            return
        product_id = random.choice(self.product_ids)
        self.client.get(f"/productos/producto/{product_id}/", name="detalle_producto")
