# 🔗 Unificador de Bases CSV

Este projeto é uma aplicação web desenvolvida com Streamlit para consolidar, limpar, filtrar e enriquecer dados a partir de múltiplos arquivos CSV. A ferramenta foi projetada para unificar bases de dados de reclamações, filtrar segmentos de mercado específicos e adicionar informações complementares a partir de um arquivo secundário.

## ✨ Funcionalidades Principais

- **Interface Web Simples**: Utiliza o Streamlit para criar uma interface amigável e intuitiva.
- **Upload Múltiplo de Arquivos**: Permite o upload de vários arquivos CSV principais (ex: `finalizadas_*.csv`) de uma só vez.
- **Enriquecimento de Dados**: Faz o upload de um arquivo de apoio (`segmento_individual.csv`) para mesclar e adicionar novas informações à base consolidada.
- **Limpeza e Normalização Automática**:
    - Padroniza os nomes das colunas (remove acentos, espaços e caracteres especiais, converte para minúsculas).
    - Converte colunas numéricas (`nota_do_consumidor`, `tempo_resposta`) para o tipo correto, tratando erros.
    - Remove linhas duplicadas em cada arquivo e na base final consolidada.
- **Filtragem por Segmento**: Filtra os dados para manter apenas os registros pertencentes a segmentos de mercado pré-definidos.
- **Download do Resultado**: Gera um arquivo CSV final (`dados_completos.csv`) e disponibiliza um botão para download direto.

## 🚀 Como Usar a Aplicação

1.  **Execute a Aplicação**: Inicie a aplicação localmente (veja a seção "Executando a Aplicação" abaixo).
2.  **Upload dos Arquivos Principais**: Na seção "📂 Faça upload dos arquivos CSV", clique em "Browse files" e selecione todos os arquivos `finalizadas_*.csv` que deseja unificar.
3.  **Upload do Arquivo de Segmento**: Na seção "📁 Faça upload do arquivo 'segmento_individual.csv'", selecione o arquivo correspondente.
4.  **Processamento Automático**: A aplicação processará os arquivos automaticamente assim que todos forem carregados.
5.  **Download**: Se o processamento for bem-sucedido, uma mensagem de sucesso aparecerá junto com um botão "⬇️ Baixar arquivo final (dados_completos.csv)". Clique nele para salvar o resultado.

A aplicação exibirá mensagens de status, erro ou aviso conforme o andamento do processo.

## 🛠️ Pré-requisitos

Para executar este projeto, você precisará ter o Python instalado. As bibliotecas necessárias são:

-   Streamlit
-   Pandas

## 📦 Instalação

1.  Clone este repositório:
    ```bash
    git clone <URL_DO_SEU_REPOSITORIO>
    cd <NOME_DA_PASTA_DO_REPOSITORIO>
    ```

2.  Crie e ative um ambiente virtual (recomendado):
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3.  Instale as dependências. Crie um arquivo `requirements.txt` com o seguinte conteúdo:
    ```txt
    streamlit
    pandas
    ```
    Em seguida, instale com o pip:
    ```bash
    pip install -r requirements.txt
    ```

## ▶️ Executando a Aplicação

Com as dependências instaladas, execute o seguinte comando no seu terminal (na pasta do projeto):

```bash
streamlit run seu_arquivo.py
```

*Substitua `seu_arquivo.py` pelo nome real do seu arquivo Python.*

A aplicação será aberta automaticamente no seu navegador padrão.

## 📂 Estrutura dos Arquivos de Entrada

### Arquivos Principais (`finalizadas_*.csv`)

-   **Formato**: CSV
-   **Delimitador**: Ponto e vírgula (`;`)
-   **Encoding**: UTF-8
-   **Colunas Esperadas**: Devem conter, no mínimo, as colunas `segmento_de_mercado`, `nome_fantasia`, `nota_do_consumidor` e `tempo_resposta`.

### Arquivo de Segmento Individual (`segmento_individual.csv`)

-   **Formato**: CSV
-   **Delimitador**: Ponto e vírgula (`;`)
-   **Encoding**: UTF-8
-   **Coluna Chave**: Deve conter a coluna `nome_fantasia`, que será usada para cruzar as informações com a base principal.

## 🧠 Lógica do Script

O fluxo de processamento do script segue os seguintes passos:

1.  **Interface e Upload**: A interface do Streamlit é configurada para receber os dois conjuntos de arquivos.
2.  **Leitura e Concatenação**: Os arquivos principais são lidos um a um, normalizados e limpos individualmente. Depois, são concatenados em um único DataFrame (`dados_combinados`).
3.  **Normalização de Colunas**: A função `normalize_column_names` remove acentos, converte espaços para `_`, e padroniza tudo para minúsculas, garantindo consistência.
4.  **Filtragem por Segmento**: A base consolidada é filtrada para manter apenas os registros dos segmentos de interesse:
    -   `Operadoras de Planos de Saúde e Administradoras de Benefícios`
    -   `Seguros, Capitalização e Previdência`
    -   `Administradoras de Consórcios`
5.  **Enriquecimento de Dados (Merge)**: A base filtrada é mesclada (`LEFT JOIN`) com os dados do arquivo `segmento_individual.csv` usando a coluna `nome_fantasia` como chave. Isso adiciona novas colunas da base de segmento à base principal.
6.  **Geração do Arquivo Final**: O DataFrame final, completo e limpo, é convertido para um arquivo CSV (com encoding `latin-1` para melhor compatibilidade com softwares como o Excel) e disponibilizado para download.