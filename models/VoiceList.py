import discord


class VoiceList(discord.ui.View):

    def __init__(self, list1, list2):
        super().__init__()
        self.list1 = list1
        self.list2 = list2
        self.current = 1
        self.rows = 30

    def create_embed(self, data):
        embed = discord.Embed(title='Voice list')
        embed.add_field(name='**Name**', value=data[0])
        embed.add_field(name='**Language**', value=data[1])
        embed.set_footer(text=f'Page {self.current}/{(len(self.list1) // self.rows) + (len(self.list1) % self.rows > 0)}')
        return embed

    def create_string(self, array):
        out = ''
        for item in array:
            out += str(item) + '\n'
        return out

    async def send(self, ctx):
        self.update_buttons()
        self.message = await ctx.send(view=self)
        data = (self.create_string(self.list1[:self.rows]), self.create_string(self.list2[:self.rows]))
        await self.update_message(data)

    async def update_message(self, data):
        self.update_buttons()
        await self.message.edit(embed=self.create_embed(data), view=self)

    def update_buttons(self):
        if self.current == 1:
            self.first.disabled = True
            self.previous.disabled = True
            self.last.disabled = False
            self.next.disabled = False
        elif self.current == ((len(self.list1) // self.rows) + (len(self.list1) % self.rows > 0)):
            print(self.current)
            self.last.disabled = True
            self.next.disabled = True
            self.first.disabled = False
            self.previous.disabled = False
        else:
            self.last.disabled = False
            self.next.disabled = False
            self.first.disabled = False
            self.previous.disabled = False

    @discord.ui.button(label='<<', style=discord.ButtonStyle.primary)
    async def first(self, interaction: discord.Interaction, button: discord.ui.button):
        await interaction.response.defer()
        self.current = 1
        until_item = self.current * self.rows
        data = (self.create_string(self.list1[:until_item]), self.create_string(self.list2[:until_item]))
        await self.update_message(data)

    @discord.ui.button(label='<', style=discord.ButtonStyle.primary)
    async def previous(self, interaction: discord.Interaction, button: discord.ui.button):
        await interaction.response.defer()
        self.current -= 1
        until_item = self.current * self.rows
        from_item = until_item - self.rows
        data = (self.create_string(self.list1[from_item:until_item]), self.create_string(self.list2[from_item:until_item]))
        await self.update_message(data)

    @discord.ui.button(label='>', style=discord.ButtonStyle.primary)
    async def next(self, interaction: discord.Interaction, button: discord.ui.button):
        await interaction.response.defer()
        self.current += 1
        until_item = self.current * self.rows
        from_item = until_item - self.rows
        data = (self.create_string(self.list1[from_item:until_item]), self.create_string(self.list2[from_item:until_item]))
        await self.update_message(data)

    @discord.ui.button(label='>>', style=discord.ButtonStyle.primary)
    async def last(self, interaction: discord.Interaction, button: discord.ui.button):
        await interaction.response.defer()
        self.current = (len(self.list1) // self.rows) + (len(self.list1) % self.rows > 0)
        until_item = self.current * self.rows
        from_item = until_item - self.rows
        data = (self.create_string(self.list1[from_item:]), self.create_string(self.list2[from_item:]))
        await self.update_message(data)
