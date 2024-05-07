import os
import re
import time
import multiprocessing
import datetime
import random
# copyright to poketwolover69
import keep_alive
# copyright to poketwolover69
# copyright to poketwolover69
import discum

version = '0.0'

owner_id
channel_id = 
catch_id = 
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
    token='', log=False)
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
        content = random.getrandbits(128)
        bot.sendMessage('', content)
        intervals = [3.0, 3.0, 3.0, 3.0] #best interval for spawns in poketwo bot
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
        log(f'the account is now active!')


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
                        bot.sendMessage(catch_id, message=f'<@{owner_id}> please solve the captcha')


if __name__ == '__main__':
    print(
        f'poketwo autocatcher has been started.\nautocatcher version: {version}\nevent log:')
    spam_process = start_spam()
    bot.gateway.run(auto_reconnect=True)
