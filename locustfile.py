from locust import HttpUser, task, between
import random

class ZomatoHungryUser(HttpUser):
    # Har fake user 0.5 se 1.5 second ke beech mein lagatar order maarega
    wait_time = between(0.5, 1.5)

    @task(3)
    def place_flash_order(self):
        items = ["Chicken Biryani", "Paneer Tikka", "Masala Dosa", "Cheese Pizza", "Cold Coffee"]
        payload = {
            "user_id": random.randint(1000, 99999),
            "item_name": random.choice(items),
            "quantity": random.randint(1, 4),
            "total_price": round(random.uniform(150.0, 800.0), 2),
            "delivery_address": "Hostel Block B, Room 302"
        }
        # Yeh seedha tere POST /orders/ endpoint par hit karega
        self.client.post("/orders/", json=payload)

    @task(1)
    def check_health(self):
        # Beech-beech mein root endpoint bhi check karega
        self.client.get("/")