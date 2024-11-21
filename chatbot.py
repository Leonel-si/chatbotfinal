import streamlit as st
from groq import Groq

#Agg name
st.set_page_config(page_title="Mi chatbot con IA", page_icon="🐼", layout="centered")

#App title
st.title("Mi primera aplicación con Streamlit")

nombre=st.text_input("Ingresa tu nombre: ")

#Botón para mostrar un saludo
if st.button("Saludar"):
    st.write(f'Hola {nombre}, Bienvenido/a a mi chatbot :)') 

#modelos=["modelo 1", "modelo 2", "modelo 3"]
modelos = 'llama3-8b-8192', 'llama3-70b-8192', 'mixtral-8x7b-32768'
def configurar_pagina():
    #Agg titulo principal a nuestra barra
    st.title("Mi modelo de chatbot con IA")
    st.sidebar.title("Configuración")
    elegirModelo = st.sidebar.selectbox("ELEGIR UN MODELO", options=
    modelos, index=0)
    return elegirModelo

#CLASE 07
#Creación de un usuario
def crea_usuario_groq():
    claveSecreta = st.secrets["CLAVE_API"]
    return Groq(api_key=claveSecreta)

def configurar_modelo(cliente,modelo,mensajeDeEntrada):
    return cliente.chat.completions.create(
        model=modelo,
        messages=[{"role":"user","content":mensajeDeEntrada}],
        stream=True
    )

def inicializar_estado():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []

#clienteUsuario = crea_usuario_groq()

#inicializar_estado()

def actualizar_historial(rol, contenido, avatar):
    st.session_state.mensajes.append({"role":rol, "content":contenido, "avatar":avatar})
#Tomamos el mensaje del usuario por el input.

#generar respuesta
def generar_respuesta(chat_completo):
    respuesta_completa = ""
    for frase in chat_completo:
        if frase.choices[0].delta.content:
            respuesta_completa += frase.choices[0].delta.content
            yield frase.choices[0].delta.content
    return respuesta_completa
def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar=mensaje["avatar"]):
            st.markdown(mensaje["content"])
#area chat
def area_chat():
    contenedorDelChat = st.container(height=300, border=True)
    with contenedorDelChat:
        mostrar_historial()   

def main():
    modelo = configurar_pagina()
    clienteUsuario = crea_usuario_groq()
    inicializar_estado()
    area_chat()
    mensaje=st.chat_input("Escribe tu mensaje: ")
    if mensaje:
        actualizar_historial("user",mensaje,"👦")
        chat_completo = configurar_modelo(clienteUsuario, modelo, mensaje)
        if chat_completo:
            with st.chat_message("assistant"):
                respuesta_completa = st.write_stream(generar_respuesta(chat_completo))
                actualizar_historial("assistent", respuesta_completa,"🤖")
        st.rerun()

if __name__ == "__main__":
    main()
