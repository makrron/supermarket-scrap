import csv
import json
import os
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium_stealth import stealth

"""
Este es un Script que se encarga de hacer el Scraping 
en los sitios de los supermercados para obtener
los precios de los supermercados.
"""

def create_driver() -> webdriver:
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--start-maximized")
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-dev-shm-using")
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("--disable-setuid-sandbox")
    options.add_argument('--headless')
    options.add_argument("enable-features=NetworkServiceInProcess")
    options.add_argument("disable-features=NetworkService")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--ignore-ssl-errors")
    options.add_argument("--force-device-scale-factor=1")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    d = webdriver.Chrome(options=options)

    stealth(d,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )
    return d


# funcion para scrapear carrefour
def scrap_carrefour(category, url):
    driver = create_driver()

    try:
        driver.get(url)
        # wait 5 seconds
        time.sleep(60)
        # hace scroll para que cargue toda la pagina
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # espera 5 segundos
        time.sleep(60)
        # obtiene el html de la pagina
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        # el producto se encuentra en la clase "product-card-list__item" con el tag "li"
        products = soup.find_all("li", class_="product-card-list__item")
        # products = BeautifulSoup(str(products), 'html.parser')
        # recorre los productos para extraer la informacion (nombre, precio, imagen, url)

        list = []
        for product in products:
            # print(product)
            soup = BeautifulSoup(str(product), 'html.parser')

            # Obtener el nombre del producto
            name_element = soup.find('h2', class_='product-card__title')
            name = name_element.text.strip() if name_element else None

            # Obtener el precio del producto
            price_element = soup.find('span', class_='product-card__price')
            price = price_element.text.strip() if price_element else None

            # Obtener la URL del producto
            url_element = soup.find('a', class_='product-card__title-link')
            url = "https://www.carrefour.es" + url_element['href'] if url_element else None

            # Obtener la imagen del producto
            image_element = soup.find('img', class_='product-card__image')
            image = image_element['src'] if image_element else None

            supermarket = 'Carrefour'  # Puedes ajustar esto según la información disponible en tu HTML

            if price is None or name is None or url is None or image is None:
                continue
            else:
                # Crear el diccionario con la información recopilada
                product = {
                    "name": name,
                    "price": price,
                    "image": image,
                    "url": url,
                    "category": category,
                    "supermarket": supermarket
                }
                list.append(product)

            # Save the list of products to a CSV file
        keys = list[0].keys()
        with open('products_carrefour.csv', 'a', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(list)

            return list
    except Exception as e:
        print(e)
    finally:
        driver.quit()


def scrap_alcampo(category, url):
    driver = create_driver()

    try:
        driver.get(url)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        products = soup.find_all("div", class_="components__OuterContainer-sc-filq44-0 htPSZi")
        list = []
        for product in products:
            # Get product name
            name_element = product.find('h3', class_='text__Text-sc-6l1yjp-0 iWlLMY')
            name = name_element.text.strip() if name_element else None

            # Get product price
            price_element = product.find('span', class_='text__Text-sc-6l1yjp-0 price__PriceText-sc-1nlvmq9-0 iWlLMY hkHDcF')
            price = price_element.text.strip() if price_element else None

            price = str(price).replace('\xa0', '')

            # Get product URL
            url_element = product.find('a', class_='link__Link-sc-14ymsi2-0 dFTuAW')
            url = "https://www.compraonline.alcampo.es" + url_element['href'] if url_element else None

            # Get product image
            image_element = product.find('img', class_='image__StyledLazyLoadImage-sc-wislgi-0 foQxui')
            image = image_element['src'] if image_element else None

            supermarket = 'Alcampo'

            if price is None or name is None or url is None or image is None:
                continue
            else:
                product = {
                    "name": name,
                    "price": price,
                    "image": image,
                    "url": url,
                    "category": category,
                    "supermarket": supermarket
                }
                list.append(product)

        keys = list[0].keys()
        with open('products_alcampo.csv', 'a', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)

            # Check if the file is empty
            if os.stat('products_alcampo.csv').st_size == 0:
                dict_writer.writeheader()

            dict_writer.writerows(list)

        return list

    except Exception as e:
        print(e)
    finally:
        driver.quit()

def get_carrefour_products():
    carrefour_list = []
    carrefour_list.append(
        scrap_carrefour("Carniceria", "https://www.carrefour.es/supermercado/productos-frescos/carniceria/cat20018/c"))

    carrefour_list.append(scrap_carrefour("Carniceria",
                                          "https://www.carrefour.es/supermercado/productos-frescos/carniceria/cat20018/c?offset=48"))
    carrefour_list.append(scrap_carrefour("Carniceria",
                                          "https://www.carrefour.es/supermercado/productos-frescos/carniceria/cat20018/c?offset=72"))
    carrefour_list.append(scrap_carrefour("Carniceria",
                                          "https://www.carrefour.es/supermercado/productos-frescos/carniceria/cat20018/c?offset=96"))

    carrefour_list.append(
        scrap_carrefour("Pescaderia", "https://www.carrefour.es/supermercado/productos-frescos/pescaderia/cat20014/c"))
    carrefour_list.append(scrap_carrefour("Pescaderia",
                                          "https://www.carrefour.es/supermercado/productos-frescos/pescaderia/cat20014/c?offset=48"))
    carrefour_list.append(scrap_carrefour("Pescaderia",
                                          "https://www.carrefour.es/supermercado/productos-frescos/pescaderia/cat20014/c?offset=72"))
    carrefour_list.append(scrap_carrefour("Pescaderia",
                                          "https://www.carrefour.es/supermercado/productos-frescos/pescaderia/cat20014/c?offset=96"))

    carrefour_list.append(
        scrap_carrefour("Frutas", "https://www.carrefour.es/supermercado/productos-frescos/frutas/cat220006/c"))
    carrefour_list.append(scrap_carrefour("Frutas",
                                          "https://www.carrefour.es/supermercado/productos-frescos/frutas/cat220006/c?offset=48"))
    carrefour_list.append(scrap_carrefour("Frutas",
                                          "https://www.carrefour.es/supermercado/productos-frescos/frutas/cat220006/c?offset=72"))
    carrefour_list.append(scrap_carrefour("Frutas",
                                          "https://www.carrefour.es/supermercado/productos-frescos/frutas/cat220006/c?offset=96"))

    carrefour_list.append(scrap_carrefour("Verduras y hortalizas",
                                          "https://www.carrefour.es/supermercado/productos-frescos/verduras-y-hortalizas/cat220014/c"))
    carrefour_list.append(scrap_carrefour("Verduras y hortalizas",
                                          "https://www.carrefour.es/supermercado/productos-frescos/verduras-y-hortalizas/cat220014/c?offset=48"))
    carrefour_list.append(scrap_carrefour("Verduras y hortalizas",
                                          "https://www.carrefour.es/supermercado/productos-frescos/verduras-y-hortalizas/cat220014/c?offset=72"))
    carrefour_list.append(scrap_carrefour("Verduras y hortalizas",
                                          "https://www.carrefour.es/supermercado/productos-frescos/verduras-y-hortalizas/cat220014/c?offset=96"))

    carrefour_list.append(scrap_carrefour("Panaderia Tradicional",
                                          "https://www.carrefour.es/supermercado/productos-frescos/panaderia-tradicional/cat20019/c"))
    carrefour_list.append(scrap_carrefour("Panaderia Tradicional",
                                          "https://www.carrefour.es/supermercado/productos-frescos/panaderia-tradicional/cat20019/c?offset=48"))
    carrefour_list.append(scrap_carrefour("Panaderia Tradicional",
                                          "https://www.carrefour.es/supermercado/productos-frescos/panaderia-tradicional/cat20019/c?offset=72"))
    carrefour_list.append(scrap_carrefour("Panaderia Tradicional",
                                          "https://www.carrefour.es/supermercado/productos-frescos/panaderia-tradicional/cat20019/c?offset=96"))

    carrefour_list.append(scrap_carrefour("Charcuteria",
                                          "https://www.carrefour.es/supermercado/productos-frescos/charcuteria/cat20017/c"))
    carrefour_list.append(scrap_carrefour("Charcuteria",
                                          "https://www.carrefour.es/supermercado/productos-frescos/charcuteria/cat20017/c?offset=48"))
    carrefour_list.append(scrap_carrefour("Charcuteria",
                                          "https://www.carrefour.es/supermercado/productos-frescos/charcuteria/cat20017/c?offset=72"))
    carrefour_list.append(scrap_carrefour("Charcuteria",
                                          "https://www.carrefour.es/supermercado/productos-frescos/charcuteria/cat20017/c?offset=96"))

    carrefour_list.append(scrap_carrefour("Charcuteria y Quesos al Corte",
                                          "https://www.carrefour.es/supermercado/productos-frescos/charcuteria-y-quesos-al-corte/cat510001/c"))
    carrefour_list.append(scrap_carrefour("Charcuteria y Quesos al Corte",
                                          "https://www.carrefour.es/supermercado/productos-frescos/charcuteria-y-quesos-al-corte/cat510001/c?offset=48"))
    carrefour_list.append(scrap_carrefour("Charcuteria y Quesos al Corte",
                                          "https://www.carrefour.es/supermercado/productos-frescos/charcuteria-y-quesos-al-corte/cat510001/c?offset=72"))
    carrefour_list.append(scrap_carrefour("Charcuteria y Quesos al Corte",
                                          "https://www.carrefour.es/supermercado/productos-frescos/charcuteria-y-quesos-al-corte/cat510001/c?offset=96"))

    carrefour_list.append(
        scrap_carrefour("Quesos", "https://www.carrefour.es/supermercado/productos-frescos/quesos/cat20020/c"))
    carrefour_list.append(scrap_carrefour("Quesos",
                                          "https://www.carrefour.es/supermercado/productos-frescos/quesos/cat20020/c?offset=48"))
    carrefour_list.append(scrap_carrefour("Quesos",
                                          "https://www.carrefour.es/supermercado/productos-frescos/quesos/cat20020/c?offset=72"))
    carrefour_list.append(scrap_carrefour("Quesos",
                                          "https://www.carrefour.es/supermercado/productos-frescos/quesos/cat20020/c?offset=96"))

    carrefour_list.append(scrap_carrefour("Platos Preparados Cocinados",
                                          "https://www.carrefour.es/supermercado/productos-frescos/platos-preparados-cocinados/cat20016/c"))
    carrefour_list.append(scrap_carrefour("Platos Preparados Cocinados",
                                          "https://www.carrefour.es/supermercado/productos-frescos/platos-preparados-cocinados/cat20016/c?offset=48"))
    carrefour_list.append(scrap_carrefour("Platos Preparados Cocinados",
                                          "https://www.carrefour.es/supermercado/productos-frescos/platos-preparados-cocinados/cat20016/c?offset=72"))
    carrefour_list.append(scrap_carrefour("Platos Preparados Cocinados",
                                          "https://www.carrefour.es/supermercado/productos-frescos/platos-preparados-cocinados/cat20016/c?offset=96"))

    with open('products_carrefour.json', 'w') as f:
        json.dump(carrefour_list, f)


def get_alcampo_products():
    scrap_alcampo("Panaderia",
                   "https://www.compraonline.alcampo.es/categories/Frescos/Panader%C3%ADa/OC1281?source=navigation")
    scrap_alcampo("Charcuteria",
                   "https://www.compraonline.alcampo.es/categories/Frescos/Charcuter%C3%ADa/OC15?source=navigation")
    scrap_alcampo("Quesos",
                   "https://www.compraonline.alcampo.es/categories/Frescos/Quesos/OCQuesos?source=navigation")
    scrap_alcampo("Carniceria",
                   "https://www.compraonline.alcampo.es/categories/Frescos/Carne/OC13?source=navigation")
    scrap_alcampo("Pescaderia",
                   "https://www.compraonline.alcampo.es/categories/Frescos/Pescados-mariscos-y-moluscos/OC14?source=navigation")
    scrap_alcampo("Verduras y hortalizas",
                   "https://www.compraonline.alcampo.es/categories/Frescos/Verduras-y-hortalizas/OC1702?source=navigation")
    scrap_alcampo("Frutas",
                   "https://www.compraonline.alcampo.es/categories/Frescos/Frutas/OC1701?source=navigation")




# define el main
if __name__ == '__main__':
    # get_carrefour_products()
    # get_alcampo_products()
    get_alcampo_products()