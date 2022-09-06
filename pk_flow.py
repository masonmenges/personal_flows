from typing import Dict
from prefect import task, flow
from prefect.filesystems import S3
from requests import get
from random import randint

from constants import random_type

@task
def poke_type_info(pk_type: str):
    return get(f"https://pokeapi.co/api/v2/type/{pk_type}").json()

@task
def get_pokemon_from_type(pk_dict: Dict):
    return pk_dict['pokemon']

@task
def get_rand_pk(pk_list: list):
    rand_num = randint(0, (len(pk_list)-1))    
    return pk_list[rand_num]

@task
def write_to_file(pk_team: list):


    with open('team.txt', 'w') as f:

        for pk in pk_team:
            f.write(f"{pk['name']}: {pk['types']} \n")

        f.close()
    
    with open('team.txt') as f:
        text = f.readlines()

    print(text)


@task
def get_pk_data(URL: str):
    response = get(URL)
    return response.json()


@flow
def get_pk_from_list(pk_list: list):

    pk_team = [get_pk_data.submit(pk['pokemon']['url']) for pk in pk_list]

    return pk_team



@flow()
def create_pk_team(pk_type: str):
    pk_type = random_type()
    pk_type_dict = poke_type_info(pk_type)
    pk_from_type = get_pokemon_from_type(pk_type_dict)
    pk_list = [get_rand_pk.submit(pk_from_type) for pk in range(6)]
    pk_team = get_pk_from_list(pk_list)
    write_to_file(pk_team)

if __name__  == "__main__":
    create_pk_team(pk_type="fire")