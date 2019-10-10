import logging
import re

import discord
import pandas as pd
import pytz
from discord.errors import HTTPException
from discord.ext import commands
from markovify import Text

from discordbot.models import MarkovText

from .utils.checks import admin_command, mod_command

logger = logging.getLogger('botLogger.Markov')


class Markov(commands.Cog):

    http_regex = re.compile(
        r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)')
    mention_regex = re.compile(r'\<\@\d+\>')
    emoji_regex = re.compile(r'\<:\w+:\d+\>')

    def __init__(self, bot):
        self.bot = bot
        self.markov_model = MarkovText.objects.first()
        self.markov_text = Text(self.markov_model.text)

    def _clean_up_markov_text(self, df: pd.DataFrame):
        # Filter empty messages and messages from bot
        df = df[df.author_id != 223837667186442240]
        df = df[~df.content.str.contains(r'^!')]
        df = df[df.content.notnull()]
        df['content'] = (df.content
                         .apply(lambda x: self.http_regex.sub(' ', x))
                         .apply(lambda x: self.mention_regex.sub(' ', x))
                         .apply(lambda x: self.emoji_regex.sub(' ', x))
                         .apply(lambda x: re.sub(r'\s+', ' ', x))
                         .str.strip())
        return re.sub(r'\s+', ' ', ' '.join(df.content)).strip()

    @commands.group(invoke_without_command=True)
    async def markov(self, ctx, *, sentence_size=200):
        if not ctx.invoked_subcommand:
            await ctx.send(self.markov_text.make_short_sentence(sentence_size))

    @markov.command()
    @admin_command
    async def update(self, ctx):
        if ctx.channel.id in [178976406288465920]:
            self.markov_model.refresh_from_db()
            if self.markov_model.last_update:
                last_update = self.markov_model.last_update.replace(tzinfo=None)
                logger.info(f'Updating markov text since {last_update}')
                messages = await ctx.channel.history(limit=None, after=last_update).flatten()
            else:
                logger.info('Downloading chat history')
                messages = await ctx.channel.history(limit=None).flatten()
            if messages:
                messages_df = pd.DataFrame([{
                    'message_id': x.id,
                    'author_id': x.author.id,
                    'content': x.content,
                    'created_at': x.created_at,
                } for x in messages]).astype({'created_at': 'datetime64'})
                new_text = self._clean_up_markov_text(messages_df)
                if new_text:
                    self.markov_model.text = f'{new_text} {self.markov_model.text}'
                    self.markov_model.last_update = (messages_df.created_at
                                                     .dt.tz_localize(pytz.UTC)
                                                     .dt.to_pydatetime().max())
                    self.markov_model.save()
                    self.markov_text = Text(self.markov_model.text)
                    logger.info(f'Markov text has been updated with {len(new_text)} characters')
                else:
                    logger.info('There are no messages to add')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if hasattr(error, 'original') and isinstance(error.original, HTTPException):
            if ctx.command.name == 'markov':
                await ctx.send(f"Can't generate text with length of {ctx.kwargs.get('sentence_size')}")


def setup(bot):
    bot.add_cog(Markov(bot))
