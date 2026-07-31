# 📊 Planilha Autônoma

**Sistema de atualização automática de planilhas Excel**, desenvolvido em Python. A aplicação coleta cotações financeiras em tempo real na web, atualiza um arquivo `.xlsx` diretamente em disco — sem precisar abrir o Excel — e aplica formatação condicional, cores e gráficos automaticamente a cada ciclo.

Projeto de portfólio focado em **automação de processos (RPA leve)**, ideal para relatórios financeiros, dashboards operacionais e rotinas de atualização de dados recorrentes.

---

## ✨ Funcionalidades

- 🌐 **Coleta de dados na web** — busca cotações de moedas e criptoativos (USD/BRL, EUR/BRL, BTC/BRL) via API pública, sem necessidade de chave de acesso.
- 📁 **Atualização direta do arquivo** — a planilha é lida, atualizada e salva com `openpyxl`, sem depender do Excel estar aberto ou instalado.
- 🎨 **Formatação automática** — cabeçalhos estilizados, cores condicionais (verde para alta, vermelho para baixa, amarelo para estabilidade), bordas e larguras de coluna ajustadas.
- 📈 **Gráficos dinâmicos** — um gráfico de linha com o histórico de preços é reconstruído a cada atualização, refletindo sempre os dados mais recentes.
- ⏱️ **Agendamento automático** — usando `schedule`, o sistema roda em loop contínuo, atualizando a planilha em intervalos configuráveis (padrão: 30 minutos), sem intervenção manual.
- 🗂️ **Histórico persistente** — cada execução registra uma nova linha na aba de histórico, criando uma série temporal para análise.
- 📝 **Logging estruturado** — todas as execuções, sucessos e falhas são registrados em arquivo de log e no console.

---

## 🧱 Stack técnica

| Biblioteca  | Uso                                                   |
|-------------|--------------------------------------------------------|
| `openpyxl`  | Leitura, escrita, formatação e geração de gráficos no Excel |
| `requests`  | Requisições HTTP à API de cotações                     |
| `schedule`  | Agendamento e execução recorrente do job de atualização |

Python 3.10+.

---

## 📂 Estrutura do projeto

```
Planilha_Autonoma/
├── main.py                    # Orquestrador: agenda e executa os ciclos de atualização
├── src/
│   ├── config.py               # Configurações (caminhos, API, intervalo, ativos monitorados)
│   ├── data_fetcher.py          # Coleta de dados na web
│   └── spreadsheet_manager.py  # Criação, formatação e atualização da planilha
├── data/
│   └── planilha_cotacoes.xlsx  # Gerado automaticamente na primeira execução
├── logs/
│   └── app.log                 # Gerado automaticamente
├── docs/
│   └── DOCUMENTACAO.md         # Documentação técnica detalhada
├── requirements.txt
└── README.md
```

---

## 🚀 Como executar

```bash
# 1. Criar e ativar um ambiente virtual (recomendado)
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Linux/Mac

# 2. Instalar as dependências
pip install -r requirements.txt

# 3. Executar a aplicação
python main.py
```

Ao iniciar, o sistema:
1. Executa uma atualização imediata.
2. Agenda novas atualizações a cada `UPDATE_INTERVAL_MINUTES` (configurável em `src/config.py`).
3. Permanece rodando em segundo plano até ser interrompido (`Ctrl+C`).

A planilha é criada automaticamente em `data/planilha_cotacoes.xlsx` na primeira execução — não é necessário criá-la manualmente.

> 💡 Se o arquivo estiver aberto no Excel no momento de uma atualização, o sistema registra um aviso no log e tenta novamente no próximo ciclo, sem travar ou corromper dados.

---

## ⚙️ Personalização

Todos os parâmetros ficam centralizados em [`src/config.py`](src/config.py):

- **Ativos monitorados**: adicione ou remova pares no dicionário `CURRENCY_PAIRS`.
- **Intervalo de atualização**: altere `UPDATE_INTERVAL_MINUTES`.
- **Limite de histórico**: `MAX_HISTORY_ROWS` controla quantas linhas ficam armazenadas antes de compactar.
- **Fonte de dados**: o padrão usa a AwesomeAPI (gratuita, sem chave), mas `data_fetcher.py` pode ser adaptado para qualquer API REST.

---

## 📄 Documentação

Para detalhes de arquitetura, fluxo de execução e decisões de design, consulte [`docs/DOCUMENTACAO.md`](docs/DOCUMENTACAO.md).

---

## 👤 Autor

Projeto desenvolvido como parte de portfólio de automação e engenharia de software em Python.