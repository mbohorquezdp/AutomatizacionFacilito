Feature: Crear nuevo usuario en la web

  Como usuario nuevo
  Quiero poder registrarme en la web
  Para acceder a mis funcionalidades restringidas

  Scenario: registro exitoso de usuario
    Given usuario ingresa sus datos al formulario de la inscripción
    When el usuario introduce credenciales válidas
    Then debería ver mensaje de registro exitoso

  Scenario: registro fallido de usuario
    Given usuario ingresa sus datos al formulario de la inscripción
    When el usuario introduce credenciales inválidas
    Then debería ver mensaje de registro erroneo