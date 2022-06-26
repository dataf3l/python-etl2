import pandas as pd
import pyodbc

# Import CSV
data = pd.read_csv (r'Prestadores.csv',sep=';' , encoding = "ISO-8859-1", engine='python' , error_bad_lines=False)     
df = pd.DataFrame(data)

# Connect to SQL Server
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=LAPTOP-A39OPMT9\SQLEXPRESS01;'
                      'Database=prestadores;'
                      'Trusted_Connection=yes;')
cursor = conn.cursor()

# Create Table
cursor.execute('''
		CREATE TABLE products (
			product_id int ,
            depa_nombre int,
            muni_nombre nvarchar(50),
            codigo_habilitacion int primary key,
            nombre_prestador nvarchar(50),
            tido_codigo nvarchar(50),
            nits_nit int,
            razon_social nvarchar(50),
            clpr_codigo int,
            clpr_nombre nvarchar(50),
            ese nvarchar(50),
            direccion nvarchar(50),
            telefono int,
            fax int,
            email nvarchar(50),
            gerente nvarchar(50),
            nivel int,
            caracter nvarchar(50),
            habilitado nvarchar(50),
            fecha_radicacion int,
            fecha_vencimiento int,
            fecha_cierre int,
            dv int,
            clase_persona nvarchar(50),
            naju_codigo int,
            naju_nombre nvarchar(50),
            numero_sede_principal int,
            fecha_corte_REPS
            telefono_adicional int,
            email_adicional nvarchar(50),
            rep_legal nvarchar(50),
			)
               ''')

# Insert DataFrame to Table
for row in df.itertuples():
    cursor.execute('''
                INSERT INTO products (depa_nombre,muni_nombre,codigo_habilitacion,tido_codigo,nits_nit,razon_social,clpr_codigo,clpr_nombre,ese,direccion,telefono,fax,email,gerente,nivel,caracter,habilitado,fecha_radicacion,fecha_vencimiento,fecha_cierre,dv,clase_persona,naju_codigo,naju_nombre,numero_sede_principal,fecha_corte_REPS,telefono_adicional,email_adicional,rep_legal)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                ''',
                row.depa_nombre,
                row.muni_nombre,
                row.codigo_habilitacion,
                row.nombre_prestador,
                row.tido_codigo,
                row.nits_nit,
                row.razon_social,
                row.clpr_codigo,
                row.clpr_nombre,
                row.ese,
                row.direccion,
                row.telefono,
                row.fax,
                row.email,
                row.gerente,
                row.nivel,
                row.caracter,
                row.habilitado,
                row.fecha_radicacion,
                row.fecha_vencimiento,
                row.fecha_cierre,
                row.dv,
                row.clase_persona,
                row.naju_codigo,
                row.naju_nombre,
                row.numero_sede_principal,
                row.fecha_corte_REPS,
                row.telefono_adicional,
                row.email_adicional,
                row.rep_legal
                )
conn.commit()