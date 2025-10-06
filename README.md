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
