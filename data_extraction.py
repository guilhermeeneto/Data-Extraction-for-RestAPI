
import requests
import json

api_url = 'https://api.football-data.org/v4/competitions/BSA/teams'
headers = {'X-Auth-Token': '18108532eb514f478062c6cf042ef6c7'}

posicao_ptbr = {
    'Goalkeeper': 'Goleiro',
    'Defence': 'Defensor',
    'Midfield': 'Meio Campo',
    'Offence': 'Atacante',
    'Right Winger': 'Ponta Direita',
    'Centre-Back': 'Zagueiro Central',
    'Centre-Forward': 'Atacante Central',
    'Left Winger': 'Ponta Esquerda',
    'Central Midfield': 'Meio Campo Central',
    'Defensive Midfield': 'Meio Campo Defensivo',
    'Left-Back': 'Lateral Esquerdo',
    'Attacking Midfield': 'Meio Campo Ofensivo'
}

response = requests.get(api_url, headers=headers)
data = response.json()

api_rest_url = 'http://localhost:5000'

for team in data['teams']:
    clube_data = {
        'nome': team['name'],
        'localizacao': team.get('address')
    }
    response_clube = requests.post(f'{api_rest_url}/clube', json=clube_data)
    if response_clube.status_code == 201:
        clube_id = response_clube.json()['id']
        print(f"Clube adicionado: {team['name']}")
    else:
        print(f"Erro ao criar clube: {response_clube.status_code}, {response_clube.text}")
        continue

    
    for player in team['squad']:
        jogador_data = {
            'nome': player['name'],
            'idade': 2024 - int(player['dateOfBirth'].split('-')[0]), 
            'posicao': posicao_ptbr.get(player['position'],'Desconhecida'),
            'clube_id': clube_id
        }
        response_jogador = requests.post(f'{api_rest_url}/jogador', json=jogador_data)
        if response_jogador.status_code == 201:
            print(f"Jogador adicionado: {player['name']}")
        else:
            print(f"Erro ao criar jogador: {response_jogador.status_code}, {response_jogador.text}")
