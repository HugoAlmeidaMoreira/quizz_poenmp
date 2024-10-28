import streamlit as st
import json
from streamlit_extras.stoggle import stoggle
from streamlit_lottie import st_lottie
import os
import random  # Importa o módulo random para baralhar as opções

def run():
    st.set_page_config(
        page_title="Quizz Plano Orçamental-Estrutural Nacional de Médio Prazo (POENMP)",
        page_icon="🇪🇺",
    )

if __name__ == "__main__":
    run()

# CSS personalizado para os botões
st.markdown("""
<style>
div.stButton > button:first-child {
    display: block;
    margin: 0 auto;
    border-width: 3px;
}
</style>
""", unsafe_allow_html=True)

# Inicializa as variáveis da sessão se elas não existirem
valores_default = {'current_index': 0, 'current_question': 0, 'score': 0, 'selected_option': None, 'answer_submitted': False, 'quiz_finalizado': False, 'mostrar_resultado': False, 'shuffled_options': []}
for key, value in valores_default.items():
    st.session_state.setdefault(key, value)

# Carrega os dados do quiz
with open('content/quiz_data.json', 'r', encoding='utf-8') as f:
    dados_quiz = json.load(f)

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

# Carrega o ficheiro JSON
lottie_animation = load_lottiefile("content/assets/badge_planapp.json")

def reiniciar_quiz():
    st.session_state.current_index = 0
    st.session_state.score = 0
    st.session_state.selected_option = None
    st.session_state.answer_submitted = False
    st.session_state.quiz_finalizado = False
    st.session_state.mostrar_resultado = False
    st.session_state.shuffled_options = []

def submeter_resposta():
    # Verifica se uma opção foi selecionada
    if st.session_state.selected_option is not None:
        # Marca a resposta como submetida
        st.session_state.answer_submitted = True
        # Verifica se a opção selecionada está correta
        if st.session_state.selected_option == dados_quiz[st.session_state.current_index]['answer']:
            st.session_state.score += 10
    else:
        # Se nenhuma opção foi selecionada, mostra uma mensagem e não marca como submetida
        st.warning("Selecione uma opção antes de submeter.")

def proxima_pergunta():
    st.session_state.current_index += 1
    st.session_state.selected_option = None
    st.session_state.answer_submitted = False
    st.session_state.shuffled_options = []

# Função que atualiza o estado para mostrar o resultado
def mostrar_resultado():
    st.session_state.mostrar_resultado = True
    st.session_state.quiz_finalizado = True

if not st.session_state.quiz_finalizado:
    # Título e descrição
    st.image("content/assets/hero.png", use_column_width=True)
    # Barra de progresso
    valor_barra_progresso = (st.session_state.current_index + 1) / len(dados_quiz)
    numero_pergunta_atual = st.session_state.current_index + 1
    st.write(f"Pergunta {numero_pergunta_atual} de {len(dados_quiz)}")
    st.progress(valor_barra_progresso)

    # Exibe a pergunta e as opções de resposta
    item_pergunta = dados_quiz[st.session_state.current_index]
    st.subheader(f"{item_pergunta['question']}")

    # Seleção de resposta
    if not st.session_state.shuffled_options:
        # Baralha as opções para apresentá-las de forma aleatória apenas na primeira vez
        st.session_state.shuffled_options = random.sample(item_pergunta['options'], len(item_pergunta['options']))

    opcoes = st.session_state.shuffled_options

if st.session_state.answer_submitted and not st.session_state.mostrar_resultado:
    # Assume que dados_quiz e item_pergunta estão definidos anteriormente no código
    item_pergunta = dados_quiz[st.session_state.current_index]
    caminho_imagem = item_pergunta.get('image_path',  '')
    caminho_caption = item_pergunta.get('caption')

    # Define a mensagem e a cor do fundo com base na corretude da resposta
    if st.session_state.selected_option == item_pergunta['answer']:
        mensagem = "Correto!🤓"
        cor_borda = "#3CB371"  # Uma cor de fundo suave para resposta correta, por exemplo, verde claro
    else:
        mensagem = "Errado!😔"
        cor_borda = "#FFCDD2"  # Uma cor de fundo suave para resposta incorreta, por exemplo, vermelho claro

    # Renderiza o feedback
    st.markdown(f"""
    <div style="border: 10px solid {cor_borda}; border-radius: 10px; padding: 20px; text-align: center;">
        <h3>{mensagem}</h3>
        <p>{item_pergunta['explanation']}</p>
    </div>
    """, unsafe_allow_html=True)

    # Verifica se o caminho da imagem existe e, se sim, mostra a imagem
    if caminho_imagem and os.path.isfile(caminho_imagem):
        st.markdown("___")
        st.image(caminho_imagem, caption=caminho_caption, use_column_width=True)

    st.divider()

# Botão de submissão e lógica de resposta
if st.session_state.answer_submitted:
    if st.session_state.current_index < len(dados_quiz) - 1:
        st.button('Próxima', on_click=proxima_pergunta, type='primary')
    else:
        # Se o quiz terminou, verifica se o resultado já foi mostrado
        if not st.session_state.get('quiz_finalizado', False):
            # Botão que altera o estado para mostrar o resultado quando clicado
            if st.button('Mostrar Resultado', on_click=mostrar_resultado):
                # Esconde o botão "Mostrar Resultado" e mostra "Reiniciar"
                st.session_state.mostrar_resultado = False
        elif st.session_state.mostrar_resultado:
            st.subheader('')                
            # Cria um bloco de Markdown para exibir a pontuação com estilo
            # Renderiza a animação Lottie no Streamlit
            st.markdown(f"""
            <div style="text-align: center;">
                <h1>🥳 Quizz Concluído! 🥳</h1>
                <h4>Obteve {st.session_state.score} pontos em {len(dados_quiz) * 10} pontos possíveis</h4>
            </div>
            """, unsafe_allow_html=True)

            st_lottie(lottie_animation, height=300, key="lottie")
            st.link_button(
                label="🧦 Acompanhe o PlanAPP nas redes que prefere",
                url="https://linktr.ee/planapp",
                type="primary",
                use_container_width=True
            )
            # Opção para reiniciar o quiz depois de mostrar o resultado
            st.subheader('', divider='rainbow')
            st.button('Reiniciar', on_click=reiniciar_quiz)

else:
    stoggle(
            "🔎 Pista",
            f"""{dados_quiz[st.session_state.current_index]['hint']}""",
        )
    st.markdown(""" ___""")
    # Renderiza os botões para seleção de opção
    for i, opcao in enumerate(opcoes):
        if st.button(opcao, key=f"option_{st.session_state.current_index}_{i}", use_container_width=True):
            st.session_state.selected_option = opcao  

    st.divider()
    
    st.button('Responder', on_click=submeter_resposta, type='primary')
