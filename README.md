<div align="center">

  <a href="">[![Pytest Testing Suite](https://github.com/diverso-lab/uvlhub/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/diverso-lab/uvlhub/actions/workflows/tests.yml)</a>
  <a href="">[![Commits Syntax Checker](https://github.com/diverso-lab/uvlhub/actions/workflows/commits.yml/badge.svg?branch=main)](https://github.com/diverso-lab/uvlhub/actions/workflows/commits.yml)</a>
  
</div>

<div style="text-align: center;">
  <img src="https://www.uvlhub.io/static/img/logos/logo-light.svg" alt="Logo">
</div>

# uvlhub.io

Repository of feature models in UVL format integrated with Zenodo and flamapy following Open Science principles - Developed by DiversoLab

## Official documentation

You can consult the official documentation of the project at [docs.uvlhub.io](https://docs.uvlhub.io/)

## Test execution
# Ejecutar TODOS los tests (unitarios + Selenium)
cd /home/antonio/Desktop/egc_p2_1/uvlhub
venv/bin/pytest -v

# Solo tests unitarios (100% pasan)
venv/bin/pytest -v -k "not selenium"

# Solo tests de Selenium
venv/bin/pytest -v -k selenium

# Test específico
venv/bin/pytest app/modules/auth/tests/test_selenium.py -v
