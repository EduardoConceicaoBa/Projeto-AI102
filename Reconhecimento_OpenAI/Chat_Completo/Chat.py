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
    speech_config = speech_sdk.SpeechConfig(subscription=speech_key, region=speech_region)
    speech_config.speech_recognition_language = "pt-BR"
    speech_config.speech_synthesis_language = "pt-BR"
    speech_config.speech_synthesis_voice_name = "pt-BR-AntonioNeural"  # Voz masculina

def ouvir_do_microfone():
    global speech_config
    if not speech_config:
        print("Erro: configuração de fala não inicializada.")
        return ""

    audio_config = speech_sdk.AudioConfig(use_default_microphone=True)
    speech_recognizer = speech_sdk.SpeechRecognizer(speech_config, audio_config)

    print(" Fale agora...")
    resultado = speech_recognizer.recognize_once_async().get()

    if resultado.reason == speech_sdk.ResultReason.RecognizedSpeech:
        return resultado.text
    elif resultado.reason == speech_sdk.ResultReason.NoMatch:
        print(" Não entendi o que você disse.")
    elif resultado.reason == speech_sdk.ResultReason.Canceled:
        print(" Reconhecimento cancelado.")
    else:
        print(f" Erro no reconhecimento: {resultado.reason}")
    return ""

def falar_texto(texto_para_falar):
    global speech_config
    if not speech_config:
        print("Erro: A configuração de fala não foi inicializada.")
        return

    audio_config = speech_sdk.audio.AudioOutputConfig(use_default_speaker=True)
    speech_synthesizer = speech_sdk.SpeechSynthesizer(speech_config, audio_config)
    speak = speech_synthesizer.speak_text_async(texto_para_falar).get()

    if speak.reason != speech_sdk.ResultReason.SynthesizingAudioCompleted:
        print(f"Erro na síntese de fala: {speak.reason}")

def main():
    global speech_config
    try:
        chaves = carregar_variaveis()
        client = inicializar_ia(chaves["azure_oai_endpoint"], chaves["azure_oai_key"])
        inicializar_fala(chaves["speech_key"], chaves["speech_region"])

        system_message = """Você é Jarvis, um assistente de voz inteligente.
Responda de forma informal, sem emojis. Quando o usuário disser 'encerrar jarvis', finalize a conversa."""
        messages_array = [{"role": "system", "content": system_message}]

        print("\n Jarvis ativado. Diga 'encerrar jarvis' ou 'sair' para finalizar.\n")

        while True:
            entrada = ouvir_do_microfone()
            if not entrada:
                continue

            if entrada.lower() in ["encerrar jarvis", "sair", "quit"]:
                print("Jarvis: Encerrando...")
                falar_texto("Encerrando. Até mais!")
                break

            messages_array.append({"role": "user", "content": entrada})
            print("Jarvis está pensando...")

            resposta = client.chat.completions.create(
                model=chaves["azure_oai_deployment"],
                messages=messages_array
            )

            texto_gerado = resposta.choices[0].message.content
            messages_array.append({"role": "assistant", "content": texto_gerado})

            print("Jarvis:", texto_gerado)
            falar_texto(texto_gerado)

    except Exception as ex:
        print(f"Ocorreu um erro: {ex}")

if __name__ == '__main__':
    main()
