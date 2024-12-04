#Next update: loa's, resignations & deny (opposite of approve (delete their entry in the db and add :x: emoji))
#Have packages be a list of dicts instead of a dict of dicts (have timestamp in the dict instead of the timestamp being the key)



import discord, json, datetime, random, requests
from discord.ext import commands
from discord import app_commands, ui
from discord.app_commands import Choice

client = commands.Bot(command_prefix="!", intents=discord.Intents.all())
client.remove_command("help")
tree = client.tree
rosec = "_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_F675C74A267189E264F3C16E2BD077D854AC1A17BFB4C375F739E30EE67D690C6A4E4263078BDF298DD93BB5AFCAD1B3F8CA6006DE16C5A04202878A1C7D8E53CAEF2D7BBC0611CA104F9C9649EE05BA18DA8760AD0FC88AC97B272744232019ACFB9CC8CBD3548449F5F5DF2878AB2D426DCD7949D0311C63ABCE0E6D754D2D832C1F715E18B5F39E4F451F11622821DD34AA90906D518205FCDB1A60E12E9FEABF7089178E312FBC82DC7FCC57F7AAD95955BA8B8FF1D2C520F55DBCE8BF1BB0C481F22961B86C44E7066EF8AA5C31218F8A94120FF63CA97501D0E40C1D897380128EE109D25F26A88B2C58E7CE4120F606F1338FC7809099C04D661FD9C145F3CCFA46F2CEA4EB5A7190A884EA6A2C11AC4FBECEF1252F4C8BDACD439C24CAB50B19D0677C252CB4BEE4802020410CFA791D3B47ACC5E1ADF50684E95558C7D4638ADB4D9DE3C74E2A4E2F2302E38C7D406DC5007A3A97FF03C4B711AD2E90C2F0A95B1C1A90E6A7042347EDDD49F322AD6C493A548E475B7139771ADDA1323D98F38F2D363267AEB004402E76FA2C4E6EB370CF208592F1970CAEFF7776497B3BD91107D8C8C443587D47160138F547A97FE9DB9E0E49D70E47D5E5F8142ADE60967030C6FD92BB9D96FDB91CE3B92A9565407F2253F36C0D0B9311FBDF7F84E1106568509125F181998A279F4BEE3F71744D3283E147923D9E08EC2CC23D214A03E00C2BF4B1C2B5906AA38C4B9BBF7C46C6C5CC3FB340A79852BA86FB956B30CBDCEE5FAE1449CD5F88D798DEDE9D2CE8D8947706E8CFB3D31F58F488900ED7726016CED6D993868244AC8F5E7BB5FF037346C45E8EF7A88BB0E8135678025FD510740E8F14EDA6DEB5D1683F6038EF4046A58F3270B49A3CC1143B485F000A8CF11AB93394A4CFA3C039975900A57C27646BB905F1D5E36765A4002F3CD0C04C37F2FC712CAB772CFEC6FD780C7494F63C199AFE58C23272B960F4B0083E1B955B871EADBCD5E55541D48E06080B5F21F5821B3549AE027E97C3E6187287974FA62F82CF9A8F432625E0267D19649D57B4769E5A3B5562D55E7228C4A5922423"

db = "./PDS/db.json"
logs = "./PDS/logs.txt"
actives = "./PDS/actives.json"
used = "./PDS/used.json"



class Colours:
    class Brand:
        red = 0xBC3131
        blue = 0x2E3E60
        gray = 0x383838
    class Logs:
        red = 0xe96c6c #very bad
        orange = 0xd18f5d #bad
        yellow = 0xe5e07a #eh
        purple = 0xa18ad1 #neutral
        green = 0x6bc96b #good



def precheck():
    async def thecheck(interaction : discord.Interaction):
        actorid = isconnected(interaction.user)
        if not actorid:
            await interaction.response.send_message(embed=discord.Embed(title="Command Error", colour=Colours.Brand.red, description="Uh-oh, it doesn't look like you've connected your **roblox** account"), ephemeral=True)
            return False
        actorrank = iscommand(actorid)
        if actorrank == None:
            await interaction.response.send_message(embed=discord.Embed(title="Command Error", colour=Colours.Brand.red, description="Uh-oh, it doesn't look like you're in the group"), ephemeral=True)
            return False
        return True
    return app_commands.check(thecheck)

def historylog(actorid, userid, timestamp, action, txtaction, division=None):
    userid = str(userid)
    with open(db, "r+") as f:
        data = json.load(f)
        if userid in data["history"]:
            data["history"][userid]["employment"][timestamp] = action
        else:
            data["history"][userid] = {
                "employment": {
                    timestamp: action
                },
                "packages": {
                    "total": 0
                }
            }
            if division:
                data["history"][userid]["division"] = division
        f.seek(0)
        f.truncate()
        json.dump(data, f, indent=4)
    with open(logs, "a") as f:
        f.write(f"[{timestamp}] {txtaction}" + "\n")



#roblox
def getuser(user):
    if isinstance(user, int):
        user = json.loads(requests.get(f"https://users.roblox.com/v1/users/{user}").text)
        if "errors" in user:
            return None
    else:
        user = json.loads(requests.post("https://users.roblox.com/v1/usernames/users", json={"usernames": [user], "excludeBannedUsers": True}).text)
        if not user["data"]:
            return None
        user = user["data"][0]
    return user

def getmugshot(userid):
    pic = json.loads(requests.get(f"https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={userid}&size=720x720&format=Png&isCircular=false").text)["data"][0]["imageUrl"]
    return pic

#returns roid
def isconnected(discorduser):
    with open(db, "r+") as f:
        data = json.load(f)
        if str(discorduser.id) in data["connections"]:
            return data["connections"][str(discorduser.id)]
    return False

#returns whether in group and if command
def iscommand(userid):
    user = [el for el in json.loads(requests.get(f"https://groups.roblox.com/v1/users/{userid}/groups/roles").text)["data"] if el["group"]["id"] == 16367093]
    if user:
        if user[0]["role"]["rank"] >= 30:
            return (True, user[0]["role"])
        else:
            return (False, user[0]["role"])
    else:
        return None



class GeneralTickets(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(emoji="❓", label="Query", style=discord.ButtonStyle.gray, custom_id="general:query")
    async def query(self, interaction : discord.Interaction, button : discord.ui.button):
        ticketcategory = interaction.guild.get_channel(1170190594782535731)
        if ("query-" + str(interaction.user.id)) not in [channel.name for channel in ticketcategory.channels]:
            await interaction.response.send_message("awooga", ephemeral=True)
        else:
            await interaction.response.send_message(f"Alr got one open {[channel.mention for channel in ticketcategory.channels if channel.name == 'query-{str(interaction.user.id)}'][0]}", ephemeral=True)
    
    @discord.ui.button(emoji="❕", label="Report", style=discord.ButtonStyle.red, custom_id="general:report")
    async def report(self, interaction : discord.Interaction, button : discord.ui.button):
        await interaction.response.send_message("agoowa", ephemeral=True)


class GetInvestigationInformation(discord.ui.Modal, title="HR Investigation Information"):
    username = discord.ui.TextInput(label="Username", custom_id="info:username", style=discord.TextStyle.short, placeholder="OnlyTwentyCharacters", required=True, min_length=3, max_length=20)
    events = discord.ui.TextInput(label="Events", custom_id="info:events", style=discord.TextStyle.paragraph, placeholder="Sequence of Events", required=True)
    evidence = discord.ui.TextInput(label="Evidence", custom_id="info:evidence", style=discord.TextStyle.paragraph, placeholder="Media Backups", required=True)
    extra = discord.ui.TextInput(label="Extra", custom_id="info:extra", style=discord.TextStyle.paragraph, placeholder="Additional Information", required=False)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(embed=discord.Embed(title="Loading", colour=Colours.Brand.gray, description="<a:loading:1169045091176951879> Loading, thank you for your patience <a:loading:1169045091176951879>").set_footer(text="Package Delivery Service", icon_url="https://cdn.discordapp.com/emojis/1172218453587935252.webp?size=96&quality=lossless"), ephemeral=True)
        self.modalInteraction = interaction
    
    async def on_error(self, interaction : discord.Interaction, error : Exception):
        await interaction.response.send_message(embed=discord.Embed(title="Error", colour=Colours.Brand.red, description="Uh-oh, it looks like something went wrong, try again").set_footer(text="Package Delivery Service", icon_url="https://cdn.discordapp.com/emojis/1172218453587935252.webp?size=96&quality=lossless"), ephemeral=True)

class CreateInvestigation(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(emoji="📋", label="Create", style=discord.ButtonStyle.gray, custom_id="investigation:create")
    async def create(self, interaction : discord.Interaction, button : discord.ui.button):
        getinvestigationinformationmodal = GetInvestigationInformation()
        await interaction.response.send_modal(getinvestigationinformationmodal)
        success = await getinvestigationinformationmodal.wait()
        if success:
            return
        with open(used, "r+") as f:
            data = json.load(f)
            num = data["nextFree"]
            data["nextFree"] += 1
            f.seek(0)
            f.truncate()
            json.dump(data, f, indent=4)
        overwrites = {
            interaction.guild.get_role(1145424590152151095): discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        ticketcategory = client.get_channel(1170190594782535731)
        ticket = await ticketcategory.create_text_channel(f"PDS-{datetime.datetime.now().strftime('%y')}-{('0' * (4 - len(str(num)))) + str(num)}", overwrites=overwrites)
        ticketinitialview = TicketInitial()
        initialmsg = await ticket.send(embed=discord.Embed(title="Investigation Ticket", colour=Colours.Brand.blue, description=f"**Created By:**{interaction.user.mention}```\nSuspect Username:{getinvestigationinformationmodal.username}\n\nIncident Details:\n{getinvestigationinformationmodal.events}\n\nEvidence Articles:\n{getinvestigationinformationmodal.evidence}\n\nAdditional Information:\n{getinvestigationinformationmodal.extra}\n```"), view=ticketinitialview)
        await initialmsg.pin()
        ping = await ticket.send(interaction.user.mention)
        await ping.delete()
        await ticket.move(beginning=True)
        await getinvestigationinformationmodal.modalInteraction.edit_original_response(embed=discord.Embed(title="Investigation Ticket", colour=Colours.Brand.blue, description=f"Your ticket has successfully been created and can be found here:\n{ticket.mention}"))

class TicketInitial(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(emoji="✅", label="Claim", style=discord.ButtonStyle.green, custom_id="initial:claim")
    async def claim(self, interaction : discord.Interaction, button : discord.ui.button):
        await interaction.channel.edit(topic=str(interaction.user.id))
        ogmsg = interaction.message
        ticketinitialclaimed = TicketInitialClaimed()
        await ogmsg.edit(view=ticketinitialclaimed)
        await ogmsg.unpin()
        ticketclaimed = TicketClaimed()
        await interaction.response.send_message(embed=discord.Embed(title="Investigation Claimed", colour=Colours.Brand.blue, description=f"This Investigation has been Claimed by {interaction.user.mention}"), view=ticketclaimed)
        newmsg = await interaction.original_response()
        await newmsg.pin()
    
    @discord.ui.button(emoji="🔒", label="Close", style=discord.ButtonStyle.red, custom_id="initial:close")
    async def close(self, interaction : discord.Interaction, button : discord.ui.button):
        overwrites = {
            interaction.guild.get_role(1145424590152151095): discord.PermissionOverwrite(read_messages=True, send_messages=False)
        }
        await interaction.channel.edit(category=client.get_channel(1170190723316985856), overwrites=overwrites)
        ogmsg = interaction.message
        ticketinitialclaimed = TicketInitialClaimed()
        await ogmsg.edit(view=ticketinitialclaimed)
        await ogmsg.unpin()
        ticketclosed = TicketClosed()
        await interaction.response.send_message(embed=discord.Embed(title="Investigation Closed", colour=Colours.Brand.blue, description=f"This Investigation has been Closed by {interaction.user.mention}"), view=ticketclosed)
        newmsg = await interaction.original_response()
        await newmsg.pin()


class TicketInitialClaimed(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(emoji="✅", label="Claim", style=discord.ButtonStyle.green, disabled=True, custom_id="initialclaimed:claim")
    async def claim(self, interaction : discord.Interaction, button : discord.ui.button):
        pass
    
    @discord.ui.button(emoji="🔒", label="Close", style=discord.ButtonStyle.red, disabled=True, custom_id="initialclaimed:close")
    async def close(self, interaction : discord.Interaction, button : discord.ui.button):
        pass

class TicketClaimed(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(emoji="🔒", label="Close", style=discord.ButtonStyle.red, custom_id="claimed:close")
    async def close(self, interaction : discord.Interaction, button : discord.ui.button):
        overwrites = {
            interaction.guild.get_role(1145424590152151095): discord.PermissionOverwrite(read_messages=True, send_messages=False)
        }
        await interaction.channel.edit(category=client.get_channel(1170190723316985856), overwrites=overwrites)
        ogmsg = interaction.message
        ticketclaimedclosed = TicketClaimedClosed()
        await ogmsg.edit(view=ticketclaimedclosed)
        await ogmsg.unpin()
        ticketclosed = TicketClosed()
        await interaction.response.send_message(embed=discord.Embed(title="Investigation Closed", colour=Colours.Brand.blue, description=f"This Investigation has been Closed by {interaction.user.mention}"), view=ticketclosed)
        newmsg = await interaction.original_response()
        await newmsg.pin()

class TicketClaimedClosed(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(emoji="🔒", label="Close", style=discord.ButtonStyle.red, disabled=True, custom_id="claimedclosed:close")
    async def close(self, interaction : discord.Interaction, button : discord.ui.button):
        pass

class TicketClosed(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(emoji="🔓", label="Re-Open", style=discord.ButtonStyle.gray, custom_id="closed:open")
    async def reopen(self, interaction : discord.Interaction, button : discord.ui.button):
        overwrites = {
            interaction.guild.get_role(1145424590152151095): discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        await interaction.channel.edit(category=client.get_channel(1170190594782535731), overwrites=overwrites)
        ogmsg = interaction.message
        ticketclosedopen = TicketClosedOpen()
        print(ticketclosedopen)
        await ogmsg.edit(view=ticketclosedopen)
        await ogmsg.unpin()
        if interaction.channel.topic:
            newmodal = TicketClaimed()
        else:
            newmodal = TicketInitial()
        await interaction.response.send_message(embed=discord.Embed(title="Investigation Re-Opened", colour=Colours.Brand.blue, description=f"This Investigation has been Re-Opened by {interaction.user.mention}"), view=newmodal)
        newmsg = await interaction.original_response()
        await newmsg.pin()

class TicketClosedOpen(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(emoji="🔓", label="Re-Open", style=discord.ButtonStyle.gray, disabled=True, custom_id="closedopen:close")
    async def reopen(self, interaction : discord.Interaction, button : discord.ui.button):
        pass

async def setup_hook(self):
    #Public & HR Only
    generalticketsview = GeneralTickets()
    createinvestigationview = CreateInvestigation()
    ticketinitialview = TicketInitial()
    ticketclaimedview = TicketClaimed()
    ticketclosedview = TicketClosed()
    views = [generalticketsview, createinvestigationview, ticketinitialview, ticketclaimedview, ticketclosedview]
    for view in views:
        self.add_view(view)

@client.event
async def on_ready():
    await setup_hook(client)
    print(f"Packages now online with {round(client.latency * 1000)}ms ping.")



@tree.command(name="link", description="Link your Roblox and Discord", guilds=[discord.Object(1145424590152151091)])
async def link(interaction : discord.Interaction, username : str):
    await interaction.response.send_message(embed=discord.Embed(title="Loading", colour=Colours.Brand.gray, description="<a:loading:1169045091176951879> Loading, thank you for your patience <a:loading:1169045091176951879>").set_footer(text="Package Delivery Service", icon_url="https://cdn.discordapp.com/emojis/1172218453587935252.webp?size=96&quality=lossless"), ephemeral=True)
    with open(db, "r+") as f:
        data = json.load(f)
        if str(interaction.user.id) in data["connections"]:
            await interaction.edit_original_response(embed=discord.Embed(title="Link Error", colour=Colours.Brand.red, description="Uh-oh, it looks like you've already connected your Roblox & Discord together\nIf you believe this is a mistake or wish to unlink your accounts, use the `/unlink` command"))
            return
    user = getuser(username)
    if not user:
        await interaction.edit_original_response(embed=discord.Embed(title="Link Error", colour=Colours.Brand.red, description="Uh-oh, it looks like the username you entered is not a valid __Roblox__ account"))
    userid = user["id"]
    colours = ["black", "blue", "brown", "green", "orange", "purple", "red", "white", "yellow"]
    animals = ["sheep", "cow", "pig", "dog", "cat", "fish", "panda", "rabbit"]
    code = f"{random.choice(colours)} {random.choice(animals)} {random.choice(colours)} {random.choice(animals)} {random.choice(colours)} {random.choice(animals)}"

    #Create View
    class ConfirmButton(discord.ui.View):
        #Setup View
        def __init__(self, *, clicked=False, timeout=180):
            #Globalise
            super().__init__(timeout=timeout)
            self.value = None
        
        #Add button to view
        @discord.ui.button(emoji="✔", label="Done", style=discord.ButtonStyle.green)
        #Button onclick function
        async def donebutton(self, button : discord.ui.Button, interaction : discord.Interaction):
            self.value = True
            self.stop()
    
    confirmChange = ConfirmButton()
    await interaction.edit_original_response(embed=discord.Embed(title="Link Code", colour=Colours.Brand.gray, description=f"Set your Roblox **About** section to;```\n{code}\n```If the code ends up being tagged, just click \"Dismiss message\" and try the command again").set_footer(text="This prompt will expire after 3 minute"), view=confirmChange)
    await confirmChange.wait()
    if confirmChange.value:
        user = getuser(user["id"])
        if code not in user["description"]:
            await interaction.edit_original_response(embed=discord.Embed(title="Link Error", colour=Colours.Brand.red, description=f"Uh-oh, it looks like you haven't put in the correct code.\nTry again"), view=None)
            return
        mugshot = getmugshot(user["id"])
        await interaction.edit_original_response(embed=discord.Embed(title="Link Success", colour=Colours.Brand.blue, description=f"You have successfully connected {interaction.user.mention} to `{username}`").set_thumbnail(url=json.loads(requests.get(f"https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={user['id']}&size=720x720&format=Png&isCircular=false").text)["data"][0]["imageUrl"]), view=None)
        with open(db, "r+") as f:
            data = json.load(f)
            data["connections"][str(interaction.user.id)] = user["id"]
            f.seek(0)
            f.truncate()
            json.dump(data, f, indent=4)
    else:
        await interaction.edit_original_response(embed=discord.Embed(title="Link Error", colour=Colours.Brand.red, description=f"3 Minute link timer expired"), view=None)

@tree.command(name="unlink", description="Unlink your Roblox and Discord", guilds=[discord.Object(1145424590152151091)])
@precheck()
async def unlink(interaction : discord.Interaction, username : str):
    await interaction.response.send_message(embed=discord.Embed(title="Loading", colour=Colours.Brand.gray, description="<a:loading:1169045091176951879> Loading, thank you for your patience <a:loading:1169045091176951879>").set_footer(text="Package Delivery Service", icon_url="https://cdn.discordapp.com/emojis/1172218453587935252.webp?size=96&quality=lossless"), ephemeral=True)
    with open(db, "r+") as f:
        data = json.load(f)
        del data["connections"][str(interaction.user.id)]
        f.seek(0)
        f.truncate()
        json.dump(data, f, indent=4)
    await interaction.edit_original_response(embed=discord.Embed(title="Unlinked", colour=Colours.Brand.blue, description="Your Roblox and Discord accounts have successfully been unlinked"))

@tree.command(name="submit", description="Submit packages", guilds=[discord.Object(1145424590152151091)])
@precheck()
async def submit(interaction : discord.Interaction, amount : int, startsc : str, endsc : str):
    await interaction.response.send_message(embed=discord.Embed(title="Loading", colour=Colours.Brand.gray, description="<a:loading:1169045091176951879> Loading, thank you for your patience <a:loading:1169045091176951879>").set_footer(text="Package Delivery Service", icon_url="https://cdn.discordapp.com/emojis/1172218453587935252.webp?size=96&quality=lossless"), ephemeral=True)
    user = str(isconnected(interaction.user))
    timestamp = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    with open(db, "r+") as f:
        data = json.load(f)
        if user in data["history"]:
            data["history"][user]["packages"][timestamp] = {
                "amount": amount,
                "startsc": startsc,
                "endsc": endsc,
                "verified": False
            }
        else:
            data["history"][user] = {
                "employment": {},
                "packages": {
                    "total": 0,
                    timestamp: {
                        "amount": amount,
                        "startsc": startsc,
                        "endsc": endsc,
                        "verified": False
                    }
                }
            }
        f.seek(0)
        f.truncate()
        json.dump(data, f, indent=4)
    mugshot = getmugshot(user)
    submitchannel = client.get_channel(1159248926684221571)
    await submitchannel.send(embed=discord.Embed(title=user, colour=Colours.Brand.blue, description=f"{timestamp}\n{amount}\n[ Start Screenshot ]({startsc})\n[ End Screenshot ]({endsc})").set_thumbnail(url=mugshot))
    await interaction.edit_original_response(embed=discord.Embed(title="Package Submission", colour=Colours.Brand.blue, description="Your packages have successfully been submitted").set_thumbnail(url=mugshot))

@tree.command(name="approve", description="Approve packages", guilds=[discord.Object(1145424590152151091)])
@precheck()
async def approve(interaction : discord.Interaction, msgid : str):
    await interaction.response.send_message(embed=discord.Embed(title="Loading", colour=Colours.Brand.gray, description="<a:loading:1169045091176951879> Loading, thank you for your patience <a:loading:1169045091176951879>").set_footer(text="Package Delivery Service", icon_url="https://cdn.discordapp.com/emojis/1172218453587935252.webp?size=96&quality=lossless"), ephemeral=True)
    try:
        msgid = int(msgid)
        packages = await interaction.channel.fetch_message(msgid)
    except:
        await interaction.edit_original_response(embed=discord.Embed(title="Approve Packages Error", colour=Colours.Brand.red, description="Uh-oh, it doesn't look like that is a valid Message ID"))
        return
    if packages.author.id != 1143679506842931231 or not packages.embeds:
        await interaction.edit_original_response(embed=discord.Embed(title="Approve Packages Error", colour=Colours.Brand.red, description="Uh-oh, it doesn't look like that message is a package submission"))
        return
    if any([reaction for reaction in ["✅", "❌"] if reaction in [reaction.emoji for reaction in packages.reactions]]):
        await interaction.edit_original_response(embed=discord.Embed(title="Approve Packages Error", colour=Colours.Brand.red, description="Uh-oh, it looks like those packages have already been handled"))
        return
    info = packages.embeds[0]
    userid = info.title
    username = getuser(int(userid))["name"]
    actorid = isconnected(interaction.user)
    actorname = getuser(actorid)["name"]
    timestamp = info.description.split("\n")[0]
    amount = int(info.description.split("\n")[1])
    await interaction.edit_original_response(embed=discord.Embed(title="Packages Approved", colour=Colours.Brand.blue, description=f"`{username}`'s `{amount}` packages have been approved"))
    with open(db, "r+") as f:
        data = json.load(f)
        data["history"][userid]["packages"][timestamp]["verified"] = actorid
        data["history"][userid]["packages"]["total"] += amount
        f.seek(0)
        f.truncate()
        json.dump(data, f, indent=4)
    with open(logs, "a") as f:
        f.write(f"[{timestamp}] {username} ({userid}) {amount} PACKAGES APPROVED BY {actorname} ({actorid})\n")
    await packages.add_reaction("✅")

@tree.command(name="reject", description="Reject packages", guilds=[discord.Object(1145424590152151091)])
@precheck()
async def reject(interaction : discord.Interaction, msgid : str, reason : str):
    await interaction.response.send_message(embed=discord.Embed(title="Loading", colour=Colours.Brand.gray, description="<a:loading:1169045091176951879> Loading, thank you for your patience <a:loading:1169045091176951879>").set_footer(text="Package Delivery Service", icon_url="https://cdn.discordapp.com/emojis/1172218453587935252.webp?size=96&quality=lossless"), ephemeral=True)
    try:
        msgid = int(msgid)
        packages = await interaction.channel.fetch_message(msgid)
    except:
        await interaction.edit_original_response(embed=discord.Embed(title="Reject Packages Error", colour=Colours.Brand.red, description="Uh-oh, it doesn't look like that is a valid Message ID"))
        return
    if packages.author.id != 1143679506842931231 or not packages.embeds:
        await interaction.edit_original_response(embed=discord.Embed(title="Reject Packages Error", colour=Colours.Brand.red, description="Uh-oh, it doesn't look like that message is a package submission"))
        return
    if any([reaction for reaction in ["✅", "❌"] if reaction in [reaction.emoji for reaction in packages.reactions]]):
        await interaction.edit_original_response(embed=discord.Embed(title="Reject Packages Error", colour=Colours.Brand.red, description="Uh-oh, it looks like those packages have already been handled"))
        return
    info = packages.embeds[0]
    userid = info.title
    username = getuser(int(userid))["name"]
    actorid = isconnected(interaction.user)
    actorname = getuser(actorid)["name"]
    timestamp = info.description.split("\n")[0]
    amount = int(info.description.split("\n")[1])
    await interaction.edit_original_response(embed=discord.Embed(title="Packages Rejected", colour=Colours.Brand.blue, description=f"`{username}`'s `{amount}` packages have been rejected"))
    with open(db, "r+") as f:
        data = json.load(f)
        del data["history"][userid]["packages"][timestamp]
        f.seek(0)
        f.truncate()
        json.dump(data, f, indent=4)
    with open(logs, "a") as f:
        f.write(f"[{timestamp}] {username} ({userid}) {amount} PACKAGES REJECTED BY {actorname} ({actorid}) FOR {reason}\n")
    await packages.add_reaction("❌")

action = app_commands.Group(name="action", description="Everything related to performing group actions")
action = app_commands.guilds(discord.Object(1145424590152151091))(action)
tree.add_command(action)

@action.command(name="hire", description="Hire a user")
@precheck()
@app_commands.choices(rank = [
    Choice(name="Manager", value="40"),
    Choice(name="Supervisor", value="30"),
    Choice(name="Senior Delivery Driver", value="20"),
    Choice(name="Delivery Driver", value="17"),
    Choice(name="Trainee Delivery Driver", value="15")
])
@app_commands.choices(division = [
    Choice(name="Delivery", value="Dlvry"),
    Choice(name="Human Resources", value="HR"),
    Choice(name="Management", value="Mgmt")
])
async def hire(interaction : discord.Interaction, user : str, rank : Choice[str]=None, division : Choice[str]=None, notes : str=None):
    await interaction.response.send_message(embed=discord.Embed(title="Loading", colour=Colours.Brand.gray, description="<a:loading:1169045091176951879> Loading, thank you for your patience <a:loading:1169045091176951879>").set_footer(text="Package Delivery Service", icon_url="https://cdn.discordapp.com/emojis/1172218453587935252.webp?size=96&quality=lossless"), ephemeral=True)
    #actor checks
    actorid = isconnected(interaction.user)
    actorname = getuser(actorid)["name"]
    actorrank = iscommand(actorid)
    if not actorrank[0]:
        await interaction.edit_original_response(embed=discord.Embed(title="Action Hire Error", colour=Colours.Brand.red, description="Uh-oh, it doesn't look like you can do that"))
        return
    #checks
    user = getuser(user)
    if not user:
        await interaction.edit_original_response(embed=discord.Embed(title="Action Hire Error", colour=Colours.Brand.red, description="Uh-oh, it doesn't look like that user exists"))
        return
    userid = user["id"]
    username = user["name"]
    #code
    embed = discord.Embed(
        title="PDS Business Actions",
        colour=Colours.Logs.green,
        description=f"**User Hired**\n`{username}` has been **hired** into the business."
    )
    mugshot = getmugshot(userid)
    embed.set_thumbnail(url=mugshot)
    embed.set_footer(text=interaction.user.nick, icon_url="https://cdn.discordapp.com/emojis/1172218453587935252.webp?size=96&quality=lossless")
    if not rank:
        class rank:
            name = "Trainee Delivery Driver"
            value = "15"
    embed.add_field(name="Rank", value=rank.name, inline=False)
    if not division:
        class division:
            name = "Delivery"
            value = "Dlvry"
    embed.add_field(name="Division", value=division.name, inline=False)
    if notes:
        embed.add_field(name="Notes", value=notes, inline=False)
    actionchannel = client.get_channel(1145424593213988967)
    actionlink = await actionchannel.send(embed=embed)
    actionlink = actionlink.jump_url
    await interaction.edit_original_response(embed=discord.Embed(title="Action Hire Successful", colour=Colours.Brand.blue, description=f"User has successfully been hired\n{actionlink}"))
    log = {
        "hired": {
            "rank": rank.name,
            "division": division.name
        }
    }
    if notes:
        log["hired"]["notes"] = notes
    log["hired"]["by"] = actorid
    timestamp = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    historylog(actorid, userid, timestamp, log, f"{username} ({userid}) HIRED BY {actorname} ({actorid}) AS {rank.name} IN {division.name} EXTRA {notes}", division.name)
    el = requests.post(f"https://groups.roblox.com/v1/groups/16367093/join-requests/users/{userid}", cookies={".ROBLOSECURITY": rosec})
    el = requests.post(f"https://groups.roblox.com/v1/groups/16367093/join-requests/users/{userid}", cookies={".ROBLOSECURITY": rosec}, headers={"x-csrf-token": el.headers["x-csrf-token"]})
    if rank.name == "Trainee Delivery Driver":
        return
    roleId = {"40": 100735232, "30": 100735223, "20": 100735217, "17": 91563673, "15": 101369050}[rank.value]
    el = requests.patch(f"https://groups.roblox.com/v1/groups/16367093/users/{userid}", data={"roleId": roleId}, cookies={".ROBLOSECURITY": rosec})
    el = requests.patch(f"https://groups.roblox.com/v1/groups/16367093/users/{userid}", data={"roleId": roleId}, cookies={".ROBLOSECURITY": rosec}, headers={"x-csrf-token": el.headers["x-csrf-token"]})

@action.command(name="rank", description="Rank a user")
@precheck()
@app_commands.choices(rank = [
    Choice(name="Manager", value="40"),
    Choice(name="Supervisor", value="30"),
    Choice(name="Senior Delivery Driver", value="20"),
    Choice(name="Delivery Driver", value="17"),
    Choice(name="Trainee Delivery Driver", value="15")
])
async def rank(interaction : discord.Interaction, user : str, rank : Choice[str], notes : str=None):
    await interaction.response.send_message(embed=discord.Embed(title="Loading", colour=Colours.Brand.gray, description="<a:loading:1169045091176951879> Loading, thank you for your patience <a:loading:1169045091176951879>").set_footer(text="Package Delivery Service", icon_url="https://cdn.discordapp.com/emojis/1172218453587935252.webp?size=96&quality=lossless"), ephemeral=True)
    #actor checks
    actorid = isconnected(interaction.user)
    actorname = getuser(actorid)["name"]
    actorrank = iscommand(actorid)
    if not actorrank[0]:
        await interaction.edit_original_response(embed=discord.Embed(title="Action Rank Error", colour=Colours.Brand.red, description="Uh-oh, it doesn't look like you can do that"))
        return
    #user checks
    user = getuser(user)
    if not user:
        await interaction.edit_original_response(embed=discord.Embed(title="Action Rank Error", colour=Colours.Brand.red, description="Uh-oh, it doesn't look like that user exists"))
        return
    userid = user["id"]
    username = user["name"]
    userrank = iscommand(userid)
    if userrank == None:
        await interaction.edit_original_response(embed=discord.Embed(title="Action Rank Error", colour=Colours.Brand.red, description="Uh-oh, it doesn't look like that user is employed in PDS"))
        return
    #vars
    actorrankrank = actorrank[1]["rank"]
    userrankrank = userrank[1]["rank"]
    userrankname = userrank[1]["name"]
    #code
    if actorrankrank <= userrankrank:
        await interaction.edit_original_response(embed=discord.Embed(title="Action Rank Error", colour=Colours.Brand.red, description=f"Uh-oh, you can't change the rank of a user that has the same or a higher rank than you"))
        return
    if actorrankrank <= int(rank.value):
        await interaction.edit_original_response(embed=discord.Embed(title="Action Rank Error", colour=Colours.Brand.red, description=f"Uh-oh, you can't rank someone to the same or a higher rank than yours"))
        return
    mugshot = getmugshot(userid)
    embed = discord.Embed(
        title="PDS Business Actions",
        colour=Colours.Logs.green,
        description=""
    )
    embed.set_thumbnail(url=mugshot)
    embed.set_footer(text=interaction.user.nick, icon_url="https://cdn.discordapp.com/emojis/1172218453587935252.webp?size=96&quality=lossless")
    promotion = None
    if int(rank.value) > userrankrank:
        promotion = True
        embed.description=f"**User Promoted**\n`{username}` has been **promoted** in the business."
    else:
        promotion = False
        embed.colour=Colours.Logs.red
        embed.description=f"**User Demoted**\n`{username}` has been **demoted** in the business."
    embed.add_field(name="Current", value=rank.name, inline=False)
    embed.add_field(name="Previous", value=userrankname, inline=False)
    if notes:
        embed.add_field(name="Notes", value=notes, inline=False)
    actionchannel = client.get_channel(1145424593213988967)
    actionlink = await actionchannel.send(embed=embed)
    actionlink = actionlink.jump_url
    await interaction.edit_original_response(embed=discord.Embed(title="Action Rank Successful", colour=Colours.Brand.blue, description=f"User rank has successfully been logged\n{actionlink}"))
    log = {
        "ranked": {
            "beforerank": userrankname,
            "afterrank": rank.name,
            "type": {"True": "Promotion", "False": "Demotion"}[str(promotion)]
        }
    }
    if notes:
        log["ranked"]["notes"] = notes
    log["ranked"]["by"] = actorid
    timestamp = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    historylog(actorid, user["id"], timestamp, log, f"{username} ({userid}) { {'True': 'PROMOTED', 'False': 'DEMOTED'}[str(promotion)]} BY {actorname} ({actorid}) FROM {userrankname} TO {rank.name} EXTRA {notes}")
    roleId = {"40": 100735232, "30": 100735223, "20": 100735217, "17": 91563673, "15": 101369050}[rank.value]
    el = requests.patch(f"https://groups.roblox.com/v1/groups/16367093/users/{userid}", data={"roleId": roleId}, cookies={".ROBLOSECURITY": rosec})
    el = requests.patch(f"https://groups.roblox.com/v1/groups/16367093/users/{userid}", data={"roleId": roleId}, cookies={".ROBLOSECURITY": rosec}, headers={"x-csrf-token": el.headers["x-csrf-token"]})

@action.command(name="transfer", description="Transfer a user")
@precheck()
@app_commands.choices(division = [
    Choice(name="Delivery", value="Dlvry"),
    Choice(name="Human Resources", value="HR"),
    Choice(name="Management", value="Mgmt")
])
async def transfer(interaction : discord.Interaction, user : str, division : Choice[str], notes : str=None):
    await interaction.response.send_message(embed=discord.Embed(title="Loading", colour=Colours.Brand.gray, description="<a:loading:1169045091176951879> Loading, thank you for your patience <a:loading:1169045091176951879>").set_footer(text="Package Delivery Service", icon_url="https://cdn.discordapp.com/emojis/1172218453587935252.webp?size=96&quality=lossless"), ephemeral=True)
    #actor checks
    actorid = isconnected(interaction.user)
    actorname = getuser(actorid)["name"]
    actorrank = iscommand(actorid)
    if not actorrank[0]:
        await interaction.edit_original_response(embed=discord.Embed(title="Action Transfer Error", colour=Colours.Brand.red, description="Uh-oh, it doesn't look like you can do that"))
        return
    #user checks
    user = getuser(user)
    if not user:
        await interaction.edit_original_response(embed=discord.Embed(title="Action Transfer Error", colour=Colours.Brand.red, description="Uh-oh, it doesn't look like that user exists"))
        return
    userid = user["id"]
    username = user["name"]
    userrank = iscommand(userid)
    if userrank == None:
        await interaction.edit_original_response(embed=discord.Embed(title="Action Transfer Error", colour=Colours.Brand.red, description="Uh-oh, it doesn't look like that user is employed in PDS"))
        return
    #vars
    userrank = iscommand(userid)
    actorrankrank = actorrank[1]["rank"]
    userrankrank = userrank[1]["rank"]
    with open(db, "r+") as f:
        data = json.load(f)
        beforedivision = data["history"][str(userid)]["division"]
    #code
    if actorrankrank <= userrankrank:
        await interaction.edit_original_response(embed=discord.Embed(title="Action Transfer Error", colour=Colours.Brand.red, description=f"Uh-oh, you can't transfer a user that has the same or a higher rank than you"))
        return
    mugshot = getmugshot(userid)
    embed = discord.Embed(
        title="PDS Business Actions",
        colour=Colours.Logs.purple,
        description=f"**User Transfered**\n`{username}` has **transferred** in the business."
    )
    embed.set_thumbnail(url=mugshot)
    embed.set_footer(text=interaction.user.nick, icon_url="https://cdn.discordapp.com/emojis/1172218453587935252.webp?size=96&quality=lossless")
    embed.add_field(name="Type", value=warntype.name, inline=False)
    embed.add_field(name="Notes", value=notes, inline=False)
    actionchannel = client.get_channel(1145424593213988967)
    actionlink = await actionchannel.send(embed=embed)
    actionlink = actionlink.jump_url
    await interaction.edit_original_response(embed=discord.Embed(title="Action Transfer Successful", colour=Colours.Brand.blue, description=f"User warn has successfully been logged\n{actionlink}"))
    log = {
        "transferred": {
            "beforedivision": beforedivision,
            "afterdivision": division.name
        }
    }
    if notes:
        log["transferred"]["notes"] = notes
    log["transferred"]["by"] = actorid
    timestamp = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    historylog(actorid, user["id"], timestamp, log, f"{username} ({userid}) TRANSFERRED FROM {beforedivision} TO {division.name} BY {actorname} ({actorid}) FOR {notes}")

@action.command(name="warn", description="Warn a user")
@precheck()
@app_commands.choices(warntype = [
    Choice(name="Verbal", value="Vrbl"),
    Choice(name="Record", value="Rcrd")
])
async def warn(interaction : discord.Interaction, user : str, warntype : Choice[str], notes : str):
    await interaction.response.send_message(embed=discord.Embed(title="Loading", colour=Colours.Brand.gray, description="<a:loading:1169045091176951879> Loading, thank you for your patience <a:loading:1169045091176951879>").set_footer(text="Package Delivery Service", icon_url="https://cdn.discordapp.com/emojis/1172218453587935252.webp?size=96&quality=lossless"), ephemeral=True)
    #actor checks
    actorid = isconnected(interaction.user)
    actorname = getuser(actorid)["name"]
    actorrank = iscommand(actorid)
    if not actorrank[0]:
        await interaction.edit_original_response(embed=discord.Embed(title="Action Warn Error", colour=Colours.Brand.red, description="Uh-oh, it doesn't look like you can do that"))
        return
    #user checks
    user = getuser(user)
    if not user:
        await interaction.edit_original_response(embed=discord.Embed(title="Action Warn Error", colour=Colours.Brand.red, description="Uh-oh, it doesn't look like that user exists"))
        return
    userid = user["id"]
    username = user["name"]
    userrank = iscommand(userid)
    if userrank == None:
        await interaction.edit_original_response(embed=discord.Embed(title="Action Warn Error", colour=Colours.Brand.red, description="Uh-oh, it doesn't look like that user is employed in PDS"))
        return
    #vars
    userrank = iscommand(userid)
    actorrankrank = actorrank[1]["rank"]
    userrankrank = userrank[1]["rank"]
    #code
    if actorrankrank <= userrankrank:
        await interaction.edit_original_response(embed=discord.Embed(title="Action Warn Error", colour=Colours.Brand.red, description=f"Uh-oh, you can't warn a user that has the same or a higher rank than you"))
        return
    mugshot = getmugshot(userid)
    embed = discord.Embed(
        title="PDS Business Actions",
        colour=Colours.Logs.orange,
        description=f"**User Warned**\n`{username}` has been **warned** in the business."
    )
    embed.set_thumbnail(url=mugshot)
    embed.set_footer(text=interaction.user.nick, icon_url="https://cdn.discordapp.com/emojis/1172218453587935252.webp?size=96&quality=lossless")
    embed.add_field(name="Type", value=warntype.name, inline=False)
    embed.add_field(name="Notes", value=notes, inline=False)
    actionchannel = client.get_channel(1145424593213988967)
    actionlink = await actionchannel.send(embed=embed)
    actionlink = actionlink.jump_url
    await interaction.edit_original_response(embed=discord.Embed(title="Action Warn Successful", colour=Colours.Brand.blue, description=f"User warn has successfully been logged\n{actionlink}"))
    log = {
        "warned": {
            "type": warntype.name
        }
    }
    if notes:
        log["warned"]["notes"] = notes
    log["warned"]["by"] = actorid
    timestamp = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    historylog(actorid, user["id"], timestamp, log, f"{username} ({userid}) {warntype.name} WARNED BY {actorname} ({actorid}) FOR {notes}")

@action.command(name="term", description="Terminate a user")
@precheck()
@app_commands.choices(termtype = [
    Choice(name="Honourable", value="Hnrbl"),
    Choice(name="General", value="Gnrl"),
    Choice(name="Dishonourable", value="Dshnrbl"),
    Choice(name="Blacklist", value="Blklst")
])
async def term(interaction : discord.Interaction, user : str, termtype : Choice[str], notes : str):
    await interaction.response.send_message(embed=discord.Embed(title="Loading", colour=Colours.Brand.gray, description="<a:loading:1169045091176951879> Loading, thank you for your patience <a:loading:1169045091176951879>").set_footer(text="Package Delivery Service", icon_url="https://cdn.discordapp.com/emojis/1172218453587935252.webp?size=96&quality=lossless"), ephemeral=True)
    #actor checks
    actorid = isconnected(interaction.user)
    actorname = getuser(actorid)["name"]
    actorrank = iscommand(actorid)
    if not actorrank[0]:
        await interaction.edit_original_response(embed=discord.Embed(title="Action Term Error", colour=Colours.Brand.red, description="Uh-oh, it doesn't look like you can do that"))
        return
    #user checks
    user = getuser(user)
    if not user:
        await interaction.edit_original_response(embed=discord.Embed(title="Action Term Error", colour=Colours.Brand.red, description="Uh-oh, it doesn't look like that user exists"))
        return
    userid = user["id"]
    username = user["name"]
    userrank = iscommand(userid)
    if userrank == None:
        await interaction.edit_original_response(embed=discord.Embed(title="Action Term Error", colour=Colours.Brand.red, description="Uh-oh, it doesn't look like that user is employed in PDS"))
        return
    #vars
    actorrankrank = actorrank[1]["rank"]
    userrankrank = userrank[1]["rank"]
    #code
    if actorrankrank <= userrankrank:
        await interaction.edit_original_response(embed=discord.Embed(title="Action Term Error", colour=Colours.Brand.red, description=f"Uh-oh, you can't terminate a user that has the same or a higher rank than you"))
        return
    embed = discord.Embed(
        title="PDS Business Actions",
        colour=Colours.Logs.red,
        description=f"**User Terminated**\n`{username}` has been **terminated** from the business."
    )
    mugshot = getmugshot(userid)
    embed.set_thumbnail(url=mugshot)
    embed.set_footer(text=interaction.user.nick, icon_url="https://cdn.discordapp.com/emojis/1172218453587935252.webp?size=96&quality=lossless")
    embed.add_field(name="Type", value=termtype.name, inline=False)
    embed.add_field(name="Notes", value=notes, inline=False)
    actionchannel = client.get_channel(1145424593213988967)
    actionlink = await actionchannel.send(embed=embed)
    actionlink = actionlink.jump_url
    await interaction.edit_original_response(embed=discord.Embed(title="Action Term Successful", colour=Colours.Brand.blue, description=f"User termination has successfully been logged\n{actionlink}"))
    log = {
        "terminated": {
            "type": termtype.name
        }
    }
    if notes:
        log["terminated"]["notes"] = notes
    log["terminated"]["by"] = actorid
    timestamp = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    historylog(actorid, userid, timestamp, log, f"{username} ({userid}) {termtype.name} TERMINATED BY {actorname} ({actorid}) FOR {notes}")
    el = requests.delete(f"https://groups.roblox.com/v1/groups/16367093/users/{userid}", cookies={".ROBLOSECURITY": rosec})
    el = requests.delete(f"https://groups.roblox.com/v1/groups/16367093/users/{userid}", cookies={".ROBLOSECURITY": rosec}, headers={"x-csrf-token": el.headers["x-csrf-token"]})

@client.command()
@commands.check(lambda ctx : ctx.author.id == 301014178703998987)
async def connect(ctx):
    await tree.sync()
    await tree.sync(guild=discord.Object(1145424590152151091))

@client.command()
@commands.check(lambda ctx : ctx.author.id == 301014178703998987)
async def sendviews(ctx):
    info = client.get_channel(1145424592798756961)
    hrresources = client.get_channel(1145427870450208768)
    generalticketsview = GeneralTickets()
    createinvestigationview = CreateInvestigation()
    await info.send(embed=discord.Embed(title="Public Tickets", colour=Colours.Brand.blue, description="This public ticketing system has been put in place to allow for any aspiring employees or current applicants to submit queries about their position (❓) or for the general public to submit a report against a Delivery Driver (❕)"), view=generalticketsview)
    await hrresources.send(embed=discord.Embed(title="HR Tickets", colour=Colours.Brand.blue, description="Use this private ticketing system to create a HR Investigation channel (📋)"), view=createinvestigationview)

client.run("MTE0MzY3OTUwNjg0MjkzMTIzMQ.GfTZmu.ak01KM5KIMvCyX4uM_nSCnWsWgaYKLZsoLtiug")

#https://discord.com/api/oauth2/authorize?client_id=1143679506842931231&permissions=8&scope=bot