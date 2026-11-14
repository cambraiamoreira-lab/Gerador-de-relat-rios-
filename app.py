import streamlit as st
from groq import Groq

# 1. Configuração da página do App
st.set_page_config(page_title="Gerador de Relatórios", page_icon="📝", layout="centered")

st.title("📝 Assistente de Relatórios Pedagógicos")
st.write("Preencha os dados abaixo para gerar um parecer descritivo baseado na BNCC.")

# 2. Criando os campos para o professor preencher (A Interface)
nome_aluno = st.text_input("Nome do Aluno:")

# Menu suspenso para escolher a série
ano_serie = st.selectbox("Ano/Série:", ["1º ano", "2º ano", "3º ano", "4º ano", "5º ano"])

# Menu suspenso para escolher a matéria
componente = st.selectbox("Componente Curricular:", ["Matemática", "Português", "Ciências", "História", "Geografia"])

# Campo para o código da BNCC
habilidade_bncc = st.text_input("Código da Habilidade BNCC (ex: EF05MA03):")

# Caixa de texto grande para as observações do professor
observacoes_professor = st.text_area("Observações do Professor (o que você notou sobre o aluno?):")

# 3. O Botão Mágico
if st.button("Gerar Relatório"):
    if not nome_aluno or not observacoes_professor:
        st.warning("Por favor, preencha pelo menos o nome do aluno e as observações.")
    else:
        # Mostra uma mensagem de carregamento enquanto a IA pensa
        with st.spinner("Escrevendo o relatório..."):
            
            # Conectando com a IA
            client = Groq(api_key="SUA_CHAVE_AQUI")
            
            prompt = f"""
            Você é um professor experiente e atencioso. 
            Escreva um parecer descritivo para o aluno {nome_aluno}, do {ano_serie}, na disciplina de {componente}.
            Observações do professor: "{observacoes_professor}"
            A habilidade da BNCC trabalhada foi: {habilidade_bncc}.
            O texto deve ser formal e acolhedor, direcionado aos pais, com 2 ou 3 parágrafos.
            """
            
            # Enviando para a IA
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="openai/gpt-oss-120b",
            )
            
            # 4. Mostrando o resultado na tela de forma bonita
            st.success("Relatório gerado com sucesso!")
            st.markdown("### Relatório:")
            st.info(chat_completion.choices[0].message.content)