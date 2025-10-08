# Automatización E2E para Shophub Commerce
# URL: ShopHub - Web App: https://shophub-commerce.vercel.app/
# Y pruebas de APIs para Airline
# URL: https://cf-automation-airline-api.onrender.com/
#
# Se considera para este proyecto:
- Automatización de pruebas UI con Selenium WebDriver.
- Automatización de pruebas APIs con Selenium WebDriver.
- Framework modular basado en Page Object Model.
- Validaciones robustas con asserts visuales y manejo de errores.
- Soporte para ejecución en modo gráfico y headless.
- Integración con CI/CD y trazabilidad de resultados.

# Gestión del proyecto
- **Jira**: "Proyecto CF Pruebas automatizadas" Tablero dedicado para seguimiento de historias, bugs y tareas técnicas.
https://acisnerosm.atlassian.net/jira/software/projects/PCPA/boards/3?atlOrigin=eyJpIjoiMWFiYTM0OWUyZTUwNDE0NmJiYTNlNzFiYWMwZGYwODUiLCJwIjoiaiJ9
- **QMetry Test Management**: Ciclo de pruebas documentado con casos vinculados a Jira.
- Trazabilidad entre historias de usuario, casos de prueba y resultados de ejecución.

# Condiciones de instalación del proyecto
- Considerar el archivo "requirements.txt", en ese documento se indicará lo que se debe instalará para el funcionamiento del proyecto

# Estructura del proyecto

    ├── config/
    │   ├── __init__.py
    │   └── settings.py                ← Configuración global (URLs, variables, entorno)
    │
    ├── features/                      ← Enfoque BDD (Behavior Driven Development)
    │   ├── steps/
    │   │   ├── __init__.py
    │   │   └── environment.py         ← Hooks before/after scenarios
    │   └── SignUp.feature             ← Escenarios Gherkin (Given/When/Then)
    │
    ├── pages/                         ← Page Object Model (POM)
    │   └── shophub_commerce/
    │       ├── __init__.py
    │       ├── base_ui_page.py        ← Clase base con funciones genéricas
    │       ├── login_ui_page.py       ← Página de login
    │       ├── cart_ui_page.py        ← Página de carrito
    │       ├── checkout_ui_page.py    ← Página de pago
    │       ├── confirmation_ui_page.py← Página de confirmación
    │       ├── categorias_ui_page.py  ← Categorías de productos
    │       └── productos_electronicos_ui_page.py
    │
    ├── tests/
    │   ├── api_tests/                 ← Pruebas de API REST (PyTest)
    │   │   ├── aircrafts/
    │   │   ├── airports/
    │   │   ├── booking/
    │   │   ├── flights/
    │   │   └── users/
    │   │       └── __init__.py
    │   │
    │   └── pages/                     ← Pruebas UI automatizadas (E2E)
    │       ├── conftest.py            ← Fixtures del navegador
    │       ├── test_1_login.py
    │       ├── test_2_descripcion_producto_electronicos.py
    │       ├── test_3_venta_E2E_OK.py
    │       ├── test_4_cancelar_venta.py
    │       ├── test_5_login_Headless.py
    │       └── test_6_cancelar_venta_Headless.py
    │
    ├── utils/                         ← Librerías de soporte
    │   ├── __init__.py
    │   ├── api_helpers.py             ← Cliente HTTP (GET, POST, etc.)
    │   ├── data_loader.py             ← Carga de datos parametrizados
    │   ├── driver_factory.py          ← Creación del WebDriver
    │   └── schemas.py                 ← Validación de esquemas JSON
    │
    ├── .env                           ← Variables de entorno
    ├── conftest.py                    ← Configuración global Pytest
    ├── pytest.ini                     ← Configuración del framework Pytest
    ├── README.md                      ← Documentación del proyecto
    ├── Requirements.txt               ← Requerimientos del sistema
    └── img.png                        ← Imagen auxiliar para pruebas UI

# Casos de prueba de interfaz de usuario
- test_1_login_GUI: prueba de acceso a a la web con un usuario existente con interfaz gráfica.
- test_2_descripción_producto_electronicos_GUI: prueba donde se muestra identificar las caracteristicas de un producto.
- test_3_venta_E2E_OK_GUI: proceso de venta completa donde se muestra la interfaz gráfica.
- test_4_cancelar_venta_GUI: proceso de cancelar una venta anulando el producto desde el carro de compras con interfaz gráfica.
- test_5_login_Headless: prueba de acceso a a la web con un usuario existente sin interfaz gráfica.
- test_6_cancelar_venta_Headless: proceso de cancelar una venta anulando el producto desde el carro de compras sin interfaz gráfica. 
- test_7_Registro_cliente_web_exitoso_BDD: se usa la prueba de creación de registro en la web de forma exitosa usando BDD.
- test_8_Registro_cliente_web_fallido_BDD: se usa la prueba de creación de registro en la web de forma fallida usando BDD.

# Casos de prueba de APIs
- Test_1_API_Creación de Usuarios_Successful Response_201
- Test_2_API_Creación de Usuarios_Email_ya_existe_400
- Test_3_API_Creación de Usuarios_Email_invalido 422
- Test_4_API_Creación de Usuarios_Email_no_vacio_422
- Test_5_API_Creación de Usuarios_Nombtr no debe ser numero
- Test_6_API_Delete_de Usuarios_caso_positivo_204
- Test_7_API_Delete_de Usuarios_caso_no_autorizado_401
- Test_8_API_Delete_de Usuarios_id_NO_VALIDO
- Test_9_API_Estructura_usuarios_positivos_admin y passenger
- Test_10_API_Estructura_usuarios_casos_negativos
- Test_11_API_Listar_usuarios
- Test_12_API_usuarios_me_Autenticado
- Test_13_API_Listar_usuarios_me_NO_AUTENTICADO
- Test_14_API_UPDATE_usuarios_caso_positivo
- Test_15_API_UPDATE_usuarios_not_found_404
- Test_16_API_UPDATE_usuarios_id_novalido_422
- Test_17_API_AIRPORT_create_caso_positivo
- Test_18_API_AIRPORT_create_caso_negativo
- Test_19_API_AIRPORT_GET_casos_positivos_limit1-5-10
- Test_20_API_AIRPORT_SCHEMA_casos_positivos
- Test_21_API_AIRPORT_LIST_Casos positivos
- Test_22_API_AIRPORT_LIST_casos_negativos
- Test_23_API_AIRPORT_SCHEMA_casos_positivos
- Test_24_API_AIRPORT_SCHEMA_casos_negativos
- Test_25_API_AIRPORT_UPDATE_casos_positivos
- Test_26_API_AIRPORT_UPDATE_casos_negtivos_404,422,401
- Test_27_API_AIRCRAFT_CREAR_CASO_POSITIVO
- Test_28_API_AIRCRAFT_CREAR_CASOS_NEGATIVOS_401,404,422
- Test_29_API_AIRCRAFT_DELETE_CASO_POSITIVO
- Test_30_API_AIRCRAFT_DELETE_CASOS_NEGATIVOS 404,01.422
- Test_31_API_AIRCRAFT_GET_CASO_POSITIVO_200,
- Test_32_API_AIRCRAFT_GET_CASOS_NEGATIVOS_401,404,422
- Test_33_API_AIRCRAFT_LIST_CASO_POSITIVO
- Test_34_API_AIRCRAFT_LIST_CASO_NEGATIVO_422
- Test_35_API_AIRCRAFT_UPDATE_CASO_POSITIVO_200
- Test_36_API_AIRCRAFT_UPDATE_CASO_NEGATIVOS_404,422
- Test_37_API_FLIGHT_CREATE_CASO_POSITIVO
- Test_38_API_FLIGHT_CREATE_CASO_NEGATIVO_401_422
- Test_39_API_FLIGHT_DELETE_CASO_POSITIVO
- Test_40_API_FLIGHT_DELETE_CASO_NEGATIVO_401_422
- Test_41_API_FLIGHT_GET_CASO_POSITIVO
- Test_42_API_FLIGHT_GET_CASO_NEGATIVO_401_422
- Test_43_API_FLIGHT_SEARCH_CASO_POSITIVO
- Test_44_API_FLIGHT_SEARCH_CASO_NEGATIVO_401_422
- Test_45_API_FLIGHT_UPDATE_CASO_POSITIVO
- Test_46_API_FLIGHT_UPDATE_CASO_NEGATIVO_401_422
- Test_47_API_BOOKING_CREATE_CASO_POSITIVO
- Test_48_API_BOOKING_CREATE_CASOS_NEGATIVOS
- Test_49_API_BOOKING_DELETE_CASO_POSITIVO
- Test_50_API_BOOKING_DELETE_CASO_NEGATIVO
- Test_51_API_BOOKING_GET_CASO_POSITIVO
- Test_52_API_BOOKING_GET_CASO_NEGATIVOS_401_422
- Test_53_API_BOOKING_LIST_CASO_POSITIVO_LIMIT_5
- Test_54_API_BOOKING_LIST_CASO_NEGATIVO_NO AUTENTICADO_ERROR EN LIMITE