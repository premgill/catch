import os
import re
import time
import multiprocessing
import datetime
import random
# Import 'keep_alive' assuming it's a custom module or part of your project.
import keep_alive
# Import 'discum' assuming it's a custom module or an external library.
# Please make sure to install the 'discum' module using the appropriate command (e.g., pip).
import discum

version = 'v2.6'


channel_id = 1234859064677105710
catch_id = 1234859064677105710

with open('pokemon.txt', 'r', encoding='utf8') as file:
    pokemon_list = file.read()
with open('legendary.txt', 'r') as file:
    legendary_list = file.read()
with open('mythical.txt', 'r') as file:
    mythical_list = file.read()
with open('level.txt', 'r') as file:
    to_level = file.readline()

num_pokemon = 0
shiny = 0
legendary = 0
mythical = 0

poketwo_id = '716390085896962058'
bot = discum.Client(
    token='OTY1NDA0NDYwMTM2NDE1Mjk0.GeGYxK.dwkJIaxnKqFPPk_nJcnNfT-GI_ARg79RKZskR4', log=False)
keep_alive.keep_alive()


def solve(message):
    hint = []
    for i in range(15, len(message) - 1):
        if message[i] != '\\':
            hint.append(message[i])
    hint_string = ''
    for i in hint:
        hint_string += i
    solution = re.findall('^'+hint_string.replace('_', '.') +
                          '$', pokemon_list, re.MULTILINE)
    return solution


def spam():
    while True:
        hash = random.getrandbits(128)
        bot.sendMessage('899654901553070091', hash)
        intervals = [3.0, 3.0, 3.0, 3.0, 3.0, 3.0]
        time.sleep(random.choice(intervals))


def start_spam():
    new_process = multiprocessing.Process(target=spam)
    new_process.start()
    return new_process


def stop(process):
    process.terminate()


def log(string):
    now = datetime.datetime.now()
    current_time = now.strftime('%H:%M:%S')
    print(f'[{current_time}]', string)


@bot.gateway.command
def on_ready(resp):
    if resp.event.ready_supplemental:
        log(f'Logged into account: ')


@bot.gateway.command
def on_message(resp):
    global spam_process
    if resp.event.message:
        m = resp.parsed.auto()
        if m['channel_id'] == catch_id:
            if m['author']['id'] == poketwo_id:
                if m['embeds']:
                    embed_title = m['embeds'][0]['title']
                    if 'wild pokémon has appeared!' in embed_title:
                        stop(spam_process)
                        time.sleep(2)
                        bot.sendMessage(catch_id, '<@716390085896962058> h')
                    elif "Congratulations" in embed_title:
                        embed_content = m['embeds'][0]['description']
                        if 'now level' in embed_content:
                            stop(spam_process)
                            split = embed_content.split(' ')
                            a = embed_content.count(' ')
                            level = int(split[a].replace('!', ''))
                            if level == 100:
                                bot.sendMessage(
                                    channel_id, f"<@716390085896962058> s {to_level}")
                                with open('level.txt', 'r') as fi:
                                    data = fi.read().splitlines(True)
                                with open('level.txt', 'w') as fo:
                                    fo.writelines(data[1:])
                                spam_process = start_spam()
                            else:
                                spam_process = start_spam()
                else:
                    content = m['content']
                    if 'The pokémon is ' in content:
                        if len(solve(content)) == 0:
                            log('Pokemon not found.')
                        else:
                            for i in solve(content):
                                stop(spam_process)
                                time.sleep(2)
                                bot.sendMessage(
                                    catch_id, f'<@716390085896962058> c {i}')
                        time.sleep(2)
                        spam_process = start_spam()

                    elif 'Congratulations' in content:
                        global shiny
                        global legendary
                        global num_pokemon
                        global mythical
                        num_pokemon += 1
                        split = content.split(' ')
                        pokemon = split[7].replace('!', '')
                        if 'These colors seem unusual...' in content:
                            shiny += 1
                            log(
                                f'A shiny Pokémon was caught! Pokémon: {pokemon}')
                            log(f'Shiny: {shiny} | Legendary: {legendary} | Mythical: {mythical}')
                        elif re.findall('^'+pokemon+'$', legendary_list, re.MULTILINE):
                            legendary += 1
                            log(
                                f'A legendary Pokémon was caught! Pokémon: {pokemon}')
                            log(f'Shiny: {shiny} | Legendary: {legendary} | Mythical: {mythical}')
                        elif re.findall('^'+pokemon+'$', mythical_list, re.MULTILINE):
                            mythical += 1
                            log(
                                f'A mythical Pokémon was caught! Pokémon: {pokemon}')
                            log(f'Shiny: {shiny} | Legendary: {legendary} | Mythical: {mythical}')
                        else:
                            print(f'Total Pokémon Caught: {num_pokemon}')

                    elif 'human' in content:
                        stop(spam_process)
                        log('Captcha Detected; Autocatcher Paused. Press enter to restart.')
                        input()
                        bot.sendMessage(catch_id, '<@716390085896962058> h')


if __name__ == '__main__':
    print(
        f'Pokétwo Autocatcher {version}\nA#Pokétwo Autocatcher# \nEvent Log:')
    spam_process = start_spam()
    bot.gateway.run(auto_reconnect=True)
