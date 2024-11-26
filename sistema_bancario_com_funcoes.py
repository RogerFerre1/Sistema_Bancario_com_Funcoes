import textwrap

saldo = 0 
limite = 500
extrato = ''
numero_saques = 0
LIMITE_SAQUES = 3

def menu():
    print("""
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [q] Sair
      
    => """)    
    
def depositar(saldo, valor, extrato, /):
    print("Depósito")
    valor = float(input("Digite o valor para depósito: "))
    if valor > 0:
        saldo += valor
        extrato += (f'Depósito de: R${valor}\n')
    else:
        print("Operação falhou! O valor informado é inválido")
    return saldo, extrato
    
def sacar(*, saldo, valor, extrato, limite, numero_saques, LIMITE_SAQUES):
    print("Saque")
    valor = float(input("Digite o valor para o saque: "))
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite 
    excedeu_saques = numero_saques >= LIMITE_SAQUES
    
    if excedeu_saldo:
        print("Operação falhou! Você não tem saldo suficiente.")
        
    elif excedeu_limite:
        print("Operação falhou! O valor do saque excede o limite.")
            
    elif excedeu_saques:
        print("Operação falhou! Número máximo de saques excedido.")
            
    elif valor > 0:
        saldo -= valor 
        extrato += f'Saque: R${valor:.2f}\n'
        numero_saques += 1
    
    else: 
        print("Operação falhou! O valor informado é inválido.")
    return saldo, extrato, numero_saques
    
def exibir_extrato(saldo, /, *, extrato):
    print("\n================ Extrato ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("===========================================")
    
def criar_usuario(usuarios):
    """
    Cadastra um novo usuário no sistema.
    """
    print("=== Cadastro de Usuário ===")
    cpf = input("Informe o CPF (somente números): ")
    # Verifica se o usuário já existe
    if any(usuario['cpf'] == cpf for usuario in usuarios):
        print("Usuário já cadastrado!")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, número - bairro - cidade/estado): ")
    
    # Cria e adiciona o novo usuário na lista
    usuarios.append({
        "nome": nome,
        "cpf": cpf,
        "data_nascimento": data_nascimento,
        "endereco": endereco
    })
    print("Usuário criado com sucesso!")


def filtrar_usuario(cpf, usuarios):
    """
    Filtra o usuário pelo CPF.
    Retorna o dicionário do usuário, se encontrado, ou None caso contrário.
    """
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            return usuario
    print("Usuário não encontrado!")
    return None


def criar_conta(agencia, numero_conta, usuarios):
    """
    Cria uma nova conta bancária para um usuário já cadastrado.
    """
    print("=== Criação de Conta ===")
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print(f"Conta criada para o usuário {usuario['nome']}")
        return {
            "agencia": agencia,
            "numero_conta": numero_conta,
            "usuario": usuario
        }
    print("Falha na criação da conta. Usuário não encontrado.")
    return None


def listar_contas(contas):
    """
    Exibe todas as contas cadastradas.
    """
    print("\n=== Listagem de Contas ===")
    for conta in contas:
        linha = f"""\
        Agência: {conta['agencia']}
        C/C: {conta['numero_conta']}
        Titular: {conta['usuario']['nome']}
        """
        print(textwrap.dedent(linha))
    print("=================================")


def main():
    """
    Função principal que executa o programa.
    """
    agencia = "0001"
    numero_conta = 1
    usuarios = []
    contas = []

    while True:
        menu()
        opcao = input().lower()

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))
            depositar(saldo, valor, extrato)

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))
            sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )

        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "c":
            criar_usuario(usuarios)

        elif opcao == "cc":
            conta = criar_conta(agencia, numero_conta, usuarios)
            if conta:
                contas.append(conta)
                numero_conta += 1

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            print("Saindo do sistema...")
            break

        else:
            print("Operação inválida! Selecione novamente a operação desejada.")
