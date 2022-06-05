from nextcord.ext import commands
import nextcord as discord
import asyncio
import json


# make it so that only author can respond
class NextButton(discord.ui.View):
    def __init__(self, questions,author,step,name):
        super().__init__(timeout=None)
        self.questions = questions
        self.author = author
        self.step = step
        self.name = name
    @discord.ui.button(label="Next", style=discord.ButtonStyle.green)
    async def one(self, button: discord.ui.Button, interaction: discord.Interaction):
        button.disabled = True
        next = int(self.step +1)
        mod = Form(questions=self.questions,step=next,name=self.name)
        await interaction.response.send_modal(mod)
        msg = await interaction.original_message()
        await msg.edit(view=self)
        self.stop()


class ConfirmDeletion(discord.ui.View):
    def __init__(self, form_name,forms_msg,msg_obj,self_msg):
        super().__init__(timeout=10)
        self.form = form_name
        self.msg = forms_msg
        self.self_msg = self_msg
        self.msg_obj = msg_obj
        with open('databases/applications.json','r') as f:
            self.apps = json.load(f)

    @discord.ui.button(label="Yes",style=discord.ButtonStyle.danger)
    async def delete_form(self, button: discord.ui.Button, interaction: discord.Interaction):
        del self.apps[str(interaction.guild_id)][self.form]
        channel = interaction.channel
        _forms = FormsView(self.apps[str(interaction.guild_id)],self.msg,await channel.fetch_message(self.msg))
        msg = await channel.fetch_message(int(self.msg))
        await msg.edit(embed=None,view=_forms,content=None)
        for item in self.children:
            item.disabled = True
        await interaction.response.edit_message(content="Form Deleted!",view=self)
        with open('databases/applications.json','w') as f:
            json.dump(self.apps,f,indent=4)
        self.stop()
    @discord.ui.button(label="No",style=discord.ButtonStyle.green)
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
        for item in self.children:
            item.disabled = True
        await interaction.response.edit_message(view=self)
        await interaction.send("Cancelling.",ephemeral=True,delete_after=5)
        self.stop()
    async def on_timeout(self):
        for x in self.children:
            x.disabled = True
        await self.self_msg.edit(view=self)

    



# VIEWS

class FormEditor(discord.ui.View):
    def __init__(self, form, msg_id,msg_obj):
        super().__init__(timeout=100)
        self.form = form
        self.msg_id = msg_id
        self.msg_obj = msg_obj
        with open('databases/applications.json','r') as f:
            self.apps = json.load(f)

    @discord.ui.button(label="Delete Form", style=discord.ButtonStyle.danger)
    async def delete(self,button: discord.ui.Button, interaction: discord.Interaction):
        ch = interaction.channel
        await interaction.response.send_message(ephemeral=True,content="Are you sure?")
        view = ConfirmDeletion(self.form,self.msg_id, await ch.fetch_message(self.msg_id),await interaction.original_message())
        await interaction.edit_original_message(view=view)
    @discord.ui.button(label="View Questions", style=discord.ButtonStyle.gray)
    async def questions(self,button: discord.ui.Button, interaction: discord.Interaction):
        ch = interaction.channel
        view = QuestionsView(self.form,self.msg_id, await ch.fetch_message(self.msg_id),interaction.guild_id)
        await interaction.response.edit_message(content="Showing All Questions",view=view,embed=None)
    @discord.ui.button(label="View Responses", style=discord.ButtonStyle.gray)
    async def responses(self,button: discord.ui.Button, interaction: discord.Interaction):
        ...
    @discord.ui.button(label="Form Open/Closed", style=discord.ButtonStyle.green)
    async def form_toggle(self,button: discord.ui.Button, interaction: discord.Interaction):
        _open = self.apps[str(interaction.guild_id)][str(self.form)]['open']
        if _open:
            self.apps[str(interaction.guild_id)][str(self.form)]['open'] = False
            await interaction.response.send_message("Form is now closed!",ephemeral=True)
        else:
            self.apps[str(interaction.guild_id)][str(self.form)]['open'] = True
            await interaction.response.send_message("Form is now open!",ephemeral=True)
        with open('databases/applications.json','w') as f:
            json.dump(self.apps, f, indent=4)
    @discord.ui.button(label="Edit Form Title", style=discord.ButtonStyle.green)
    async def form_edit(self,button: discord.ui.Button, interaction: discord.Interaction):
        form = NewFormTitle(self.msg_id, self.form)
        await interaction.response.send_modal(form)
    @discord.ui.button(label="Back", style=discord.ButtonStyle.blurple)
    async def form_back(self,button: discord.ui.Button, interaction: discord.Interaction):
        ch = interaction.channel
        _forms = FormsView(self.apps[str(interaction.guild_id)],self.msg_id,await ch.fetch_message(self.msg_id))
        await interaction.response.edit_message(embed=None,view=_forms,content=None)
        self.parent.stop()

    async def on_timeout(self):
        for x in self.children:
            x.disabled = True
        await self.msg_obj.edit(view=self)

class Forms(discord.ui.Select):
    def __init__(self,forms,id,parent):
        items = []
        self.parent = parent
        self.msg_id = id
        for item in forms:
            items.append(discord.SelectOption(label=f"{item} Form"))
        super().__init__(placeholder="Choose a form to edit.",min_values=1,max_values=1,options=items)
    async def callback(self, interaction: discord.Interaction):
        with open('databases/applications.json','r') as f:
            apps = json.load(f)
        e = discord.Embed(title=f"Settings for {self.values[0][:-5]} Form",color=discord.Color.random())
        e.add_field(name="Responses",value=len(apps[str(interaction.guild_id)][self.values[0][:-5]]['responses']))
        ch = interaction.channel
        view = FormEditor(self.values[0][:-5],self.msg_id, await ch.fetch_message(self.msg_id))
        await interaction.response.edit_message(view=view,embed=e)
        self.parent.stop()


class Questions(discord.ui.Select):
    def __init__(self,form,id,guild_id,msg_obj):
        items = []
        with open('databases/applications.json','r') as f:
            apps = json.load(f)
        self.msg_id = id
        self.obj = msg_obj
        self.g_id = guild_id
        _form = apps[str(self.g_id)][form]['questions']
        self.form = _form
        for item in _form:
            items.append(discord.SelectOption(label=item['label']))
        super().__init__(placeholder="Choose a question to edit.",min_values=1,max_values=1,options=items)
    async def callback(self,interaction: discord.Interaction) -> None:
        question = ...
        for i in self.form:
            if i['label'] == self.values[0]:
                question = i
                break
        e = discord.Embed(title="Question Editor",color=discord.Color.random())
        e.add_field(name="Placeholder",value=question['placeholder'])
        e.add_field(name="Required",value=('True' if question['required'] else 'False'))
        e.add_field(name="Style",value=f"{'One Line' if question['style'] == 0  else 'Paragraph'}")
        e.add_field(name="Question",value=question['label'])
        await interaction.response.edit_message(embed=e,content=None)
class Responses(discord.ui.Select):
    ...

# force timeouts
class QuestionsView(discord.ui.View):
    def __init__(self,form,id,msg_obj,guild_id):
        super().__init__(timeout=10)
        self.add_item(Questions(form,id,guild_id,msg_obj))
        self.msg_id = id
        self.msg_obj = msg_obj
        self.form = form
        with open('databases/applications.json','r') as f:
            self.apps = json.load(f)


    @discord.ui.button(label="Edit Question",style=discord.ButtonStyle.blurple)
    async def edit(self, button: discord.ui.Button, interaction: discord.Interaction):
        ...

    @discord.ui.button(label="Delete Question",style=discord.ButtonStyle.danger)
    async def delete(self, button: discord.ui.Button, interaction: discord.Interaction):
        ...
    @discord.ui.button(label="Back", style=discord.ButtonStyle.blurple)
    async def form_back(self,button: discord.ui.Button, interaction: discord.Interaction):
        ch = interaction.channel
        e = discord.Embed(title=f"Settings for {self.form} Form",color=discord.Color.random())
        e.add_field(name="Responses",value=len(self.apps[str(interaction.guild_id)][self.form]['responses']))
        _forms = FormEditor(self.form,self.msg_id,await ch.fetch_message(self.msg_id))
        await interaction.response.edit_message(embed=e,view=_forms,content=None)

    async def on_timeout(self):
        for x in self.children:
            x.disabled = True
        await self.msg_obj.edit(view=self)

class ResponsesView(discord.ui.View):
    ...



class FormsView(discord.ui.View):
    def __init__(self,forms,id,msg_obj):
        super().__init__(timeout=100)
        self.add_item(Forms(forms,id,self))
        self.id = id
        self.msg_obj = msg_obj

    @discord.ui.button(label="Add new Form",style=discord.ButtonStyle.green)
    async def new(self, button: discord.ui.button, interaction: discord.Interaction):
        with open('databases/applications.json','r') as f:
            apps = json.load(f)
        forms = len(apps[str(interaction.guild_id)])
        if forms == 5:
            return await interaction.response.send_message("You have the max amount of forms (5)! Remove one to create a new form!")
        modal = NewForm(self.id)
        await interaction.response.send_modal(modal)

    async def on_timeout(self):
        for x in self.children:
            x.disabled = True
        await self.msg_obj.edit(view=self)

# MODALS

class NewFormTitle(discord.ui.Modal):
    def __init__(self,id,form_name):
        super().__init__(title="Edit Form Title",timeout=None)
        self._title = discord.ui.TextInput(label="New Title",placeholder="Ex: Staff Application",required=True,style= discord.TextInputStyle.short)
        self._id = id
        self.form_name = form_name
        self.add_item(self._title)

    async def callback(self, interaction: discord.Interaction) -> None:
        with open('databases/applications.json','r') as f:
            apps = json.load(f)
        value = self._title.value
        forms = apps[str(interaction.guild_id)]
        new_forms = {value if k == self.form_name else k:v for k,v in forms.items()}
        apps[str(interaction.guild_id)] = new_forms
        await interaction.send(content="Form title changed!",delete_after=5)
        with open('databases/applications.json','w') as f:
            json.dump(apps,f,indent=4)
        ch = interaction.channel
        view = FormEditor(self._title.value,self._id, await ch.fetch_message(self._id))
        e = discord.Embed(title=f"Settings for {value} Form",color=discord.Color.random())
        e.add_field(name="Responses",value=len(apps[str(interaction.guild_id)][value]['responses']))
        await interaction.followup.edit_message(self._id,view=view,embed=e)

class NewForm(discord.ui.Modal):
    def __init__(self,id):
        super().__init__(title="Create new Form",timeout=None)
        self._title = discord.ui.TextInput(label="Title",placeholder="Ex: Staff Application",required=True,style= discord.TextInputStyle.short)
        self._id = id
        self.add_item(self._title)


    async def callback(self, interaction: discord.Interaction) -> None:
        with open('databases/applications.json','r') as f:
            apps = json.load(f)
        value = self._title.value
        ch = interaction.channel
        apps[str(interaction.guild_id)][value] = {}
        apps[str(interaction.guild_id)][value]['questions'] = []
        apps[str(interaction.guild_id)][value]['open'] = True
        apps[str(interaction.guild_id)][value]['responses'] = {}
        await interaction.send(content="Form created!",delete_after=5)
        with open('databases/applications.json','w') as f:
            json.dump(apps,f,indent=4)
        view = FormsView(apps[str(interaction.guild_id)],self._id, await ch.fetch_message(self._id))
        await interaction.followup.edit_message(self._id,view=view)


        
class Form(discord.ui.Modal):
    def __init__(self,questions,step: int,name):
        super().__init__(
            title=name,
            custom_id="gru:form",
            timeout=None)  # Modal title
        self.name = name
        self.step = step
        self.questions = None
        self.tmp = questions
        if self.step == 1:
            self.questions = questions[0:(len(questions) if len(questions) < 5 else 5)]
        elif self.step ==2:
            self.questions = questions[5:(len(questions) if len(questions) < 10 else 10)]
        elif self.step == 3:
            self.questions = questions[10:(len(questions) if len(questions) < 15 else 15)]
        elif self.step ==4:
            self.questions = questions[15:(len(questions) if len(questions) < 20 else 20)]
        self.modals = []
        for item in self.questions:
            i = discord.ui.TextInput(
                label=item['label'],
                placeholder = item['placeholder'] if item['placeholder'] else None,
                required = item['required'],
                style= discord.TextInputStyle.paragraph if item['style'] == 1 else discord.TextInputStyle.short
            )
            self.modals.append(i)
            self.add_item(i)
    
    
    async def callback(self, interaction: discord.Interaction) -> None:
        """This is the function that gets called when the submit button is pressed"""
        response = ''
        submission_data = []
        for item in self.modals:
            response += f"{item.label}: {item.value}\n"
            id = interaction.guild_id
            submission_data.append(item.value)
        with open('databases/applications.json','r') as f:
            apps = json.load(f)
        try:
            apps[str(id)]['responses']
        except:
            apps[str(id)]['responses'] = {}
        try:
            apps[str(id)]['responses'][str(interaction.user.id)]
        except:
             apps[str(id)]['responses'][str(interaction.user.id)] = {}
        if apps[str(id)]['responses'][str(interaction.user.id)] == {}:
            apps[str(id)]['responses'][str(interaction.user.id)] = {'answers':submission_data,'accepted':False,'denied':False,'reason':''}
        else:
            apps[str(id)]['responses'][str(interaction.user.id)]['answers'] += submission_data
        with open('databases/applications.json','w') as f:
            json.dump(apps, f, indent=4)
        if len(self.tmp) >self.step*5:
            await interaction.send("Click here to go to the next step of the form!",view=NextButton(self.tmp, interaction.user,self.step,self.name),ephemeral=True)
        else:
            return await interaction.send("You have finished this form! I will message you when your form status has changed.",ephemeral=True)


# @application.subcommand(description="Allows you to do the application process for staff in this server.")
# async def start(interaction: discord.Interaction):
#     with open('databases/applications.json','r') as f:
#         apps = json.load(f)
#     if not apps[str(interaction.guild_id)]['Staff Application']['open']:
#         return await interaction.response.send_message("Sorry, applications are not open on this server.")
#     try:
#         us= apps[str(interaction.guild_id)]['Staff Application']['responses'][str(interaction.user.id)]
    
#         if us['accepted'] == False and us['denied'] == False:
#             return await interaction.response.send_message("You already have an application open!")
#     except:
#         pass
#     modal = Form(apps[str(interaction.guild_id)]["Staff Application"]['questions'],1,"Staff Application form")
    
#     await interaction.response.send_modal(modal)





class FormsCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    
    @commands.command()
    async def forms(self,ctx):
        with open('databases/applications.json','r') as f:
            apps = json.load(f)
        msg = await ctx.reply("Showing all forms.")
        _forms = FormsView(apps[str(ctx.guild.id)],msg.id,msg)
    
        await msg.edit(view=_forms)



def setup(bot):
    bot.add_cog(FormsCog(bot))