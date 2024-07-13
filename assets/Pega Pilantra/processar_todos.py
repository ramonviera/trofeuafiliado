import pandas as pd
import os

# Função para encontrar todos os arquivos com uma extensão específica no diretório atual
def find_files_with_extension(extension):
    files = [file for file in os.listdir('.') if file.endswith(extension)]
    return files

# Função para processar cada arquivo
def process_file(file):
    try:
        print(f"Processando arquivo: {file}")
        
        # Carregar o arquivo CSV
        df = pd.read_csv(file)
        
        # Passo 1: Remover duplicatas do "document_number"
        df_recebedor_unicos = df.drop_duplicates(subset='document_number')
        
        # Passo 2: Verificar se o CPF do pagador é igual ao CPF do recebedor
        df_recebedor_unicos['Igual'] = df_recebedor_unicos['documento_pagador'] == df_recebedor_unicos['document_number']
        
        # Passo 2.5: Duplicar a planilha e excluir os verdadeiros na nova aba
        df_filtrado = df_recebedor_unicos[df_recebedor_unicos['Igual'] == False]
        
        # Passo 3: Contar quantas vezes o CPF do pagador se repete
        contagem = df_filtrado['documento_pagador'].value_counts().reset_index()
        contagem.columns = ['documento_pagador', 'Contagem']
        
        # Merge para adicionar a contagem ao dataframe original
        df_filtrado = df_filtrado.merge(contagem, on='documento_pagador', how='left')
        
        # Passo 4: Excluir linhas com contagem menor que 3
        df_filtrado = df_filtrado[df_filtrado['Contagem'] >= 3]
        
        # Passo 5: Criar nova aba e remover duplicatas
        df_pagadores_unicos = df_filtrado[['documento_pagador']].drop_duplicates()
        
        # Passo 6: Criar aba com document_number da aba filtrada
        df_document_number_filtrado = df_filtrado[['document_number']].drop_duplicates()
        
        # Nome da pasta de resultado com base no nome do arquivo original
        base_name = os.path.splitext(os.path.basename(file))[0]
        result_folder = f"resultado_{base_name}"
        os.makedirs(result_folder, exist_ok=True)
        
        # Nome do arquivo de resultado dentro da pasta, usando o mesmo nome da pasta
        output_file = os.path.join(result_folder, f"{base_name}.xlsx")
        
        # Salvar o resultado em um novo arquivo Excel com várias abas
        with pd.ExcelWriter(output_file) as writer:
            df_recebedor_unicos.to_excel(writer, sheet_name='Original_Com_Igual', index=False)
            df_filtrado.to_excel(writer, sheet_name='Filtrado', index=False)
            df_pagadores_unicos.to_excel(writer, sheet_name='Pagadores_Unicos', index=False)
            df_document_number_filtrado.to_excel(writer, sheet_name='Document_Number_Filtrado', index=False)
        
        print(f"Arquivo de resultado criado: {output_file}")
    except Exception as e:
        print(f"Erro ao processar arquivo {file}: {e}")

# Encontrar todos os arquivos CSV na pasta atual
csv_files = find_files_with_extension('.csv')

# Processar cada arquivo CSV
if not csv_files:
    print("Nenhum arquivo CSV encontrado no diretório atual.")
else:
    for csv_file in csv_files:
        process_file(csv_file)

print("Processamento concluído para todos os arquivos.")
