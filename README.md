<p align="left">
  <a href="https://github.com/Abraham089/backend-workpal/actions/workflows/ci.yml"><img src="https://github.com/Abraham089/backend-workpal/actions/workflows/ci.yml/badge.svg" alt="CI/CD Pipeline" /></a>
  <img src="https://img.shields.io/badge/python-3.12-blue" alt="Python Version" />
  <a href="https://sonarcloud.io/summary/new_code?id=Abraham089_backend-workpal"><img src="https://sonarcloud.io/api/project_badges/measure?project=Abraham089_backend-workpal&metric=alert_status&token=095b7288b35cf14d1974a68839c3bebea9bfe4a7" alt="Quality Gate Status" /></a>
  <a href="https://sonarcloud.io/summary/new_code?id=Abraham089_backend-workpal"><img src="https://sonarcloud.io/api/project_badges/measure?project=Abraham089_backend-workpal&metric=coverage&token=095b7288b35cf14d1974a68839c3bebea9bfe4a7" alt="Coverage" /></a>
</p>

<h1>Proyecto: Workpal</h1>

<h2>1. Proposito central:</h2>
<p>Crear una API REST para gestion de proyectos</p>

<h2>

<h2>2. Tech Stack</h2>
<ul>
<li><b>Lenguaje:</b> Python 3.12</li>
<li><b>Framework:</b> FastAPI</li>
<li><b>ORM:</b> SQLModel (SQLAlchemy Core)</li>
<li><b>Base de datos:</b> SQLite (dev/test) / PostgreSQL (producción)</li>
<li><b>Gestor de paquetes:</b> Poetry</li>
<li><b>Testing & Calidad:</b> Pytest, pytest-cov, SonarQube Cloud, pip-audit</li>
<li><b>Contenedores y Orquestación:</b> Docker, Docker Compose, Kubernetes</li>
</ul>

<h2>3. Requisitos previos</h2>

<ul>
<li>Python 3.12</li>
<li>Poetry</li>
<li>Docker y Kubernetes</li>
</ul>

<h2>4. Instalación y Configuración Local</h2>

<p>**Clonar repositorio</p>

<p>git clone url-repo</p>
<p>cd backend-workpal</p>

<p>**Instalar dependencias con Poetry</p>

<p>poetry install</p>

<p>**Configurar variables de entorno</p>

<p>cp .env.example .env</p>

<h2>5. Pruebas y Cobertura (Testing)</h2>

<p>**Correr todos los tests</p>
<p>poetry run pytest</p>

<p>**Correr tests con reporte de cobertura en consola</p>
<p>poetry run pytest --cov=src/backend_workpal --cov-report=term-missing</p>

<h2>6. Flujo de CI/CD y Calidad de Código</h2>

<ul>
<li><b>Job 1 (SonarQube):</b> Analisis estático de codigo, Quality Gate y cobertura mínima requerida</li>

<li><b>Job 2 (Dependencies):</b> Auditoria de vulnerabilidades con pip-audit</li>
</ul>

<h2>7. Estructura del proyecto</h2>
<p><b>src/backend_workpal/api/v1/:</b> Rutas, modelos y servicios por módulo</p>

<p><b>src/backend_workpal/core/:</b> Configuración (config.py), seguridad (security.py), middleware</p>

<p><b>src/backend_workpal/database/:</b> Conexión de base de datos y sesiones</p>

<p><b>tests/:</b> Fixtures globales en conftest.py y pruebas unitarias/integración</p>
