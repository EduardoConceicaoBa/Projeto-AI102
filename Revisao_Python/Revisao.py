

# # Print -> Imprime algo na tela 
# print("Bom Dia!")

# nome = "Eduardo"
# inteiro = 6
# dinheiro = 4.50

# booleana = True 

# print(booleana)

# # Ler alguma informação - input
# nome = input("Informe um nome:")

# # Bibliotecas - Importar um conjunto de codigos prontos

# import os 

# # Funções - trechos de codigos que pode ser reutilizado 

# # def NOME():
# def boas_vindas():
#     print("Seja bem vindo!")
#     print("Esta é a minha função!")

# boas_vindas()

# # Uma função pode receber informações (parametros/argumentos)
# # Dar boas vindas com o nome da pessoa
# def boas_vindas(algum_nome, algum_sobrenome):
#     print("Seja bem vindo,", algum_nome, algum_sobrenome)

# sobrenome = input("Informe seu sobrenome:")

# boas_vindas("Eduardo", "Conceição")
# boas_vindas(nome, sobrenome)

# # Função que recebe dois numeros e mostra a soma deles
# numero1 = int(input("Informe o numero:"))
# numero2 = int(input("Informe outro numero:"))

# def soma(algum_numero1, algum_numero2):
#     print("O resultado da soma é:", algum_numero1 + algum_numero2)

# soma(numero1, numero2)


# # Subtração
# numero1 = int(input("Informe um numero:"))
# numero2 = int(input("Informe outro numero:"))

# def subtracao(algum_numero1, algum_numero2):
#     print("O resultado da subtração é:", algum_numero1 - algum_numero2)

# subtracao(numero1, numero2)


# #Divisão
# numero1 = int(input("Informe um numero:"))
# numero2 = int(input("Informe um outro numero:"))

# def divisao(algum_numero1, algum_numero2):
#     print("O resultado da divisão é:", algum_numero1 / algum_numero2)

# divisao(numero1, numero2)


# #Multiplicação
# numero1 = int(input("Informe um numero:"))
# numero2 = int(input("Informe um outro numero:"))

# def multiplicacao(algum_numero1, algum_numero2):
#     print("O resultado da multiplicação é:",algum_numero1 * algum_numero2)

# multiplicacao(numero1, numero2)

# Tratamento de Exception
# Try/except
try:
    numero1 = int(input("Informe um numero:"))
    numero2 = int(input("Informe um outro numero:"))
except ValueError:
    print("Deu Ruim!")
except Exception:
    print("Deu muito RUIM!")


# Exception - Exceções

# Metodo Principal
def main():
    print("Principal")

# Permite que o codigo seja executado 
# SEMPRE NO FINAL DO CODIGO 
if __name__ == '__main__':
    main()