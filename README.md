# Meu Plano de Desenvolvimento Individual (PDI)
Este repositório contém meu PDI e outros documentos importantes para meu desenvolvimento profissional.

Detalhes e Funcionalidades:
Configuração da API Gemini:

import os, import json, import pathlib, from dotenv import load_dotenv, import google.generativeai as genai: Importa os módulos necessários para manipulação de variáveis de ambiente, JSON, caminhos de arquivo e a biblioteca do Google Gemini.

load_dotenv(): Carrega as variáveis de ambiente de um arquivo .env, o que é crucial para manter chaves de API seguras e fora do código-fonte versionado no Git.

API_KEY = os.getenv("GEMINI_API_KEY"): Obtém a chave da API Gemini da variável de ambiente, garantindo que o acesso à API seja configurado corretamente. A verificação if not API_KEY: raise RuntimeError(...) assegura que o programa não continue sem a chave.

genai.configure(api_key=API_KEY): Configura a biblioteca Gemini com a chave da API.

model = genai.GenerativeModel("gemini-1.5-flash"): Inicializa o modelo de IA específico (gemini-1.5-flash) que será usado para gerar os PDIs.

Função generate_pdi_plan(responses):

Propósito: Esta função é a peça central para a geração do PDI. Ela recebe uma lista de respostas do usuário (responses) e as formata em um prompt para o modelo Gemini.

Criação do Prompt: Constrói um prompt detalhado que instrui o modelo de IA a atuar como um "consultor de carreira" e a gerar um PDI com seções específicas: metas SMART, competências a desenvolver, ações recomendadas, prazos e indicadores de sucesso.

Geração de Conteúdo: Utiliza o model.generate_content(prompt, ...) para enviar o prompt ao Gemini e obter a resposta gerada. A generation_config={ "temperature": 0.4 } indica uma temperatura baixa, visando respostas mais focadas e menos criativas, ideal para um PDI estruturado.

Retorno: Retorna o texto do PDI gerado, limpo de espaços extras.

Função faq_cert(cert_name):

Propósito: Fornece informações detalhadas sobre certificações.

Leitura de Dados: Lê o arquivo certs.json (presumivelmente um arquivo JSON que armazena informações de certificações) usando pathlib.Path("certs.json").read_text().

Busca de Informações: Tenta encontrar a certificação pelo cert_name fornecido.

Formatação da Saída: Se a certificação for encontrada, formata uma string amigável com o nome, código do exame, descrição e links de estudo. Caso contrário, retorna uma mensagem de erro.

Relevância para o Git:
Separação de Preocupações: Este módulo mantém a lógica de integração com a IA e a manipulação de dados de certificações separadas da interface do usuário, facilitando a manutenção e o teste.

Gerenciamento de Credenciais: O uso de .env e os.getenv demonstra boas práticas de segurança, evitando que chaves de API sensíveis sejam versionadas no repositório Git, o que é crucial para a segurança do projeto.

Modelo de Geração: A função generate_pdi_plan é o algoritmo central para a criação do PDI, sendo um componente chave que evoluirá com o tempo (novas versões do modelo, prompts mais elaborados, etc.).

Código 2: main.py (Interface de Linha de Comando e Orquestrador)
Este arquivo (que seria o arquivo principal ou main.py em uma estrutura de projeto típica) atua como a interface de linha de comando (CLI) do aplicativo, usando a biblioteca Typer. Ele orquestra a interação com o usuário, invoca as funções de lógica de negócio e gerencia o salvamento das sessões.

Detalhes e Funcionalidades:
Importações Essenciais:

import json, random, datetime: Módulos padrão para lidar com JSON, aleatoriedade (para simulados) e datas.

import typer: Importa a biblioteca Typer, que facilita a criação de aplicações de linha de comando interativas.

from pathlib import Path: Para manipulação de caminhos de arquivo de forma orientada a objetos.

from ia import generate_pdi_plan, faq_cert: Importa as funções chave do módulo ia.py (o primeiro código analisado), demonstrando a modularidade do projeto.

from storage import save_session: Importa a função para salvar dados, presumindo a existência de um módulo storage.py.

Configuração do Typer:

app = typer.Typer(): Inicializa a aplicação Typer, que gerenciará os comandos.

QUESTIONS_FILE = Path("questions.json"): Define o caminho para o arquivo JSON que contém as perguntas da entrevista do PDI.

Comando pdi():

Propósito: Inicia a entrevista para a criação do PDI e gera o plano.

Carregamento de Perguntas: Lê as perguntas de questions.json.

Interação com o Usuário: Usa typer.prompt() para fazer cada pergunta ao usuário e coleta as respostas.

Geração do PDI: Chama generate_pdi_plan(responses) (do módulo ia.py) para obter o texto do PDI.

Exibição: Imprime o PDI gerado no terminal com formatação colorida (typer.secho).

Salvamento de Sessão: Extrai o e-mail do usuário e chama save_session() para persistir as respostas e o PDI gerado em um arquivo (presumivelmente pdi_data.json), incluindo um timestamp.

Comando faq(cert_name: str):

Propósito: Permite que o usuário consulte informações sobre uma certificação específica.

Interação: Recebe o nome da certificação como argumento de linha de comando.

Busca de FAQ: Chama faq_cert(cert_name) (do módulo ia.py) e exibe o resultado.

Comando simulado(cert_name: str = "comptia_itf", n: int = 5):

Propósito: Oferece a funcionalidade de um simulado rápido de questões de certificação.

Carregamento de Questões: Carrega questões de um arquivo JSON específico para a certificação (exams/{cert_name}.json). Inclui tratamento de erro se o arquivo não existir.

Seleção de Questões: Usa random.sample() para selecionar um número (n) de questões.

Loop de Perguntas: Apresenta cada questão e suas opções, pedindo a resposta do usuário.

Cálculo da Pontuação: Verifica as respostas, calcula a pontuação e exibe o resultado com cores (verde para aprovação, vermelho para reprovação).

Questões Incorretas: Lista as questões erradas com as respostas corretas para revisão.

if __name__ == "__main__": app():

Ponto de entrada do aplicativo Typer, garantindo que os comandos sejam executados quando o script for chamado diretamente.

Relevância para o Git:
Interface do Usuário (CLI): Este arquivo define como os usuários interagem com o sistema, sendo o ponto de acesso principal para as funcionalidades.

Modularidade e Dependências: A forma como ele importa funções de ia.py e storage.py demonstra uma arquitetura modular, facilitando o desenvolvimento colaborativo e a organização do código no repositório.

Versionamento de Funcionalidades: Cada comando (pdi, faq, simulado) representa uma funcionalidade distinta que pode ser desenvolvida e versionada independentemente dentro do ciclo de vida do projeto Git.

Persistência de Dados: O salvamento das sessões (save_session) é crucial para manter um histórico das interações do usuário e dos PDIs gerados, o que pode ser útil para futuras análises ou recuperação.
