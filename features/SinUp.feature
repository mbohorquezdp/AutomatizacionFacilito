Feature: Crear nuevo usuario en la web

  Como usuario nuevo
  Quiero poder registrarme en la web
  Para acceder a mis funcionalidades restringidas

  Scenario: registro de usuario
    Given el usuario ingresa sus datos al formulario de la inscripción
    When el usuario introduce los datos válidos al formulario
    Then debería ver mensaje de registro exitoso.
