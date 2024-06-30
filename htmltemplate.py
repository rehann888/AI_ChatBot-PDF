# htmltemplates.py
css = """
<style>
body {
    font-family: Arial, sans-serif;
}
</style>
"""

bot_template = """
<div style="background-color:#120303; padding:10px; border-radius:5px; margin:10px 0;">
    <b>Bot:</b> {{MSG}}
</div>
"""

user_template = """
<div style="background-color:#120303; padding:10px; border-radius:5px; margin:10px 0;">
    <b>You:</b> {{MSG}}
</div>
"""
