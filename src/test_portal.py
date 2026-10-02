import pytest
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


@pytest.fixture
def navegador():
    driver = webdriver.Chrome()

    caminho_portal = Path(__file__).resolve().parent / "portal.html"
    driver.get(caminho_portal.as_uri())

    yield driver

    driver.quit()


def test_preencher_formulario(navegador):
    assert navegador.title == "Portal do Colaborador"

    nome = navegador.find_element(By.ID, "nome_usuario")
    email = navegador.find_element(By.ID, "email")
    botao_enviar = navegador.find_element(By.ID, "btn-enviar")

    nome.send_keys("João da Silva")
    email.send_keys("joao.silva@empresa.com")

    botao_enviar.click()

    mensagem = navegador.find_element(By.ID, "msg-sucesso")

    assert mensagem.is_displayed()
    assert mensagem.text == "Dados enviados com sucesso!"


def test_acoes_avancadas_mouse(navegador):
    botao_duplo = navegador.find_element(By.ID, "btn-duplo")

    ActionChains(navegador).double_click(botao_duplo).perform()

    assert botao_duplo.text == "Autorizado!"

    botao_direito = navegador.find_element(By.ID, "btn-direito")

    ActionChains(navegador).context_click(botao_direito).perform()

    assert botao_direito.text == "Menu Aberto!"


def test_acoes_teclado(navegador):
    campo_obs = navegador.find_element(By.ID, "obs")

    campo_obs.click()

    ActionChains(navegador)         .key_down(Keys.CONTROL)         .send_keys("a")         .key_up(Keys.CONTROL)         .send_keys(Keys.BACKSPACE)         .perform()

    campo_obs.send_keys("Teste automatizado finalizado.")

    assert campo_obs.get_attribute("value") == "Teste automatizado finalizado."
