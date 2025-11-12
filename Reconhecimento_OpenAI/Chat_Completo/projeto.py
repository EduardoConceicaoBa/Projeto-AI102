import os
from dotenv import load_dotenv
from openai import AzureOpenAI
import azure.cognitiveservices.speech as speech_sdk

# OBJETIVO:
# - Carregar as variáveis de ambiente para Azure.
# - Conectar-se ao serviço Azure OpenAI e Azure Speech.
# - Manter o histórico de conversa.
# - Enviar o prompt do usuário para a IA e receber a resposta.
# - Sintetizar a resposta da IA em fala.

# Variáveis globais para a configuração do serviço de fala
speech_config = None

def main():
    global speech_config
    try:
        # 1. CARREGAR VARIÁVEIS DE AMBIENTE
        load_dotenv()
        azure_oai_endpoint = os.getenv("AZURE_OAI_ENDPOINT")
        azure_oai_key = os.getenv("AZURE_OAI_KEY")
        azure_oai_deployment = os.getenv("AZURE_OAI_DEPLOYMENT")
        speech_key = os.getenv("AZURE_SPEECH_KEY")
        speech_region = os.getenv("AZURE_SPEECH_REGION")

        # 2. INICIALIZAR CLIENTE DA IA
        client = AzureOpenAI(
            azure_endpoint=azure_oai_endpoint, 
            api_key=azure_oai_key, 
            api_version="2024-02-15-preview"
        )

        # 3. CONFIGURAR O SERVIÇO DE FALA
        speech_config = speech_sdk.SpeechConfig(speech_key, speech_region)
        speech_config.speech_synthesis_voice_name = "pt-BR-FranciscaNeural"

        # 4. DEFINIR A PERSONALIDADE DA IA (Mensagem do Sistema)
        system_message = """Eu sou um assistente de IA prestativo.
        Eu respondo perguntas de forma concisa e direta.Não utilize emojis"""

        # O 'messages_array' guarda todo o histórico da conversa
        messages_array = [{"role": "system", "content": system_message}]

        print("--- Chatbot IA Iniciado (digite 'quit' para sair) ---")

        while True:
            # 5. OBTER O PROMPT DO USUÁRIO
            input_text = input("Você: ")
            if input_text.lower() == "quit":
                break

            # Adicionamos a pergunta do usuário ao histórico
            messages_array.append({"role": "user", "content": input_text})

            # 6. ENVIAR PARA A IA E OBTER RESPOSTA
            print("IA está pensando...")
            response = client.chat.completions.create(
                model=azure_oai_deployment,
                messages=messages_array
            )

            # Extraímos o TEXTO da resposta da IA
            generated_text = response.choices[0].message.content

            # Adicionamos a resposta da IA ao histórico
            messages_array.append({"role": "assistant", "content": generated_text})

            # 7. SINTETIZAR O TEXTO DA IA EM FALA
            print("IA: " + generated_text + "\n")
            falar_texto(generated_text)

    except Exception as ex:
        print(f"Ocorreu um erro: {ex}")

def falar_texto(texto_para_falar):
    """
    Esta função recebe qualquer string de texto e a transforma em fala.
    """
    global speech_config
    
    if not speech_config:
        print("Erro: A configuração de fala (speech_config) não foi inicializada.")
        return

    print(f"\nSintetizando fala para: '{texto_para_falar[:20]}...'")
    
    # Configura a saída de áudio para o alto-falante padrão
    audio_config = speech_sdk.audio.AudioOutputConfig(use_default_speaker=True)
    
    # Cria o "sintetizador"
    speech_synthesizer = speech_sdk.SpeechSynthesizer(speech_config, audio_config)

    # Envia o texto para o Azure e aguarda o áudio
    speak = speech_synthesizer.speak_text_async(texto_para_falar).get()

    # Verifica se a síntese foi bem-sucedida
    if speak.reason != speech_sdk.ResultReason.SynthesizingAudioCompleted:
        print(f"Erro na síntese de fala: {speak.reason}")

if __name__ == "__main__":
    main()
