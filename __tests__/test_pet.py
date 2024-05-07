# 1 - Biblioteca
import pytest 
import requests
import json

from utils.utils import ler_csv # import a função de leitura do csv

#from utils.utils import ler_csv     # importar a função de leitura do csv
# 2 - Classe ( opcional no Python , em muitos casos)

# 2.1 - Atributos ou variaveis 
# Consulta e resultado esperado 
pet_id = 938944501
pet_name = "Leticia"
pet_category_id = 1 
pet_category_name = "Cat"
pet_tag_id = 1
pet_tag_name = "Vacinado"

# informações em comun
url_base = 'https://petstore.swagger.io/v2/pet'
headers = { 'Content-Type': 'application/json' }

# 2.2 - Funções / Métodos 

def test_post_pet(): 
    # Configura
    # dados de entrada estão no arquivo json
    pet=open('./fixtures/json/pet1.json')
    data=json.loads(pet.read()) # ler o conteúdo e carrega como json em uma variavel data


    # Executa
    response = requests.post( # executa o método post com as informações a seguir 
        url=url_base, # endereço
        headers=headers, # cabeçalho / informações extras  da mensagem
        data=json.dumps(data), # a mensagem = json
        timeout=5 # Opcional / tempo limite da transmissão , em segundos
    )

    # Valida
    response_body = response.json()  # cria uma variavel e carrega a resposta em formato json

    assert response.status_code == 200
    assert response_body['id'] == pet_id
    assert response_body['name'] == pet_name
    assert response_body['category']['id'] == pet_category_id
    assert response_body['tags'][0]['id'] == pet_tag_id
    assert response_body['status'] == 'available'

def test_get_pet():
    #Configura
    # Dados de Entrada e Saída / Resultado Esperado estão na seção de atributos antes das funções
    #Executa
    response = requests.get(
        url=f'{url_base}/{pet_id}',
        headers=headers
    )

    # Valida 
    response_body  = response.json()

    assert response.status_code == 200
    assert response_body['name'] == pet_name
    assert response_body['category']['name'] == pet_category_name
    assert response_body['category']['id'] == pet_category_id
    assert response_body['tags'][0]['id'] == pet_tag_id
    assert response_body['status'] == 'available'

def test_put_pet():
    # Configura
    # dados entrada vem de um arquivo json
    pet = open('./fixtures/json/pet2.json')
    data = json.loads(pet.read())
    # dados de saída / resultado esperado vem dos atributos descritos antes das funções
    
    # Executa
    response = requests.put(
        url=url_base,
        headers=headers,
        data=json.dumps(data),
        timeout=5
    ) 

    # Valida
    response_body = response.json()

    assert response.status_code == 200
    assert response_body['id'] == pet_id
    assert response_body['name'] == pet_name
    assert response_body['category']['id'] == pet_category_id
    assert response_body['category']['name'] == pet_category_name
    assert response_body['tags'][0]['id'] == pet_tag_id
    assert response_body['tags'][0]['name'] == pet_tag_name
    assert response_body['status'] == 'sold'    

def test_delete_pet():
    # Configura
    # Dados de entrada e saída virão dos atributos

    # Executa
    response = requests.delete(
        url=f'{url_base}/{pet_id}',
        headers=headers
    )

    # Valida
    response_body = response.json()

    assert response.status_code == 200
    assert response_body['code'] == 200
    assert response_body['type'] == 'unknown'
    assert response_body['message'] == str(pet_id)
    
@pytest.mark.parametrize('pet_id,category_id,category_name,pet_name,tags,status', 
                            ler_csv('./fixtures/csv/pets.csv'))

def test_post_pet_dinamico(pet_id,category_id,category_name,pet_name,tags,status):
    
    pet = {} # Cria uma lista vazia chamada pet
    pet['id'] = int(pet_id)
    pet['category'] = {}
    pet['category']['id'] = int(category_id)
    pet['category']['name'] = category_name
    pet['name'] = pet_name
    pet['photoUrls'] = []
    pet['photoUrls'].append('')
    pet['tags'] = []

    tags = tags.split(';')
    for tag in tags:
        tag = tag.split('-')
        tag_formatada = {}
        tag_formatada['id'] = int(tag[0])
        tag_formatada['name'] = tag[1]
        pet['tags'].append(tag_formatada)

    pet['status'] = status   
        
    pet = json.dumps(obj=pet, indent=4)
    print('\n' + pet) # visualiza como ficou o json criado dinamicamente

    # Executa
    response = requests.post(
        url=url_base,
        headers=headers,
        data=pet,
        timeout=5
    )

    # Compara

    response_body = response.json()

    assert response.status_code == 200
    assert response_body['id'] == int(pet_id)
    assert response_body['name'] == pet_name
    assert response_body['status'] == status

    # # pytest -svk ' dinamico'  \\ comando para rodar apenas um teste verboso 


