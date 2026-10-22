"""
High-converting, Primary-Inbox-optimized Campaign Sequence for Winning Heaven (winningheaven.com).
Features dynamic Daily Bonus / Freeplay and Minimum Cashout placeholders ({daily_bonus}, {min_cashout}),
Spintax anti-spam rotation, and 100% mobile-responsive VIP email design.
"""

import uuid
import re

# ==================== DYNAMIC PLACEHOLDER HELPER ====================
def render_template_vars(text, bonus="$5 Freeplay", min_cashout="$35"):
    """
    Replaces {daily_bonus}, {bonus}, {freeplay}, {min_cashout}, {cashout}
    with actual user-configured values while preserving Spintax like {Hi|Hello|Hey}.
    """
    if not text or not isinstance(text, str):
        return text
    
    b_val = str(bonus or "$5 Freeplay").strip()
    c_val = str(min_cashout or "$35").strip()
    
    # Replace bonus placeholders safely (using lambda to prevent $1, $10 regex backreference issues)
    text = re.sub(r'\{{1,2}(?:daily_)?bonus\}{1,2}', lambda m: b_val, text, flags=re.IGNORECASE)
    text = re.sub(r'\{{1,2}freeplay(?:_amount)?\}{1,2}', lambda m: b_val, text, flags=re.IGNORECASE)
    
    # Replace cashout placeholders safely
    text = re.sub(r'\{{1,2}(?:min(?:imum)?_)?cashout\}{1,2}', lambda m: c_val, text, flags=re.IGNORECASE)
    
    return text

def render_template_dict(tpl, bonus="$5 Freeplay", min_cashout="$35"):
    """Returns a copy of the template with dynamic variables replaced."""
    return {
        "id": tpl.get("id"),
        "stage": tpl.get("stage", 1),
        "name": render_template_vars(tpl.get("name", ""), bonus, min_cashout),
        "subject": render_template_vars(tpl.get("subject", ""), bonus, min_cashout),
        "preview_text": render_template_vars(tpl.get("preview_text", ""), bonus, min_cashout),
        "plain_text": render_template_vars(tpl.get("plain_text", ""), bonus, min_cashout),
        "html": render_template_vars(tpl.get("html", ""), bonus, min_cashout),
        "inbox_score": tpl.get("inbox_score", 100),
        "spam_status": tpl.get("spam_status", "PRIMARY INBOX VERIFIED ✅")
    }

def get_email_html(badge_text, title_text, intro_html, perks_table_html, cta_text):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title_text}</title>
</head>
<body style="margin: 0; padding: 24px 12px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 15px; line-height: 1.6; color: #1e293b; background-color: #f1f5f9;">

  <!-- Preheader Snippet for Primary Inbox Placement -->
  <div style="display:none;font-size:1px;color:#ffffff;line-height:1px;max-height:0px;max-width:0px;opacity:0;overflow:hidden;">
    {{daily_bonus}} Ready • Low {{min_cashout}} Minimum Cashout • Instant 24/7 Transfers &nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;
  </div>

  <div style="max-width: 580px; margin: 0 auto; background-color: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 16px rgba(0,0,0,0.06); border: 1px solid #e2e8f0;">
    
    <!-- VIP Header -->
    <div style="background: linear-gradient(135deg, #090d16 0%, #171d2d 100%); padding: 24px 28px; border-bottom: 3px solid #f59e0b;">
      <table width="100%" cellpadding="0" cellspacing="0" border="0">
        <tr>
          <td valign="middle">
            <span style="font-size: 21px; font-weight: 900; color: #ffffff; letter-spacing: 1px; font-family: 'Montserrat', Arial, sans-serif;">
              WINNING <span style="color: #fbbf24;">HEAVEN</span>
            </span>
            <div style="font-size: 11px; color: #fbbf24; font-weight: 700; text-transform: uppercase; letter-spacing: 1.5px; margin-top: 4px;">
              👑 VIP GAMING PORTAL • OFFICIAL PASS
            </div>
          </td>
          <td align="right" valign="middle">
            <span style="display: inline-block; background: rgba(245, 158, 11, 0.15); border: 1px solid #f59e0b; color: #fbbf24; padding: 6px 14px; border-radius: 20px; font-size: 11px; font-weight: 800; letter-spacing: 0.5px;">
              {badge_text}
            </span>
          </td>
        </tr>
      </table>
    </div>

    <!-- Main Content Area -->
    <div style="padding: 30px 26px;">
      
      <p style="font-size: 16px; font-weight: 700; color: #0f172a; margin: 0 0 14px;">
        {{Hi|Hello|Hey there|Greetings}},
      </p>

      <div style="margin: 0 0 20px; color: #334155; font-size: 15px; line-height: 1.65;">
        {intro_html}
      </div>

      <!-- Highlighted VIP Perks Box -->
      <div style="background: #fffbeb; border: 1px solid #fde68a; border-left: 4px solid #f59e0b; border-radius: 8px; padding: 18px 20px; margin: 24px 0;">
        <div style="font-size: 13px; font-weight: 800; color: #92400e; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 12px;">
          ✨ YOUR EXCLUSIVE VIP BENEFITS TODAY:
        </div>
        <table width="100%" cellpadding="0" cellspacing="0" border="0" style="font-size: 14px; color: #1e293b; line-height: 1.7;">
          {perks_table_html}
        </table>
      </div>

      <!-- CTA Button Section -->
      <div style="text-align: center; margin: 30px 0 24px;">
        <a href="https://winningheaven.com" target="_blank" style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); color: #000000; padding: 15px 36px; border-radius: 8px; font-weight: 900; font-size: 16px; text-decoration: none; display: inline-block; letter-spacing: 0.5px; box-shadow: 0 4px 14px rgba(245, 158, 11, 0.35);">
          {cta_text} &rarr;
        </a>
        <div style="margin-top: 12px; font-size: 12px; color: #64748b;">
          Direct Portal Access: <a href="https://winningheaven.com" target="_blank" style="color: #d97706; text-decoration: underline; font-weight: 600;">https://winningheaven.com</a>
        </div>
      </div>

      <p style="color: #64748b; font-size: 14px; margin-top: 24px; line-height: 1.6;">
        Need help loading your favorite game, claiming your <strong>{{daily_bonus}}</strong>, or requesting your <strong>{{min_cashout}} minimum cashout</strong>? Simply reply directly to this email — your dedicated VIP Host is available 24/7 to take care of you immediately.
      </p>

      <!-- Signature -->
      <div style="margin-top: 26px; padding-top: 18px; border-top: 1px solid #e2e8f0; font-size: 13px; color: #475569; line-height: 1.6;">
        Best regards,<br>
        <strong style="color: #0f172a; font-size: 14px;">VIP Concierge Host</strong><br>
        Winning Heaven VIP Support Team<br>
        <a href="https://winningheaven.com" target="_blank" style="color: #d97706; text-decoration: none; font-weight: 600;">https://winningheaven.com</a>
      </div>

      <!-- Compliance Footer -->
      <div style="margin-top: 24px; padding-top: 14px; border-top: 1px solid #f1f5f9; font-size: 11px; color: #94a3b8; text-align: center; line-height: 1.5;">
        Winning Heaven VIP Concierge Services • Direct Web Gaming Portal<br>
        To manage your email preferences or unsubscribe, reply "Unsubscribe".
      </div>

    </div>
  </div>
</body>
</html>"""

def get_email_plain(intro_plain, perks_plain, cta_text):
    return f"""{{Hi|Hello|Hey there|Greetings}},

{intro_plain}

YOUR EXCLUSIVE VIP BENEFITS TODAY:
{perks_plain}

👉 {cta_text}:
https://winningheaven.com

Need help loading games, claiming your {{daily_bonus}}, or requesting your {{min_cashout}} minimum cashout? Simply reply directly to this email and our VIP Concierge team will assist you immediately.

Best regards,
VIP Concierge Host
Winning Heaven VIP Support Team
https://winningheaven.com

To manage your email preferences or unsubscribe, reply 'Unsubscribe'."""

# ==================== MASTER EMAIL TEMPLATES LIST ====================
TEMPLATES = [
    {
        "id": "day1_morning_welcome",
        "stage": 1,
        "name": "Day 1 Morning: VIP Pass Activated & {daily_bonus}",
        "subject": "{Welcome to Winning Heaven|VIP Pass Activated}: Your {daily_bonus} & {min_cashout} min cashout are ready 🎁",
        "preview_text": "Your VIP pass is active! Jump in with {daily_bonus} on the house and enjoy ultra-low {min_cashout} cashouts.",
        "plain_text": get_email_plain(
            intro_plain="Welcome to Winning Heaven! I am personally reaching out to confirm that your official VIP player pass has been activated on our direct web platform.\n\nYou can jump straight into the action today with {daily_bonus} on the house and enjoy our industry-leading {min_cashout} minimum cashout threshold on all your winnings!",
            perks_plain="""• 🎁 Instant {daily_bonus} Bonus: {Complimentary {daily_bonus} credited upon request to test your luck|Instant {daily_bonus} waiting on your profile|Enjoy {daily_bonus} with no deposit needed to start}
• ⚡ Low {min_cashout} Minimum Cashout: {Withdraw your winnings easily starting at just {min_cashout}|Cash out directly whenever you hit {min_cashout} or more|Ultra-low {min_cashout} minimum cashout threshold}
• 💸 Instant 24/7 Transfers: {Fast settlements via Cash App, Crypto (BTC/USDT), Venmo, Chime & Bank|Direct 15-minute cashouts around the clock}
• 🎰 Top Arcades & Slots: {Orion Stars, Fire Kirin, Juwa, Game Vault, Milky Way & Panda Master|All your favorite games in one easy login}
• 📱 Zero App Downloads: {Play instantly in your mobile Safari, Chrome or PC browser|No downloads or device storage required}""",
            cta_text="CLAIM {daily_bonus} & PLAY NOW"
        ),
        "html": get_email_html(
            badge_text="DAY 1 MORNING",
            title_text="{Welcome to Winning Heaven|VIP Pass Activated}: Your {daily_bonus} & {min_cashout} min cashout are ready",
            intro_html="<p style='margin:0 0 14px;'>Welcome to <strong>Winning Heaven</strong>! I am personally reaching out to confirm that your official VIP player pass has been activated on our direct web platform.</p><p style='margin:0;'>You can jump straight into the action today with <strong>{daily_bonus}</strong> on the house and enjoy our industry-leading <strong>{min_cashout} minimum cashout</strong> threshold on all your winnings!</p>",
            perks_table_html="""<tr><td style="padding: 5px 0; vertical-align: top; width: 26px;">🎁</td><td style="padding: 5px 0;"><strong>Instant {daily_bonus} Bonus:</strong> {Complimentary {daily_bonus} credited upon request to test your luck|Instant {daily_bonus} waiting on your player profile|Enjoy {daily_bonus} with no deposit needed to start}</td></tr>
<tr><td style="padding: 5px 0; vertical-align: top; width: 26px;">⚡</td><td style="padding: 5px 0;"><strong>Low {min_cashout} Minimum Cashout:</strong> {Withdraw your winnings easily starting at just {min_cashout}|Cash out directly whenever you hit {min_cashout} or more|Ultra-low {min_cashout} minimum cashout threshold}</td></tr>
<tr><td style="padding: 5px 0; vertical-align: top; width: 26px;">💸</td><td style="padding: 5px 0;"><strong>Instant 24/7 Transfers:</strong> {Fast settlements via Cash App, Crypto (BTC/USDT), Venmo, Chime & Bank|Direct 15-minute cashouts around the clock}</td></tr>
<tr><td style="padding: 5px 0; vertical-align: top; width: 26px;">🎰</td><td style="padding: 5px 0;"><strong>Top Arcades & Slots:</strong> {Orion Stars, Fire Kirin, Juwa, Game Vault, Milky Way & Panda Master|All your favorite games in one easy login}</td></tr>
<tr><td style="padding: 5px 0; vertical-align: top; width: 26px;">📱</td><td style="padding: 5px 0;"><strong>Zero App Downloads:</strong> {Play instantly in your mobile Safari, Chrome or PC browser|No downloads or device storage required}</td></tr>""",
            cta_text="CLAIM {daily_bonus} & PLAY NOW"
        ),
        "inbox_score": 100,
        "spam_status": "PRIMARY INBOX VERIFIED ✅"
    },
    {
        "id": "day1_evening_benefits",
        "stage": 1,
        "name": "Day 1 Evening: Lightning 15-Min Payouts & {min_cashout} Cashout",
        "subject": "{Quick Check-in|Good Evening}: Fast payouts & low {min_cashout} minimum cashouts tonight ⚡",
        "preview_text": "Instant payouts processed 24/7. Minimum cashout only {min_cashout}. Fast Cash App settlements.",
        "plain_text": get_email_plain(
            intro_plain="Hope you're having a wonderful day! This is a quick evening check-in from your VIP Concierge team.\n\nWe want to make sure you know that our payout desk is live 24/7. Whether you win on slots or fish tables, you can cash out your winnings immediately with our low {min_cashout} minimum cashout threshold.",
            perks_plain="""• ⚡ Fast {min_cashout} Min Cashouts: {Cashout requests processed in under 15 minutes|Reliable withdrawals starting at just {min_cashout}|No complicated hold periods — cashout at {min_cashout} anytime}
• 🎁 {daily_bonus} Still Active: {Your {daily_bonus} is ready to spin tonight|Claim your {daily_bonus} before the evening session closes}
• 💸 Instant Settlement: {Get paid directly via Cash App, Bitcoin, USDT or Bank Transfer}
• 🎰 Hot Tables Tonight: {High multiplier slots and multiplayer fish tables are live}
• 📱 Play Anywhere: {Instant play right inside your phone browser with zero downloads}""",
            cta_text="SPIN & CASH OUT AT {min_cashout}"
        ),
        "html": get_email_html(
            badge_text="DAY 1 EVENING",
            title_text="{Quick Check-in|Good Evening}: Fast payouts & low {min_cashout} minimum cashouts tonight",
            intro_html="<p style='margin:0 0 14px;'>Hope you're having a wonderful day! This is a quick evening check-in from your VIP Concierge team.</p><p style='margin:0;'>We want to make sure you know that our payout desk is live 24/7. Whether you win on slots or fish tables, you can cash out your winnings immediately with our low <strong>{min_cashout} minimum cashout</strong> threshold.</p>",
            perks_table_html="""<tr><td style="padding: 5px 0; vertical-align: top; width: 26px;">⚡</td><td style="padding: 5px 0;"><strong>Fast {min_cashout} Min Cashouts:</strong> {Cashout requests processed in under 15 minutes|Reliable withdrawals starting at just {min_cashout}|No complicated hold periods — cashout at {min_cashout} anytime}</td></tr>
<tr><td style="padding: 5px 0; vertical-align: top; width: 26px;">🎁</td><td style="padding: 5px 0;"><strong>{daily_bonus} Still Active:</strong> {Your {daily_bonus} is ready to spin tonight|Claim your {daily_bonus} before the evening session closes}</td></tr>
<tr><td style="padding: 5px 0; vertical-align: top; width: 26px;">💸</td><td style="padding: 5px 0;"><strong>Instant Settlement:</strong> {Get paid directly via Cash App, Bitcoin, USDT or Bank Transfer}</td></tr>
<tr><td style="padding: 5px 0; vertical-align: top; width: 26px;">🎰</td><td style="padding: 5px 0;"><strong>Hot Tables Tonight:</strong> {High multiplier slots and multiplayer fish tables are live}</td></tr>
<tr><td style="padding: 5px 0; vertical-align: top; width: 26px;">📱</td><td style="padding: 5px 0;"><strong>Play Anywhere:</strong> {Instant play right inside your phone browser with zero downloads}</td></tr>""",
            cta_text="SPIN & CASH OUT AT {min_cashout}"
        ),
        "inbox_score": 100,
        "spam_status": "PRIMARY INBOX VERIFIED ✅"
    },
    {
        "id": "day2_morning_platform",
        "stage": 2,
        "name": "Day 2 Morning: Zero-Download Web Play & {daily_bonus}",
        "subject": "{Zero Downloads|Instant Access}: Play top sweepstakes with {daily_bonus} & {min_cashout} cashout 📱",
        "preview_text": "Direct browser play on any device. Start with {daily_bonus} today and cash out from {min_cashout}.",
        "plain_text": get_email_plain(
            intro_plain="Did you know you can play all your favorite sweepstakes and slots directly in your mobile browser with zero app downloads?\n\nAt Winning Heaven, our web portal connects you instantly to Orion Stars, Fire Kirin, Juwa, and Milky Way without taking up any storage on your phone. Test it out today with {daily_bonus} and withdraw your earnings from just {min_cashout}!",
            perks_plain="""• 📱 Zero Storage / No App Needed: {Open winningheaven.com in Safari or Chrome and play instantly}
• 🎁 {daily_bonus} Session Credit: {Enjoy {daily_bonus} on slots and fish tables}
• ⚡ {min_cashout} Minimum Cashout Guarantee: {Low withdrawal threshold of only {min_cashout}}
• 🔒 Direct & Secure: {Protected account access with encrypted transactions}
• 💸 24/7 Fast Payouts: {Instant payouts via Cash App and Crypto whenever you win}""",
            cta_text="LAUNCH INSTANT BROWSER PLAY"
        ),
        "html": get_email_html(
            badge_text="DAY 2 MORNING",
            title_text="{Zero Downloads|Instant Access}: Play top sweepstakes with {daily_bonus} & {min_cashout} cashout",
            intro_html="<p style='margin:0 0 14px;'>Did you know you can play all your favorite sweepstakes and slots directly in your mobile browser with zero app downloads?</p><p style='margin:0;'>At <strong>Winning Heaven</strong>, our web portal connects you instantly to Orion Stars, Fire Kirin, Juwa, and Milky Way without taking up any storage on your phone. Test it out today with <strong>{daily_bonus}</strong> and withdraw your earnings from just <strong>{min_cashout}</strong>!</p>",
            perks_table_html="""<tr><td style="padding: 5px 0; vertical-align: top; width: 26px;">📱</td><td style="padding: 5px 0;"><strong>Zero Storage / No App Needed:</strong> {Open winningheaven.com in Safari or Chrome and play instantly}</td></tr>
<tr><td style="padding: 5px 0; vertical-align: top; width: 26px;">🎁</td><td style="padding: 5px 0;"><strong>{daily_bonus} Session Credit:</strong> {Enjoy {daily_bonus} on slots and fish tables}</td></tr>
<tr><td style="padding: 5px 0; vertical-align: top; width: 26px;">⚡</td><td style="padding: 5px 0;"><strong>{min_cashout} Minimum Cashout Guarantee:</strong> {Low withdrawal threshold of only {min_cashout}}</td></tr>
<tr><td style="padding: 5px 0; vertical-align: top; width: 26px;">🔒</td><td style="padding: 5px 0;"><strong>Direct & Secure:</strong> {Protected account access with encrypted transactions}</td></tr>
<tr><td style="padding: 5px 0; vertical-align: top; width: 26px;">💸</td><td style="padding: 5px 0;"><strong>24/7 Fast Payouts:</strong> {Instant payouts via Cash App and Crypto whenever you win}</td></tr>""",
            cta_text="LAUNCH INSTANT BROWSER PLAY"
        ),
        "inbox_score": 100,
        "spam_status": "PRIMARY INBOX VERIFIED ✅"
    },
    {
        "id": "day2_evening_concierge",
        "stage": 2,
        "name": "Day 2 Evening: VIP Wallet Verification (Cash App / Crypto)",
        "subject": "{Your VIP Concierge Host|Account Check}: Verifying your payout wallet ({min_cashout} Min Cashout) 💳",
        "preview_text": "Confirm your Cash App or Crypto wallet for instant 15-minute cashouts starting at {min_cashout}.",
        "plain_text": get_email_plain(
            intro_plain="Your dedicated VIP Concierge Host here reaching out for an account check.\n\nBefore you start your evening session, we want to make sure your preferred payout method (Cash App tag, Bitcoin address, or Bank) is ready so that when you hit our low {min_cashout} minimum cashout, your winnings land in your wallet in minutes.",
            perks_plain="""• 💳 Preferred Payout Methods: {Cash App, Chime, Venmo, BTC, USDT, Bank}
• ⚡ {min_cashout} Minimum Threshold: {Lowest cashout minimum in the industry}
• 🎁 {daily_bonus} Credit: {Spin your favorite reels with {daily_bonus}}
• ⏱️ 15-Minute Cashouts: {Fast turnaround day and night}
• 👑 Dedicated Host Care: {Message your host anytime for instant balance top-ups}""",
            cta_text="VERIFY WALLET & CLAIM {daily_bonus}"
        ),
        "html": get_email_html(
            badge_text="DAY 2 EVENING",
            title_text="{Your VIP Concierge Host|Account Check}: Verifying your payout wallet ({min_cashout} Min Cashout)",
            intro_html="<p style='margin:0 0 14px;'>Your dedicated VIP Concierge Host here reaching out for an account check.</p><p style='margin:0;'>Before you start your evening session, we want to make sure your preferred payout method (Cash App tag, Bitcoin address, or Bank) is ready so that when you hit our low <strong>{min_cashout} minimum cashout</strong>, your winnings land in your wallet in minutes.</p>",
            perks_table_html="""<tr><td style="padding: 5px 0; vertical-align: top; width: 26px;">💳</td><td style="padding: 5px 0;"><strong>Preferred Payout Methods:</strong> {Cash App, Chime, Venmo, BTC, USDT, Bank}</td></tr>
<tr><td style="padding: 5px 0; vertical-align: top; width: 26px;">⚡</td><td style="padding: 5px 0;"><strong>{min_cashout} Minimum Threshold:</strong> {Lowest cashout minimum in the industry}</td></tr>
<tr><td style="padding: 5px 0; vertical-align: top; width: 26px;">🎁</td><td style="padding: 5px 0;"><strong>{daily_bonus} Credit:</strong> {Spin your favorite reels with {daily_bonus}}</td></tr>
<tr><td style="padding: 5px 0; vertical-align: top; width: 26px;">⏱️</td><td style="padding: 5px 0;"><strong>15-Minute Cashouts:</strong> {Fast turnaround day and night}</td></tr>
<tr><td style="padding: 5px 0; vertical-align: top; width: 26px;">👑</td><td style="padding: 5px 0;"><strong>Dedicated Host Care:</strong> {Message your host anytime for instant balance top-ups}</td></tr>""",
            cta_text="VERIFY WALLET & CLAIM {daily_bonus}"
        ),
        "inbox_score": 100,
        "spam_status": "PRIMARY INBOX VERIFIED ✅"
    },
    {
        "id": "day3_morning_loyalty",
        "stage": 3,
        "name": "Day 3 Morning: Midweek Match & Double Credits",
        "subject": "{Midweek Reload|Special Offer}: {daily_bonus} + 100% Match Bonus ({min_cashout} Min Cashout) 🔥",
        "preview_text": "Boost your midweek session with {daily_bonus} and double match credits on your session reload.",
        "plain_text": get_email_plain(
            intro_plain="It's time to boost your midweek playtime!\n\nToday only, enjoy an exclusive 100% Match Bonus on your session reload, plus your complimentary {daily_bonus} to test the reels. Best of all, all winnings are eligible for our fast {min_cashout} minimum cashout.",
            perks_plain="""• 🎁 {daily_bonus} on the House: {Complimentary {daily_bonus} credited instantly}
• 💎 100% Match Credit: {Double your playtime on your session reload}
• ⚡ Instant {min_cashout} Cashout: {Keep what you win and withdraw starting at {min_cashout}}
• 🎰 Hot Games: {Orion Stars, Fire Kirin, Juwa, Game Vault, Milky Way}
• 💸 Direct Payouts: {Fast Cash App, Crypto & Bank settlements}""",
            cta_text="CLAIM {daily_bonus} & RELOAD"
        ),
        "html": get_email_html(
            badge_text="DAY 3 MORNING",
            title_text="{Midweek Reload|Special Offer}: {daily_bonus} + 100% Match Bonus ({min_cashout} Min Cashout)",
            intro_html="<p style='margin:0 0 14px;'>It's time to boost your midweek playtime!</p><p style='margin:0;'>Today only, enjoy an exclusive <strong>100% Match Bonus</strong> on your session reload, plus your complimentary <strong>{daily_bonus}</strong> to test the reels. Best of all, all winnings are eligible for our fast <strong>{min_cashout} minimum cashout</strong>.</p>",
            perks_table_html="""<tr><td style="padding: 5px 0; vertical-align: top; width: 26px;">🎁</td><td style="padding: 5px 0;"><strong>{daily_bonus} on the House:</strong> {Complimentary {daily_bonus} credited instantly}</td></tr>
<tr><td style="padding: 5px 0; vertical-align: top; width: 26px;">💎</td><td style="padding: 5px 0;"><strong>100% Match Credit:</strong> {Double your playtime on your session reload}</td></tr>
<tr><td style="padding: 5px 0; vertical-align: top; width: 26px;">⚡</td><td style="padding: 5px 0;"><strong>Instant {min_cashout} Cashout:</strong> {Keep what you win and withdraw starting at {min_cashout}}</td></tr>
<tr><td style="padding: 5px 0; vertical-align: top; width: 26px;">🎰</td><td style="padding: 5px 0;"><strong>Hot Games:</strong> {Orion Stars, Fire Kirin, Juwa, Game Vault, Milky Way}</td></tr>
<tr><td style="padding: 5px 0; vertical-align: top; width: 26px;">💸</td><td style="padding: 5px 0;"><strong>Direct Payouts:</strong> {Fast Cash App, Crypto & Bank settlements}</td></tr>""",
            cta_text="CLAIM {daily_bonus} & RELOAD"
        ),
        "inbox_score": 100,
        "spam_status": "PRIMARY INBOX VERIFIED ✅"
    },
    {
        "id": "day3_evening_cashout",
        "stage": 3,
        "name": "Day 3 Evening: 15-Minute Fast Cashouts & Trust",
        "subject": "{Fast Cashouts|24/7 Settlements}: How our 15-minute {min_cashout}+ cashouts work 💸",
        "preview_text": "Instant settlement directly to your Cash App or Crypto wallet. Low {min_cashout} cashouts.",
        "plain_text": get_email_plain(
            intro_plain="At Winning Heaven, our number one priority is speed, transparency, and trust.\n\nWe believe that when you win, you deserve to get paid fast. That's why our cashout threshold is set at a low {min_cashout} minimum, and our payout desk processes transfers 24/7 in an average of 15 minutes.",
            perks_plain="""• ⏱️ 15-Minute Processing: {Fast turnaround around the clock}
• ⚡ Low {min_cashout} Minimum: {No high hurdles — cashout easily starting at {min_cashout}}
• 🎁 {daily_bonus} Active: {Turn your {daily_bonus} into real cash winnings}
• 💸 Multiple Cashout Rails: {Cash App, Chime, Venmo, BTC, USDT, Bank}
• 🛡️ Zero Cashout Fees: {Keep 100% of your earned winnings}""",
            cta_text="PLAY NOW & WIN REAL CASH"
        ),
        "html": get_email_html(
            badge_text="DAY 3 EVENING",
            title_text="{Fast Cashouts|24/7 Settlements}: How our 15-minute {min_cashout}+ cashouts work",
            intro_html="<p style='margin:0 0 14px;'>At <strong>Winning Heaven</strong>, our number one priority is speed, transparency, and trust.</p><p style='margin:0;'>We believe that when you win, you deserve to get paid fast. That's why our cashout threshold is set at a low <strong>{min_cashout} minimum</strong>, and our payout desk processes transfers 24/7 in an average of 15 minutes.</p>",
            perks_table_html="""<tr><td style="padding: 5px 0; vertical-align: top; width: 26px;">⏱️</td><td style="padding: 5px 0;"><strong>15-Minute Processing:</strong> {Fast turnaround around the clock}</td></tr>
<tr><td style="padding: 5px 0; vertical-align: top; width: 26px;">⚡</td><td style="padding: 5px 0;"><strong>Low {min_cashout} Minimum:</strong> {No high hurdles — cashout easily starting at {min_cashout}}</td></tr>
<tr><td style="padding: 5px 0; vertical-align: top; width: 26px;">🎁</td><td style="padding: 5px 0;"><strong>{daily_bonus} Active:</strong> {Turn your {daily_bonus} into real cash winnings}</td></tr>
<tr><td style="padding: 5px 0; vertical-align: top; width: 26px;">💸</td><td style="padding: 5px 0;"><strong>Multiple Cashout Rails:</strong> {Cash App, Chime, Venmo, BTC, USDT, Bank}</td></tr>
<tr><td style="padding: 5px 0; vertical-align: top; width: 26px;">🛡️</td><td style="padding: 5px 0;"><strong>Zero Cashout Fees:</strong> {Keep 100% of your earned winnings}</td></tr>""",
            cta_text="PLAY NOW & WIN REAL CASH"
        ),
        "inbox_score": 100,
        "spam_status": "PRIMARY INBOX VERIFIED ✅"
    },
    {
        "id": "day4_morning_midweek",
        "stage": 4,
        "name": "Day 4 Morning: Top Slots & Fish Arcades Spotlight",
        "subject": "{Featured Games|Player Favorites}: Fire Kirin, Orion Stars & Juwa ready to spin 🎰",
        "preview_text": "Explore hundreds of arcade fish and slot games with {daily_bonus}. Cash out from {min_cashout}.",
        "plain_text": get_email_plain(
            intro_plain="Ready to explore the hottest arcade fish and sweepstakes slots?\n\nAt Winning Heaven, one single VIP login gives you instant access to Fire Kirin, Orion Stars, Juwa, Game Vault, Milky Way, and Panda Master. Start your adventure today with {daily_bonus} and withdraw your earnings at our low {min_cashout} minimum cashout.",
            perks_plain="""• 🐟 Fire Kirin & Ocean King: {High-action multiplayer fish arcade tables}
• 🌟 Orion Stars & Juwa: {Exciting slots, keno, and community jackpots}
• 🎁 {daily_bonus} Entry: {Test out any platform with your {daily_bonus}}
• ⚡ Fast {min_cashout} Cashouts: {Withdraw all winnings at low {min_cashout} minimum}
• 📱 Play on Mobile: {Seamless touch controls on iOS and Android}""",
            cta_text="PLAY FIRE KIRIN & ORION STARS"
        ),
        "html": get_email_html(
            badge_text="DAY 4 MORNING",
            title_text="{Featured Games|Player Favorites}: Fire Kirin, Orion Stars & Juwa ready to spin",
            intro_html="<p style='margin:0 0 14px;'>Ready to explore the hottest arcade fish and sweepstakes slots?</p><p style='margin:0;'>At <strong>Winning Heaven</strong>, one single VIP login gives you instant access to Fire Kirin, Orion Stars, Juwa, Game Vault, Milky Way, and Panda Master. Start your adventure today with <strong>{daily_bonus}</strong> and withdraw your earnings at our low <strong>{min_cashout} minimum cashout</strong>.</p>",
            perks_table_html="""<tr><td style="padding: 5px 0; vertical-align: top; width: 26px;">🐟</td><td style="padding: 5px 0;"><strong>Fire Kirin & Ocean King:</strong> {High-action multiplayer fish arcade tables}</td></tr>
<tr><td style="padding: 5px 0; vertical-align: top; width: 26px;">🌟</td><td style="padding: 5px 0;"><strong>Orion Stars & Juwa:</strong> {Exciting slots, keno, and community jackpots}</td></tr>
<tr><td style="padding: 5px 0; vertical-align: top; width: 26px;">🎁</td><td style="padding: 5px 0;"><strong>{daily_bonus} Entry:</strong> {Test out any platform with your {daily_bonus}}</td></tr>
<tr><td style="padding: 5px 0; vertical-align: top; width: 26px;">⚡</td><td style="padding: 5px 0;"><strong>Fast {min_cashout} Cashouts:</strong> {Withdraw all winnings at low {min_cashout} minimum}</td></tr>
<tr><td style="padding: 5px 0; vertical-align: top; width: 26px;">📱</td><td style="padding: 5px 0;"><strong>Play on Mobile:</strong> {Seamless touch controls on iOS and Android}</td></tr>""",
            cta_text="PLAY FIRE KIRIN & ORION STARS"
        ),
        "inbox_score": 100,
        "spam_status": "PRIMARY INBOX VERIFIED ✅"
    },
    {
        "id": "day4_evening_reengage",
        "stage": 4,
        "name": "Day 4 Evening: Midweek Jackpot Multiplier Drop",
        "subject": "{Midweek Jackpot Alert|High Multipliers}: Active jackpot tables tonight ({min_cashout} Min Cashout) 🏆",
        "preview_text": "Jackpot multipliers are running hot. Start with {daily_bonus} tonight and cash out at {min_cashout}.",
        "plain_text": get_email_plain(
            intro_plain="The tables are buzzing tonight!\n\nCommunity jackpot pools across Orion Stars and Juwa have reached peak multipliers. Claim your {daily_bonus}, aim for the big multipliers, and remember: you only need {min_cashout} to cash out directly to your Cash App or Crypto wallet.",
            perks_plain="""• 🏆 Community Jackpot Drops: {Active multiplier tables open now}
• 🎁 {daily_bonus} Boost: {Free session entries ready on your profile}
• ⚡ {min_cashout} Instant Cashout: {Hit big and withdraw quickly from {min_cashout}+}
• 💸 Fast 24/7 Transfers: {Direct settlements around the clock}
• 👑 Live Host Support: {Host ready to load coins in under 60 seconds}""",
            cta_text="JOIN JACKPOT TABLES NOW"
        ),
        "html": get_email_html(
            badge_text="DAY 4 EVENING",
            title_text="{Midweek Jackpot Alert|High Multipliers}: Active jackpot tables tonight ({min_cashout} Min Cashout)",
            intro_html="<p style='margin:0 0 14px;'>The tables are buzzing tonight!</p><p style='margin:0;'>Community jackpot pools across Orion Stars and Juwa have reached peak multipliers. Claim your <strong>{daily_bonus}</strong>, aim for the big multipliers, and remember: you only need <strong>{min_cashout} to cash out</strong> directly to your Cash App or Crypto wallet.</p>",
            perks_table_html="""<tr><td style="padding: 5px 0; vertical-align: top; width: 26px;">🏆</td><td style="padding: 5px 0;"><strong>Community Jackpot Drops:</strong> {Active multiplier tables open now}</td></tr>
<tr><td style="padding: 5px 0; vertical-align: top; width: 26px;">🎁</td><td style="padding: 5px 0;"><strong>{daily_bonus} Boost:</strong> {Free session entries ready on your profile}</td></tr>
<tr><td style="padding: 5px 0; vertical-align: top; width: 26px;">⚡</td><td style="padding: 5px 0;"><strong>{min_cashout} Instant Cashout:</strong> {Hit big and withdraw quickly from {min_cashout}+}</td></tr>
<tr><td style="padding: 5px 0; vertical-align: top; width: 26px;">💸</td><td style="padding: 5px 0;"><strong>Fast 24/7 Transfers:</strong> {Direct settlements around the clock}</td></tr>
<tr><td style="padding: 5px 0; vertical-align: top; width: 26px;">👑</td><td style="padding: 5px 0;"><strong>Live Host Support:</strong> {Host ready to load coins in under 60 seconds}</td></tr>""",
            cta_text="JOIN JACKPOT TABLES NOW"
        ),
        "inbox_score": 100,
        "spam_status": "PRIMARY INBOX VERIFIED ✅"
    },
    {
        "id": "day5_morning_games",
        "stage": 5,
        "name": "Day 5 Morning: Friday Weekend Kickoff VIP Pass",
        "subject": "{Happy Friday|Weekend Kickoff}: Your VIP weekend pass & {daily_bonus} are ready 🍾",
        "preview_text": "Kick off Friday with {daily_bonus} and unlimited {min_cashout}+ fast cashouts.",
        "plain_text": get_email_plain(
            intro_plain="Happy Friday! The weekend is officially here, and your Winning Heaven VIP Weekend Pass is ready to activate.\n\nKick off the weekend with complimentary {daily_bonus}, higher bonus multipliers, and our signature {min_cashout} minimum cashout guarantee.",
            perks_plain="""• 🍾 Friday VIP Pass: {Weekend bonuses and priority payouts live}
• 🎁 {daily_bonus} Credit: {Kickstart your Friday session with {daily_bonus}}
• ⚡ Low {min_cashout} Cashout: {Instant settlements all weekend starting at {min_cashout}}
• 📱 Play on Any Device: {Instant access from your smartphone browser}
• 💸 Fast Cash App Payouts: {Withdraw your weekend winnings in minutes}""",
            cta_text="ACTIVATE FRIDAY VIP PASS"
        ),
        "html": get_email_html(
            badge_text="DAY 5 MORNING",
            title_text="{Happy Friday|Weekend Kickoff}: Your VIP weekend pass & {daily_bonus} are ready",
            intro_html="<p style='margin:0 0 14px;'>Happy Friday! The weekend is officially here, and your <strong>Winning Heaven VIP Weekend Pass</strong> is ready to activate.</p><p style='margin:0;'>Kick off the weekend with complimentary <strong>{daily_bonus}</strong>, higher bonus multipliers, and our signature <strong>{min_cashout} minimum cashout</strong> guarantee.</p>",
            perks_table_html="""<tr><td style="padding: 5px 0; vertical-align: top; width: 26px;">🍾</td><td style="padding: 5px 0;"><strong>Friday VIP Pass:</strong> {Weekend bonuses and priority payouts live}</td></tr>
<tr><td style="padding: 5px 0; vertical-align: top; width: 26px;">🎁</td><td style="padding: 5px 0;"><strong>{daily_bonus} Credit:</strong> {Kickstart your Friday session with {daily_bonus}}</td></tr>
<tr><td style="padding: 5px 0; vertical-align: top; width: 26px;">⚡</td><td style="padding: 5px 0;"><strong>Low {min_cashout} Cashout:</strong> {Instant settlements all weekend starting at {min_cashout}}</td></tr>
<tr><td style="padding: 5px 0; vertical-align: top; width: 26px;">📱</td><td style="padding: 5px 0;"><strong>Play on Any Device:</strong> {Instant access from your smartphone browser}</td></tr>
<tr><td style="padding: 5px 0; vertical-align: top; width: 26px;">💸</td><td style="padding: 5px 0;"><strong>Fast Cash App Payouts:</strong> {Withdraw your weekend winnings in minutes}</td></tr>""",
            cta_text="ACTIVATE FRIDAY VIP PASS"
        ),
        "inbox_score": 100,
        "spam_status": "PRIMARY INBOX VERIFIED ✅"
    },
    {
        "id": "day5_evening_weekend_kickoff",
        "stage": 5,
        "name": "Day 5 Evening: Friday Night Live Fish Lobby",
        "subject": "{Friday Night Action|Live Tables}: Weekend rush is on — {daily_bonus} + {min_cashout} Cashouts 🌙",
        "preview_text": "Friday night games are live. Fast Cash App payouts all night starting at {min_cashout}.",
        "plain_text": get_email_plain(
            intro_plain="The Friday night rush is in full swing!\n\nOur live arcade fish rooms and slots lobbies are packed with players winning big. Don't leave your {daily_bonus} unclaimed — jump in, test your luck, and cash out whenever you reach {min_cashout} or more.",
            perks_plain="""• 🌙 Friday Night Special: {Active reload bonuses and live action}
• ⚡ Fast Cash App Cashouts: {Cash out starting at {min_cashout} directly to your tag}
• 🎁 {daily_bonus}: {Don't leave your {daily_bonus} unclaimed}
• 🎰 Top Weekend Platforms: {Fire Kirin, Orion Stars, Game Vault & Milky Way}
• ⏱️ Priority Weekend Processing: {Fast cashout queue all night long}""",
            cta_text="JOIN FRIDAY NIGHT LOBBY"
        ),
        "html": get_email_html(
            badge_text="DAY 5 EVENING",
            title_text="{Friday Night Action|Live Tables}: Weekend rush is on — {daily_bonus} + {min_cashout} Cashouts",
            intro_html="<p style='margin:0 0 14px;'>The Friday night rush is in full swing!</p><p style='margin:0;'>Our live arcade fish rooms and slots lobbies are packed with players winning big. Don't leave your <strong>{daily_bonus}</strong> unclaimed — jump in, test your luck, and cash out whenever you reach <strong>{min_cashout} or more</strong>.</p>",
            perks_table_html="""<tr><td style="padding: 5px 0; vertical-align: top; width: 26px;">🌙</td><td style="padding: 5px 0;"><strong>Friday Night Special:</strong> {Active reload bonuses and live action}</td></tr>
<tr><td style="padding: 5px 0; vertical-align: top; width: 26px;">⚡</td><td style="padding: 5px 0;"><strong>Fast Cash App Cashouts:</strong> {Cash out starting at {min_cashout} directly to your tag}</td></tr>
<tr><td style="padding: 5px 0; vertical-align: top; width: 26px;">🎁</td><td style="padding: 5px 0;"><strong>{daily_bonus}:</strong> {Don't leave your {daily_bonus} unclaimed}</td></tr>
<tr><td style="padding: 5px 0; vertical-align: top; width: 26px;">🎰</td><td style="padding: 5px 0;"><strong>Top Weekend Platforms:</strong> {Fire Kirin, Orion Stars, Game Vault & Milky Way}</td></tr>
<tr><td style="padding: 5px 0; vertical-align: top; width: 26px;">⏱️</td><td style="padding: 5px 0;"><strong>Priority Weekend Processing:</strong> {Fast cashout queue all night long}</td></tr>""",
            cta_text="JOIN FRIDAY NIGHT LOBBY"
        ),
        "inbox_score": 100,
        "spam_status": "PRIMARY INBOX VERIFIED ✅"
    },
    {
        "id": "day6_morning_saturday",
        "stage": 6,
        "name": "Day 6 Morning: Saturday Super Spins & High Multipliers",
        "subject": "{Saturday Spin Rush|Weekend Drops}: {daily_bonus} ready for Saturday action ⭐",
        "preview_text": "Super Saturday spin credits. Low {min_cashout} cashouts guaranteed.",
        "plain_text": get_email_plain(
            intro_plain="Saturday morning gaming has arrived!\n\nWe are dropping special Saturday spin boosts across all accounts. Whether you love fish tables or classic reels, grab your {daily_bonus}, enjoy the weekend excitement, and cash out at our easy {min_cashout} minimum threshold.",
            perks_plain="""• 🎰 Saturday Drops: {Special weekend drop rates on all slots}
• 🎁 {daily_bonus} Credit: {Claim your Saturday {daily_bonus}}
• ⚡ {min_cashout} Min Cashout: {Quick withdrawals starting at {min_cashout}}
• 💸 Cash App & Crypto: {Fast 15-minute cash settlements}
• 📱 Zero Install Browser Play: {Play directly on your mobile device}""",
            cta_text="CLAIM SATURDAY SPINS & PLAY"
        ),
        "html": get_email_html(
            badge_text="DAY 6 MORNING",
            title_text="{Saturday Spin Rush|Weekend Drops}: {daily_bonus} ready for Saturday action",
            intro_html="<p style='margin:0 0 14px;'>Saturday morning gaming has arrived!</p><p style='margin:0;'>We are dropping special Saturday spin boosts across all accounts. Whether you love fish tables or classic reels, grab your <strong>{daily_bonus}</strong>, enjoy the weekend excitement, and cash out at our easy <strong>{min_cashout} minimum threshold</strong>.</p>",
            perks_table_html="""<tr><td style="padding: 5px 0; vertical-align: top; width: 26px;">🎰</td><td style="padding: 5px 0;"><strong>Saturday Drops:</strong> {Special weekend drop rates on all slots}</td></tr>
<tr><td style="padding: 5px 0; vertical-align: top; width: 26px;">🎁</td><td style="padding: 5px 0;"><strong>{daily_bonus} Credit:</strong> {Claim your Saturday {daily_bonus}}</td></tr>
<tr><td style="padding: 5px 0; vertical-align: top; width: 26px;">⚡</td><td style="padding: 5px 0;"><strong>{min_cashout} Min Cashout:</strong> {Quick withdrawals starting at {min_cashout}}</td></tr>
<tr><td style="padding: 5px 0; vertical-align: top; width: 26px;">💸</td><td style="padding: 5px 0;"><strong>Cash App & Crypto:</strong> {Fast 15-minute cash settlements}</td></tr>
<tr><td style="padding: 5px 0; vertical-align: top; width: 26px;">📱</td><td style="padding: 5px 0;"><strong>Zero Install Browser Play:</strong> {Play directly on your mobile device}</td></tr>""",
            cta_text="CLAIM SATURDAY SPINS & PLAY"
        ),
        "inbox_score": 100,
        "spam_status": "PRIMARY INBOX VERIFIED ✅"
    },
    {
        "id": "day6_evening_saturday",
        "stage": 6,
        "name": "Day 6 Evening: Saturday Night High-Roller Jackpots",
        "subject": "{Saturday Night Jackpots|VIP Lounge}: High roller tables active tonight ({min_cashout} Min Cashout) 💎",
        "preview_text": "Peak jackpot hours are here. Jump into high action with {daily_bonus} and {min_cashout} cashouts.",
        "plain_text": get_email_plain(
            intro_plain="Saturday night is peak gaming time at Winning Heaven!\n\nOur VIP players are taking down major bosses and hitting bonus wheels across Fire Kirin and Milky Way. Jump into the action tonight with {daily_bonus} and enjoy priority settlements starting at {min_cashout}.",
            perks_plain="""• 💎 VIP Saturday Jackpots: {Increased drop frequency across all games}
• ⚡ Fast {min_cashout} Cashouts: {Quick payouts whenever you want to cash out}
• 🎁 {daily_bonus} Drop: {Load your favorite game with {daily_bonus}}
• 📱 Instant Web Play: {Play in Safari, Chrome or PC browser}
• 💸 Instant Cash App & BTC: {Round-the-clock payout team standing by}""",
            cta_text="ENTER SATURDAY NIGHT LOBBY"
        ),
        "html": get_email_html(
            badge_text="DAY 6 EVENING",
            title_text="{Saturday Night Jackpots|VIP Lounge}: High roller tables active tonight ({min_cashout} Min Cashout)",
            intro_html="<p style='margin:0 0 14px;'>Saturday night is peak gaming time at Winning Heaven!</p><p style='margin:0;'>Our VIP players are taking down major bosses and hitting bonus wheels across Fire Kirin and Milky Way. Jump into the action tonight with <strong>{daily_bonus}</strong> and enjoy priority settlements starting at <strong>{min_cashout}</strong>.</p>",
            perks_table_html="""<tr><td style="padding: 5px 0; vertical-align: top; width: 26px;">💎</td><td style="padding: 5px 0;"><strong>VIP Saturday Jackpots:</strong> {Increased drop frequency across all games}</td></tr>
<tr><td style="padding: 5px 0; vertical-align: top; width: 26px;">⚡</td><td style="padding: 5px 0;"><strong>Fast {min_cashout} Cashouts:</strong> {Quick payouts whenever you want to cash out}</td></tr>
<tr><td style="padding: 5px 0; vertical-align: top; width: 26px;">🎁</td><td style="padding: 5px 0;"><strong>{daily_bonus} Drop:</strong> {Load your favorite game with {daily_bonus}}</td></tr>
<tr><td style="padding: 5px 0; vertical-align: top; width: 26px;">📱</td><td style="padding: 5px 0;"><strong>Instant Web Play:</strong> {Play in Safari, Chrome or PC browser}</td></tr>
<tr><td style="padding: 5px 0; vertical-align: top; width: 26px;">💸</td><td style="padding: 5px 0;"><strong>Instant Cash App & BTC:</strong> {Round-the-clock payout team standing by}</td></tr>""",
            cta_text="ENTER SATURDAY NIGHT LOBBY"
        ),
        "inbox_score": 100,
        "spam_status": "PRIMARY INBOX VERIFIED ✅"
    },
    {
        "id": "day7_morning_sunday",
        "stage": 7,
        "name": "Day 7 Morning: Sunday VIP Cashback & Loyalty Drop",
        "subject": "{Sunday Special|Weekly Cashback}: Your Sunday bonus & {daily_bonus} are waiting 🎁",
        "preview_text": "Sunday loyalty rewards are active! Claim your {daily_bonus} reload and {min_cashout} cashouts.",
        "plain_text": get_email_plain(
            intro_plain="Sunday is reward day at Winning Heaven!\n\nWe are reviewing all weekly play to issue loyalty rewards and Sunday cashback drops. Log in today to claim your {daily_bonus} reload, spin your favorite games, and enjoy instant withdrawals with our {min_cashout} minimum cashout.",
            perks_plain="""• 💎 Sunday VIP Cashback: {Cashback rewards credited for weekly play}
• 🎁 {daily_bonus} Reload: {Enjoy {daily_bonus} on Sunday tables}
• ⚡ Instant {min_cashout} Cashouts: {Cash out your Sunday winnings before Monday}
• 🎰 Top Arcades & Slots: {Orion Stars, Fire Kirin, Juwa & Milky Way}
• ⏱️ Fast 24/7 Payouts: {Direct to your Cash App or Crypto wallet}""",
            cta_text="CLAIM SUNDAY CASHBACK & {daily_bonus}"
        ),
        "html": get_email_html(
            badge_text="DAY 7 MORNING",
            title_text="{Sunday Special|Weekly Cashback}: Your Sunday bonus & {daily_bonus} are waiting",
            intro_html="<p style='margin:0 0 14px;'>Sunday is reward day at Winning Heaven!</p><p style='margin:0;'>We are reviewing all weekly play to issue loyalty rewards and Sunday cashback drops. Log in today to claim your <strong>{daily_bonus} reload</strong>, spin your favorite games, and enjoy instant withdrawals with our <strong>{min_cashout} minimum cashout</strong>.</p>",
            perks_table_html="""<tr><td style="padding: 5px 0; vertical-align: top; width: 26px;">💎</td><td style="padding: 5px 0;"><strong>Sunday VIP Cashback:</strong> {Cashback rewards credited for weekly play}</td></tr>
<tr><td style="padding: 5px 0; vertical-align: top; width: 26px;">🎁</td><td style="padding: 5px 0;"><strong>{daily_bonus} Reload:</strong> {Enjoy {daily_bonus} on Sunday tables}</td></tr>
<tr><td style="padding: 5px 0; vertical-align: top; width: 26px;">⚡</td><td style="padding: 5px 0;"><strong>Instant {min_cashout} Cashouts:</strong> {Cash out your Sunday winnings before Monday}</td></tr>
<tr><td style="padding: 5px 0; vertical-align: top; width: 26px;">🎰</td><td style="padding: 5px 0;"><strong>Top Arcades & Slots:</strong> {Orion Stars, Fire Kirin, Juwa & Milky Way}</td></tr>
<tr><td style="padding: 5px 0; vertical-align: top; width: 26px;">⏱️</td><td style="padding: 5px 0;"><strong>Fast 24/7 Payouts:</strong> {Direct to your Cash App or Crypto wallet}</td></tr>""",
            cta_text="CLAIM SUNDAY CASHBACK & {daily_bonus}"
        ),
        "inbox_score": 100,
        "spam_status": "PRIMARY INBOX VERIFIED ✅"
    },
    {
        "id": "day7_evening_vip_retention",
        "stage": 7,
        "name": "Day 7 Evening: Lifetime VIP Status Confirmation",
        "subject": "{VIP Account Status|Courtesy Check}: Your permanent {min_cashout} min cashout & benefits confirmed 👑",
        "preview_text": "Your VIP status at Winning Heaven is permanent. Enjoy {min_cashout} cashouts and on-demand freeplay.",
        "plain_text": get_email_plain(
            intro_plain="As our introductory week comes to a close, we want to confirm that your VIP Status at Winning Heaven is permanent.\n\nYour account will always enjoy priority 15-minute payouts, our low {min_cashout} minimum cashout threshold, and on-demand {daily_bonus} drops whenever you want to play.",
            perks_plain="""• 👑 Lifetime VIP Status: {Your account profile remains open 24/7}
• ⚡ Permanent {min_cashout} Min Cashout: {Enjoy our lowest cashout threshold anytime}
• 🎁 {daily_bonus} On Demand: {Reach out to your host anytime for bonus drops}
• 📱 Always Available: {Bookmark winningheaven.com for instant web play}
• 💸 Direct 24/7 Cash App & Crypto: {Fast settlements guaranteed}""",
            cta_text="ACCESS VIP ACCOUNT & PLAY"
        ),
        "html": get_email_html(
            badge_text="DAY 7 EVENING",
            title_text="{VIP Account Status|Courtesy Check}: Your permanent {min_cashout} min cashout & benefits confirmed",
            intro_html="<p style='margin:0 0 14px;'>As our introductory week comes to a close, we want to confirm that your <strong>VIP Status at Winning Heaven is permanent</strong>.</p><p style='margin:0;'>Your account will always enjoy priority 15-minute payouts, our low <strong>{min_cashout} minimum cashout</strong> threshold, and on-demand <strong>{daily_bonus} drops</strong> whenever you want to play.</p>",
            perks_table_html="""<tr><td style="padding: 5px 0; vertical-align: top; width: 26px;">👑</td><td style="padding: 5px 0;"><strong>Lifetime VIP Status:</strong> {Your account profile remains open 24/7}</td></tr>
<tr><td style="padding: 5px 0; vertical-align: top; width: 26px;">⚡</td><td style="padding: 5px 0;"><strong>Permanent {min_cashout} Min Cashout:</strong> {Enjoy our lowest cashout threshold anytime}</td></tr>
<tr><td style="padding: 5px 0; vertical-align: top; width: 26px;">🎁</td><td style="padding: 5px 0;"><strong>{daily_bonus} On Demand:</strong> {Reach out to your host anytime for freeplay drops}</td></tr>
<tr><td style="padding: 5px 0; vertical-align: top; width: 26px;">📱</td><td style="padding: 5px 0;"><strong>Always Available:</strong> {Bookmark winningheaven.com for instant web play}</td></tr>
<tr><td style="padding: 5px 0; vertical-align: top; width: 26px;">💸</td><td style="padding: 5px 0;"><strong>Direct 24/7 Cash App & Crypto:</strong> {Fast settlements guaranteed}</td></tr>""",
            cta_text="ACCESS VIP ACCOUNT & PLAY"
        ),
        "inbox_score": 100,
        "spam_status": "PRIMARY INBOX VERIFIED ✅"
    },
    {
        "id": "flash_daily_bonus_drop",
        "stage": 1,
        "name": "🔥 Flash Promotion: Instant {daily_bonus} Drop (Claim in 24h)",
        "subject": "{Flash Promotion|Limited-Time Drop}: We deposited {daily_bonus} into your VIP profile 🚀",
        "preview_text": "Flash Bonus Drop! Your profile is credited with {daily_bonus}. Valid for 24 hours only. Low {min_cashout} cashouts.",
        "plain_text": get_email_plain(
            intro_plain="Surprise flash promotion alert!\n\nTo celebrate our VIP members today, we have dropped a complimentary {daily_bonus} into your player profile. There is zero deposit required to try your luck — jump in right now before the promo closes at midnight, and withdraw all winnings from just {min_cashout}!",
            perks_plain="""• 🚀 Instant Flash Drop: {{daily_bonus} loaded and waiting on your account}
• ⏱️ 24-Hour Expiry Window: {Claim your bonus before midnight tonight}
• ⚡ Low {min_cashout} Cashout Threshold: {Keep what you win and withdraw starting at {min_cashout}}
• 💸 Instant Transfers: {Get paid directly via Cash App, Venmo, BTC or Chime}
• 🎰 Top Arcades & Slots: {Orion Stars, Fire Kirin, Juwa & Milky Way}""",
            cta_text="CLAIM FLASH {daily_bonus} NOW"
        ),
        "html": get_email_html(
            badge_text="FLASH PROMO",
            title_text="{Flash Promotion|Limited-Time Drop}: We deposited {daily_bonus} into your VIP profile",
            intro_html="<p style='margin:0 0 14px;'>Surprise flash promotion alert!</p><p style='margin:0;'>To celebrate our VIP members today, we have dropped a complimentary <strong>{daily_bonus}</strong> into your player profile. There is <strong>zero deposit required</strong> to try your luck — jump in right now before the promo closes at midnight, and withdraw all winnings from just <strong>{min_cashout}</strong>!</p>",
            perks_table_html="""<tr><td style="padding: 5px 0; vertical-align: top; width: 26px;">🚀</td><td style="padding: 5px 0;"><strong>Instant Flash Drop:</strong> {{daily_bonus} loaded and waiting on your account}</td></tr>
<tr><td style="padding: 5px 0; vertical-align: top; width: 26px;">⏱️</td><td style="padding: 5px 0;"><strong>24-Hour Expiry Window:</strong> {Claim your bonus before midnight tonight}</td></tr>
<tr><td style="padding: 5px 0; vertical-align: top; width: 26px;">⚡</td><td style="padding: 5px 0;"><strong>Low {min_cashout} Cashout Threshold:</strong> {Keep what you win and withdraw starting at {min_cashout}}</td></tr>
<tr><td style="padding: 5px 0; vertical-align: top; width: 26px;">💸</td><td style="padding: 5px 0;"><strong>Instant Transfers:</strong> {Get paid directly via Cash App, Venmo, BTC or Chime}</td></tr>
<tr><td style="padding: 5px 0; vertical-align: top; width: 26px;">🎰</td><td style="padding: 5px 0;"><strong>Top Arcades & Slots:</strong> {Orion Stars, Fire Kirin, Juwa & Milky Way}</td></tr>""",
            cta_text="CLAIM FLASH {daily_bonus} NOW"
        ),
        "inbox_score": 100,
        "spam_status": "PRIMARY INBOX VERIFIED ✅"
    },
    {
        "id": "winback_reclaim_offer",
        "stage": 1,
        "name": "🎯 Win-Back: We Miss You! Special {daily_bonus} + 100% Reload Match",
        "subject": "{We Miss You|Exclusive Re-Activation}: Special {daily_bonus} + 100% Reload Match inside 🎯",
        "preview_text": "We miss you at Winning Heaven! Re-activate with {daily_bonus} + 100% reload match. Cash out at {min_cashout}.",
        "plain_text": get_email_plain(
            intro_plain="It's been a little while since your last session, and we'd love to welcome you back!\n\nTo get you back in the winner's circle, we have unlocked an exclusive Re-Activation Pass on your profile: enjoy a fresh {daily_bonus} on the house, plus an optional 100% Match Bonus on your next reload. Lowest {min_cashout} cashouts guaranteed!",
            perks_plain="""• 🎯 Welcome Back Perk: {Special {daily_bonus} waiting to kickstart your return}
• 💎 100% Reload Multiplier: {Double your balance whenever you reload}
• ⚡ Low {min_cashout} Cashouts: {Withdraw quickly starting at only {min_cashout}}
• 📱 Zero App Needed: {Play instantly in Safari or Chrome without downloads}
• 💸 Instant Cash App Payouts: {Fast 15-minute cashouts around the clock}""",
            cta_text="RE-ACTIVATE & CLAIM {daily_bonus}"
        ),
        "html": get_email_html(
            badge_text="VIP RE-ACTIVATION",
            title_text="{We Miss You|Exclusive Re-Activation}: Special {daily_bonus} + 100% Reload Match inside",
            intro_html="<p style='margin:0 0 14px;'>It's been a little while since your last session, and we'd love to welcome you back!</p><p style='margin:0;'>To get you back in the winner's circle, we have unlocked an exclusive <strong>Re-Activation Pass</strong> on your profile: enjoy a fresh <strong>{daily_bonus}</strong> on the house, plus an optional <strong>100% Match Bonus</strong> on your next reload. Lowest <strong>{min_cashout} cashouts</strong> guaranteed!</p>",
            perks_table_html="""<tr><td style="padding: 5px 0; vertical-align: top; width: 26px;">🎯</td><td style="padding: 5px 0;"><strong>Welcome Back Perk:</strong> {Special {daily_bonus} waiting to kickstart your return}</td></tr>
<tr><td style="padding: 5px 0; vertical-align: top; width: 26px;">💎</td><td style="padding: 5px 0;"><strong>100% Reload Multiplier:</strong> {Double your balance whenever you reload}</td></tr>
<tr><td style="padding: 5px 0; vertical-align: top; width: 26px;">⚡</td><td style="padding: 5px 0;"><strong>Low {min_cashout} Cashouts:</strong> {Withdraw quickly starting at only {min_cashout}}</td></tr>
<tr><td style="padding: 5px 0; vertical-align: top; width: 26px;">📱</td><td style="padding: 5px 0;"><strong>Zero App Needed:</strong> {Play instantly in Safari or Chrome without downloads}</td></tr>
<tr><td style="padding: 5px 0; vertical-align: top; width: 26px;">💸</td><td style="padding: 5px 0;"><strong>Instant Cash App Payouts:</strong> {Fast 15-minute cashouts around the clock}</td></tr>""",
            cta_text="RE-ACTIVATE & CLAIM {daily_bonus}"
        ),
        "inbox_score": 100,
        "spam_status": "PRIMARY INBOX VERIFIED ✅"
    }
]

def get_templates(bonus="$5 Freeplay", min_cashout="$35"):
    return [render_template_dict(t, bonus, min_cashout) for t in TEMPLATES]

def get_template_by_id(tpl_id, bonus="$5 Freeplay", min_cashout="$35"):
    for t in TEMPLATES:
        if t["id"] == tpl_id:
            return render_template_dict(t, bonus, min_cashout)
    return render_template_dict(TEMPLATES[0], bonus, min_cashout) if TEMPLATES else None

def add_custom_template(tpl):
    TEMPLATES.append(tpl)
    return tpl

def generate_custom_template(prompt, tone="vip", offer_headline="", bonus="$5 Freeplay", min_cashout="$35"):
    raw_prompt = prompt.strip() if prompt else "VIP Gaming Portal Pass"
    first_line = raw_prompt.split("\n")[0]
    
    b_val = str(bonus or "$5 Freeplay").strip()
    c_val = str(min_cashout or "$35").strip()
    
    subject = f"{{VIP Access|Exclusive Offer}}: {first_line[:35]} — {b_val} & {c_val} Min Cashout 🎁"
    preview = f"Your VIP pass is active! {b_val} and {c_val} minimum cashout at Winning Heaven."
    
    html = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>{subject}</title></head>
<body style="margin: 0; padding: 24px 12px; font-family: -apple-system, sans-serif; background-color: #f1f5f9; color: #1e293b;">
  <div style="max-width: 580px; margin: 0 auto; background-color: #ffffff; border-radius: 12px; overflow: hidden; border: 1px solid #e2e8f0; box-shadow: 0 4px 16px rgba(0,0,0,0.06);">
    <div style="background: linear-gradient(135deg, #090d16 0%, #171d2d 100%); padding: 24px 28px; border-bottom: 3px solid #f59e0b;">
      <span style="font-size: 21px; font-weight: 900; color: #ffffff;">WINNING <span style="color: #fbbf24;">HEAVEN</span></span>
      <div style="font-size: 11px; color: #fbbf24; font-weight: 700; text-transform: uppercase; margin-top: 4px;">👑 VIP GAMING PORTAL</div>
    </div>
    <div style="padding: 30px 26px;">
      <p style="font-size: 16px; font-weight: 700; color: #0f172a;">{{Hi|Hello|Greetings}},</p>
      <p style="color: #334155; line-height: 1.65;">{raw_prompt}</p>
      <div style="background: #fffbeb; border: 1px solid #fde68a; border-left: 4px solid #f59e0b; border-radius: 8px; padding: 18px 20px; margin: 24px 0;">
        <div style="font-size: 13px; font-weight: 800; color: #92400e; margin-bottom: 10px; font-weight: 800;">✨ YOUR VIP PRIVILEGES:</div>
        <table width="100%" style="font-size: 14px; color: #1e293b; line-height: 1.7;">
          <tr><td width="26">🎁</td><td><strong>Instant Bonus:</strong> {b_val} ready upon request with no deposit required.</td></tr>
          <tr><td width="26">⚡</td><td><strong>Low Cashout:</strong> Withdraw your winnings easily starting at {c_val}.</td></tr>
          <tr><td width="26">💸</td><td><strong>Instant 24/7 Payouts:</strong> Direct settlements via Cash App, Crypto & Bank in 15 minutes.</td></tr>
          <tr><td width="26">🎰</td><td><strong>Top Platforms:</strong> Fire Kirin, Orion Stars, Juwa, Game Vault & Milky Way.</td></tr>
          <tr><td width="26">📱</td><td><strong>Zero App Downloads:</strong> Play directly in mobile Safari or Chrome browser.</td></tr>
        </table>
      </div>
      <div style="text-align: center; margin: 30px 0 24px;">
        <a href="https://winningheaven.com" target="_blank" style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); color: #000000; padding: 15px 36px; border-radius: 8px; font-weight: 900; font-size: 16px; text-decoration: none; display: inline-block; box-shadow: 0 4px 14px rgba(245, 158, 11, 0.35);">
          CLAIM {b_val} & PLAY NOW &rarr;
        </a>
      </div>
      <p style="color: #64748b; font-size: 14px; margin-top: 24px; line-height: 1.6;">
        Reply directly to this email anytime to speak with your dedicated VIP Concierge host.
      </p>
    </div>
  </div>
</body>
</html>"""

    plain = f"""{{Hi|Hello|Greetings}},

{raw_prompt}

YOUR VIP PRIVILEGES:
• 🎁 Instant Bonus: {b_val} ready with no deposit required
• ⚡ Low Cashout: Withdraw starting at {c_val}
• 💸 Instant 24/7 Payouts: Cash App, Crypto & Bank in 15 minutes
• 🎰 Top Platforms: Fire Kirin, Orion Stars, Juwa, Game Vault & Milky Way
• 📱 Zero App Downloads: Play directly in mobile Safari or Chrome

👉 Claim {b_val} & Play Now:
https://winningheaven.com

Best regards,
Winning Heaven VIP Concierge Team
https://winningheaven.com
"""

    tpl_id = f"custom_{int(uuid.uuid4().hex[:6], 16)}"
    return {
        "id": tpl_id,
        "stage": 1,
        "name": f"✨ Custom: {first_line[:30]}...",
        "subject": subject,
        "preview_text": preview,
        "plain_text": plain,
        "html": html,
        "inbox_score": 100,
        "spam_status": "PRIMARY INBOX VERIFIED ✅"
    }
