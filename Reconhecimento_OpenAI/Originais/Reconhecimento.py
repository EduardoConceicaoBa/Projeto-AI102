import os
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speech_sdk

# OBJETIVO DESTE SCRIPT:
# 1. Carregar chaves de um arquivo .env.
# 2. Conectar-se ao serviço de Fala do Azure.
# 3. Usar o microfone padrão.
# 4. Ouvir o que o usuário diz e converter em uma string de TEXTO.
# 5. RETORNAR essa string de texto.

# Variável global para a configuração do serviço de fala
speech_config = None

def main():
    global speech_config
    try:
        # 1. CARREGAR VARIÁVEIS DE AMBIENTE
        load_dotenv()
        speech_key = os.getenv("AZURE_SPEECH_KEY")
        speech_region = os.getenv("AZURE_SPEECH_REGION")

        # 2. CONFIGURAR O SERVIÇO DE FALA
        speech_config = speech_sdk.SpeechConfig(speech_key, speech_region)
        
        # 3. DEFINIR IDIOMA DO RECONHECIMENTO
        # Muito importante! Define o idioma que o serviço tentará reconhecer.
        speech_config.speech_recognition_language = "pt-BR"
        
        print("Serviço de reconhecimento de fala pronto.")

        # Para demonstrar, vamos chamar nossa função 'ouvir_do_microfone'
        # e imprimir o que ela nos *retornou*.
        print("Testando a função de ouvir... Fale algo!")
        
        texto_ouvido = ouvir_do_microfone()
        
        if texto_ouvido:
            print(f"\nLegal! O texto que eu ouvi e 'retornei' foi: '{texto_ouvido}'")
        else:
            print("\nNão ouvi nada ou não entendi.")

        # PERGUNTA: O que mais poderíamos fazer com a variável 'texto_ouvido'?
        # DESAFIO: E se esse texto fosse usado como o 'input_text'
        # no script 1_chatbot_ia.py?

    except Exception as ex:
        print(f"Ocorreu um erro no main: {ex}")

def ouvir_do_microfone():
    """
    Esta função escuta o microfone e retorna o que foi dito como uma string de texto.
    """
    global speech_config
    
    if not speech_config:
        print("Erro: A configuração de fala (speech_config) não foi inicializada.")
        return "" # Retorna string vazia em caso de erro

    # Configura o áudio para usar o microfone padrão
    audio_config = speech_sdk.AudioConfig(use_default_microphone=True)
    
    # Cria o "reconhecedor"
    speech_recognizer = speech_sdk.SpeechRecognizer(speech_config, audio_config)

    print("Fale agora... (estou ouvindo)")

    # Inicia o reconhecimento. 
    # 'recognize_once_async().get()' espera até que você pare de falar.
    speech = speech_recognizer.recognize_once_async().get()

    # Verifica o resultado
    if speech.reason == speech_sdk.ResultReason.RecognizedSpeech:
        # Sucesso! Retorna o texto.
        return speech.text
    elif speech.reason == speech_sdk.ResultReason.NoMatch:
        print("Não consegui entender o que você disse.")
        return "" # Retorna string vazia
    elif speech.reason == speech_sdk.ResultReason.Canceled:
        print("Reconhecimento cancelado.")
        return "" # Retorna string vazia
    else:
        print(f"Erro no reconhecimento: {speech.reason}")
        return "" # Retorna string vazia

if __name__ == "__main__":
    main()