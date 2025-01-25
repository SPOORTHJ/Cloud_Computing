from products import dao


class Product:
    def __init__(self, id: int, name: str, description: str, cost: float, qty: int = 0):
        self.id = id
        self.name = name
        self.description = description
        self.cost = cost
        self.qty = qty

    @staticmethod
    def load(data):
        """Creates a Product instance from a dictionary."""
        return Product(
            id=data['id'],
            name=data['name'],
            description=data['description'],
            cost=data['cost'],
            qty=data['qty']
        )


def list_products() -> list[Product]:
    """Fetches and returns a list of Product instances."""
    return [Product.load(product) for product in dao.list_products()]


def get_product(product_id: int) -> Product:
    """Fetches and returns a Product instance by ID."""
    data = dao.get_product(product_id)
    if not data:
        raise ValueError(f"Product with ID {product_id} not found.")
    return Product.load(data)


def add_product(product: dict):
    """Adds a new product."""
    if not isinstance(product, dict) or not {'name', 'description', 'cost', 'qty'}.issubset(product):
        raise ValueError("Product dictionary must contain 'name', 'description', 'cost', and 'qty'.")
    dao.add_product(product)


def update_qty(product_id: int, qty: int):
    """Updates the quantity of a product."""
    if qty < 0:
        raise ValueError("Quantity cannot be negative.")
    dao.update_qty(product_id, qty)
