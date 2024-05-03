# **Price Tracker** 💸

![banner_proyecto](images/Data_banner.jpg)

## Contexto 📈
En algunas ocasiones es dificil encontrar la mejor oferta y tener la certeza de que lo que estamos comprando esta al mejor precio. Muchas veces el querer saber el historial de precion de algunas plataformas conlleva el pagar por esta informacion. Lo ideal seria generar nuestra propia informacion y asi poder saber con certeza que estamos encontrando una verdadera ofera que vale la pena. Sin emgargo, muchas veces las mejores ofertas en precios suceden en un lapso de tiempo que puede ser horas. Por lo cual tener la informacion mas actual se vuelve vital.

## Objetivo 💢
Se utilizara un webscraping para poder obtener la informacion de precios de un producto, el resultado se alamcenara en una tabla de SQL la cual servira para llevar un rastreo de precio por dia. Adicionalmente se tendra una tabla historica conectada a un tablero para poder visualizar la informacion

## Diagrama del pipeline
![pipeline](images/Diagrama_proto.jpg)

## Acerca del Dataset 🗃️
El conjunto de datos se generara todos los dias en tres horarios para llevar un segumiento diario. Adicionalmente, todos los dias se pasara la informacion a una tabla historico la cual estara conectada a un visulizador en este caso Power Bi el cual nos podra mostrar de manera grafica las variaciones que ha sufrido el precio del producto asi como el rate de los comment que tiene.

## 🔗 Link importantes 🔗
1. [Link a la pagina de extraccion](https://www.amazon.com.mx/s?k=samsung+a54+desbloquedo&rh=n%3A9687460011&__mk_es_MX=%C3%85M%C3%85%C5%BD%C3%95%C3%91&ref=nb_sb_noss)
2. [Base da datos Duckdb](../scripts/products_base.duckdb)
3. [Archivo con la descripcion del proyecto](../doc/proyecto.md)
4. [PDF presentación del proyecto]()
5. [Visualizador de datos en Power Bi]()



Creado por Sergio Maldonado Rodriguez
