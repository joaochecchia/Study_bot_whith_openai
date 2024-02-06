import discord
from discord.ext import commands, tasks
import asyncio
from dotenv import load_dotenv
import openai
import os

load_dotenv(override=True)

discord_token = os.getenv('discord_key')
openai_key = os.getenv('openai_key')

intents = discord.Intents.all()

# Command prefix
bot = commands.Bot(command_prefix='.', intents=intents)

tasks_list = []

@bot.event
async def on_ready():
    print(f'Bot is online as {bot.user}.')

# Bot menu
@bot.command(name='menu')
async def send_hello(ctx):
    name = ctx.author.name
    response = f'Hello {name}, this is your study bot:\n' \
               f'To add a task, type [.1]\n' \
               f'To list tasks, type [.2]\n' \
               f'To remove a task, type [.3]\n' \
               f'To edit a task, type [.4]\n' \
               f'To ask a question, start with [.?]\n' \
               f'I will ask you what you are doing every hour. To disable, type [.5]'

    await ctx.send(response)

# Add task function
@bot.command(name='1')
async def add_task(ctx):
    await ctx.send('Enter your task: ')
    response = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
    task = response.content
    tasks_list.append(task)
    await ctx.send(f'{task} has been added to your task list.')

# List tasks function
@bot.command(name='2')
async def list_tasks(ctx):
    if len(tasks_list) == 0:
        await ctx.send('There is nothing in the list.')
    else:
        for index, task in enumerate(tasks_list, start=1):
            await ctx.send(f'[{index}] = {task}\n')

# Remove task function
@bot.command(name='3')
async def remove_task(ctx):
    await ctx.send('Enter the task to remove: ')
    response = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
    task_to_remove = response.content
    if task_to_remove in tasks_list:
        tasks_list.remove(task_to_remove)
        await ctx.send(f'{task_to_remove} successfully removed.')
    else:
        await ctx.send(f'{task_to_remove} does not exist.')

# Edit task function
@bot.command(name='4')
async def edit_task(ctx):
    if len(tasks_list) == 0:
        await ctx.send('There are no tasks in the list.')
    else:
        await ctx.send('Enter the task to edit and the new task: ')
        response = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
        edit_task_msg = response.content
        split_edit = edit_task_msg.split(':')

        if split_edit[0] in tasks_list:
            index_to_edit = tasks_list.index(split_edit[0])
            split_edit[1] = split_edit[1].strip()
            tasks_list[index_to_edit] = split_edit[1]
            await ctx.send(f'Task edited successfully: {split_edit[0]} -> {split_edit[1]}')
        else:
            await ctx.send(f'Task "{split_edit[0]}" not found in the list.')

# Define Pomodoro function
@bot.command(name='5')
async def define_pomodoro(ctx):
    global timer_task
    await ctx.send('Enter the time in hh:mm\n[.Stop] to stop the timer.')
    timer_input = await bot.wait_for('message', check=lambda m: m.author == ctx.author)

    if int(timer_input.content[3]) > 5 or timer_input.content[2] != ':':
        await ctx.send('Invalid format!')
        return
    elif timer_input.content[0].lower() == 's':
        await ctx.send('The timer has not been configured yet.')
        return

    min_converter = int(timer_input.content[3] + timer_input.content[4]) * 60
    timer_duration = int(timer_input.content[0] + timer_input.content[1]) * 3600 + min_converter

    @tasks.loop(seconds=timer_duration)
    async def timer_task():
        channel = bot.get_channel(1202614642472652811)
        await channel.send('What are you doing now?')
        check_response = await bot.wait_for('message', check=lambda m: m.author == ctx.author)

        if check_response.content in tasks_list:
            await channel.send('Well done! Keep up with your studies...')
        else:
            await channel.send('You procrastinated, get back to your task.')

    timer_task.start()
    await asyncio.sleep(timer_duration)

# Stop Pomodoro function
@bot.command(name='Stop')
async def stop_pomodoro(ctx):
    global timer_task
    if not timer_task.is_running():
        await ctx.send('The timer has not been configured or is already stopped.')
    else:
        timer_task.stop()
        await ctx.send('The timer will stop in the next cycle.')

# OpenAI chat function
@bot.command(name='?')
async def openai_chat(ctx):
    await ctx.send('What is your question?')
    question_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)

    openai.api_key = openai_key

    def send_message(message, messages_list=[]):
        messages_list.append({'role': 'user', 'content': message})

        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=messages_list
        )

        return response['choices'][0]['message']['content']

    messages_list = []
    answer = send_message(question_msg.content, messages_list)
    messages_list.append(answer)
    await ctx.send(answer)

bot.run(discord_token)
