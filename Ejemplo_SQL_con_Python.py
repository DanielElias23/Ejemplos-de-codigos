import sqlite3    #Se conecta con el gestor SQLite
import pandas as pd
import matplotlib.pyplot as plt

#Se conecta con la base de datos Northwind.db, alfinal se debe
#desconectar, conn es una variable cualquiera, la coneccion se queda
#en forma de vairable
conn = sqlite3.connect("Northwind.db")

#Para hacer la consulta, query es solo una variable cualquiera que contiee
#la consulta
query = """ SELECT ProductName, SUM(Price * Quantity) as Revenue
   FROM OrderDetails od
   JOIN Products p ON p.ProductID = od.ProductID
   GROUP BY od.ProductID
   ORDER BY Revenue DESC
   LIMITE 10 """

#Para leer la consulta de SQL
top_products = pd.read_sql_query(query,conn)

#Para hacer un plot con la consulta
top_products.plot(x="ProductName", y="Revenue", kind="bar", figsize=(10,5), legend=False)

plt.title("10 Productos más rentables")
plt.xlabel("Productos")
plt.ylabel("Revenue")
#Para rotar los nombres en 90° en el eje x
plt.xticks(rotation=90)

plt.show()


#Se puede seguir haciendo consultas porque la coneccion no se ha
#detenido, se debe hacer otra variable query

#desconecta la coneccion
conn.close()


#--------------------------------------------------------------------------------------------
#Para hacer funciones en python que se utilicen en la consulta

#import sqlite3
#import pandas as pd

#definimos una funcion
#K(x) = x^2
Square = Lambda n: n*n

#Se ocupa como Square(x), tambien puede definirse con def

conn = sqlite3.connect("Northwind.db")

#Crea una funcion para utilizar en la base de datos
#square de la izquierda es el nombre de la funcion, el de la derecha es la funcion entregada
conn.create_function("square",1, square)

#Crea una consulta y la almacena en cursor, se deben cerrar
cursor = conn.cursor()
cursor.execute("""
               SELECT *, square(Price) FROM Products""")

#El resulado de la consulta de obtiene por fetchall() almacenado en results
#pero se entrega en forma de lista con tuplas, no se muestra como tabla
results = cursor.fetchall()

#Los ordena muy similar para visual como tablas de SQL
results_df = pd.DataFrame(results)

#hace efectivo cualquier tipo de cambio
conn.commit()

#cierra la coneccion con el cursor
cursor.close()

conn.close()


#------------------------------------------------------------------------------------------
#Se puede crear un contexto para evitar crear conecciones

#import sqlite3
#importa pandas as pd

with sqlite3.connect("Northwind.db") as conn:
    conn.create_function("square", 1, square)
    cursor = conn.cursor()
    cursor.execute("SELECT *, square(Price) FROM Products")
    results = cursor.fetchall()
    results_df = pd.DataFrame(results)

print(results_df)

#aca no se cierran automaticamente las conecciones

