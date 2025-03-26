import json
import heapq

def carregar_dados(arquivo):
    try:
        with open(arquivo, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Erro: Arquivo não encontrado.")
        return {}
    except json.JSONDecodeError:
        print("Erro: Arquivo JSON mal formatado.")
        return {}

# Dijkstra modificado para evitar saltos diretos
def dijkstra_forcado(mapa, origem, destino):
    if origem not in mapa or destino not in mapa:
        return None, "Cidade de origem ou destino não encontrada."

    # Fila de prioridade (distância acumulada, número de cidades visitadas, cidade atual, caminho percorrido)
    fila = [(0, 0, origem, [origem])]
    visitados = {}

    while fila:
        distancia_atual, cidades_visitadas, cidade_atual, caminho = heapq.heappop(fila)

        # Se chegamos ao destino e passamos por pelo menos 1 intermediário, retorna o caminho
        if cidade_atual == destino and len(caminho) > 2:
            return caminho, distancia_atual

        # Se já visitamos essa cidade com menos distância, ignoramos
        if cidade_atual in visitados and visitados[cidade_atual] <= distancia_atual:
            continue
        visitados[cidade_atual] = distancia_atual

        # Explorar vizinhos 
        for vizinho, distancia in sorted(mapa[cidade_atual].items(), key=lambda x: (x[1], -len(mapa[x[0]]))):
            if vizinho not in caminho:
                heapq.heappush(fila, (distancia_atual + distancia, cidades_visitadas + 1, vizinho, caminho + [vizinho]))

    return None, "Não há caminho possível entre essas cidades."

def main():
    mapa_cidades = carregar_dados('cidadesSCDistancias.json')

    origem = input("\nDigite a cidade de origem: ")
    destino = input("Digite a cidade de destino: ")

    if origem not in mapa_cidades or destino not in mapa_cidades:
        print(f"\nErro: '{origem}' ou '{destino}' não encontrada no mapa. Verifique a grafia.")
        return

    caminho, distancia = dijkstra_forcado(mapa_cidades, origem, destino)

    if caminho:
        print("\nCaminho encontrado (cidade por cidade):")
        for i in range(len(caminho) - 1):
            print(f"{caminho[i].title()} -> {caminho[i+1].title()} ({mapa_cidades[caminho[i]].get(caminho[i+1], 'Desconhecido')} km)")
        print(f"\nDistância total percorrida: {distancia} km")
    else:
        print(f"\n{distancia}")

if __name__ == "__main__":
    main()
