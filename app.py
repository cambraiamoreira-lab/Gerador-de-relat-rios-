import streamlit as st
from groq import Groq
import bncc

# 1. Configuração da página do App
st.set_page_config(page_title="Assistente de Relatórios", page_icon="📝", layout="centered")

st.title("📝 Assistente de Relatórios Pedagógicos")
st.write("Preencha os dados abaixo para gerar um parecer descritivo completo e alinhado à BNCC.")

# 2. Dicionário com a estrutura de etapas, séries e disciplinas da BNCC
estrutura_bncc = {
    "Ensino Fundamental - Anos Iniciais": {
        "séries": ["1º ano", "2º ano", "3º ano", "4º ano", "5º ano"],
        "disciplinas": ["Língua Portuguesa", "Arte", "Educação Física", "Língua Inglesa", "Matemática", "Ciências", "História", "Geografia"]
    },
    "Ensino Fundamental - Anos Finais": {
        "séries": ["6º ano", "7º ano", "8º ano", "9º ano"],
        "disciplinas": ["Língua Portuguesa", "Arte", "Educação Física", "Língua Inglesa", "Matemática", "Ciências", "História", "Geografia"]
    },
    "Ensino Médio": {
        "séries": ["1ª série", "2ª série", "3ª série"],
        "disciplinas": ["Língua Portuguesa", "Arte", "Educação Física", "Língua Inglesa", "Matemática", "Biologia", "Física", "Química", "Filosofia", "Geografia", "História", "Sociologia"]
    }
}

# 3. Interface: Seleção da Etapa e Série
etapa = st.selectbox("Etapa de Ensino:", list(estrutura_bncc.keys()))
ano_serie = st.selectbox("Ano/Série:", estrutura_bncc[etapa]["séries"])

# 4. Interface: Seleção da Disciplina
componente = st.selectbox("Componente Curricular:", estrutura_bncc[etapa]["disciplinas"])

# 5. Busca local de habilidades usando a biblioteca bncc
mapa_siglas = {
    "Língua Portuguesa": "LP", "Arte": "AR", "Educação Física": "EF",
    "Língua Inglesa": "LI", "Matemática": "MA", "Ciências": "CI",
    "História": "HI", "Geografia": "GE", "Biologia": "BI",
    "Física": "FI", "Química": "QU", "Filosofia": "FI", "Sociologia": "SO"
}
sigla_componente = mapa_siglas.get(componente, "")

numero_ano = "".join(filter(str.isdigit, ano_serie))
etapa_codigo = "EF" if "Fundamental" in etapa else "EM"

habilidade_selecionada = None
try:
    # Busca as habilidades de forma local (offline)
    if etapa_codigo == "EF":
        habilidades_encontradas = bncc.habilidades_ef(componente=sigla_componente, ano=int(numero_ano))
    else:
        # No Ensino Médio a BNCC é organizada por áreas, buscamos de forma abrangente
        habilidades_encontradas = bncc.buscar("", etapa="EM", componente=sigla_componente)

    if habilidades_encontradas:
        opcoes = [f"{h['codigo']} - {h['texto']}" for h in habilidades_encontradas]
        habilidade_selecionada = st.selectbox("Selecione a Habilidade da BNCC:", opcoes)
    else:
        st.warning("Nenhuma habilidade encontrada para esta combinação de série e disciplina.")
except Exception as e:
    st.error(f"Erro ao carregar dados da BNCC: {e}")

# 6. Campo de observações
observacoes_professor = st.text_area("Observações do Professor (o que você notou sobre o aluno?):", height=150)

# 7. Botão para gerar o relatório
if st.button("✨ Gerar Relatório", type="primary"):
    if not habilidade_selecionada or not observacoes_professor:
        st.warning("Por favor, selecione uma habilidade da BNCC e preencha as observações.")
    else:
        with st.spinner("Escrevendo o relatório com a IA..."):
            codigo_bncc = habilidade_selecionada.split(" - ")[0]

            try:
                client = Groq(api_key=st.secrets["GROQ_API_KEY"])

                prompt = f"""
                Você é um professor experiente e muito atencioso.
                Escreva um parecer descritivo para um aluno do(a) {ano_serie}, na disciplina de {componente}.
                A habilidade da BNCC trabalhada foi a de código {codigo_bncc}.
                Aqui estão as observações brutas do professor sobre o aluno: "{observacoes_professor}"
                O texto deve ser formal, porém acolhedor, direcionado aos pais ou responsáveis.
                Transforme a dificuldade citada em um ponto de melhoria construtivo, sugerindo como a família pode ajudar em casa.
                O parecer deve ter entre 2 e 3 parágrafos curtos.
                """

                chat_completion = client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="openai/gpt-oss-120b",
                )

                st.success("Relatório gerado com sucesso!")
                st.markdown("### 📄 Relatório:")
                st.info(chat_completion.choices[0].message.content)
            except Exception as e:
                st.error(f"Erro ao gerar o relatório: {e}")