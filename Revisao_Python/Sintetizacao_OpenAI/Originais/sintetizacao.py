import os
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speech_sdk

# OBJETIVO DESTE SCRIPT:
# 1. Carregar chaves de um arquivo .env.
# 2. Conectar-se ao serviço de Fala do Azure.
# 3. Receber uma string de TEXTO como entrada.
# 4. Sintetizar esse texto e FALAR usando o alto-falante.

# Variável global para a configuração do serviço de fala
# (Assim, não precisamos passá-la para a função 'falar_texto')
speech_config = None

def main():
    global speech_config
    try:
        # 1. CARREGAR VARIÁVEIS DE AMBIENTE
        load_dotenv()
        speech_key = os.getenv("AZURE_SPEECH_KEY")
        speech_region = os.getenv("AZURE_SPEECH_REGION")

        # 2. CONFIGURAR O SERVIÇO DE FALA
        # Isso prepara a "conexão" com o serviço de fala.
        speech_config = speech_sdk.SpeechConfig(speech_key, speech_region)

        # 3. DEFINIR A VOZ
        # Vamos usar uma voz em Português do Brasil.
        # Você pode encontrar outras vozes na documentação do Azure.
        speech_config.speech_synthesis_voice_name = "pt-BR-FranciscaNeural"
        
        print("Serviço de fala pronto.")

        # Para demonstrar, vamos chamar nossa função 'falar_texto'
        # com um texto fixo.
        print("Testando a função de falar...")
        falar_texto("Olá, alunos! Este é um teste da síntese de voz. Eu funciono!")
        
        # PERGUNTA: De onde mais poderia vir o texto para esta função?
        # DESAFIO: E se quiséssemos falar um texto que veio de outro lugar, 
        # como do script da IA?

    except Exception as ex:
        print(f"Ocorreu um erro no main: {ex}")

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