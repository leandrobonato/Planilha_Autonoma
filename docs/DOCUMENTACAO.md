# Documentação Técnica — Planilha Autônoma

## 1. Visão geral

A **Planilha Autônoma** é uma aplicação Python que automatiza todo o ciclo de vida de uma planilha de acompanhamento de cotações financeiras: coleta de dados, gravação, formatação visual e geração de gráficos, executando em intervalos regulares sem intervenção humana.

O objetivo é eliminar o processo manual de "abrir a planilha, copiar dados de um site, colar, formatar e salvar", substituindo-o por um serviço que roda em background e mantém o arquivo sempre atualizado.

---

## 2. Arquitetura

```
┌─────────────┐      ┌──────────────────┐      ┌────────────────────────┐
│   main.py   │─────▶│ data_fetcher.py  │─────▶│ spreadsheet_manager.py │
│ (scheduler) │      │ (coleta na web)  │      │ (grava e formata .xlsx)│
└─────────────┘      └──────────────────┘      └────────────────────────┘
       │                                                    │
       ▼                                                    ▼
   schedule                                        data/planilha_cotacoes.xlsx
  (loop a cada N min)                              (Dashboard + Histórico)
```

O sistema segue uma separação clara de responsabilidades (single responsibility):

| Módulo | Responsabilidade |
|---|---|
| `main.py` | Orquestra o ciclo: agenda a execução periódica, trata erros de alto nível e configura logging. |
| `src/config.py` | Fonte única de configuração: caminhos de arquivo, API, ativos monitorados, intervalos. |
| `src/data_fetcher.py` | Faz a requisição HTTP à API pública e normaliza a resposta em estruturas tipadas (`Quote`). |
| `src/spreadsheet_manager.py` | Cria/abre o workbook, escreve os dados, aplica formatação condicional e reconstrói o gráfico. |

---

## 3. Fluxo de execução

1. **Inicialização** (`main.py`): configura logging (arquivo + console) e agenda o `job()` para rodar a cada `UPDATE_INTERVAL_MINUTES`.
2. **Execução imediata**: o primeiro ciclo roda assim que o programa inicia, sem esperar o primeiro intervalo.
3. **Coleta** (`data_fetcher.fetch_quotes`): requisição GET à AwesomeAPI (`economia.awesomeapi.com.br`) trazendo preço atual e variação percentual para cada par configurado.
4. **Persistência e formatação** (`spreadsheet_manager.update_spreadsheet`):
   - Abre o arquivo `.xlsx` existente ou cria um novo com as abas `Dashboard` e `Histórico`.
   - Reescreve a aba **Dashboard** com os valores mais recentes, aplicando cor verde/vermelha/amarela conforme a variação.
   - Adiciona uma nova linha na aba **Histórico** com timestamp e preços.
   - Reconstrói o gráfico de linha (`LineChart`) a partir de todo o intervalo de dados históricos.
   - Salva o arquivo. Se estiver aberto no Excel (erro de permissão no Windows), registra um aviso no log e tenta novamente no próximo ciclo — **não interrompe o processo**.
5. **Loop**: o processo permanece vivo (`while True` + `schedule.run_pending()`), repetindo o passo 3 e 4 a cada intervalo configurado, até ser interrompido manualmente (`Ctrl+C`).

---

## 4. Estrutura da planilha gerada

### Aba `Dashboard`
- Título e timestamp da última atualização.
- Tabela com colunas: `Ativo`, `Preço (R$)`, `Variação (%)`, `Situação`.
- Formatação condicional automática:
  - 🟢 Verde (`▲ Alta`) quando a variação é positiva.
  - 🔴 Vermelho (`▼ Baixa`) quando a variação é negativa.
  - 🟡 Amarelo (`► Estável`) quando não há variação.

### Aba `Histórico`
- Uma linha por ciclo de atualização, com data/hora e o preço de cada ativo monitorado.
- Gráfico de linha (`LineChart`) posicionado à direita dos dados, reconstruído a cada atualização para refletir toda a série temporal.
- Poda automática: quando o número de linhas ultrapassa `MAX_HISTORY_ROWS`, as linhas mais antigas são removidas para manter o arquivo leve.

---

## 5. Tratamento de erros

| Cenário | Comportamento |
|---|---|
| Falha de rede / API fora do ar | `RequestException` é capturada em `main.job()`, registrada no log; o próximo ciclo tenta novamente normalmente. |
| Par de moeda ausente na resposta da API | Log de aviso (`logger.warning`), o par é ignorado naquele ciclo sem interromper os demais. |
| Arquivo `.xlsx` aberto no Excel no momento do salvamento | `PermissionError` capturado; log de erro orientando o usuário a fechar o arquivo; nova tentativa ocorre no próximo ciclo agendado. |
| Nenhuma cotação recebida | A atualização da planilha é abortada para aquele ciclo, evitando sobrescrever dados válidos com um arquivo vazio. |
| Erro inesperado | Capturado genericamente em `main.job()` com `logger.exception`, preservando o loop principal ativo. |

---

## 6. Extensibilidade

- **Novos ativos**: adicionar entradas ao dicionário `CURRENCY_PAIRS` em `src/config.py` (chave = código aceito pela API, valor = rótulo exibido).
- **Outra fonte de dados**: substituir a implementação de `fetch_quotes()` em `data_fetcher.py`, mantendo o mesmo contrato de retorno (`dict[str, Quote]`) para que `spreadsheet_manager.py` não precise ser alterado.
- **Novas abas/gráficos**: `spreadsheet_manager.py` já centraliza estilos (`HEADER_FILL`, `UP_FILL`, etc.) reutilizáveis para novas visualizações.
- **Execução como serviço**: o loop de `main.py` pode ser encapsulado em um serviço do Windows (via `NSSM` ou Agendador de Tarefas) ou em um processo `systemd`/`cron` no Linux para rodar de forma totalmente desatendida.

---

## 7. Requisitos e execução

Ver seção "Como executar" no [`README.md`](../README.md). Requer Python 3.10+ e as dependências listadas em `requirements.txt` (`openpyxl`, `requests`, `schedule`).
