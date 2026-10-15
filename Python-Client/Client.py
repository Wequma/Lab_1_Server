import requests


API_URL = "http://localhost:8000/index.php"


def fetch_products():
    print(f"Звернення до сервера: {API_URL} ...\n")

    try:
        response = requests.get(API_URL, timeout=5)

        if response.status_code == 200:
            api_data = response.json()
            products = api_data.get("products", [])

            print(f"{'ID':<5} | {'Назва':<28} | {'Категорія':<15} | {'Ціна':>10} | {'Наявність':<12}")
            print("-" * 82)

            for product in products:
                product_id = product.get("id", "N/A")
                name = product.get("name", "N/A")
                category = product.get("category", "N/A")
                price = product.get("price", "N/A")
                in_stock = "Є" if product.get("in_stock", False) else "Немає"

                print(
                    f"{product_id:<5} | {name:<28} | {category:<15} | "
                    f"{price:>10} | {in_stock:<12}"
                )

            print("-" * 82)
            print(f"Успішно отримано записів: {len(products)}")
        else:
            print(f"Помилка сервера! Код статусу: {response.status_code}")
            print("Відповідь:", response.text)

    except requests.exceptions.ConnectionError:
        print("Помилка підключення: сервер недоступний.")
        print(
            "Переконайся, що PHP-сервер запущено командою: "
            "php -S localhost:8000 -t API-Server"
        )
    except requests.exceptions.Timeout:
        print("Помилка: час очікування відповіді від сервера вичерпано.")
    except requests.exceptions.RequestException as error:
        print(f"Помилка HTTP-запиту: {error}")
    except ValueError:
        print("Помилка: сервер повернув некоректний JSON.")
    except Exception as error:
        print(f"Непередбачена помилка: {error}")


if __name__ == "__main__":
    fetch_products()
