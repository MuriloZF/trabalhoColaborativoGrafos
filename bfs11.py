import matplotlib
import networkx as nx
import matplotlib.pyplot as plt

matplotlib.use('qtagg')

def recomendar_amigos_matriz(matriz_adj, usuario_id):
    amigos_diretos = set()
    recomendacoes = set()
    for i in range(len(matriz_adj)):
        if matriz_adj[usuario_id][i] == 1: # O usuário i é amigo do usuário
            amigos_diretos.add(i)
        for amigo in amigos_diretos:
            for j in range(len(matriz_adj)):
                if matriz_adj[amigo][j] == 1: # Amigo do amigo
                    if j != usuario_id and j not in amigos_diretos: # Garante que a recomendação não vai ser o próprio usuário ou um amigo direto
                        recomendacoes.add(j)
    return list(recomendacoes)
            
def desenhar_recomendacoes_matriz(matriz_adj, usuario_id, recomendacoes, nomes_usuarios):
    """
    Desenha o grafo com o usuário selecionado e suas recomendações de amizade.
    Utiliza a biblioteca NetworkX para criação do grafo e Matplotlib para desenhar.
    """
    G = nx.Graph() # Cria um grafo não direcionado.
    cores_nomes = {} # Dicionário para armazenar as cores dos nós (nomes dos usuários).
    # Adiciona arestas ao grafo usando os nomes dos usuários.
    for i in range(len(matriz_adj)):
        for j in range(i, len(matriz_adj)): # Itera apenas uma vez por par (i, j).
            if matriz_adj[i][j] == 1: # Verifica a existência de uma aresta.
                G.add_edge(nomes_usuarios[i], nomes_usuarios[j]) # Adiciona aresta.
    # Define as cores dos nós baseando-se em nomes de usuários e recomendações.
    for i in range(len(matriz_adj)):
        if i == usuario_id:
            cores_nomes[nomes_usuarios[i]] = 'green' # Cor do usuário selecionado.
        elif i in recomendacoes:
            cores_nomes[nomes_usuarios[i]] = 'red' # Cor para recomendações.
        else:
            cores_nomes[nomes_usuarios[i]] = 'black' # Cor para os outros nós.
    # Calcula a posição dos nós para o layout do grafo.
    pos = nx.spring_layout(G) # Usa o layout de mola para distribuir os nós.
    plt.figure(figsize=(6, 4)) # Define o tamanho da figura.
    
    # Define o título do grafo.
    nomes_recomendados = [nomes_usuarios[i] for i in recomendacoes]
    Tit = f"Recomendações de amizade para {nomes_usuarios[usuario_id]}:\n"
    Tit += ", ".join(nomes_recomendados) +"."
    plt.title(Tit)
    # Desenha o grafo com cores dos vértices em branco e peso de fonte em negrito.
    nx.draw(G, pos, with_labels=False, node_color='white', font_weight='bold')
    # Itera sobre cada item no dicionário "pos", que contém as posições
    # dos nós do grafo. Cada item é uma chave-valor, onde a chave "node"
    # é o nome do nó (por exemplo, 'Ana', 'Bruno') e o valor "(x, y)"
    # é uma tupla contendo as coordenadas de posição do nó no plano 2D.
    for node, (x, y) in pos.items():
        # Verifica se o nó atual é o usuário selecionado.
        if node == nomes_usuarios[usuario_id]:
            facecolor = '#FFD700' # Define a cor de fundo como amarelo um pouco mais escuro.
        # Se o nó não for o usuário selecionado, verifica se ele está na lista de recomendações.
        elif node in [nomes_usuarios[i] for i in recomendacoes]:
            facecolor = '#ADD8E6' # Define a cor de fundo como azul claro para recomendações.
        # Se o nó não for o usuário nem uma recomendação, define a cor de fundo como branca.
        else:
            facecolor = 'white'
        # Desenha o texto do nome do nó no grafo com as configurações de cor de fundo e texto.
        plt.text(x, y, node, fontsize=10, ha='center', va='center',
                bbox=dict(facecolor=facecolor, edgecolor='black', boxstyle='round,pad=0.2'),
                color=cores_nomes[node])
    # Exibe a figura.
    plt.show() # Mostra o grafo na tela.
def criar_grafo_exemplo_matriz():
    """
    Cria um grafo exemplo com 10 vértices e uma densidade moderada
    para testar a recomendação de amizade.
    """
    # Matriz de adjacência representando as conexões de amizade.
    #0, 1, 2, 3, 4, 5, 6, 7, 8, 9
    matriz_adj = [
    [0, 1, 0, 0, 1, 1, 0, 0, 0, 1], # 0Ana -> Bruno, Eduarda, Fábio, João.
    [1, 0, 1, 1, 0, 0, 1, 0, 0, 0], # 1Bruno -> Ana, Carla, Daniel, Gabriela.
    [0, 1, 0, 0, 0, 0, 0, 1, 1, 0], # 2Carla -> Bruno, Henrique, Isabela.
    [0, 1, 0, 0, 1, 0, 1, 0, 0, 0], # 3Daniel -> Bruno, Eduarda, Gabriela.
    [1, 0, 0, 1, 0, 0, 1, 0, 0, 0], # 4Eduarda -> Ana, Daniel, Gabriela.
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 1], # 5Fabio -> Ana, Henrique, João.
    [0, 1, 0, 0, 1, 0, 0, 0, 1, 0], # 6Gabriela -> Bruno, Eduarda, Isabela.
    [0, 0, 1, 1, 0, 1, 0, 0, 0, 0], # 7Henrique -> Carla, Daniel, Fábio.
    [0, 0, 1, 0, 0, 0, 1, 0, 0, 1], # 8Isabela -> Carla, Gabriela, João.
    [1, 0, 0, 0, 0, 1, 0, 0, 1, 0] # 9João -> Ana, Fábio, Isabela.
    ]
    return matriz_adj # Retorna a matriz de adjacência.
# Execução do exemplo de uso.
nomes_usuarios = ["Ana", "Bruno", "Carla", "Daniel", "Eduarda",
"Fabio", "Gabriela", "Henrique", "Isabela", "João"]
matriz_adj = criar_grafo_exemplo_matriz() # Cria o grafo exemplo.
# Solicita ao usuário para escolher um nome da lista.
print("Usuários disponíveis:", ", ".join(nomes_usuarios))
nome_usuario = input("Digite o nome do usuário para ver as recomendações: ")
usuario_id = nomes_usuarios.index(nome_usuario) # Obtém o índice do usuário selecionado.
# Gera e exibe as recomendações de amizade.
recomendacoes = recomendar_amigos_matriz(matriz_adj, usuario_id)
# Desenha o grafo com as recomendações.
desenhar_recomendacoes_matriz(matriz_adj, usuario_id, recomendacoes, nomes_usuarios)
