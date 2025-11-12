import os
from dotenv import load_dotenv
from openai import AzureOpenAI
import azure.cognitiveservices.speech as speech_sdk

# Configuração global do serviço de fala
speech_config = None

def carregar_variaveis():
    load_dotenv()
    return {
        "azure_oai_endpoint": os.getenv("AZURE_OAI_ENDPOINT"),
        "azure_oai_key": os.getenv("AZURE_OAI_KEY"),
        "azure_oai_deployment": os.getenv("AZURE_OAI_DEPLOYMENT"),
        "speech_key": os.getenv("AZURE_SPEECH_KEY"),
        "speech_region": os.getenv("AZURE_SPEECH_REGION")
    }

def inicializar_ia(endpoint, key):
    return AzureOpenAI(
        azure_endpoint=endpoint,
        api_key=key,
        api_version="2024-02-15-preview"
    )

def inicializar_fala(speech_key, speech_region):
    global speech_config
    speech_config = speech_sdk.SpeechConfig(speech_key, speech_region)
    speech_config.speech_recognition_language = "pt-BR"

def ouvir_do_microfone():
    global speech_config
    if not speech_config:
        print("Erro: configuração de fala não inicializada.")
        return ""

    audio_config = speech_sdk.AudioConfig(use_default_microphone=True)
    speech_recognizer = speech_sdk.SpeechRecognizer(speech_config, audio_config)

    print(" Fale agora... (estou ouvindo)")
    speech = speech_recognizer.recognize_once_async().get()

    if speech.reason == speech_sdk.ResultReason.RecognizedSpeech:
        return speech.text
    elif speech.reason == speech_sdk.ResultReason.NoMatch:
        print("Não entendi o que você disse.")
    elif speech.reason == speech_sdk.ResultReason.Canceled:
        print("Reconhecimento cancelado.")
    else:
        print(f"Erro no reconhecimento: {speech.reason}")
    return ""

def main():
    try:
        chaves = carregar_variaveis()
        client = inicializar_ia(chaves["azure_oai_endpoint"], chaves["azure_oai_key"])
        inicializar_fala(chaves["speech_key"], chaves["speech_region"])

        system_message = """Eu sou Jarvis seu assistente .
        Eu respondo perguntas de forma informal, sem emojis.E quando voce dizer: encerrar jarvis eu desligo o microfone"""
        messages_array = [{"role": "system", "content": system_message}]

        print("--- Chatbot IA com entrada por voz (diga 'sair' para encerrar) ---")

        while True:
            input_text = ouvir_do_microfone()
            if not input_text:
                continue
            if input_text.lower() in ["sair", "quit"]:
                break

            messages_array.append({"role": "user", "content": input_text})
            print("IA está pensando...")

            response = client.chat.completions.create(
                model=chaves["azure_oai_deployment"],
                messages=messages_array
            )

            generated_text = response.choices[0].message.content
            messages_array.append({"role": "assistant", "content": generated_text})

            print("IA: " + generated_text + "\n")

    except Exception as ex:
        print(f"Ocorreu um erro: {ex}")

if __name__ == '__main__':
    main()
