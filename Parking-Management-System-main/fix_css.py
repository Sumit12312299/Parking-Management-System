import re

with open('d:/Parking-Management-System-main/Parking-Management-System-main/static/css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Make navbar sticky and glassmorphic
old_navbar = """.navbar {
    height: 70px;
    background: #1F6F43;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 60px;
    color: white;
}"""
new_navbar = """.navbar {
    height: 75px;
    background: rgba(31, 111, 67, 0.85);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 60px;
    color: white;
    position: sticky;
    top: 0;
    z-index: 1000;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
}"""
css = css.replace(old_navbar, new_navbar)

old_navlinks = """.navbar .nav-links a {
    margin-left: 25px;
    color: white;
    text-decoration: none;
    font-weight: 500;
    transition: 0.3s;
}

.navbar .nav-links a:hover {
    opacity: 0.8;
}"""
new_navlinks = """.navbar .nav-links a {
    margin-left: 30px;
    color: white;
    text-decoration: none;
    font-weight: 500;
    position: relative;
    padding-bottom: 5px;
    transition: 0.3s;
}
.navbar .nav-links a::after {
    content: '';
    position: absolute;
    width: 0;
    height: 2px;
    bottom: 0;
    left: 0;
    background-color: #22c55e;
    transition: width 0.3s ease;
}
.navbar .nav-links a:hover::after {
    width: 100%;
}
.navbar .nav-links a:hover {
    color: #22c55e;
}"""
css = css.replace(old_navlinks, new_navlinks)

# Fix hero
old_hero_410 = """.hero {
    width: 100vw;
    margin-left: calc(-50vw + 50%);
    background: linear-gradient(135deg, #064e3b, #065f46);
    color: white;
    padding: 140px 60px;
}"""
css = css.replace(old_hero_410, "")

old_hero_66 = """.hero {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 80px;
}"""
css = css.replace(old_hero_66, "")

old_hero_353 = """.hero {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 80px 0;
}"""
css = css.replace(old_hero_353, "")

old_hero_main = """.hero {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 100px 8%;
    background: linear-gradient(135deg, #0f5d3f, #0c4c33);
    color: white;
    min-height: 80vh;
}"""
new_hero_main = """.hero {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 100px 8%;
    background: linear-gradient(135deg, #0f5d3f 0%, #064e3b 100%);
    color: white;
    min-height: 85vh;
    width: 100vw;
    margin-left: calc(-50vw + 50%);
    position: relative;
    overflow: hidden;
}
/* Subtle pattern overlay */
.hero::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background-image: radial-gradient(circle at 2px 2px, rgba(255,255,255,0.05) 1px, transparent 0);
    background-size: 32px 32px;
    z-index: 0;
}
.hero-left, .hero-right {
    z-index: 1;
}"""
css = css.replace(old_hero_main, new_hero_main)

# Add floating animation to stats box
old_stats_box = """.stats-box {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 25px;
    background: rgba(255,255,255,0.08);
    padding: 40px;
    border-radius: 20px;
    backdrop-filter: blur(12px);
}"""
new_stats_box = """@keyframes float {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-15px); }
    100% { transform: translateY(0px); }
}

.stats-box {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 25px;
    background: rgba(255, 255, 255, 0.08);
    padding: 45px;
    border-radius: 24px;
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 20px 40px rgba(0,0,0,0.2);
    animation: float 6s ease-in-out infinite;
}"""
css = css.replace(old_stats_box, new_stats_box)

# Buttons upgrade
old_btn_primary = """.btn-primary {
    background: #00c853;
    color: white;
    padding: 14px 28px;
    border-radius: 10px;
    text-decoration: none;
    margin-right: 15px;
}"""
new_btn_primary = """.btn-primary {
    background: #22c55e;
    color: white;
    padding: 14px 32px;
    border-radius: 12px;
    text-decoration: none;
    margin-right: 15px;
    font-weight: 600;
    transition: all 0.3s ease;
    box-shadow: 0 8px 20px rgba(34, 197, 94, 0.3);
    display: inline-block;
}
.btn-primary:hover {
    background: #16a34a;
    transform: translateY(-3px) scale(1.02);
    box-shadow: 0 12px 25px rgba(34, 197, 94, 0.4);
}"""
css = css.replace(old_btn_primary, new_btn_primary)

old_btn_outline = """.btn-outline {
    border: 2px solid #00c853;
    padding: 12px 26px;
    border-radius: 10px;
    text-decoration: none;
    color: #00c853;
}"""
new_btn_outline = """.btn-outline {
    border: 2px solid #22c55e;
    padding: 12px 30px;
    border-radius: 12px;
    text-decoration: none;
    color: #22c55e;
    font-weight: 600;
    transition: all 0.3s ease;
    display: inline-block;
}
.btn-outline:hover {
    background: rgba(34, 197, 94, 0.1);
    transform: translateY(-3px);
}"""
css = css.replace(old_btn_outline, new_btn_outline)

# Cards upgrade
old_card = """.card {
    background: white;
    padding: 25px;
    border-radius: 14px;
    border: 1px solid #E0EFE5;
    transition: 0.3s ease;
}

.card:hover {
    transform: translateY(-6px);
    box-shadow: 0 8px 20px rgba(0,0,0,0.05);
}"""
new_card = """.card {
    background: white;
    padding: 30px;
    border-radius: 18px;
    border: 1px solid #E0EFE5;
    transition: all 0.4s ease;
    position: relative;
    overflow: hidden;
}

.card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; width: 100%; height: 4px;
    background: #22c55e;
    transform: scaleX(0);
    transform-origin: left;
    transition: transform 0.4s ease;
}

.card:hover::before {
    transform: scaleX(1);
}

.card:hover {
    transform: translateY(-10px);
    box-shadow: 0 20px 40px rgba(31, 111, 67, 0.08);
}"""
css = css.replace(old_card, new_card)

with open('d:/Parking-Management-System-main/Parking-Management-System-main/static/css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("CSS updated successfully")
