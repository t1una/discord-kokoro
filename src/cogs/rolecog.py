from discord.ext import commands # Bot Commands Frameworkのインポート
from lib.settings import settings
from discord.ext.commands import errors
import discord

# コグとして用いるクラスを定義。
class RoleCog(commands.Cog):

    # TestCogクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot
        self.role_list = settings.get_role_list()

    # メインとなるroleコマンド
    @commands.group()
    async def role(self, ctx):
        # サブコマンドが指定されていない場合、メッセージを送信する。
        if ctx.invoked_subcommand is None:
            await ctx.send('このコマンドにはサブコマンドが必要です。')

    # roleコマンドのサブコマンド
    # 指定したユーザーに指定した役職を付与する。
    @role.command()
    async def add(self, ctx, role: discord.Role):
        if str(role) not in self.role_list:
            await ctx.send('指定可能なロール外です。')
            return None

        if role in ctx.guild.roles:
            try:
                await ctx.author.add_roles(role)
            except errors.BadArgument:
                await ctx.send('実際の役割とソース指定の役割が相違しているよ。')

    # roleコマンドのサブコマンド
    # 指定したユーザーに指定した役職を付与する。
    @role.command()
    async def remove(self, ctx, role: discord.Role):
        if str(role) not in self.role_list:
            await ctx.send('指定可能なロール外です。')
            return None

        if role in ctx.guild.roles:
            try:
                await ctx.author.remove_roles(role)
            except errors.BadArgument:
                await ctx.send('実際の役割とソース指定の役割が相違しているよ。')

    @role.command()
    async def help(self, ctx, *mes: str):
        list_str = "\n".join(self.role_list)
        message = ""
        message = message + "役割一覧は以下の通りだよ。\n" + list_str
        await ctx.send(message)

# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    bot.add_cog(RoleCog(bot)) # TestCogにBotを渡してインスタンス化し、Botにコグとして登録する。