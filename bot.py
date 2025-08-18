import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import View, Select, Modal, TextInput
from discord.ext import tasks
from discord import SelectOption, ui
from discord.ext import tasks
import time
import datetime, random
import random
import json
import os

# ---------- Khởi tạo intents ----------
intents = discord.Intents.default()
intents.message_content = True

# ---------- Dữ liệu lore, fate, class, item, quest ----------
lore_dict = {
    "abyss": "🌌 Abyss: Vực Thẳm không có đáy. Nơi ánh sáng từng hiện hữu đã bị nuốt trọn, để lại một màu đen đặc sệt đến mức linh hồn cũng không thể thở. Truyền thuyết kể rằng tất cả những linh hồn sa ngã – dù mạnh mẽ đến đâu – cuối cùng cũng sẽ rơi vào Abyss. Ở đó, thời gian dừng lại, ý niệm tan rã. Người bị giam cầm sẽ dần quên tên mình, mục đích của mình, và cuối cùng là chính mình. Chỉ còn lại một bóng đen lang thang gọi là “Những kẻ không-mặt”. Kẻ mạnh không sợ chết – chỉ sợ bị nuốt mất tồn tại.",
    "gate": "⛩ The Gate: Cánh cổng trấn giữ ranh giới giữa thế giới người sống và cõi tử thần. Là nơi những linh hồn chưa định đoạt được vận mệnh phải xếp hàng chờ phán xét. Người ta nói rằng vào những đêm trăng đen, cánh cổng tự hé mở, và một số linh hồn… trốn thoát. Người sống có thể nhìn thấy Gate trong khoảnh khắc họ sắp chết – nhưng một khi nhìn thấy, không ai trở lại là người bình thường. Gate là điểm khởi đầu và cũng là nơi kết thúc, với người sống, kẻ chết và cả những gì nằm giữa.",
    "hollow": "🌫 Whispering Hollow: Một khu rừng nơi gió không bao giờ ngừng thì thầm. Mỗi tán lá, mỗi rễ cây đều mang một câu chuyện chưa hoàn tất – những cái chết bất ngờ, những lời thề chưa thực hiện. Người bước vào Hollow sẽ nghe thấy tiếng gọi bằng giọng của người thân đã khuất, của chính bản thân từ tương lai, hoặc từ những thực tại không bao giờ xảy ra. Họ đi theo tiếng gọi, và tan vào màn sương. Người duy nhất từng sống sót khi trở về... đã tự xé lưỡi mình để không kể lại những gì nghe được.",
    "sanctuary": "🌿 Sanctuary of Aether: Ẩn sâu trong tầng trời cao nhất, nơi ánh sáng nguyên thủy vẫn còn vẹn nguyên, Sanctuary là nơi những linh hồn lạc lối tìm kiếm sự cứu rỗi. Không ai bước vào được nếu trong tim còn nỗi oán thù. Ánh sáng ở đây không chỉ soi sáng thân xác, mà còn bóc trần mọi dối trá trong linh hồn. Nhiều kẻ từng vào đây với hy vọng thanh tẩy… nhưng rồi bị thiêu rụi bởi chính sự thật trong tâm can họ. Sanctuary là nơi thánh thiện nhất – và cũng là nơi nguy hiểm nhất – với những ai còn mang bóng tối trong mình.",
    "court": "⚔ The Shattered Court: Cựu kinh đô lộng lẫy nay chỉ còn lại cung điện nứt vỡ và ngai vàng bị lật úp. Đây từng là nơi 7 vị “Hiến Chủ” ngự trị – những linh hồn tối cao từng giữ thăng bằng cho Yami no Sekai. Nhưng sự phản bội từ chính trong lòng Court đã khiến mọi thứ sụp đổ. Giờ đây, các linh hồn chiến binh tụ họp tại đây để tranh đoạt quyền lực, bất kể hậu quả. Mỗi trận chiến lại đánh thức thêm một cơn ác mộng từ lòng đất. Kẻ nào giành được ngai sẽ kế vị toàn bộ tội lỗi xưa kia.",
    "veil": "🩸 Veil of Crimson: Màn sương đỏ thẫm bao phủ một vùng đất không có bản đồ. Mỗi bước đi qua là một ký ức bị rút cạn. Nhiều người lạc vào Veil vẫn sống, vẫn cười, nhưng không còn nhớ vì sao mình tồn tại. Cái tên, lý tưởng, tình yêu – tất cả bị xóa sạch. Đổi lại, họ trở nên yên tĩnh, bất động… như thể cuối cùng họ đã tìm thấy sự an bình. Nhưng thực chất, họ đã chết – không phải về thể xác, mà là về bản thể. Thần thoại gọi Veil là “Tấm màn của sự quên lãng vĩnh cửu.",
    "catacombs": "💀 Catacombs of Silence: Dưới mặt đất, sâu hơn bất kỳ ngôi mộ nào, là mê cung hầm mộ nơi giọng nói bị hút sạch ngay khi cất ra. Tại đây, bạn không thể hét, không thể thì thầm, chỉ còn lại tiếng bước chân và nhịp tim đập dồn dập của chính bạn. Các bức tường được khắc đầy lời nguyền, máu khô và những gương mặt hoảng loạn đông cứng. Người ta tin rằng đây là nơi linh hồn bị phong ấn – những tội đồ không được phép tái sinh, không được phép bị quên lãng. Lối ra không tồn tại, chỉ có lối xuống.",
    "eldertree": "🌲 Elder Tree: Nó không phải cây. Nó là ký ức cổ xưa hóa thành hình, cắm rễ vào mọi chiều không gian. Elder Tree là nơi các linh hồn tới để hỏi một câu hỏi – nhưng chỉ được hỏi một lần duy nhất trong đời. Trả lời của nó có thể cứu rỗi… hoặc nguyền rủa cả dòng máu. Người nào cố chặt nó, biến mất khỏi mọi ký ức của thế giới. Người nào cầu nguyện dưới gốc nó vào nửa đêm… sẽ thấy chính mình từ kiếp trước. Nó không tốt, cũng không ác – chỉ là tồn tại.",
    "mirrorrealm": "🪞 Mirror Realm: Một chiều không gian phản chiếu, nơi mỗi sự thật đều bị bóp méo một cách tinh tế. Những linh hồn lạc vào đó sẽ nhìn thấy bản thể mình… nhưng lệch đi, khác đi, đủ để khiến họ nghi ngờ chính bản thân. Ở đây, không có ánh sáng thật – chỉ có thứ ánh sáng giả lập tạo ra từ vô vàn gương vỡ. Các sinh vật sống trong Mirror Realm là những “Bản sao thất lạc”, sinh ra từ những ký ức bị giấu kín. Một khi bước vào gương, bạn không chỉ mất lối về – bạn còn mất bản gốc.",
    "dawnspire": "🌤 Dawnspire: Một ngọn tháp xuyên lên khỏi rìa thế giới, nối trời và vực thẳm. Mỗi bậc thang lên cao là một thử thách: vượt qua ảo ảnh, đối mặt với chính mình, và chứng kiến tương lai mình từng né tránh. Dawnspire chỉ mở cửa khi thời gian đứng yên – tức là khi một linh hồn từ chối tiến về phía trước hay quay lại. Nơi đây có thể là cứu rỗi... hoặc kết thúc vĩnh viễn. Người cuối cùng từng bước tới đỉnh tháp đã để lại câu này: “Trên đỉnh không có gì. Và chính điều đó khiến ta nhẹ nhõm."
}

fate_list = [
    "🕯️ Bạn mơ thấy một cánh cổng đang rỉ máu… và khi tỉnh dậy, nó ở ngay trước cửa.",
    "🌒 Bóng bạn biến mất dưới ánh trăng. Người khác vẫn thấy bạn, nhưng bạn thì không còn phản chiếu trong gương.",
    "🕸️ Một con quạ thì thầm tên thật của bạn... nhưng bạn chưa từng kể nó cho ai.",
    "📜 Bạn nhận được một bức thư viết bằng giọng chữ của chính bạn – ký tên là bạn trong tương lai.",
    "🔮 Một ngọn nến không bao giờ tắt bắt đầu cháy ngay giữa lòng bàn tay bạn, nhưng bạn không thấy đau.",
    "👁️ Một linh hồn xa lạ theo bạn từ Hollow. Nó không nói gì, chỉ nhìn, và mỉm cười.",
    "⛩ Bạn vô tình nói ra một từ cổ ngữ – và mọi đồng hồ quanh bạn dừng lại trong 10 giây.",
    "💀 Bạn tỉnh dậy và thấy mình đang mặc bộ đồ tang lễ… nhưng không biết của ai.",
    "🩸 Mỗi bước chân bạn để lại vết máu, dù cơ thể không hề bị thương.",
    "📖 Bạn tìm thấy một trang sách trong túi áo, ghi lại tương lai bạn chưa từng nghĩ đến…"
]

class_data = {
    "Knight": {
        "hệ": "Ánh Sáng",
        "kỹ_năng": ["Divine Shield", "Oathblade"],
        "mô_tả": "Chiến binh mang ánh sáng, bảo vệ và tấn công bằng ý chí thuần khiết."
    },
    "Witch": {
        "hệ": "Hắc Ám",
        "kỹ_năng": ["Cursed Flame", "Hex Mark"],
        "mô_tả": "Phù thủy thao túng bóng tối, lời nguyền và lửa tà ma."
    },
    "Oracle": {
        "hệ": "Tinh Linh",
        "kỹ_năng": ["Foresight", "Echo of Time"],
        "mô_tả": "Nhà tiên tri có thể thấy tương lai, điều khiển thời gian và giấc mộng."
    },
    "Reaper": {
        "hệ": "Tử Thần",
        "kỹ_năng": ["Soul Harvest", "Phantom Step"],
        "mô_tả": "Kẻ gặt linh hồn trong đêm, ra tay không chớp mắt."
    },
    "Ronin": {
        "hệ": "Vô Chủ",
        "kỹ_năng": ["Shadowstep", "Blood Pact"],
        "mô_tả": "Kiếm sĩ lang thang vô danh, dùng máu và bóng để chiến đấu."
    }
}
item_data = {
    "Blood Talisman": {
        "loại": "Hiệu ứng",
        "mô_tả": "Bùa máu tăng 20% tỉ lệ chiến thắng PvE trong 30 phút.",
        "hiệu_ứng": {
            "tên": "pve_boost",
            "mô_tả": "+20% tỉ lệ thắng PvE",
            "thời_gian": 1800  # giây
        }
    },
    "Shadow Orb": {
        "loại": "Tiêu hao",
        "mô_tả": "Gọi ra một bóng ma hỗ trợ trong 1 lượt.",
        "hiệu_ứng": {
            "tên": "summon_ghost",
            "mô_tả": "Triệu hồi Ghost Ally",
            "thời_gian": 600
        }
    }
}
quest_data = {
    "trial_of_shadows": {
        "tên": "Thử Thách Bóng Tối",
        "mô_tả": "Đi vào Whispering Hollow và sống sót qua đêm.",
        "phần_thưởng": ["Soul Fragment", "EXP:100"]
    },
    "echo_of_gate": {
        "tên": "Tiếng Vọng Từ Cổng",
        "mô_tả": "Giải mã thông điệp từ The Gate trong giấc mơ.",
        "phần_thưởng": ["Aether Elixir", "EXP:150"]
    }
}

# ---------- Tạo bot ----------
bot = commands.Bot(command_prefix="~", intents=intents)

# ---------- Hàm tiện ích ----------
def unlock_title(user_id, data, title):
    if "titles" not in data[user_id]:
        data[user_id]["titles"] = []
    if title not in data[user_id]["titles"]:
        data[user_id]["titles"].append(title)
        return True
    return False

def load_characters():
    if os.path.exists("characters.json"):
        with open("characters.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_characters(data):
    with open("characters.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def gain_exp(char_data, amount):
    char_data["exp"] += amount
    level_up_exp = char_data["level"] * 100
    leveled_up = False
    while char_data["exp"] >= level_up_exp:
        char_data["exp"] -= level_up_exp
        char_data["level"] += 1
        level_up_exp = char_data["level"] * 100
        leveled_up = True
    return leveled_up

def load_party():
    if not os.path.exists("party.json"):
        return {}
    with open("party.json", "r", encoding="utf-8") as f:
        return json.load(f)

def save_party(data):
    with open("party.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def load_achievements():
    if not os.path.exists("achievements.json"):
        return {}
    with open("achievements.json", "r", encoding="utf-8") as f:
        return json.load(f)

def save_achievements(data):
    with open("achievements.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def load_quests():
    with open("quests.json", "r", encoding="utf-8") as f:
        return json.load(f)

class QuestDropdown(ui.View):
    def __init__(self, quests, user_id, data):
        super().__init__()
        self.user_id = user_id
        self.data = data
        self.quests = {q["id"]: q for q in quests}
        options = [SelectOption(label=q["name"], description=q["description"][:80], value=q["id"]) for q in quests]
        self.add_item(ui.Select(placeholder="Chọn nhiệm vụ", options=options, custom_id="quest_select"))

def reset_daily_quests():
    all_quests = load_quests()
    daily = random.sample(all_quests, k=min(5, len(all_quests)))
    
    with open("daily_quests.json", "w", encoding="utf-8") as f:
        json.dump(daily, f, indent=4, ensure_ascii=False)

def reset_shop_items():
    with open("shop_items.json", "r", encoding="utf-8") as f:
        all_items = json.load(f)

    daily_items = random.sample(all_items, k=min(5, len(all_items)))

    with open("shop_today.json", "w", encoding="utf-8") as f:
        json.dump(daily_items, f, indent=4, ensure_ascii=False)

# ---------- Sự kiện on_ready ----------
@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print("✅ Slash commands:")
        for cmd in synced:
            print(f"→ /{cmd.name} ({cmd.description})")
    except Exception as e:
        print(f"❌ Lỗi sync slash command: {e}")

    if not daily_reset.is_running():
        daily_reset.start()
        print("✅ Daily reset task started.")

    if not cleanup_effects.is_running():
        cleanup_effects.start()
        print("✅ Effect cleanup task started.")

    await bot.change_presence(status=discord.Status.online, activity=discord.Game("⛩ Yami no Sekai ⛩"))
    print(f"🟢 Bot online: {bot.user}")

# ---------- SLASH COMMANDS ----------
@bot.tree.command(name="leaderboard", description="Xem bảng xếp hạng level")
async def slash_leaderboard(interaction: discord.Interaction):
    data = load_characters()
    sorted_users = sorted(data.items(), key=lambda x: x[1].get("level", 1), reverse=True)
    embed = discord.Embed(
        title="🏆 Bảng Xếp Hạng",
        description="Top các lữ khách mạnh nhất trong Yami no Sekai",
        color=discord.Color.blue()
    )
    for i, (uid, char) in enumerate(sorted_users[:10], start=1):
        name = char["tên"]
        level = char.get("level", 1)
        embed.add_field(name=f"#{i} – {name}", value=f"🎚️ Level {level}", inline=False)

    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="help", description="Hiển thị hướng dẫn sử dụng bot RP Yami no Sekai")
async def slash_help(interaction: discord.Interaction):
    embed = discord.Embed(
        title="📖 Hướng Dẫn Sử Dụng Bot RP: Yami no Sekai",
        description="Chào mừng đến với thế giới RP huyền bí!\nDưới đây là các nhóm lệnh bạn có thể sử dụng:",
        color=0x3498db
    )

    embed.add_field(
        name="🎭 Nhân Vật",
        value="`/character_create`, `/character_view`, `/character_delete`, `/character_create_form`, `/character_sheet`",
        inline=False
    )
    embed.add_field(
        name="🧪 Vật Phẩm & Kỹ Năng",
        value="`/inventory`, `/item_use`, `/use_skill`",
        inline=False
    )
    embed.add_field(
        name="🎯 Nhiệm Vụ",
        value="`/quest_list`, `/quest_accept`, `/quest_random`, `/my_quests`, `/quest_complete`",
        inline=False
    )
    embed.add_field(
        name="🧩 Sự Kiện & Chiến Đấu",
        value="`/event_items`, `/pve_fight`, `/fight`",
        inline=False
    )
    embed.add_field(
        name="🏆 Danh Hiệu & Thành Tích",
        value="`/titles`, `/achievement`, `/leaderboard`",
        inline=False
    )
    embed.add_field(
        name="🧙‍♂️ Class & Kỹ Năng",
        value="`/class_info`, `/skills_list`",
        inline=False
    )
    embed.add_field(
        name="🎲 Ngẫu Nhiên & Lore",
        value="`/fate`, `/lore_random`, `/lore`",
        inline=False
    )
    embed.add_field(
        name="💰 Tiền tệ & Cửa hàng",
        value="`/coin_balance`, `/coin_give`, `/shop`, `/buy`",
        inline=False
    )
    embed.add_field(
        name="👥 Tổ Đội (Party)",
        value="`/party_create`, `/party_invite`, `/party_join`, `/party_leave`, `/party_info`",
        inline=False
    )
    embed.add_field(
        name="🛠️ Hỗ Trợ & Hệ Thống",
        value="`/hello`, `/safe_ping`, `/help`",
        inline=False
    )

    embed.set_footer(text="⛩ Yami no Sekai • RP Bot Việt hoá toàn diện")
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="guide", description="Hướng dẫn nhập vai dành cho người chơi mới")
async def slash_guide(interaction: discord.Interaction):
    embed = discord.Embed(
        title="📘 Hướng Dẫn Nhập Vai - Yami no Sekai",
        description="Chào mừng đến với thế giới Yami no Sekai. Dưới đây là các bước để bắt đầu RP:",
        color=0x00bfff
    )
    embed.add_field(name="1️⃣ Tạo nhân vật", value="Dùng `/character_create_form` để tạo nhân vật RP.", inline=False)
    embed.add_field(name="2️⃣ Xem hồ sơ", value="Dùng `/character_view` để xem thông tin chi tiết.", inline=False)
    embed.add_field(name="3️⃣ Nhận định mệnh", value="Dùng `/fate` để nhận định mệnh RP đầu tiên.", inline=False)
    embed.add_field(name="4️⃣ Làm nhiệm vụ", value="Dùng `/quest_random` hoặc `/quest_list` để nhận nhiệm vụ.", inline=False)
    embed.add_field(name="5️⃣ Chiến đấu & phiêu lưu", value="Khám phá vùng đất mới bằng `/pve_fight`, `/lore_random`, `/use_skill`.", inline=False)
    embed.add_field(name="💡 Mẹo", value="Hãy tương tác với NPC, tổ đội và nhận danh hiệu để phát triển nhân vật!", inline=False)
    embed.set_footer(text="⛩ Yami no Sekai • RP Bot Việt hoá • Chúc bạn nhập vai vui vẻ!")

    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="titles", description="Xem danh hiệu bạn đang có")
async def slash_titles(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    data = load_characters()
    if user_id not in data:
        await interaction.response.send_message("❌ Bạn chưa có hồ sơ.", ephemeral=True)
        return

    titles = data[user_id].get("titles", [])
    if not titles:
        await interaction.response.send_message("🎖️ Bạn chưa có danh hiệu nào.", ephemeral=True)
        return

    embed = discord.Embed(
        title="🎖️ Danh hiệu của bạn",
        description="\n".join([f"🔸 {title}" for title in titles]),
        color=discord.Color.dark_gold()
    )
    embed.set_footer(text="⛩ Yami no Sekai | Title System")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="party_join", description="Tham gia tổ đội của người khác")
@app_commands.describe(user="Thủ lĩnh tổ đội")
async def slash_party_join(interaction: discord.Interaction, user: discord.Member):
    leader_id = str(user.id)
    user_id = str(interaction.user.id)
    data = load_characters()

    if leader_id not in data or "party" not in data[leader_id]:
        await interaction.response.send_message("❌ Người này không có tổ đội.", ephemeral=True)
        return

    if user_id in data and "party" in data[user_id]:
        await interaction.response.send_message("⚠️ Bạn đã ở trong một tổ đội khác.", ephemeral=True)
        return

    data[user_id]["party"] = data[leader_id]["party"]
    data[leader_id]["party"]["members"].append(user_id)
    save_characters(data)
    await interaction.response.send_message(f"🤝 Bạn đã tham gia tổ đội **{data[leader_id]['party']['name']}**!", ephemeral=True)

@bot.tree.command(name="achievement", description="Xem danh hiệu RP của bạn")
async def slash_achievement(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    data = load_achievements()
    titles = data.get(user_id, [])
    if not titles:
        await interaction.response.send_message("⚪ Bạn chưa có danh hiệu nào.")
        return
    title_list = "\n".join([f"🏅 {t}" for t in titles])
    await interaction.response.send_message(f"🎖️ Danh hiệu của bạn:\n{title_list}")

@bot.tree.command(name="party_create", description="Tạo tổ đội RP")
async def slash_party_create(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    data = load_party()
    if user_id in data:
        await interaction.response.send_message("❌ Bạn đã có tổ đội hoặc đang trong một tổ đội.", ephemeral=True)
        return
    data[user_id] = {"leader": user_id, "members": [user_id]}
    save_party(data)
    await interaction.response.send_message("✅ Tổ đội của bạn đã được tạo.")

@bot.tree.command(name="party_invite", description="Mời người chơi vào tổ đội RP")
@app_commands.describe(member="Người chơi bạn muốn mời")
async def slash_party_invite(interaction: discord.Interaction, member: discord.Member):
    user_id = str(interaction.user.id)
    member_id = str(member.id)
    data = load_party()

    if user_id not in data or data[user_id]["leader"] != user_id:
        await interaction.response.send_message("❌ Bạn không phải đội trưởng.", ephemeral=True)
        return
    if member_id in data:
        await interaction.response.send_message("❌ Người này đã ở trong tổ đội khác.", ephemeral=True)
        return

    data[member_id] = data[user_id]
    data[member_id]["members"].append(member_id)
    save_party(data)
    await interaction.response.send_message(f"📨 Đã mời {member.mention} vào tổ đội.")

@bot.tree.command(name="party_leave", description="Rời khỏi tổ đội RP")
async def slash_party_leave(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    data = load_party()
    if user_id not in data:
        await interaction.response.send_message("❌ Bạn không trong tổ đội nào.", ephemeral=True)
        return
    team = data[user_id]
    team["members"].remove(user_id)
    del data[user_id]
    # Nếu là leader và team rỗng -> giải tán
    if user_id == team["leader"] and not team["members"]:
        for uid in list(data):
            if data[uid]["leader"] == user_id:
                del data[uid]
    save_party(data)
    await interaction.response.send_message("🚪 Bạn đã rời tổ đội.")

@bot.tree.command(name="party_info", description="Xem thông tin tổ đội RP")
async def slash_party_info(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    data = load_party()
    if user_id not in data:
        await interaction.response.send_message("❌ Bạn không thuộc tổ đội nào.", ephemeral=True)
        return

    team = data[user_id]
    leader = await bot.fetch_user(int(team["leader"]))
    members = [await bot.fetch_user(int(mid)) for mid in team["members"]]
    member_list = "\n".join([f"- {m.display_name}" for m in members])

    embed = discord.Embed(
        title="🛡️ Tổ Đội RP",
        description=f"👑 Đội trưởng: {leader.display_name}\n👥 Thành viên:\n{member_list}",
        color=discord.Color.purple()
    )
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="skills_list", description="Xem toàn bộ kỹ năng theo class và hệ")
async def slash_skills_list(interaction: discord.Interaction):
    hệ_dict = {}

    for class_name, info in class_data.items():
        hệ = info["hệ"]
        if hệ not in hệ_dict:
            hệ_dict[hệ] = []
        hệ_dict[hệ].append((class_name, info["kỹ_năng"]))

    embed = discord.Embed(
        title="✨ Danh sách Kỹ Năng Theo Class & Hệ",
        color=discord.Color.purple()
    )

    for hệ, class_list in hệ_dict.items():
        desc = ""
        for cls, kỹ_năng in class_list:
            desc += f"**{cls}**: {', '.join(kỹ_năng)}\n"
        embed.add_field(name=f"🔮 Hệ: {hệ}", value=desc, inline=False)

    embed.set_footer(text="⛩ Yami no Sekai | Skill System")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="event_items", description="Xem các vật phẩm bạn đã nhận từ sự kiện")
async def slash_event_items(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    data = load_characters()

    if user_id not in data:
        await interaction.response.send_message("❌ Bạn chưa có hồ sơ nhân vật.", ephemeral=True)
        return

    all_items = data[user_id].get("vật_phẩm", [])
    event_items = [item for item in all_items if item.startswith("🎁") or item.lower().startswith("event")]

    if not event_items:
        await interaction.response.send_message("📦 Bạn chưa có vật phẩm nào từ sự kiện.", ephemeral=True)
        return

    embed = discord.Embed(
        title="🎁 Vật phẩm sự kiện của bạn",
        description="\n".join([f"🔹 {item}" for item in event_items]),
        color=discord.Color.magenta()
    )
    embed.set_footer(text="⛩ Yami no Sekai | Event Inventory")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="quest_random", description="Nhận một nhiệm vụ ngẫu nhiên")
async def slash_quest_random(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    data = load_characters()
    quests =slash_quest_list()

    available = [q for q in quests if q["id"] not in data[user_id].get("quests", [])]
    if not available:
        await interaction.response.send_message("✅ Bạn đã nhận hết nhiệm vụ hiện có!", ephemeral=True)
        return

    chosen = random.choice(available)
    data[user_id].setdefault("quests", []).append(chosen["id"])
    save_characters(data)

    await interaction.response.send_message(
        f"🎲 **Nhiệm vụ ngẫu nhiên:** {chosen['name']}\n📝 {chosen['description']}", ephemeral=True
    )

@bot.tree.command(name="quest_complete", description="Hoàn thành một nhiệm vụ bạn đang làm")
@app_commands.describe(quest_id="ID nhiệm vụ muốn hoàn thành")
async def slash_quest_complete(interaction: discord.Interaction, quest_id: str):
    user_id = str(interaction.user.id)
    data = load_characters()
    quests = load_quests()
    char = data.get(user_id)

    if not char or quest_id not in char.get("quests", []):
        await interaction.response.send_message("❌ Bạn chưa nhận nhiệm vụ này!", ephemeral=True)
        return

    if quest_id not in quests:
        await interaction.response.send_message("⚠️ Không tìm thấy nhiệm vụ.", ephemeral=True)
        return

    quest = quests[quest_id]
    phần_thưởng = quest.get("phần_thưởng", [])
    exp = 0
    items = []

    for pt in phần_thưởng:
        if pt.startswith("EXP:"):
            exp += int(pt.replace("EXP:", ""))
        else:
            items.append(pt)

    char["exp"] = char.get("exp", 0) + exp
    char.setdefault("vật_phẩm", []).extend(items)
    char["quests"].remove(quest_id)
    save_characters(data)

    msg = f"🎉 **Hoàn thành:** {quest['tên']}\n🏅 +{exp} EXP\n"
    if items:
        msg += "🎁 Nhận vật phẩm: " + ", ".join([f"`{i}`" for i in items])

    await interaction.response.send_message(msg, ephemeral=True)

@bot.tree.command(name="my_quests", description="Xem các nhiệm vụ bạn đang làm")
async def slash_my_quests(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    data = load_characters()
    quests = get_all_quests()
    user_quests = data.get(user_id, {}).get("quests", [])

    if not user_quests:
        await interaction.response.send_message("📭 Bạn chưa nhận nhiệm vụ nào.", ephemeral=True)
        return

    embed = discord.Embed(title="📜 Nhiệm vụ đang làm", color=0x9b59b6)
    for quest_id in user_quests:
        q = next((q for q in quests if q["id"] == quest_id), None)
        if q:
            embed.add_field(name=q["name"], value=q["description"], inline=False)

    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="safe_ping", description="Ping nếu bot đã sẵn sàng")
async def safe_ping(interaction: discord.Interaction):
    if not bot.is_ready():
        await interaction.response.send_message("⏳ Bot chưa sẵn sàng...", ephemeral=True)
        return
    await interaction.response.send_message("🏓 Bot is ready and online!")

@bot.tree.command(name="use_skill", description="Dùng kỹ năng của class bạn")
@app_commands.describe(skill_name="Tên kỹ năng muốn sử dụng")
async def slash_use_skill(interaction: discord.Interaction, skill_name: str):
    user_id = str(interaction.user.id)
    data = load_characters()

    if user_id not in data:
        await interaction.response.send_message("❌ Bạn chưa có hồ sơ. Dùng /character_create_form để tạo.", ephemeral=True)
        return

    char = data[user_id]
    kỹ_năng = char.get("kỹ_năng", [])

    if skill_name not in kỹ_năng:
        await interaction.response.send_message(f"❌ Bạn không có kỹ năng {skill_name}.", ephemeral=True)
        return

    await interaction.response.send_message(f"✨ *{char['tên']}* đã dùng kỹ năng *{skill_name}*!\n🌀 Một luồng năng lượng bùng phát giữa bóng tối...")

@bot.tree.command(name="character_create", description="Tạo hồ sơ nhân vật RP của bạn")
@app_commands.describe(
    ten="Tên nhân vật",
    chung_toc="Chủng tộc (Human, Demon, Spirit, v.v.)",
    lop="Lớp (Knight, Witch, Oracle, v.v.)",
    truyen_thuyet="Truyền thuyết / Background nhân vật"
)
async def slash_character_create(
    interaction: discord.Interaction,
    ten: str,
    chung_toc: str,
    lop: str,
    truyen_thuyet: str
):
    user_id = str(interaction.user.id)
    data = load_characters()

    if user_id in data:
        await interaction.response.send_message("⚠️ Bạn đã có hồ sơ nhân vật. Dùng /character_delete để xoá trước khi tạo mới.", ephemeral=True)
        return

    if lop not in class_data:
        await interaction.response.send_message("❌ Lớp không hợp lệ. Dùng /class_info để xem danh sách.", ephemeral=True)
        return

    info = class_data[lop]

    lore_ngau_nhien = random.choice(list(lore_dict.values()))
    fate_ngau_nhien = random.choice(fate_list)

    data[user_id] = {
        "tên": ten,
        "chủng_tộc": chung_toc,
        "lớp": lop,
        "truyền_thuyết": truyen_thuyet,
        "hệ": info["hệ"],
        "kỹ_năng": info["kỹ_năng"],
        "lore": lore_ngau_nhien,
        "định_mệnh": fate_ngau_nhien,
        "level": 1,
        "exp": 0,
        "vật_phẩm": [],
        "nhiệm_vụ": []
    }
    save_characters(data)

    await interaction.response.send_message(f"✅ Đã tạo hồ sơ nhân vật cho *{ten}*.")

@bot.tree.command(name="character_view", description="Xem hồ sơ nhân vật RP của bạn")
async def slash_character_view(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    data = load_characters()

    if user_id not in data:
        await interaction.response.send_message("❌ Bạn chưa có hồ sơ nhân vật. Dùng /character_create_form để tạo.", ephemeral=True)
        return

    char = data[user_id]
    embed = discord.Embed(
        title=f"📜 Hồ sơ của {char['tên']}",
        color=discord.Color.blue()
    )
    embed.add_field(name="🧬 Chủng tộc", value=char["chủng_tộc"], inline=True)
    embed.add_field(name="⚔️ Lớp", value=char["lớp"], inline=True)
    embed.add_field(name="🌌 Hệ", value=char.get("hệ", "Không rõ"), inline=True)
    embed.add_field(name="✨ Kỹ năng", value=", ".join(char.get("kỹ_năng", [])), inline=False)
    embed.add_field(name="📖 Truyền thuyết", value=char["truyền_thuyết"], inline=False)

    if "lore" in char:
        embed.add_field(name="🌒 Lore ngẫu nhiên", value=char["lore"][:200] + "...", inline=False)
    if "định_mệnh" in char:
        embed.add_field(name="🕯️ Định mệnh", value=char["định_mệnh"], inline=False)
    if "level" in char:
        embed.add_field(name="🎚️ Cấp độ", value=f"Level {char['level']} | EXP: {char['exp']}", inline=True)
    if "vật_phẩm" in char and char["vật_phẩm"]:
        embed.add_field(name="🎒 Vật phẩm", value=", ".join(char["vật_phẩm"]), inline=False)
    embed.set_footer(text="⛩ Yami no Sekai | Character Sheet")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="class_info", description="Xem thông tin các lớp nhân vật RP")
async def slash_class_info(interaction: discord.Interaction):
    embed = discord.Embed(
        title="📚 Danh sách Class & Hệ",
        description="Chi tiết về các lớp nhân vật trong Yami no Sekai.",
        color=discord.Color.orange()
    )

    for class_name, data in class_data.items():
        kỹ_năng = ", ".join(data["kỹ_năng"])
        embed.add_field(
            name=f"{class_name} ({data['hệ']})",
            value=f"{data['mô_tả']}\n🔮 Kỹ năng: {kỹ_năng}",
            inline=False
        )

    embed.set_footer(text="⛩ Yami no Sekai | Class Lore")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="fate", description="Nhận một định mệnh ngẫu nhiên")
async def slash_fate(interaction: discord.Interaction):
    định_mệnh = random.choice(fate_list)
    embed = discord.Embed(
        title="🕯️ Định Mệnh Của Bạn",
        description=định_mệnh,
        color=discord.Color.dark_red()
    )
    embed.set_footer(text="⛩ Yami no Sekai | Fate has chosen")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="lore_random", description="Nhận một vùng lore ngẫu nhiên từ Yami no Sekai")
async def slash_lore_random(interaction: discord.Interaction):
    vùng = random.choice(list(lore_dict.keys()))
    nội_dung = lore_dict[vùng]
    embed = discord.Embed(
        title=f"🎲 Vùng lore ngẫu nhiên: {vùng.title()}",
        description=nội_dung,
        color=discord.Color.teal()
    )
    embed.set_footer(text="⛩ Yami no Sekai | Fate chooses your lore...")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="hello", description="Chào hỏi lữ khách từ vực thẳm")
async def slash_hello(interaction: discord.Interaction):
    await interaction.response.send_message("🌒 Xin chào, lữ khách từ vực thẳm.")

@bot.tree.command(name="lore", description="Xem lore của một vùng cụ thể (ví dụ: abyss, gate...)")
@app_commands.describe(vung="Tên vùng lore (ví dụ: abyss, gate, hollow...)")
async def slash_lore(interaction: discord.Interaction, vung: str):
    v = vung.lower()
    if v in lore_dict:
        nội_dung = lore_dict[v]
        embed = discord.Embed(
            title=f"📖 Lore: {vung.title()}",
            description=nội_dung,
            color=discord.Color.dark_purple()
        )
        embed.set_footer(text="⛩ Yami no Sekai | Lore System")
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message("❓ Chủ đề không tồn tại.", ephemeral=True)

@bot.tree.command(name="character_sheet", description="Hiện mẫu hồ sơ nhân vật RP để bạn điền")
async def slash_character_sheet(interaction: discord.Interaction):
    embed = discord.Embed(
        title="📜 Hồ Sơ Nhân Vật RP",
        description="Dưới đây là mẫu hồ sơ cơ bản. Hãy sao chép và điền thông tin của bạn để bắt đầu hành trình.",
        color=discord.Color.gold()
    )
    embed.add_field(name="🌑 Tên nhân vật", value="Nhập tại đây...", inline=False)
    embed.add_field(name="🧬 Chủng tộc", value="Human / Demon / Spirit / Undead / Other...", inline=True)
    embed.add_field(name="⚔️ Class", value="Knight / Witch / Oracle / Reaper / ???", inline=True)
    embed.add_field(name="🩸 Lời nguyền", value="Chưa rõ / Máu quỷ / Gương vỡ / Vô hình...", inline=False)
    embed.add_field(name="🔮 Kỹ năng đặc biệt", value="Shadowstep / Time Echo / Blood Pact...", inline=False)
    embed.add_field(name="📖 Truyền thuyết cá nhân", value="(Viết tóm tắt background RP của nhân vật)", inline=False)
    embed.set_footer(text="⛩ Yami no Sekai | Character Sheet System")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="character_delete", description="Xoá hồ sơ nhân vật RP của bạn")
async def slash_character_delete(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    data = load_characters()

    if user_id not in data:
        await interaction.response.send_message("⚠️ Bạn không có hồ sơ để xoá.", ephemeral=True)
        return

    del data[user_id]
    save_characters(data)
    await interaction.response.send_message("🗑️ Hồ sơ của bạn đã bị xoá.")

class CharacterCreateModal(Modal, title="Tạo Hồ Sơ Nhân Vật"):

    ten = TextInput(label="🌑 Tên nhân vật", placeholder="Ví dụ: Akuma", max_length=30)
    chung_toc = TextInput(label="🧬 Chủng tộc", placeholder="Human / Demon / Spirit...", max_length=30)
    truyen_thuyet = TextInput(label="📖 Truyền thuyết", style=discord.TextStyle.paragraph, max_length=300)

    async def on_submit(self, interaction: discord.Interaction):
        view = ClassSelectView(self.ten.value, self.chung_toc.value, self.truyen_thuyet.value)
        await interaction.response.send_message("⚔️ Chọn class cho nhân vật của bạn:", view=view, ephemeral=True)

class ClassSelectView(View):
    def __init__(self, ten, chung_toc, truyen_thuyet):
        super().__init__(timeout=180)
        self.ten = ten
        self.chung_toc = chung_toc
        self.truyen_thuyet = truyen_thuyet

        options = [
            discord.SelectOption(label=cls, description=info["mô_tả"][:80], emoji="✨")
            for cls, info in class_data.items()
        ]
        self.add_item(ClassSelect(options, self))

class ClassSelect(Select):
    def __init__(self, options, parent_view):
        super().__init__(placeholder="Chọn class...", min_values=1, max_values=1, options=options)
        self.parent_view = parent_view

    async def callback(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        data = load_characters()

        if user_id in data:
            await interaction.response.send_message("⚠️ Bạn đã có hồ sơ nhân vật. Dùng /character_delete để xoá trước khi tạo mới.", ephemeral=True)
            return

        lop = self.values[0]
        info = class_data[lop]
        lore_ngau_nhien = random.choice(list(lore_dict.values()))
        fate_ngau_nhien = random.choice(fate_list)

        data[user_id] = {
            "tên": self.parent_view.ten,
            "chủng_tộc": self.parent_view.chung_toc,
            "lớp": lop,
            "hệ": info["hệ"],
            "kỹ_năng": info["kỹ_năng"],
            "truyền_thuyết": self.parent_view.truyen_thuyet,
            "lore": lore_ngau_nhien,
            "định_mệnh": fate_ngau_nhien,
            "level": 1,
            "exp": 0
        }

        save_characters(data)
        await interaction.response.send_message(f"✅ Đã tạo nhân vật **{self.parent_view.ten}** – Class: **{lop}**.\n✨ Một vùng lore và định mệnh đã được chọn cho bạn!", ephemeral=True)

@bot.tree.command(name="character_create_form", description="Tạo nhân vật RP (chọn class bằng menu)")
async def character_create_form(interaction: discord.Interaction):
    modal = CharacterCreateModal()
    await interaction.response.send_modal(modal)

@bot.tree.command(name="inventory", description="Xem vật phẩm bạn đang sở hữu")
async def slash_inventory(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    data = load_characters()

    if user_id not in data:
        await interaction.response.send_message("❌ Bạn chưa có hồ sơ nhân vật.", ephemeral=True)
        return

    items = data[user_id].get("vật_phẩm", [])
    if not items:
        await interaction.response.send_message("🎒 Bạn chưa có vật phẩm nào.", ephemeral=True)
        return

    embed = discord.Embed(
        title="🎒 Túi đồ của bạn",
        description="\n".join([f"• {item} - {item_data[item]['mô_tả']}" for item in items]),
        color=discord.Color.green()
    )
    embed.set_footer(text="⛩ Yami no Sekai | Inventory System")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="quest_list", description="Xem danh sách nhiệm vụ có thể nhận")
async def slash_quest_list(interaction: discord.Interaction):
    quests = load_quests()
    embed = discord.Embed(title="📜 Danh sách nhiệm vụ", description="Các thử thách trong Yami no Sekai đang chờ bạn...", color=0xffcc00)

    for qid, quest in quests.items():
        phần_thưởng = quest["phần_thưởng"]
        reward_str = ", ".join(phần_thưởng)
        embed.add_field(
            name=f"{quest['tên']} (ID: `{qid}`)",
            value=f"{quest['mô_tả']}\n🎁 {reward_str} | 🔒 Cấp {quest['cấp_độ_tối_thiểu']}",
            inline=False
        )

    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="quest_accept", description="Nhận một nhiệm vụ từ bảng nhiệm vụ")
@app_commands.describe(quest_id="ID nhiệm vụ muốn nhận")
async def slash_quest_accept(interaction: discord.Interaction, quest_id: str):
    user_id = str(interaction.user.id)
    data = load_characters()
    quests = load_quests()

    if quest_id not in quests:
        await interaction.response.send_message("❓ Nhiệm vụ không tồn tại.", ephemeral=True)
        return

    char = data.setdefault(user_id, {})
    char.setdefault("quests", [])

    if quest_id in char["quests"]:
        await interaction.response.send_message("⚠️ Bạn đã nhận nhiệm vụ này rồi.", ephemeral=True)
        return

    # Kiểm tra cấp độ yêu cầu
    level = char.get("level", 1)
    min_level = quests[quest_id].get("cấp_độ_tối_thiểu", 1)
    if level < min_level:
        await interaction.response.send_message(f"🔒 Yêu cầu cấp độ {min_level} mới có thể nhận nhiệm vụ này!", ephemeral=True)
        return

    char["quests"].append(quest_id)
    save_characters(data)

    quest = quests[quest_id]
    await interaction.response.send_message(
        f"📝 **Đã nhận nhiệm vụ:** {quest['tên']}\n{quest['mô_tả']}", ephemeral=True)

@bot.tree.command(name="item_use", description="Dùng một vật phẩm từ túi đồ của bạn")
@app_commands.describe(item_name="Tên vật phẩm muốn sử dụng")
async def slash_item_use(interaction: discord.Interaction, item_name: str):
    user_id = str(interaction.user.id)
    data = load_characters()

    if user_id not in data:
        await interaction.response.send_message("❌ Bạn chưa có hồ sơ nhân vật.", ephemeral=True)
        return

    char = data[user_id]
    inventory = char.get("vật_phẩm", [])

    if item_name not in inventory:
        await interaction.response.send_message("❌ Bạn không có vật phẩm này.", ephemeral=True)
        return

    item = item_data.get(item_name)
    if not item:
        await interaction.response.send_message("❓ Vật phẩm không tồn tại trong hệ thống.", ephemeral=True)
        return

    msg = f"📦 Bạn đã dùng vật phẩm **{item_name}**."

    # ==== Hiệu ứng theo cấu trúc tùy chỉnh ====
    if "hiệu_ứng" in item:
        effect = item["hiệu_ứng"]
        char.setdefault("hiệu_ứng", {})[effect["tên"]] = {
            "mô_tả": effect["mô_tả"],
            "hết_hạn": time.time() + effect["thời_gian"]
        }
        msg = f"✨ Bạn đã dùng **{item_name}**. {effect['mô_tả']}"

    # ==== Hiệu ứng đặc biệt cố định ====
    elif item.get("loại") == "Tiêu hao":
        effect = item.get("effect")
        if effect == "heal":
            msg = "🧪 Bạn đã hồi phục năng lượng."
        elif effect == "summon_ghost":
            char.setdefault("buffed", []).append("Ghost Ally")
            msg = "👻 Một linh hồn tạm thời xuất hiện và hỗ trợ bạn!"
        elif effect == "shield":
            char.setdefault("hiệu_ứng", {})["shield"] = {
                "mô_tả": "🛡️ Khiên ánh sáng",
                "hết_hạn": time.time() + 300  # 5 phút
            }
            msg = "🛡️ Bạn được bao phủ bởi một lớp khiên ánh sáng!"

    # Xoá vật phẩm sau khi dùng
    inventory.remove(item_name)
    save_characters(data)

    await interaction.response.send_message(msg)

@bot.tree.command(name="pve_fight", description="Chiến đấu với một Boss huyền bí")
async def slash_pve_fight(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    data = load_characters()
    char = data.get(user_id)

    if not char:
        await interaction.response.send_message("❌ Bạn chưa có nhân vật.", ephemeral=True)
        return

    level = char.get("level", 1)
    exp = char.get("exp", 0)
    base_chance = 40 + level * 5

    # Bonus từ vật phẩm/kỹ năng
    if "Phantom Blade" in char.get("vật_phẩm", []):
        base_chance += 15
    if "buffed" in char:
        base_chance += 10

    outcome = random.randint(1, 100)
    if outcome <= base_chance:
        exp_gain = random.randint(50, 120)
        char["exp"] += exp_gain
        save_characters(data)

        embed = discord.Embed(
            title="🏆 Chiến thắng Boss huyền bí!",
            description=f"🎁 Bạn nhận được **{exp_gain} EXP**!",
            color=0x00ff99
        )
    else:
        embed = discord.Embed(
            title="💀 Bạn thất bại trước Boss!",
            description="😵 Nhưng bạn đã học được điều gì đó từ thất bại...",
            color=0xff5555
        )

    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="fight", description="Thách đấu một người chơi khác (PvP)")
@app_commands.describe(target="Người chơi bạn muốn thách đấu")
async def slash_fight(interaction: discord.Interaction, target: discord.Member):
    attacker_id = str(interaction.user.id)
    defender_id = str(target.id)

    if attacker_id == defender_id:
        await interaction.response.send_message("❌ Bạn không thể thách đấu chính mình!", ephemeral=True)
        return

    data = load_characters()
    atk_char = data.get(attacker_id)
    def_char = data.get(defender_id)

    if not atk_char or not def_char:
        await interaction.response.send_message("❌ Một trong hai người chưa có nhân vật RP.", ephemeral=True)
        return

    atk_power = atk_char["level"] * 10 + random.randint(1, 30)
    def_power = def_char["level"] * 10 + random.randint(1, 30)

    embed = discord.Embed(title="⚔️ PvP Thách Đấu", color=0x7289DA)
    embed.add_field(name="👤 Kẻ thách đấu", value=interaction.user.mention, inline=True)
    embed.add_field(name="🛡️ Người bị thách đấu", value=target.mention, inline=True)
    embed.add_field(name="🎯 Kết quả", value="...", inline=False)

    if atk_power >= def_power:
        exp_gain = random.randint(40, 100)
        atk_char["exp"] += exp_gain
        save_characters(data)
        embed.set_field_at(2, name="🎯 Kết quả", value=f"🏆 **{interaction.user.name}** chiến thắng!\n🎁 Nhận {exp_gain} EXP", inline=False)
    else:
        embed.set_field_at(2, name="🎯 Kết quả", value=f"🛡️ **{target.name}** đã phòng thủ thành công!", inline=False)

    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="coin_balance", description="Xem số coin bạn đang có")
async def coin_balance(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    data = load_characters()
    if user_id not in data:
        await interaction.response.send_message("❌ Bạn chưa có nhân vật.")
        return
    coin = data[user_id].get("coin", 0)
    await interaction.response.send_message(f"💰 Bạn có **{coin} coins**.")

@bot.tree.command(name="daily_quest", description=" Xem các nhiệm vụ hằng ngày hôm nay")
async def daily_quest(interaction: discord.Interaction):
    daily = load_json("data/daily_quests.json")
    if not daily:
        await interaction.response.send_message("⚠️ Hiện chưa có nhiệm vụ hằng ngày nào.", ephemeral=True)
        return

    embed = discord.Embed(title="📅 Nhiệm vụ Hằng Ngày", color=0x3498db)
    for q in daily:
        reward = q.get("reward", {})
        reward_text = f"+{reward.get('exp', 0)} EXP"
        if reward.get("item"):
            reward_text += f", 🎁 {reward['item']}"
        embed.add_field(name=f"📝 {q['name']}", value=f"{q['description']}\n**Phần thưởng:** {reward_text}", inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="shop", description=" Xem vật phẩm có sẵn trong cửa hàng")
async def slash_shop(interaction: discord.Interaction):
    items = load_json("data/shop_items.json")
    if not items:
        await interaction.response.send_message("🛒 Hiện tại shop trống.", ephemeral=True)
        return

    embed = discord.Embed(title="🛒 Shop Vật Phẩm", color=0xf1c40f)
    for category, item_list in items.items():
        embed.add_field(name=f"🔹 {category}", value="—", inline=False)
        for item in items:
            embed.add_field(
                name=f"{item['name']} - 💰 {item['price']} coin",
                value=item["description"],
                inline=False
        )
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="effects", description="Xem hiệu ứng đang hoạt động")
async def slash_effects(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    data = load_characters()

    char = data.get(user_id)
    if not char or "hiệu_ứng" not in char or not char["hiệu_ứng"]:
        await interaction.response.send_message("✨ Bạn không có hiệu ứng nào đang hoạt động.", ephemeral=True)
        return

    embed = discord.Embed(title="💠 Hiệu ứng đang hoạt động", color=0x3498db)
    for k, v in char["hiệu_ứng"].items():
        thời_gian = int(v["hết_hạn"] - time.time())
        phút = thời_gian // 60
        giây = thời_gian % 60
        embed.add_field(name=k, value=f"{v['mô_tả']} ({phút}m {giây}s còn lại)", inline=False)

    await interaction.response.send_message(embed=embed, ephemeral=True)

@tasks.loop(time=datetime.time(hour=0, minute=0, tzinfo=datetime.timezone.utc))
async def daily_reset():
    print("🔄 Đang reset daily quest và shop...")
    reset_daily_quests()
    reset_shop_items()

@tasks.loop(hours=24)
async def daily_reset():
    now = datetime.datetime.now()
    if now.hour != 0: return  # chỉ reset vào 0h

    # Reset Daily Quests
    all_quests = load_json("data/all_quests.json")
    daily = random.sample(all_quests, k=min(3, len(all_quests)))
    save_json("data/daily_quests.json", daily)
    print("✅ Reset nhiệm vụ hằng ngày.")

    # Reset Shop Items
    full_shop = load_json("data/shop_items.json")
    today_shop = random.sample(full_shop, k=min(4, len(full_shop)))
    save_json("data/shop_items.json", today_shop)
    print("🛒 Reset shop items hằng ngày.")

@tasks.loop(minutes=1)
async def cleanup_effects():
    data = load_characters()
    for uid, char in data.items():
        effects = char.get("hiệu_ứng", [])
        new_effects = []
        for e in effects:
            if e["type"] == "shield":
                e["thời_gian"] -= 1
                if e["thời_gian"] > 0:
                    new_effects.append(e)
        char["hiệu_ứng"] = new_effects
    save_characters(data)

@tasks.loop(hours=1)
async def auto_event():
    channel = discord.utils.get(bot.get_all_channels(), name="event-board")  # 👈 thay bằng tên kênh event
    if not channel:
        return

    users = load_characters()
    for uid in users:
        user = await bot.fetch_user(int(uid))
        item = random.choice(["🎁 Hộp bí ẩn", "Soul Fragment", "Aether Elixir"])
        users[uid].setdefault("vật_phẩm", []).append(item)

        try:
            await channel.send(f"🎉 {user.mention} đã nhận được **{item}** từ một sự kiện định mệnh!")
        except:
            continue

    save_characters(users)

@tasks.loop(seconds=60)
async def cleanup_effects():
    data = load_characters()
    updated = False

    for user_id, char in data.items():
        effects = char.get("hiệu_ứng")
        if not isinstance(effects, dict):
            # Nếu hiệu ứng là list (kiểu cũ), bỏ qua hoặc convert nếu cần
            continue

        expired_keys = []
        for key, info in effects.items():
            if time.time() > info.get("hết_hạn", 0):
                expired_keys.append(key)

        for k in expired_keys:
            del effects[k]
            updated = True

        # Nếu không còn hiệu ứng nào, xoá luôn
        if isinstance(effects, dict) and not effects:
            del char["hiệu_ứng"]
            updated = True

    if updated:
        save_characters(data)

@tasks.loop(minutes=1)
async def cleanup_effects():
    data = load_characters()
    now = time.time()

    for char in data.values():
        # Nếu hiệu_ứng không phải dict thì bỏ qua
        if not isinstance(char.get("hiệu_ứng"), dict):
            continue

        char["hiệu_ứng"] = {
            k: v for k, v in char["hiệu_ứng"].items()
            if v["hết_hạn"] > now
        }

    save_characters(data)
class Shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Load dữ liệu shop_items.json
        with open("shop_weapons.json", "r", encoding="utf-8") as f:
            self.shop_items = json.load(f)

    @app_commands.command(name="shop", description="Xem cửa hàng")
    @app_commands.describe(category="Loại item muốn xem (vd: weapons)")
    async def shop_view(self, interaction: discord.Interaction, category: str):
        # Lọc item theo category
        items = [item for item in self.shop_items if item.get("category") == category]

        if not items:
            await interaction.response.send_message(f"❌ Không có sản phẩm nào trong category `{category}`.", ephemeral=True)
            return

        # Tạo embed
        embed = discord.Embed(
            title=f"🛒 Shop - {category.capitalize()}",
            description=f"Danh sách {category} hiện có:",
            color=discord.Color.gold()
        )

        for item in items:
            name = item.get("name")
            desc = item.get("desc", "Không có mô tả.")
            price = item.get("price", "?")
            rarity = item.get("rarity", "common").capitalize()

            # Hiển thị stats riêng cho weapon vs armor
            if item["category"] == "weapon":
                stats = f"⚔️ ATK: {item.get('atk',0)} | 🎯 Crit: {item.get('crit',0)}%"
            elif item["category"] == "armor":
                stats = f"🛡 DEF: {item.get('def',0)} | ⏳ Durability: {item.get('durability',0)}"
            else:
                stats = "Không có chỉ số."

            embed.add_field(
                name=f"{item['id']} | {name} ({rarity}) - 💰 {price} coins",
                value=f"{desc}\n{stats}",
                inline=False
            )
        await interaction.response.send_message(embed=embed)
    @app_commands.command(name="buy", description="Mua vật phẩm từ shop")
    @app_commands.describe(item_id="ID của item muốn mua")
    async def shop_buy(self, interaction: discord.Interaction, item_id: str):
        user_id = str(interaction.user.id)
        users = load_users()

        # Nếu user chưa có data thì tạo mới
        if user_id not in users:
            users[user_id] = {"coins": 100, "inventory": []}  # mặc định 100 coins

        user_data = users[user_id]

        # Tìm item
        item = next((i for i in self.shop_weapons_n_armors if i["id"] == item_id), None)
        if not item:
            await interaction.response.send_message("❌ Item không tồn tại!", ephemeral=True)
            return

        # Check đủ tiền không
        if user_data["coins"] < item["price"]:
            await interaction.response.send_message("💸 Bạn không đủ coins để mua vật phẩm này!", ephemeral=True)
            return

        # Trừ tiền + thêm vào inventory
        user_data["coins"] -= item["price"]
        user_data["inventory"].append(item_id)

        # Lưu lại
        users[user_id] = user_data
        save_users(users)

        await interaction.response.send_message(
            f"✅ Bạn đã mua **{item['name']}** với giá 💰 {item['price']} coins!\n"
            f"💳 Số dư còn lại: {user_data['coin']} coins."
        )
async def setup(bot):
    await bot.add_cog(Shop(bot))

USERS_FILE = "characters.json"
SHOP_FILE = "shop_weapons_n_armors.json"

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def load_shop():
    with open(SHOP_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

class Weapons(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.shop_items = load_shop()

    @app_commands.command(name="weapons", description="Xem túi đồ của bạn")
    async def weapons(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        users = load_users()

        if user_id not in users:
            await interaction.response.send_message("❌ Bạn chưa có dữ liệu. Hãy thử mua gì đó trước!", ephemeral=True)
            return

        user_data = users[user_id]
        coins = user_data.get("coins", 0)
        weapons = user_data.get("weapons", [])

        if not weapons:
            await interaction.response.send_message(f"🎒 Túi đồ trống rỗng.\n💳 Coins: {coins}", ephemeral=True)
            return

        # Gom thông tin item từ shop
        weapons = []
        for item_id in weapons:
            item = next((i for i in self.shop_items if i["id"] == item_id), None)
            if not item:
                continue
            if item["category"] == "weapon":
                weapons.append(item)
        # Weapons
        if weapons:
            weapon_text = "\n".join(
                f"- **{w['name']}** (⚔ {w.get('atk',0)}, 🎯 {w.get('crit',0)}%)"
                for w in weapons
            )
        else:
            weapon_text = "_Không có_"
        embed.add_field(name="⚔️ Weapons", value=weapon_text, inline=False)

        await interaction.response.send_message(embed=embed)
async def setup(bot):
    await bot.add_cog(Weapons(bot))
class Armors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.shop_armors = load_shop()

    @app_commands.command(name="armors", description="Xem túi đồ của bạn")
    async def armors(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        users = load_users()

        if user_id not in users:
            await interaction.response.send_message("❌ Bạn chưa có dữ liệu. Hãy thử mua gì đó trước!", ephemeral=True)
            return

        user_data = users[user_id]
        coins = user_data.get("coins", 0)
        armors = user_data.get("armors", [])

        if not armors:
            await interaction.response.send_message(f"🎒 Túi đồ trống rỗng.\n💳 Coins: {coins}", ephemeral=True)
            return

        # Gom thông tin item từ shop
        armors = []
        for item_id in armors:
            item = next((i for i in self.shop_items if i["id"] == item_id), None)
            if not item:
                continue
            if item["category"] == "armor":
                armors.append(item)

        embed = discord.Embed(
            title=f"🎒 Túi đồ của {interaction.user.display_name}",
            description=f"💳 Coins còn lại: {coins}",
            color=discord.Color.green()
        )

        # Armors
        if armors:
            armor_text = "\n".join(
                f"- **{a['name']}** (🛡 {a.get('def',0)}, ⏳ {a.get('durability',0)})"
                for a in armors
            )
        else:
            armor_text = "_Không có_"
        embed.add_field(name="🛡 Armors", value=armor_text, inline=False)

        await interaction.response.send_message(embed=embed)
async def setup(bot):
    await bot.add_cog(Armors(bot))

# ---------- Chạy bot ----------
bot.run("MTM5MDM1OTAyMTQ2MjIyOTExMg.G0k625.gDXG_Ss2yB1l999fesnbD1P9SBUTIH-JT5Gx0M")