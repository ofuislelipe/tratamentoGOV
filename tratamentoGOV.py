import streamlit as st
import pandas as pd
import unicodedata
import io

st.set_page_config(page_title="Unificador de Bases", layout="wide")

# Função para normalizar nomes de colunas
def normalize_column_names(df):
    df.columns = [
        unicodedata.normalize('NFKD', col).encode('ASCII', 'ignore').decode('ASCII').strip()
        .replace(' ', '_').replace('-', '_').lower()
        for col in df.columns
    ]
    return df

# Título
st.title("🔗 Unificador de Bases CSV")

# Upload dos arquivos principais
uploaded_files = st.file_uploader(
    "📂 Faça upload dos arquivos CSV (finalizadas_*.csv)", 
    type="csv", 
    accept_multiple_files=True
)

# Upload do arquivo de segmentos individuais
segmento_individual_file = st.file_uploader(
    "📁 Faça upload do arquivo 'segmento_individual.csv'", 
    type="csv"
)

if uploaded_files and segmento_individual_file:
    list_dfs = []

    for file in uploaded_files:
        try:
            df = pd.read_csv(file, delimiter=';', encoding='utf-8', on_bad_lines='skip')
            df = normalize_column_names(df)
            df['nota_do_consumidor'] = pd.to_numeric(df.get('nota_do_consumidor'), errors='coerce').astype('Int64')
            df['tempo_resposta'] = pd.to_numeric(df.get('tempo_resposta'), errors='coerce').astype('Int64')
            df.drop_duplicates(inplace=True)
            list_dfs.append(df)
        except Exception as e:
            st.error(f"Erro ao processar o arquivo {file.name}: {e}")

    if list_dfs:
        dados_combinados = pd.concat(list_dfs, ignore_index=True).drop_duplicates()

        coluna_segmento = 'segmento_de_mercado'
        segmentos_desejados = [
            'Operadoras de Planos de Saúde e Administradoras de Benefícios',
            'Seguros, Capitalização e Previdência',
            'Administradoras de Consórcios'
        ]

        if coluna_segmento in dados_combinados.columns:
            dados_combinados['nome_fantasia'] = dados_combinados['nome_fantasia'].str.lower()
            dados_filtrados = dados_combinados[dados_combinados[coluna_segmento].isin(segmentos_desejados)]

            if not dados_filtrados.empty:
                try:
                    df_segmento_individual = pd.read_csv(segmento_individual_file, delimiter=';', encoding='utf-8')
                    df_segmento_individual = normalize_column_names(df_segmento_individual)
                    df_segmento_individual['nome_fantasia'] = df_segmento_individual['nome_fantasia'].str.lower()
                    df_segmento_individual.drop_duplicates(subset='nome_fantasia', inplace=True)

                    dados_completos = dados_filtrados.merge(
                        df_segmento_individual,
                        how='left',
                        on='nome_fantasia'
                    ).drop_duplicates()

                    # Baixar arquivo final
                    output_csv = dados_completos.to_csv(index=False, encoding='latin-1')
                    st.success("✅ Base combinada com sucesso!")
                    st.download_button(
                        label="⬇️ Baixar arquivo final (dados_completos.csv)",
                        data=output_csv,
                        file_name="dados_completos.csv",
                        mime="text/csv"
                    )
                except Exception as e:
                    st.error(f"Erro ao processar o arquivo de segmento individual: {e}")
            else:
                st.warning(f"Nenhum dado encontrado para os segmentos desejados: {segmentos_desejados}")
        else:
            st.error(f"A coluna '{coluna_segmento}' não foi encontrada nos arquivos.")
    else:
        st.warning("Nenhum dado foi lido dos arquivos CSV fornecidos.")
else:
    st.info("Por favor, faça upload dos arquivos necessários para começar.")