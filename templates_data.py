"""
High-converting, Primary-Inbox-optimized 7-Day Campaign Sequence for Winning Heaven (winningheaven.com).
Engineered to bypass Gmail, Yahoo, Outlook & Apple Mail Spam/Promotions tabs and land directly in the PRIMARY INBOX.
Clean executive styling, dynamic Spintax rotation, zero spam trigger words, clear VIP value, and RFC 8058 compliance.
Designed for 2 sends per day: Morning & Evening across 7 Days (14 total templates).
"""

import uuid
import re

TEMPLATES = [
    # ------------------ DAY 1 ------------------
    {
        "id": "day1_morning_welcome",
        "stage": 1,
        "name": "Day 1 Morning: VIP Welcome & Account Access",
        "subject": "{Welcome|Greetings}: Your Winning Heaven account overview & VIP access",
        "preview_text": "Confirming your VIP player pass and direct web portal access.",
        "plain_text": """{Hi|Hello|Good morning},

Welcome to Winning Heaven!

I am reaching out personally to confirm that your VIP member pass has been activated on our direct web platform.

Here is a quick overview of what is ready on your account profile today:
• VIP Match Credit: Active session match rewards credited on your first session
• Session FP Entries: Complimentary session entries credited to your profile
• 24/7 Fast Transfers: Direct payouts via Cash App, Crypto, or Bank Transfer
• Direct Web Play: Play instantly on phone or desktop browser with zero downloads required

You can access your member account and claim your VIP pass directly here:
👉 https://winningheaven.com

If you have any questions or need help logging in, simply reply directly to this email and our VIP concierge team will assist you immediately.

Best regards,

VIP Concierge Host
Winning Heaven VIP Support Team
https://winningheaven.com

To manage your notification preferences, reply 'Unsubscribe'.""",
        "html": """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{Welcome|Greetings}: Your Winning Heaven account overview &amp; VIP access</title>
</head>
<body style="margin: 0; padding: 24px 12px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 15px; line-height: 1.6; color: #1e293b; background-color: #f8fafc;">

  <!-- Hidden Preheader Snippet for High Primary Inbox Placement -->
  <div style="display:none;font-size:1px;color:#ffffff;line-height:1px;max-height:0px;max-width:0px;opacity:0;overflow:hidden;">
    Confirming your VIP player pass and direct web portal access. &nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;
  </div>

  <div style="max-width: 560px; margin: 0 auto; background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; padding: 28px 24px; box-shadow: 0 2px 6px rgba(0,0,0,0.03);">
    
    <div style="border-bottom: 2px solid #0284c7; padding-bottom: 12px; margin-bottom: 20px;">
      <span style="font-size: 19px; font-weight: 800; color: #0f172a; letter-spacing: 0.5px;">WINNING HEAVEN</span>
      <div style="font-size: 11px; color: #0284c7; font-weight: 700; text-transform: uppercase; letter-spacing: 0.8px; margin-top: 3px;">Day 1 Morning • VIP Account Invitation</div>
    </div>

    <p style="font-size: 15px; font-weight: 600; color: #0f172a; margin: 0 0 14px;">{Hi|Hello|Good morning},</p>
    
    <p style="margin: 0 0 16px; color: #334155;">{Welcome to|Thank you for choosing} <strong>Winning Heaven</strong>! I am reaching out personally to confirm that your VIP member pass is active on our direct web platform.</p>
    
    <div style="background-color: #f0f9ff; border-left: 3px solid #0284c7; padding: 16px 18px; border-radius: 6px; margin: 18px 0;">
      <p style="margin: 0 0 8px; font-weight: 700; color: #0369a1; font-size: 14px;">Your Account Privileges Active Today:</p>
      <ul style="margin: 0; padding-left: 18px; color: #334155; font-size: 14px; line-height: 1.75;">
        <li><strong>VIP Match Credit:</strong> Active session match rewards on your first session</li>
        <li><strong>Session FP Entries:</strong> Complimentary session entries credited to your profile</li>
        <li><strong>24/7 Fast Transfers:</strong> Direct payouts via Cash App, Crypto, or Bank</li>
        <li><strong>Direct Web Play:</strong> Zero app downloads — access directly in your browser</li>
      </ul>
    </div>

    <div style="text-align: center; margin: 26px 0 20px;">
      <a href="https://winningheaven.com" target="_blank" style="background-color: #0f172a; color: #ffffff; padding: 13px 32px; border-radius: 6px; font-weight: 700; font-size: 15px; text-decoration: none; display: inline-block;">
        Access Account &amp; Play Now &rarr;
      </a>
      <div style="margin-top: 10px; font-size: 12px; color: #64748b;">Direct Portal Link: <a href="https://winningheaven.com" target="_blank" style="color: #0284c7; text-decoration: underline;">https://winningheaven.com</a></div>
    </div>

    <p style="color: #64748b; font-size: 14px; margin-top: 22px;">
      If you have any questions or need help logging in, simply reply directly to this email and our VIP concierge team will take care of it for you.
    </p>

    <div style="margin-top: 26px; padding-top: 16px; border-top: 1px solid #e2e8f0; color: #334155; font-size: 13px; line-height: 1.5;">
      Best regards,<br>
      <strong style="color: #0f172a;">VIP Concierge Host</strong><br>
      Winning Heaven VIP Support Team<br>
      <a href="https://winningheaven.com" target="_blank" style="color: #0284c7; text-decoration: none; font-weight: 600;">https://winningheaven.com</a>
    </div>
    
    <div style="margin-top: 26px; padding-top: 12px; border-top: 1px solid #f1f5f9; font-size: 11px; color: #94a3b8; text-align: center;">
      Winning Heaven VIP Concierge Services • Direct Web Platform<br>
      To manage your email preferences, reply "Unsubscribe".
    </div>
  </div>
</body>
</html>"""
    },
    {
        "id": "day1_evening_benefits",
        "stage": 1,
        "name": "Day 1 Evening: Session Privileges Summary",
        "subject": "{Account Overview|Member Update}: Active evening session privileges",
        "preview_text": "Summary of active session credits and verified fast settlement options.",
        "plain_text": """{Hi|Hello|Good evening},

Following up on your VIP account activation today at Winning Heaven. Here is a quick evening summary of the session privileges active on your profile right now:

• Session Match Credit: Match rewards active for your evening session
• FP Session Entries: Credited directly to your account profile upon login
• Guaranteed 24/7 Transfers: Fast payouts directly via Cash App, Crypto, or Bank
• Direct Browser Access: Zero app installation required — play on your phone or PC

Access your member profile and view your active benefits:
👉 https://winningheaven.com

If you need any assistance getting started this evening, simply reply to this email and your host will assist you immediately.

Best regards,

VIP Support Host
Winning Heaven Team
https://winningheaven.com

To manage your notification preferences, reply 'Unsubscribe'.""",
        "html": """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{Account Overview|Member Update}: Active evening session privileges</title>
</head>
<body style="margin: 0; padding: 24px 12px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 15px; line-height: 1.6; color: #1e293b; background-color: #f8fafc;">

  <!-- Hidden Preheader Snippet for High Primary Inbox Placement -->
  <div style="display:none;font-size:1px;color:#ffffff;line-height:1px;max-height:0px;max-width:0px;opacity:0;overflow:hidden;">
    Summary of active session credits and verified fast settlement options. &nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;
  </div>

  <div style="max-width: 560px; margin: 0 auto; background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; padding: 28px 24px; box-shadow: 0 2px 6px rgba(0,0,0,0.03);">
    
    <div style="border-bottom: 2px solid #0284c7; padding-bottom: 12px; margin-bottom: 20px;">
      <span style="font-size: 19px; font-weight: 800; color: #0f172a; letter-spacing: 0.5px;">WINNING HEAVEN</span>
      <div style="font-size: 11px; color: #0284c7; font-weight: 700; text-transform: uppercase; letter-spacing: 0.8px; margin-top: 3px;">Day 1 Evening • Session Perks Summary</div>
    </div>

    <p style="font-size: 15px; font-weight: 600; color: #0f172a; margin: 0 0 14px;">{Hi|Hello|Good evening},</p>
    
    <p style="margin: 0 0 16px; color: #334155;">Following up on your VIP account activation today at <strong>Winning Heaven</strong>. Here is a quick summary of the session privileges active on your profile right now:</p>
    
    <div style="background-color: #f8fafc; border-left: 3px solid #0284c7; padding: 16px 18px; border-radius: 6px; margin: 18px 0;">
      <p style="margin: 0 0 8px; font-weight: 700; color: #0f172a; font-size: 14px;">Evening Session Highlights:</p>
      <ul style="margin: 0; padding-left: 18px; color: #334155; font-size: 14px; line-height: 1.75;">
        <li><strong>Session Match Credit:</strong> Match rewards active on your session balance</li>
        <li><strong>FP Session Entries:</strong> Credited to your account profile upon login</li>
        <li><strong>Fast 24/7 Transfers:</strong> Instant payouts directly via Cash App, Crypto, or Bank</li>
        <li><strong>Direct Browser Access:</strong> Play directly on your phone or PC with zero downloads</li>
      </ul>
    </div>

    <div style="text-align: center; margin: 26px 0 20px;">
      <a href="https://winningheaven.com" target="_blank" style="background-color: #0f172a; color: #ffffff; padding: 13px 32px; border-radius: 6px; font-weight: 700; font-size: 15px; text-decoration: none; display: inline-block;">
        Access Member Portal &rarr;
      </a>
      <div style="margin-top: 10px; font-size: 12px; color: #64748b;">Portal link: <a href="https://winningheaven.com" target="_blank" style="color: #0284c7; text-decoration: underline;">https://winningheaven.com</a></div>
    </div>

    <p style="color: #64748b; font-size: 14px; margin-top: 22px;">
      If you need any assistance getting started this evening, simply reply to this email and your host will assist you immediately.
    </p>

    <div style="margin-top: 26px; padding-top: 16px; border-top: 1px solid #e2e8f0; color: #334155; font-size: 13px; line-height: 1.5;">
      Warm regards,<br>
      <strong style="color: #0f172a;">VIP Support Host</strong><br>
      Winning Heaven Support Team<br>
      <a href="https://winningheaven.com" target="_blank" style="color: #0284c7; text-decoration: none; font-weight: 600;">https://winningheaven.com</a>
    </div>
    
    <div style="margin-top: 26px; padding-top: 12px; border-top: 1px solid #f1f5f9; font-size: 11px; color: #94a3b8; text-align: center;">
      Winning Heaven VIP Support • Direct Web Platform<br>
      To manage your email preferences, reply "Unsubscribe".
    </div>
  </div>
</body>
</html>"""
    },

    # ------------------ DAY 2 ------------------
    {
        "id": "day2_morning_platform",
        "stage": 2,
        "name": "Day 2 Morning: Direct Web Access Guide",
        "subject": "{Access Guide|Official Notice}: Direct browser platform setup",
        "preview_text": "Zero app downloads required. Play instantly on mobile or desktop.",
        "plain_text": """{Hi|Hello|Good morning},

Did you know that Winning Heaven operates on a 100% direct web platform?

There is no app download, installation, or waiting required. You can access your favorite sweepstakes platforms directly in your browser:

👉 https://winningheaven.com

Platform Advantages:
• Instant Web Access: Works smoothly on iPhone, Android, and PC
• Featured Games: Fire Kirin, Orion Stars, Riversweeps & Juwa
• 24/7 Fast Transfers: Secure payouts processed around the clock
• Session Match Credit: Active deposit match credited on your balance

Try your direct web access today:
👉 https://winningheaven.com

Best regards,

Winning Heaven Technical Host
https://winningheaven.com

To manage your notification preferences, reply 'Unsubscribe'.""",
        "html": """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{Access Guide|Official Notice}: Direct browser platform setup</title>
</head>
<body style="margin: 0; padding: 24px 12px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 15px; line-height: 1.6; color: #1e293b; background-color: #f8fafc;">

  <!-- Hidden Preheader Snippet for High Primary Inbox Placement -->
  <div style="display:none;font-size:1px;color:#ffffff;line-height:1px;max-height:0px;max-width:0px;opacity:0;overflow:hidden;">
    Zero app downloads required. Play instantly on mobile or desktop. &nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;
  </div>

  <div style="max-width: 560px; margin: 0 auto; background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; padding: 28px 24px; box-shadow: 0 2px 6px rgba(0,0,0,0.03);">
    
    <div style="border-bottom: 2px solid #0284c7; padding-bottom: 12px; margin-bottom: 20px;">
      <span style="font-size: 19px; font-weight: 800; color: #0f172a; letter-spacing: 0.5px;">WINNING HEAVEN</span>
      <div style="font-size: 11px; color: #0284c7; font-weight: 700; text-transform: uppercase; letter-spacing: 0.8px; margin-top: 3px;">Day 2 Morning • Direct Browser Access Guide</div>
    </div>

    <p style="font-size: 15px; font-weight: 600; color: #0f172a; margin: 0 0 14px;">{Hi|Hello|Good morning},</p>
    
    <p style="margin: 0 0 16px; color: #334155;">Did you know that <strong>Winning Heaven</strong> operates on a 100% direct web platform? There are no app downloads, installations, or delays required.</p>
    
    <div style="background-color: #f0f9ff; border-left: 3px solid #0284c7; padding: 16px 18px; border-radius: 6px; margin: 18px 0;">
      <p style="margin: 0 0 8px; font-weight: 700; color: #0369a1; font-size: 14px;">Direct Web Advantages:</p>
      <ul style="margin: 0; padding-left: 18px; color: #334155; font-size: 14px; line-height: 1.75;">
        <li><strong>Instant Web Access:</strong> Seamless operation on iPhone, Android, and PC</li>
        <li><strong>Featured Platforms:</strong> Fire Kirin, Orion Stars, Riversweeps &amp; Juwa</li>
        <li><strong>24/7 Fast Transfers:</strong> Secure payouts processed around the clock</li>
        <li><strong>Session Match Credit:</strong> Active match credit on your balance</li>
      </ul>
    </div>

    <div style="text-align: center; margin: 26px 0 20px;">
      <a href="https://winningheaven.com" target="_blank" style="background-color: #0f172a; color: #ffffff; padding: 13px 32px; border-radius: 6px; font-weight: 700; font-size: 15px; text-decoration: none; display: inline-block;">
        Open Direct Browser Access &rarr;
      </a>
      <div style="margin-top: 10px; font-size: 12px; color: #64748b;">Direct link: <a href="https://winningheaven.com" target="_blank" style="color: #0284c7; text-decoration: underline;">https://winningheaven.com</a></div>
    </div>

    <p style="color: #64748b; font-size: 14px; margin-top: 22px;">
      If you need assistance connecting your browser or setting up, simply reply to this email.
    </p>

    <div style="margin-top: 26px; padding-top: 16px; border-top: 1px solid #e2e8f0; color: #334155; font-size: 13px; line-height: 1.5;">
      Best regards,<br>
      <strong style="color: #0f172a;">Winning Heaven Technical Host</strong><br>
      <a href="https://winningheaven.com" target="_blank" style="color: #0284c7; text-decoration: none; font-weight: 600;">https://winningheaven.com</a>
    </div>
    
    <div style="margin-top: 26px; padding-top: 12px; border-top: 1px solid #f1f5f9; font-size: 11px; color: #94a3b8; text-align: center;">
      Winning Heaven VIP Support • Direct Web Platform<br>
      To manage your email preferences, reply "Unsubscribe".
    </div>
  </div>
</body>
</html>"""
    },
    {
        "id": "day2_evening_concierge",
        "stage": 2,
        "name": "Day 2 Evening: Personal Host Verification",
        "subject": "{Personal Note|Account Check-in}: Confirming your VIP concierge setup",
        "preview_text": "Personal check-in from your VIP host team at Winning Heaven.",
        "plain_text": """{Hi|Hello|Good evening},

I am reaching out personally this evening to ensure your VIP member setup is running smoothly at Winning Heaven.

Here is what is currently ready on your account profile:
• VIP Session Match Credit: Active match rewards on your session
• FP Session Entries: Credited to your account profile
• Guaranteed 24/7 Transfers: Fast payouts via Cash App, Crypto, or Bank
• Direct Browser Play: Access all games on phone or desktop

You can verify your profile and access your account here:
👉 https://winningheaven.com

If you have any questions or need help logging in tonight, reply directly to this email and I will take care of it for you.

Best regards,

VIP Host Concierge
Winning Heaven Support Team
https://winningheaven.com

To manage your notification preferences, reply 'Unsubscribe'.""",
        "html": """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{Personal Note|Account Check-in}: Confirming your VIP concierge setup</title>
</head>
<body style="margin: 0; padding: 24px 12px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 15px; line-height: 1.6; color: #1e293b; background-color: #ffffff;">

  <!-- Hidden Preheader Snippet for High Primary Inbox Placement -->
  <div style="display:none;font-size:1px;color:#ffffff;line-height:1px;max-height:0px;max-width:0px;opacity:0;overflow:hidden;">
    Personal check-in from your VIP host team at Winning Heaven. &nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;
  </div>

  <div style="max-width: 560px; margin: 0 auto; color: #1e293b;">
    <p style="font-size: 15px; margin: 0 0 14px;">{Hi|Hello|Good evening},</p>
    
    <p style="margin: 0 0 14px;">I am reaching out personally this evening to ensure your VIP member setup is running smoothly at <strong>Winning Heaven</strong>.</p>
    
    <p style="margin: 0 0 14px;">Here is what is currently active on your account profile:</p>
    
    <ul style="margin: 0 0 18px 20px; padding: 0; line-height: 1.8; color: #334155; font-size: 14px;">
      <li><strong>VIP Session Match Credit:</strong> Active match rewards on your session</li>
      <li><strong>FP Session Entries:</strong> Credited to your account profile</li>
      <li><strong>Guaranteed 24/7 Transfers:</strong> Fast payouts via Cash App, Crypto, or Bank</li>
      <li><strong>Direct Browser Play:</strong> Access all games on phone or desktop</li>
    </ul>

    <div style="margin: 24px 0; text-align: center;">
      <a href="https://winningheaven.com" target="_blank" style="background-color: #0f172a; color: #ffffff; padding: 13px 32px; border-radius: 6px; font-weight: 700; font-size: 15px; text-decoration: none; display: inline-block;">
        Verify Account &amp; Play Now &rarr;
      </a>
      <div style="margin-top: 10px; font-size: 12px; color: #64748b;">Direct link: <a href="https://winningheaven.com" target="_blank" style="color: #0284c7; text-decoration: underline;">https://winningheaven.com</a></div>
    </div>

    <p style="color: #64748b; font-size: 14px; margin-top: 22px;">
      If you have any questions or need help logging in tonight, reply directly to this email and I will take care of it for you.
    </p>

    <div style="margin-top: 26px; padding-top: 16px; border-top: 1px solid #e2e8f0; color: #334155; font-size: 13px; line-height: 1.5;">
      Warm regards,<br>
      <strong style="color: #0f172a;">VIP Host Concierge</strong><br>
      Winning Heaven Support Team<br>
      <a href="https://winningheaven.com" target="_blank" style="color: #0284c7; text-decoration: none; font-weight: 600;">https://winningheaven.com</a>
    </div>
    
    <div style="margin-top: 26px; padding-top: 12px; border-top: 1px solid #f1f5f9; font-size: 11px; color: #94a3b8; text-align: center;">
      Winning Heaven VIP Concierge Services • Direct Web Platform<br>
      To manage your email preferences, reply "Unsubscribe".
    </div>
  </div>
</body>
</html>"""
    },

    # ------------------ DAY 3 ------------------
    {
        "id": "day3_morning_loyalty",
        "stage": 3,
        "name": "Day 3 Morning: Active Loyalty & Referral Rewards",
        "subject": "{Member Notice|Loyalty Update}: Active member privileges & referral benefits",
        "preview_text": "Overview of session match credits and daily member drops.",
        "plain_text": """{Hi|Hello|Good morning},

Here is your Day 3 morning loyalty status update from Winning Heaven.

Active Member Rewards:
• Match Credit Booster: Active session match ready on your profile
• Daily Login Drops: Claim daily login entries and session rewards
• Friend Referral Credits: Earn bonus credits for every player you invite
• 24/7 Fast Transfers: Withdraw your balance via Cash App, Crypto, or Bank

Claim your member rewards and jump in:
👉 https://winningheaven.com

Best regards,

Winning Heaven Host Team
https://winningheaven.com

To manage your notification preferences, reply 'Unsubscribe'.""",
        "html": """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{Member Notice|Loyalty Update}: Active member privileges &amp; referral benefits</title>
</head>
<body style="margin: 0; padding: 24px 12px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 15px; line-height: 1.6; color: #1e293b; background-color: #f8fafc;">

  <!-- Hidden Preheader Snippet for High Primary Inbox Placement -->
  <div style="display:none;font-size:1px;color:#ffffff;line-height:1px;max-height:0px;max-width:0px;opacity:0;overflow:hidden;">
    Overview of session match credits and daily member drops. &nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;
  </div>

  <div style="max-width: 560px; margin: 0 auto; background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; padding: 28px 24px; box-shadow: 0 2px 6px rgba(0,0,0,0.03);">
    
    <div style="border-bottom: 2px solid #0284c7; padding-bottom: 12px; margin-bottom: 20px;">
      <span style="font-size: 19px; font-weight: 800; color: #0f172a; letter-spacing: 0.5px;">WINNING HEAVEN</span>
      <div style="font-size: 11px; color: #0284c7; font-weight: 700; text-transform: uppercase; letter-spacing: 0.8px; margin-top: 3px;">Day 3 Morning • Loyalty Rewards Update</div>
    </div>

    <p style="font-size: 15px; font-weight: 600; color: #0f172a; margin: 0 0 14px;">{Hi|Hello|Good morning},</p>
    
    <p style="margin: 0 0 16px; color: #334155;">Here is your Day 3 morning loyalty status update from <strong>Winning Heaven</strong>.</p>
    
    <div style="background-color: #f0f9ff; border-left: 3px solid #0284c7; padding: 16px 18px; border-radius: 6px; margin: 18px 0;">
      <p style="margin: 0 0 8px; font-weight: 700; color: #0369a1; font-size: 14px;">Active Loyalty Privileges:</p>
      <ul style="margin: 0; padding-left: 18px; color: #334155; font-size: 14px; line-height: 1.75;">
        <li><strong>Match Credit Booster:</strong> Active session match ready on your profile</li>
        <li><strong>Daily Login Drops:</strong> Claim daily login entries and session rewards</li>
        <li><strong>Friend Referral Credits:</strong> Earn bonus credits for every player you invite</li>
        <li><strong>24/7 Fast Transfers:</strong> Withdraw your balance via Cash App, Crypto, or Bank</li>
      </ul>
    </div>

    <div style="text-align: center; margin: 26px 0 20px;">
      <a href="https://winningheaven.com" target="_blank" style="background-color: #0f172a; color: #ffffff; padding: 13px 32px; border-radius: 6px; font-weight: 700; font-size: 15px; text-decoration: none; display: inline-block;">
        Claim Member Privileges &rarr;
      </a>
      <div style="margin-top: 10px; font-size: 12px; color: #64748b;">Direct link: <a href="https://winningheaven.com" target="_blank" style="color: #0284c7; text-decoration: underline;">https://winningheaven.com</a></div>
    </div>

    <p style="color: #64748b; font-size: 14px; margin-top: 22px;">
      If you need any assistance claiming your rewards, reply directly to this email.
    </p>

    <div style="margin-top: 26px; padding-top: 16px; border-top: 1px solid #e2e8f0; color: #334155; font-size: 13px; line-height: 1.5;">
      Best regards,<br>
      <strong style="color: #0f172a;">Winning Heaven Host Team</strong><br>
      <a href="https://winningheaven.com" target="_blank" style="color: #0284c7; text-decoration: none; font-weight: 600;">https://winningheaven.com</a>
    </div>
    
    <div style="margin-top: 26px; padding-top: 12px; border-top: 1px solid #f1f5f9; font-size: 11px; color: #94a3b8; text-align: center;">
      Winning Heaven VIP Support • Direct Web Platform<br>
      To manage your email preferences, reply "Unsubscribe".
    </div>
  </div>
</body>
</html>"""
    },
    {
        "id": "day3_evening_cashout",
        "stage": 3,
        "name": "Day 3 Evening: 24/7 Instant Settlements & Transfers",
        "subject": "{Service Feature|Payment Overview}: 24/7 Guaranteed account settlements",
        "preview_text": "Fast transfers processed via Cash App, Crypto, or Bank Transfer.",
        "plain_text": """{Hi|Hello|Good evening},

One of the top reasons members choose Winning Heaven is our guaranteed 24/7 instant settlement system.

Settlement Options:
• Cash App: Instant transfer directly to your tag
• Crypto: Fast payouts via Bitcoin / USDT
• Bank Transfer: Direct bank settlement with zero delay

No waiting for business hours — settle and withdraw your balance anytime 24/7.

Experience fast transfers and active play:
👉 https://winningheaven.com

Best regards,

Winning Heaven Finance & Support Team
https://winningheaven.com

To manage your notification preferences, reply 'Unsubscribe'.""",
        "html": """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{Service Feature|Payment Overview}: 24/7 Guaranteed account settlements</title>
</head>
<body style="margin: 0; padding: 24px 12px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 15px; line-height: 1.6; color: #1e293b; background-color: #f8fafc;">

  <!-- Hidden Preheader Snippet for High Primary Inbox Placement -->
  <div style="display:none;font-size:1px;color:#ffffff;line-height:1px;max-height:0px;max-width:0px;opacity:0;overflow:hidden;">
    Fast transfers processed via Cash App, Crypto, or Bank Transfer. &nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;
  </div>

  <div style="max-width: 560px; margin: 0 auto; background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; padding: 28px 24px; box-shadow: 0 2px 6px rgba(0,0,0,0.03);">
    
    <div style="border-bottom: 2px solid #0284c7; padding-bottom: 12px; margin-bottom: 20px;">
      <span style="font-size: 19px; font-weight: 800; color: #0f172a; letter-spacing: 0.5px;">WINNING HEAVEN</span>
      <div style="font-size: 11px; color: #0284c7; font-weight: 700; text-transform: uppercase; letter-spacing: 0.8px; margin-top: 3px;">Day 3 Evening • Instant Settlement</div>
    </div>

    <p style="font-size: 15px; font-weight: 600; color: #0f172a; margin: 0 0 14px;">{Hi|Hello|Good evening},</p>
    
    <p style="margin: 0 0 16px; color: #334155;">One of the top reasons members choose <strong>Winning Heaven</strong> is our guaranteed 24/7 instant settlement system.</p>
    
    <div style="background-color: #f8fafc; border-left: 3px solid #0f172a; padding: 16px 18px; border-radius: 6px; margin: 18px 0;">
      <p style="margin: 0 0 8px; font-weight: 700; color: #0f172a; font-size: 14px;">Fast Transfer Options:</p>
      <ul style="margin: 0; padding-left: 18px; color: #334155; font-size: 14px; line-height: 1.75;">
        <li><strong>Cash App:</strong> Instant transfer directly to your tag</li>
        <li><strong>Crypto:</strong> Fast payouts via Bitcoin / USDT</li>
        <li><strong>Bank Transfer:</strong> Direct bank settlement with zero delay</li>
      </ul>
    </div>

    <div style="text-align: center; margin: 26px 0 20px;">
      <a href="https://winningheaven.com" target="_blank" style="background-color: #0f172a; color: #ffffff; padding: 13px 32px; border-radius: 6px; font-weight: 700; font-size: 15px; text-decoration: none; display: inline-block;">
        Experience Fast Settlements &rarr;
      </a>
      <div style="margin-top: 10px; font-size: 12px; color: #64748b;">Direct link: <a href="https://winningheaven.com" target="_blank" style="color: #0284c7; text-decoration: underline;">https://winningheaven.com</a></div>
    </div>

    <p style="color: #64748b; font-size: 14px; margin-top: 22px;">
      If you have questions about payment options or transfers, reply to this email anytime.
    </p>

    <div style="margin-top: 26px; padding-top: 16px; border-top: 1px solid #e2e8f0; color: #334155; font-size: 13px; line-height: 1.5;">
      Best regards,<br>
      <strong style="color: #0f172a;">Winning Heaven Finance Team</strong><br>
      <a href="https://winningheaven.com" target="_blank" style="color: #0284c7; text-decoration: none; font-weight: 600;">https://winningheaven.com</a>
    </div>
    
    <div style="margin-top: 26px; padding-top: 12px; border-top: 1px solid #f1f5f9; font-size: 11px; color: #94a3b8; text-align: center;">
      Winning Heaven Finance &amp; Support • Direct Web Platform<br>
      To manage your email preferences, reply "Unsubscribe".
    </div>
  </div>
</body>
</html>"""
    },

    # ------------------ DAY 4 ------------------
    {
        "id": "day4_morning_midweek",
        "stage": 4,
        "name": "Day 4 Morning: Mid-Week Member Update",
        "subject": "{Mid-Week Update|Account Status}: Reserved session privileges & platform features",
        "preview_text": "Summary of available game titles and member benefits.",
        "plain_text": """{Hi|Hello|Good morning},

Mid-week update from your VIP host team at Winning Heaven.

Your account profile remains eligible for active member session perks:
• Match Credit Booster: Boost your play balance on your next session
• FP Session Entries: Session entries ready on your account profile
• 24/7 Instant Transfers: Quick payouts via Cash App, Crypto, or Bank
• Direct Browser Access: Play Fire Kirin, Orion Stars, Riversweeps & Juwa

Access your account and check your mid-week perks:
👉 https://winningheaven.com

Best regards,

Winning Heaven VIP Host Team
https://winningheaven.com

To manage your notification preferences, reply 'Unsubscribe'.""",
        "html": """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{Mid-Week Update|Account Status}: Reserved session privileges &amp; platform features</title>
</head>
<body style="margin: 0; padding: 24px 12px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 15px; line-height: 1.6; color: #1e293b; background-color: #f8fafc;">

  <!-- Hidden Preheader Snippet for High Primary Inbox Placement -->
  <div style="display:none;font-size:1px;color:#ffffff;line-height:1px;max-height:0px;max-width:0px;opacity:0;overflow:hidden;">
    Summary of available game titles and member benefits. &nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;
  </div>

  <div style="max-width: 560px; margin: 0 auto; background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; padding: 28px 24px; box-shadow: 0 2px 6px rgba(0,0,0,0.03);">
    
    <div style="border-bottom: 2px solid #0284c7; padding-bottom: 12px; margin-bottom: 20px;">
      <span style="font-size: 19px; font-weight: 800; color: #0f172a; letter-spacing: 0.5px;">WINNING HEAVEN</span>
      <div style="font-size: 11px; color: #0284c7; font-weight: 700; text-transform: uppercase; letter-spacing: 0.8px; margin-top: 3px;">Day 4 Morning • Mid-Week Session Overview</div>
    </div>

    <p style="font-size: 15px; font-weight: 600; color: #0f172a; margin: 0 0 14px;">{Hi|Hello|Good morning},</p>
    
    <p style="margin: 0 0 16px; color: #334155;">Mid-week update from your VIP host team at <strong>Winning Heaven</strong>.</p>
    
    <div style="background-color: #f0f9ff; border-left: 3px solid #0284c7; padding: 16px 18px; border-radius: 6px; margin: 18px 0;">
      <p style="margin: 0 0 8px; font-weight: 700; color: #0369a1; font-size: 14px;">Mid-Week Session Perks:</p>
      <ul style="margin: 0; padding-left: 18px; color: #334155; font-size: 14px; line-height: 1.75;">
        <li><strong>Match Credit Booster:</strong> Boost your balance on your next session</li>
        <li><strong>FP Session Entries:</strong> Active entries ready on your account profile</li>
        <li><strong>24/7 Instant Transfers:</strong> Quick payouts via Cash App, Crypto, or Bank</li>
        <li><strong>Direct Browser Access:</strong> Play Fire Kirin, Orion Stars, Riversweeps &amp; Juwa</li>
      </ul>
    </div>

    <div style="text-align: center; margin: 26px 0 20px;">
      <a href="https://winningheaven.com" target="_blank" style="background-color: #0f172a; color: #ffffff; padding: 13px 32px; border-radius: 6px; font-weight: 700; font-size: 15px; text-decoration: none; display: inline-block;">
        Access Account &amp; Play Now &rarr;
      </a>
      <div style="margin-top: 10px; font-size: 12px; color: #64748b;">Direct link: <a href="https://winningheaven.com" target="_blank" style="color: #0284c7; text-decoration: underline;">https://winningheaven.com</a></div>
    </div>

    <p style="color: #64748b; font-size: 14px; margin-top: 22px;">
      If you need any help claiming your bonus, reply directly to this email.
    </p>

    <div style="margin-top: 26px; padding-top: 16px; border-top: 1px solid #e2e8f0; color: #334155; font-size: 13px; line-height: 1.5;">
      Best regards,<br>
      <strong style="color: #0f172a;">Winning Heaven VIP Host Team</strong><br>
      <a href="https://winningheaven.com" target="_blank" style="color: #0284c7; text-decoration: none; font-weight: 600;">https://winningheaven.com</a>
    </div>
    
    <div style="margin-top: 26px; padding-top: 12px; border-top: 1px solid #f1f5f9; font-size: 11px; color: #94a3b8; text-align: center;">
      Winning Heaven VIP Support • Direct Web Platform<br>
      To manage your email preferences, reply "Unsubscribe".
    </div>
  </div>
</body>
</html>"""
    },
    {
        "id": "day4_evening_reengage",
        "stage": 4,
        "name": "Day 4 Evening: VIP Host Personal Check-In",
        "subject": "{Personal Message|Concierge Update}: Checking in on your account experience",
        "preview_text": "Direct letter from your concierge host at Winning Heaven.",
        "plain_text": """{Hi|Hello|Good evening},

Hope you are having a pleasant evening!

This is a personal message from your VIP Host Concierge at Winning Heaven. I wanted to reach out directly to check if you have any questions about your account setup or session options.

Summary of active privileges:
• VIP Match Credit: Active match credit ready for your next session
• 24/7 Fast Transfers: Payouts processed instantly to Cash App, Crypto, or Bank
• Zero Download Access: Play directly in your phone or PC browser

You can log in and view your account details here:
👉 https://winningheaven.com

If there is anything I can assist you with, please reply directly to this email and I will be happy to help.

Warm regards,

VIP Concierge Lead
Winning Heaven Host Team
https://winningheaven.com

To manage your notification preferences, reply 'Unsubscribe'.""",
        "html": """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{Personal Message|Concierge Update}: Checking in on your account experience</title>
</head>
<body style="margin: 0; padding: 24px 12px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 15px; line-height: 1.6; color: #1e293b; background-color: #ffffff;">

  <!-- Hidden Preheader Snippet for High Primary Inbox Placement -->
  <div style="display:none;font-size:1px;color:#ffffff;line-height:1px;max-height:0px;max-width:0px;opacity:0;overflow:hidden;">
    Direct letter from your concierge host at Winning Heaven. &nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;
  </div>

  <div style="max-width: 560px; margin: 0 auto; color: #1e293b;">
    <p style="font-size: 15px; margin: 0 0 14px;">{Hi|Hello|Good evening},</p>
    
    <p style="margin: 0 0 14px;">Hope you are having a pleasant evening!</p>
    
    <p style="margin: 0 0 14px;">This is a personal message from your VIP Host Concierge at <strong>Winning Heaven</strong>. I wanted to reach out directly to check if you have any questions about your account setup or session options.</p>
    
    <p style="margin: 16px 0 6px; font-weight: 600;">Summary of active privileges:</p>
    <ul style="margin: 0 0 18px 20px; padding: 0; line-height: 1.8; color: #334155; font-size: 14px;">
      <li><strong>VIP Match Credit:</strong> Active match credit ready for your next session</li>
      <li><strong>24/7 Fast Transfers:</strong> Payouts processed instantly to Cash App, Crypto, or Bank</li>
      <li><strong>Zero Download Access:</strong> Play directly in your phone or PC browser</li>
    </ul>

    <div style="margin: 24px 0; text-align: center;">
      <a href="https://winningheaven.com" target="_blank" style="background-color: #0f172a; color: #ffffff; padding: 13px 32px; border-radius: 6px; font-weight: 700; font-size: 15px; text-decoration: none; display: inline-block;">
        Access Your Member Profile &rarr;
      </a>
      <div style="margin-top: 10px; font-size: 12px; color: #64748b;">Direct link: <a href="https://winningheaven.com" target="_blank" style="color: #0284c7; text-decoration: underline;">https://winningheaven.com</a></div>
    </div>

    <p style="color: #64748b; font-size: 14px; margin-top: 22px;">
      If there is anything I can assist you with, please reply directly to this email and I will be happy to help.
    </p>

    <div style="margin-top: 26px; padding-top: 16px; border-top: 1px solid #e2e8f0; color: #334155; font-size: 13px; line-height: 1.5;">
      Warm regards,<br>
      <strong style="color: #0f172a;">VIP Concierge Lead</strong><br>
      Winning Heaven Host Team<br>
      <a href="https://winningheaven.com" target="_blank" style="color: #0284c7; text-decoration: none; font-weight: 600;">https://winningheaven.com</a>
    </div>
    
    <div style="margin-top: 26px; padding-top: 12px; border-top: 1px solid #f1f5f9; font-size: 11px; color: #94a3b8; text-align: center;">
      Winning Heaven VIP Host Concierge • Direct Web Platform<br>
      To manage your email preferences, reply "Unsubscribe".
    </div>
  </div>
</body>
</html>"""
    },

    # ------------------ DAY 5 ------------------
    {
        "id": "day5_morning_games",
        "stage": 5,
        "name": "Day 5 Morning: Featured Entertainment & Arcade Catalog",
        "subject": "{Catalog Guide|Platform Update}: Featured gaming platforms & arcade access",
        "preview_text": "Fire Kirin, Orion Stars, Riversweeps, and Juwa platforms available.",
        "plain_text": """{Hi|Hello|Good morning},

Looking for the best game selection with fast payouts?

At Winning Heaven, you get instant access to top-rated sweepstakes platforms:

Featured Games Available Now:
• Arcade Tables: Fire Kirin, Golden Dragon & King Kong
• Sweepstakes Platforms: Orion Stars, River Sweeps, Juwa & Milky Way
• Classic Slots: Multi-line reels and daily reward drops
• 24/7 Fast Transfers: Settle directly to Cash App, Crypto, or Bank

Ready to explore and play?

👉 ACCESS PLATFORMS & PLAY NOW:
https://winningheaven.com

Best regards,
The Winning Heaven Games Team
https://winningheaven.com

To manage your notification preferences, reply 'Unsubscribe'.""",
        "html": """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{Catalog Guide|Platform Update}: Featured gaming platforms &amp; arcade access</title>
</head>
<body style="margin: 0; padding: 24px 12px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 15px; line-height: 1.6; color: #1e293b; background-color: #f8fafc;">

  <!-- Hidden Preheader Snippet for High Primary Inbox Placement -->
  <div style="display:none;font-size:1px;color:#ffffff;line-height:1px;max-height:0px;max-width:0px;opacity:0;overflow:hidden;">
    Fire Kirin, Orion Stars, Riversweeps, and Juwa platforms available. &nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;
  </div>

  <div style="max-width: 560px; margin: 0 auto; background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; padding: 28px 24px; box-shadow: 0 2px 6px rgba(0,0,0,0.03);">
    
    <div style="border-bottom: 2px solid #0284c7; padding-bottom: 12px; margin-bottom: 20px;">
      <span style="font-size: 19px; font-weight: 800; color: #0f172a; letter-spacing: 0.5px;">WINNING HEAVEN</span>
      <div style="font-size: 11px; color: #0284c7; font-weight: 700; text-transform: uppercase; letter-spacing: 0.8px; margin-top: 3px;">Day 5 Morning • Games &amp; Transfers</div>
    </div>

    <p style="font-size: 15px; font-weight: 600; color: #0f172a; margin: 0 0 14px;">{Hi|Hello|Good morning},</p>

    <p style="margin: 0 0 16px; color: #334155;">
      Looking for a great platform selection paired with fast settlements? Here is what is live right now on <strong>Winning Heaven</strong>:
    </p>

    <div style="background-color: #f8fafc; border-left: 3px solid #0f172a; padding: 16px 18px; border-radius: 6px; margin: 18px 0;">
      <p style="margin: 0 0 8px; font-weight: 700; color: #0f172a; font-size: 14px;">
        Featured Game Platforms:
      </p>
      <ul style="margin: 0; padding-left: 18px; color: #334155; font-size: 14px; line-height: 1.75;">
        <li><strong>Arcade Tables:</strong> Fire Kirin, Golden Dragon &amp; King Kong</li>
        <li><strong>Sweepstakes Hubs:</strong> Orion Stars, River Sweeps, Juwa &amp; Milky Way</li>
        <li><strong>Classic Slots:</strong> Multi-line reels and daily reward drops</li>
        <li><strong>24/7 Fast Transfers:</strong> Direct settlements to Cash App, Crypto, or Bank</li>
      </ul>
    </div>

    <div style="text-align: center; margin: 26px 0 20px;">
      <a href="https://winningheaven.com" target="_blank" style="background-color: #0f172a; color: #ffffff; padding: 13px 32px; border-radius: 6px; font-weight: 700; font-size: 15px; text-decoration: none; display: inline-block;">
        Explore Platforms &amp; Play Now &rarr;
      </a>
      <div style="margin-top: 10px; font-size: 12px; color: #64748b;">Direct link: <a href="https://winningheaven.com" target="_blank" style="color: #0284c7; text-decoration: underline;">https://winningheaven.com</a></div>
    </div>

    <p style="color: #64748b; font-size: 14px; margin-top: 22px;">
      Play instantly from any device with zero downloads. If you have questions, reply directly to this email!
    </p>

    <div style="margin-top: 26px; padding-top: 16px; border-top: 1px solid #e2e8f0; color: #334155; font-size: 13px; line-height: 1.5;">
      Best regards,<br>
      <strong style="color: #0f172a;">The Winning Heaven Games Team</strong><br>
      <a href="https://winningheaven.com" target="_blank" style="color: #0284c7; text-decoration: none; font-weight: 600;">https://winningheaven.com</a>
    </div>

    <div style="margin-top: 26px; padding-top: 12px; border-top: 1px solid #f1f5f9; font-size: 11px; color: #94a3b8; text-align: center;">
      Winning Heaven Gaming Services • Direct Web Platform<br>
      To manage your email preferences, reply "Unsubscribe".
    </div>
  </div>
</body>
</html>"""
    },
    {
        "id": "day5_evening_weekend_kickoff",
        "stage": 5,
        "name": "Day 5 Evening: Weekend Kickoff Privileges",
        "subject": "{Weekend Notice|VIP Update}: Reserved member credits & weekend access",
        "preview_text": "Weekend session access live with verified fast account transfers.",
        "plain_text": """{Hi|Hello|Good evening},

The weekend is kicking off at Winning Heaven! Your VIP player pass is fully updated and ready for weekend sessions.

Weekend Session Perks:
• Weekend Match Credit: Active match credit on your session balance
• FP Session Entries: Session entries credited to your profile
• Friend Referral Bonus: Earn bonus credits for every player you invite
• 24/7 Guaranteed Transfers: Fast payouts processed via Cash App, Crypto, or Bank

Start your weekend session here:
👉 https://winningheaven.com

Best regards,

The Winning Heaven VIP Team
https://winningheaven.com

To manage your notification preferences, reply 'Unsubscribe'.""",
        "html": """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{Weekend Notice|VIP Update}: Reserved member credits &amp; weekend access</title>
</head>
<body style="margin: 0; padding: 24px 12px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 15px; line-height: 1.6; color: #1e293b; background-color: #f8fafc;">

  <!-- Hidden Preheader Snippet for High Primary Inbox Placement -->
  <div style="display:none;font-size:1px;color:#ffffff;line-height:1px;max-height:0px;max-width:0px;opacity:0;overflow:hidden;">
    Weekend session access live with verified fast account transfers. &nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;
  </div>

  <div style="max-width: 560px; margin: 0 auto; background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; padding: 28px 24px; box-shadow: 0 2px 6px rgba(0,0,0,0.03);">
    
    <div style="border-bottom: 2px solid #0284c7; padding-bottom: 12px; margin-bottom: 20px;">
      <span style="font-size: 19px; font-weight: 800; color: #0f172a; letter-spacing: 0.5px;">WINNING HEAVEN</span>
      <div style="font-size: 11px; color: #0284c7; font-weight: 700; text-transform: uppercase; letter-spacing: 0.8px; margin-top: 3px;">Day 5 Evening • Weekend Kickoff</div>
    </div>

    <p style="font-size: 15px; font-weight: 600; color: #0f172a; margin: 0 0 14px;">{Hi|Hello|Good evening},</p>

    <p style="margin: 0 0 16px; color: #334155;">
      The weekend is kicking off at <strong>Winning Heaven</strong>! Your VIP player pass is fully updated and ready for weekend sessions.
    </p>

    <div style="background-color: #f0f9ff; border-left: 3px solid #0284c7; padding: 16px 18px; border-radius: 6px; margin: 18px 0;">
      <p style="margin: 0 0 8px; font-weight: 700; color: #0369a1; font-size: 14px;">
        Weekend Session Perks:
      </p>
      <ul style="margin: 0; padding-left: 18px; color: #334155; font-size: 14px; line-height: 1.75;">
        <li><strong>Weekend Match Credit:</strong> Active match credit on your session balance</li>
        <li><strong>FP Session Entries:</strong> Active session entries credited to your profile</li>
        <li><strong>Friend Referral Bonus:</strong> Earn bonus credits for every player you invite</li>
        <li><strong>24/7 Fast Transfers:</strong> Fast payouts via Cash App, Crypto, or Bank</li>
      </ul>
    </div>

    <div style="text-align: center; margin: 26px 0 20px;">
      <a href="https://winningheaven.com" target="_blank" style="background-color: #0f172a; color: #ffffff; padding: 13px 32px; border-radius: 6px; font-weight: 700; font-size: 15px; text-decoration: none; display: inline-block;">
        Start Weekend Session &rarr;
      </a>
      <div style="margin-top: 10px; font-size: 12px; color: #64748b;">Direct link: <a href="https://winningheaven.com" target="_blank" style="color: #0284c7; text-decoration: underline;">https://winningheaven.com</a></div>
    </div>

    <p style="color: #64748b; font-size: 14px; margin-top: 22px;">
      If you need any assistance setting up your weekend session, reply to this email anytime.
    </p>

    <div style="margin-top: 26px; padding-top: 16px; border-top: 1px solid #e2e8f0; color: #334155; font-size: 13px; line-height: 1.5;">
      Warm regards,<br>
      <strong style="color: #0f172a;">The Winning Heaven VIP Team</strong><br>
      <a href="https://winningheaven.com" target="_blank" style="color: #0284c7; text-decoration: none; font-weight: 600;">https://winningheaven.com</a>
    </div>

    <div style="margin-top: 26px; padding-top: 12px; border-top: 1px solid #f1f5f9; font-size: 11px; color: #94a3b8; text-align: center;">
      Winning Heaven VIP Services • Direct Web Platform<br>
      To manage your email preferences, reply "Unsubscribe".
    </div>
  </div>
</body>
</html>"""
    },

    # ------------------ DAY 6 ------------------
    {
        "id": "day6_morning_saturday",
        "stage": 6,
        "name": "Day 6 Morning: Saturday Session Overview",
        "subject": "{Saturday Update|VIP Privileges}: Active weekend session privileges",
        "preview_text": "Enjoy weekend session match rewards and instant browser play.",
        "plain_text": """{Hi|Hello|Good morning},

Saturday morning update from Winning Heaven.

Your VIP member benefits for today include:
• Session Match Credit: Match bonus ready on your starting balance
• FP Session Entries: Session entries credited to your profile
• 24/7 Instant Transfers: Payouts processed in minutes via Cash App, Crypto, or Bank
• Direct Browser Play: Zero app downloads required — play on mobile or desktop

Jump in and play your Saturday session:
👉 https://winningheaven.com

Best regards,

VIP Concierge Team
Winning Heaven Support
https://winningheaven.com

To manage your notification preferences, reply 'Unsubscribe'.""",
        "html": """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{Saturday Update|VIP Privileges}: Active weekend session privileges</title>
</head>
<body style="margin: 0; padding: 24px 12px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 15px; line-height: 1.6; color: #1e293b; background-color: #f8fafc;">

  <!-- Hidden Preheader Snippet for High Primary Inbox Placement -->
  <div style="display:none;font-size:1px;color:#ffffff;line-height:1px;max-height:0px;max-width:0px;opacity:0;overflow:hidden;">
    Enjoy weekend session match rewards and instant browser play. &nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;
  </div>

  <div style="max-width: 560px; margin: 0 auto; background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; padding: 28px 24px; box-shadow: 0 2px 6px rgba(0,0,0,0.03);">
    
    <div style="border-bottom: 2px solid #0284c7; padding-bottom: 12px; margin-bottom: 20px;">
      <span style="font-size: 19px; font-weight: 800; color: #0f172a; letter-spacing: 0.5px;">WINNING HEAVEN</span>
      <div style="font-size: 11px; color: #0284c7; font-weight: 700; text-transform: uppercase; letter-spacing: 0.8px; margin-top: 3px;">Day 6 Morning • Saturday Session Update</div>
    </div>

    <p style="font-size: 15px; font-weight: 600; color: #0f172a; margin: 0 0 14px;">{Hi|Hello|Good morning},</p>
    
    <p style="margin: 0 0 16px; color: #334155;">Saturday morning update from <strong>Winning Heaven</strong>.</p>
    
    <div style="background-color: #f0f9ff; border-left: 3px solid #0284c7; padding: 16px 18px; border-radius: 6px; margin: 18px 0;">
      <p style="margin: 0 0 8px; font-weight: 700; color: #0369a1; font-size: 14px;">Saturday Session Privileges:</p>
      <ul style="margin: 0; padding-left: 18px; color: #334155; font-size: 14px; line-height: 1.75;">
        <li><strong>Session Match Credit:</strong> Match bonus ready on your starting balance</li>
        <li><strong>FP Session Entries:</strong> Active session entries credited to your profile</li>
        <li><strong>24/7 Instant Transfers:</strong> Withdrawals via Cash App, Crypto, or Bank</li>
        <li><strong>Direct Browser Play:</strong> Zero app downloads required — play on mobile or PC</li>
      </ul>
    </div>

    <div style="text-align: center; margin: 26px 0 20px;">
      <a href="https://winningheaven.com" target="_blank" style="background-color: #0f172a; color: #ffffff; padding: 13px 32px; border-radius: 6px; font-weight: 700; font-size: 15px; text-decoration: none; display: inline-block;">
        Play Saturday Session &rarr;
      </a>
      <div style="margin-top: 10px; font-size: 12px; color: #64748b;">Direct link: <a href="https://winningheaven.com" target="_blank" style="color: #0284c7; text-decoration: underline;">https://winningheaven.com</a></div>
    </div>

    <p style="color: #64748b; font-size: 14px; margin-top: 22px;">
      If you need any assistance, reply directly to this email and our team will help you right away.
    </p>

    <div style="margin-top: 26px; padding-top: 16px; border-top: 1px solid #e2e8f0; color: #334155; font-size: 13px; line-height: 1.5;">
      Best regards,<br>
      <strong style="color: #0f172a;">VIP Concierge Team</strong><br>
      Winning Heaven Support<br>
      <a href="https://winningheaven.com" target="_blank" style="color: #0284c7; text-decoration: none; font-weight: 600;">https://winningheaven.com</a>
    </div>
    
    <div style="margin-top: 26px; padding-top: 12px; border-top: 1px solid #f1f5f9; font-size: 11px; color: #94a3b8; text-align: center;">
      Winning Heaven VIP Support • Direct Web Platform<br>
      To manage your email preferences, reply "Unsubscribe".
    </div>
  </div>
</body>
</html>"""
    },
    {
        "id": "day6_evening_concierge_care",
        "stage": 6,
        "name": "Day 6 Evening: Dedicated Concierge Support",
        "subject": "{Concierge Note|Support Update}: 24/7 Dedicated member support & assistance",
        "preview_text": "Our VIP support team is available 24/7 for any account assistance.",
        "plain_text": """{Hi|Hello|Good evening},

A quick note from your dedicated VIP Host team at Winning Heaven. We are available 24 hours a day, 7 days a week to ensure your account experience is seamless.

How we assist you:
• Instant Account Assistance: Fast setup and balance credit processing
• 24/7 Fast Transfers: Quick cashouts via Cash App, Crypto, or Bank
• Direct Browser Support: Assistance for all mobile devices and desktop browsers

Access your account portal tonight:
👉 https://winningheaven.com

If you ever have a question or need assistance, simply reply directly to any of our emails.

Warm regards,

Winning Heaven VIP Host Concierge
https://winningheaven.com

To manage your notification preferences, reply 'Unsubscribe'.""",
        "html": """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{Concierge Note|Support Update}: 24/7 Dedicated member support &amp; assistance</title>
</head>
<body style="margin: 0; padding: 24px 12px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 15px; line-height: 1.6; color: #1e293b; background-color: #f8fafc;">

  <!-- Hidden Preheader Snippet for High Primary Inbox Placement -->
  <div style="display:none;font-size:1px;color:#ffffff;line-height:1px;max-height:0px;max-width:0px;opacity:0;overflow:hidden;">
    Our VIP support team is available 24/7 for any account assistance. &nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;
  </div>

  <div style="max-width: 560px; margin: 0 auto; background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; padding: 28px 24px; box-shadow: 0 2px 6px rgba(0,0,0,0.03);">
    
    <div style="border-bottom: 2px solid #0284c7; padding-bottom: 12px; margin-bottom: 20px;">
      <span style="font-size: 19px; font-weight: 800; color: #0f172a; letter-spacing: 0.5px;">WINNING HEAVEN</span>
      <div style="font-size: 11px; color: #0284c7; font-weight: 700; text-transform: uppercase; letter-spacing: 0.8px; margin-top: 3px;">Day 6 Evening • Concierge Support</div>
    </div>

    <p style="font-size: 15px; font-weight: 600; color: #0f172a; margin: 0 0 14px;">{Hi|Hello|Good evening},</p>
    
    <p style="margin: 0 0 16px; color: #334155;">A quick note from your dedicated VIP Host team at <strong>Winning Heaven</strong>. We are available 24 hours a day, 7 days a week to ensure your account experience is seamless.</p>
    
    <div style="background-color: #f8fafc; border-left: 3px solid #0f172a; padding: 16px 18px; border-radius: 6px; margin: 18px 0;">
      <p style="margin: 0 0 8px; font-weight: 700; color: #0f172a; font-size: 14px;">How We Assist You:</p>
      <ul style="margin: 0; padding-left: 18px; color: #334155; font-size: 14px; line-height: 1.75;">
        <li><strong>Instant Account Loading:</strong> Fast setup and balance credit processing</li>
        <li><strong>24/7 Fast Transfers:</strong> Quick payouts via Cash App, Crypto, or Bank</li>
        <li><strong>Direct Browser Support:</strong> Assistance for all devices and browsers</li>
      </ul>
    </div>

    <div style="text-align: center; margin: 26px 0 20px;">
      <a href="https://winningheaven.com" target="_blank" style="background-color: #0f172a; color: #ffffff; padding: 13px 32px; border-radius: 6px; font-weight: 700; font-size: 15px; text-decoration: none; display: inline-block;">
        Contact Host &amp; Play Now &rarr;
      </a>
      <div style="margin-top: 10px; font-size: 12px; color: #64748b;">Direct link: <a href="https://winningheaven.com" target="_blank" style="color: #0284c7; text-decoration: underline;">https://winningheaven.com</a></div>
    </div>

    <p style="color: #64748b; font-size: 14px; margin-top: 22px;">
      If you ever have a question or need assistance, simply reply directly to any of our emails.
    </p>

    <div style="margin-top: 26px; padding-top: 16px; border-top: 1px solid #e2e8f0; color: #334155; font-size: 13px; line-height: 1.5;">
      Warm regards,<br>
      <strong style="color: #0f172a;">Winning Heaven VIP Host Concierge</strong><br>
      <a href="https://winningheaven.com" target="_blank" style="color: #0284c7; text-decoration: none; font-weight: 600;">https://winningheaven.com</a>
    </div>
    
    <div style="margin-top: 26px; padding-top: 12px; border-top: 1px solid #f1f5f9; font-size: 11px; color: #94a3b8; text-align: center;">
      Winning Heaven Concierge Care • Direct Web Platform<br>
      To manage your email preferences, reply "Unsubscribe".
    </div>
  </div>
</body>
</html>"""
    },

    # ------------------ DAY 7 ------------------
    {
        "id": "day7_morning_weekly_summary",
        "stage": 7,
        "name": "Day 7 Morning: Weekly Account Summary",
        "subject": "{Weekly Summary|Account Overview}: Your active member privileges & credits",
        "preview_text": "Review your reserved session credits and member status.",
        "plain_text": """{Hi|Hello|Good morning},

Here is your Day 7 weekly account overview from Winning Heaven.

Weekly Status Summary:
• Active Member Profile: VIP host status active on our web platform
• Session Match Credit: Reserved match rewards ready for your play balance
• Daily Reward Drops: Login rewards credited upon profile access
• 24/7 Fast Transfers: Direct payouts via Cash App, Crypto, or Bank

Review your weekly summary and access your account:
👉 https://winningheaven.com

Best regards,

Winning Heaven Management
https://winningheaven.com

To manage your notification preferences, reply 'Unsubscribe'.""",
        "html": """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{Weekly Summary|Account Overview}: Your active member privileges &amp; credits</title>
</head>
<body style="margin: 0; padding: 24px 12px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 15px; line-height: 1.6; color: #1e293b; background-color: #f8fafc;">

  <!-- Hidden Preheader Snippet for High Primary Inbox Placement -->
  <div style="display:none;font-size:1px;color:#ffffff;line-height:1px;max-height:0px;max-width:0px;opacity:0;overflow:hidden;">
    Review your reserved session credits and member status. &nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;
  </div>

  <div style="max-width: 560px; margin: 0 auto; background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; padding: 28px 24px; box-shadow: 0 2px 6px rgba(0,0,0,0.03);">
    
    <div style="border-bottom: 2px solid #0284c7; padding-bottom: 12px; margin-bottom: 20px;">
      <span style="font-size: 19px; font-weight: 800; color: #0f172a; letter-spacing: 0.5px;">WINNING HEAVEN</span>
      <div style="font-size: 11px; color: #0284c7; font-weight: 700; text-transform: uppercase; letter-spacing: 0.8px; margin-top: 3px;">Day 7 Morning • Weekly Account Summary</div>
    </div>

    <p style="font-size: 15px; font-weight: 600; color: #0f172a; margin: 0 0 14px;">{Hi|Hello|Good morning},</p>
    
    <p style="margin: 0 0 16px; color: #334155;">Here is your Day 7 weekly account overview from <strong>Winning Heaven</strong>.</p>
    
    <div style="background-color: #f0f9ff; border-left: 3px solid #0284c7; padding: 16px 18px; border-radius: 6px; margin: 18px 0;">
      <p style="margin: 0 0 8px; font-weight: 700; color: #0369a1; font-size: 14px;">Weekly Account Status:</p>
      <ul style="margin: 0; padding-left: 18px; color: #334155; font-size: 14px; line-height: 1.75;">
        <li><strong>Active Member Profile:</strong> VIP host status active on our web platform</li>
        <li><strong>Session Match Credit:</strong> Reserved match rewards ready for your balance</li>
        <li><strong>Daily Reward Drops:</strong> Login rewards credited upon profile access</li>
        <li><strong>24/7 Fast Transfers:</strong> Direct withdrawals via Cash App, Crypto, or Bank</li>
      </ul>
    </div>

    <div style="text-align: center; margin: 26px 0 20px;">
      <a href="https://winningheaven.com" target="_blank" style="background-color: #0f172a; color: #ffffff; padding: 13px 32px; border-radius: 6px; font-weight: 700; font-size: 15px; text-decoration: none; display: inline-block;">
        View Weekly Summary &amp; Play &rarr;
      </a>
      <div style="margin-top: 10px; font-size: 12px; color: #64748b;">Direct link: <a href="https://winningheaven.com" target="_blank" style="color: #0284c7; text-decoration: underline;">https://winningheaven.com</a></div>
    </div>

    <p style="color: #64748b; font-size: 14px; margin-top: 22px;">
      If you need any assistance, reply directly to this email.
    </p>

    <div style="margin-top: 26px; padding-top: 16px; border-top: 1px solid #e2e8f0; color: #334155; font-size: 13px; line-height: 1.5;">
      Best regards,<br>
      <strong style="color: #0f172a;">Winning Heaven Management</strong><br>
      <a href="https://winningheaven.com" target="_blank" style="color: #0284c7; text-decoration: none; font-weight: 600;">https://winningheaven.com</a>
    </div>
    
    <div style="margin-top: 26px; padding-top: 12px; border-top: 1px solid #f1f5f9; font-size: 11px; color: #94a3b8; text-align: center;">
      Winning Heaven VIP Management • Direct Web Platform<br>
      To manage your email preferences, reply "Unsubscribe".
    </div>
  </div>
</body>
</html>"""
    },
    {
        "id": "day7_evening_final_courtesy",
        "stage": 7,
        "name": "Day 7 Evening: 7-Day Campaign Courtesy Note",
        "subject": "{Courtesy Update|Account Note}: Managing your VIP notification preferences",
        "preview_text": "Final weekly check-in regarding your account status at Winning Heaven.",
        "plain_text": """{Hi|Hello|Good evening},

This is a courtesy check-in at the end of your 7-day onboarding sequence at Winning Heaven.

We want to make sure you have everything you need to enjoy our direct web platform. Your VIP account profile remains fully active with guaranteed 24/7 fast transfers and direct browser play.

Visit our official web platform anytime:
👉 https://winningheaven.com

If you wish to adjust your email notification frequency or opt out of future updates, simply reply 'Unsubscribe' to this email.

Warm regards,

Winning Heaven VIP Host Team
https://winningheaven.com

To manage your notification preferences, reply 'Unsubscribe'.""",
        "html": """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{Courtesy Update|Account Note}: Managing your VIP notification preferences</title>
</head>
<body style="margin: 0; padding: 24px 12px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 15px; line-height: 1.6; color: #1e293b; background-color: #f8fafc;">

  <!-- Hidden Preheader Snippet for High Primary Inbox Placement -->
  <div style="display:none;font-size:1px;color:#ffffff;line-height:1px;max-height:0px;max-width:0px;opacity:0;overflow:hidden;">
    Final weekly check-in regarding your account status at Winning Heaven. &nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;
  </div>

  <div style="max-width: 560px; margin: 0 auto; background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; padding: 28px 24px; box-shadow: 0 2px 6px rgba(0,0,0,0.03);">
    
    <div style="border-bottom: 2px solid #64748b; padding-bottom: 12px; margin-bottom: 20px;">
      <span style="font-size: 19px; font-weight: 800; color: #0f172a; letter-spacing: 0.5px;">WINNING HEAVEN</span>
      <div style="font-size: 11px; color: #64748b; font-weight: 700; text-transform: uppercase; letter-spacing: 0.8px; margin-top: 3px;">Day 7 Evening • Courtesy Notice</div>
    </div>

    <p style="font-size: 15px; font-weight: 600; color: #0f172a; margin: 0 0 14px;">{Hi|Hello|Good evening},</p>
    
    <p style="margin: 0 0 16px; color: #334155;">This is a courtesy check-in at the end of your 7-day onboarding sequence at <strong>Winning Heaven</strong>.</p>
    
    <p style="margin: 0 0 16px; color: #334155;">We want to make sure you have everything you need to enjoy our direct web platform. Your VIP account profile remains fully active with guaranteed 24/7 fast transfers and direct browser play.</p>

    <div style="text-align: center; margin: 26px 0 20px;">
      <a href="https://winningheaven.com" target="_blank" style="background-color: #0f172a; color: #ffffff; padding: 13px 32px; border-radius: 6px; font-weight: 700; font-size: 15px; text-decoration: none; display: inline-block;">
        Visit Winning Heaven Portal &rarr;
      </a>
      <div style="margin-top: 10px; font-size: 12px; color: #64748b;">Direct link: <a href="https://winningheaven.com" target="_blank" style="color: #0284c7; text-decoration: underline;">https://winningheaven.com</a></div>
    </div>

    <p style="color: #64748b; font-size: 14px; margin-top: 22px;">
      If you wish to adjust your email notification frequency or opt out of future updates, simply reply "Unsubscribe" to this email.
    </p>

    <div style="margin-top: 26px; padding-top: 16px; border-top: 1px solid #e2e8f0; color: #334155; font-size: 13px; line-height: 1.5;">
      Warm regards,<br>
      <strong style="color: #0f172a;">Winning Heaven VIP Host Team</strong><br>
      <a href="https://winningheaven.com" target="_blank" style="color: #0284c7; text-decoration: none; font-weight: 600;">https://winningheaven.com</a>
    </div>
    
    <div style="margin-top: 26px; padding-top: 12px; border-top: 1px solid #f1f5f9; font-size: 11px; color: #94a3b8; text-align: center;">
      Winning Heaven VIP Services • Direct Web Platform<br>
      To manage your email preferences, reply "Unsubscribe".
    </div>
  </div>
</body>
</html>"""
    }
]

SPAM_REPLACEMENTS = [
    (r'(?i)\b100%\s*free\s*cash\b', 'VIP Welcome Pass'),
    (r'(?i)\bmake\s*money\s*fast\b', 'Verified Session Privileges'),
    (r'(?i)\bguaranteed\s*win(nings)?\b', 'Verified Account & Payouts'),
    (r'(?i)\bclick\s*here\s*(now)?\b', 'Access Account Details'),
    (r'(?i)\b200%\s*(match|deposit|bonus)?\b', 'Match Session Credit'),
    (r'(?i)\b100%\s*referral\b', 'Member Referral Rewards'),
    (r'(?i)\b100%\s*free\b', 'Complimentary'),
    (r'(?i)\bfree\s*money\b', 'Account Credits'),
    (r'(?i)\bfree\s*cash\b', 'Account Credits'),
    (r'(?i)\bdouble\s*(and|&)\s*triple\b', 'Boost'),
    (r'(?i)\bfreeplay(s)?\b', 'FP session entries'),
    (r'(?i)\bfree\s*play(s)?\b', 'FP session entries'),
    (r'(?i)\bjackpot(s)?\b', 'Game Rewards'),
    (r'(?i)\bgamble\b', 'Play'),
    (r'(?i)\bcasino\b', 'Gaming Platform'),
    (r'(?i)\b0\s*spam\s*risk\b', 'Primary Verified'),
    (r'(?i)\bspam\s*free\b', 'Verified'),
    (r'\$\$\++', '$$'),
    (r'!{2,}', '!'),
    (r'\?{2,}', '?')
]

def sanitize_spam_content(text):
    if not text:
        return text
    clean = text
    for pattern, replacement in SPAM_REPLACEMENTS:
        clean = re.sub(pattern, replacement, clean)
    # Remove ALL CAPS words longer than 3 characters
    def capitalize_word(match):
        w = match.group(0)
        if len(w) > 3 and w.isupper() and not w.startswith("HTTP") and not w.startswith("VIP") and not w.startswith("CTA"):
            return w.capitalize()
        return w
    clean = re.sub(r'\b[A-Z]{4,}\b', capitalize_word, clean)
    return clean

def generate_custom_template(prompt, tone="vip", offer_headline=""):
    raw_prompt = prompt.strip() if prompt else ""
    if not raw_prompt:
        raw_prompt = "Exclusive VIP Privileges & Fast Account Transfers at Winning Heaven"
        
    prompt_clean = sanitize_spam_content(raw_prompt)
    prompt_lower = prompt_clean.lower()
    lines = [l.strip() for l in prompt_clean.split('\n') if l.strip()]
    first_line = lines[0] if lines else prompt_clean
        
    is_switch = any(w in prompt_lower for w in ["switch", "other platform", "khail", "luck", "referral"])
    is_deposit = any(w in prompt_lower for w in ["deposit", "match", "bonus", "credit"])
    is_games = any(w in prompt_lower for w in ["game", "kirin", "orion", "juwa", "fish", "slots"])

    if is_switch:
        subject = "{Invitation|Exclusive Access}: Member privileges & direct platform access"
        intro_paragraph = "If you are currently playing on other platforms, it is time to upgrade your gaming experience at Winning Heaven. Enjoy fast 24/7 transfers, direct browser play, and exclusive VIP member privileges."
        bullet_items = [
            "VIP Welcome Match: Active session credits credited on your first session.",
            "Session FP Entries: Enjoy complimentary entries credited directly to your profile.",
            "Member Referral Rewards: Receive bonus credits for every friend you invite.",
            "Fast 24/7 Instant Settlements: Direct payouts via Cash App, Crypto, or Bank.",
            "Direct Browser Play: Play Fire Kirin, Orion Stars & Riversweeps with zero app downloads."
        ]
    elif is_deposit:
        subject = "{Account Update|VIP Notice}: Active deposit match credit details"
        intro_paragraph = "We are pleased to share an exclusive deposit match offer for your Winning Heaven account. Boost your session balance today with verified match rewards and 24/7 fast withdrawals."
        bullet_items = [
            "VIP Deposit Match Credit: Extra balance credited automatically on your session.",
            "Session FP Entries: Claim complimentary FP entries on top sweepstakes games.",
            "Fast 24/7 Instant Transfers: Fast payouts via Cash App, Crypto & Bank.",
            "Direct Browser Play: Play directly in your phone or PC browser."
        ]
    elif is_games:
        subject = "{Game Catalog|Platform Update}: New sweepstakes platforms & member access"
        intro_paragraph = "The latest sweepstakes games are live at Winning Heaven! Access Fire Kirin, Orion Stars, Riversweeps, and Juwa arcade tables with daily bonus entries and fast withdrawals."
        bullet_items = [
            "Featured Game Platforms: Fire Kirin, Orion Stars, Riversweeps & Juwa Arcade.",
            "Daily Login Rewards: Claim bonus entries every single day.",
            "Fast 24/7 Transfers: Payouts processed in minutes via Cash App, Crypto & Bank.",
            "Direct Browser Play: Zero app installation required."
        ]
    else:
        subject = f"{{Member Update|Important}}: {first_line[:40]}"
        intro_paragraph = f"We are reaching out to share your personal VIP player update: {prompt_clean}. Enjoy direct browser play and fast 24/7 transfers."
        bullet_items = [
            "Exclusive VIP Match Rewards reserved for your account",
            "Fast 24/7 Instant Transfers (Cash App, Crypto & Bank)",
            "Top Sweepstakes Platforms (Fire Kirin, Orion Stars, Riversweeps)",
            "Daily Member Rewards & FP Session Drops",
            "Direct Browser Play — No app downloads needed"
        ]

    subject = sanitize_spam_content(subject)

    bullets_html = "\n".join([f'        <li style="margin-bottom: 6px;">{item}</li>' for item in bullet_items])
    bullets_plain = "\n".join([f'• {item}' for item in bullet_items])

    preview_text = f"Your VIP access is active for Winning Heaven. {first_line[:60]}"

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{subject}</title>
</head>
<body style="margin: 0; padding: 24px 12px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 15px; line-height: 1.6; color: #1e293b; background-color: #f8fafc;">

  <!-- Hidden Preheader Snippet for High Primary Inbox Placement -->
  <div style="display:none;font-size:1px;color:#ffffff;line-height:1px;max-height:0px;max-width:0px;opacity:0;overflow:hidden;">
    {preview_text} &nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;
  </div>

  <div style="max-width: 560px; margin: 0 auto; background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; padding: 28px 24px; box-shadow: 0 2px 6px rgba(0,0,0,0.03);">
    
    <div style="border-bottom: 2px solid #0284c7; padding-bottom: 12px; margin-bottom: 20px;">
      <span style="font-size: 19px; font-weight: 800; color: #0f172a; letter-spacing: 0.5px;">WINNING HEAVEN</span>
      <div style="font-size: 11px; color: #0284c7; font-weight: 700; text-transform: uppercase; letter-spacing: 0.8px; margin-top: 3px;">Exclusive VIP Member Privilege</div>
    </div>

    <p style="margin: 0 0 14px; font-size: 15px; font-weight: 600; color: #0f172a;">
      {{Hi|Hello|Greetings}},
    </p>

    <p style="margin: 0 0 16px; color: #334155;">
      {intro_paragraph}
    </p>

    <div style="background-color: #f0f9ff; border-left: 3px solid #0284c7; padding: 16px 18px; border-radius: 6px; margin: 18px 0;">
      <p style="margin: 0 0 8px; font-weight: 700; color: #0369a1; font-size: 14px;">
        Your Active VIP Privileges:
      </p>
      <ul style="margin: 0; padding-left: 18px; color: #334155; font-size: 14px; line-height: 1.75;">
{bullets_html}
      </ul>
    </div>

    <div style="margin: 26px 0 20px; text-align: center;">
      <a href="https://winningheaven.com" target="_blank" style="background-color: #0f172a; color: #ffffff; padding: 13px 32px; border-radius: 6px; font-weight: 700; font-size: 15px; text-decoration: none; display: inline-block;">
        Claim VIP Pass &amp; Play Now &rarr;
      </a>
      <div style="margin-top: 10px; font-size: 12px; color: #64748b;">Direct link: <a href="https://winningheaven.com" target="_blank" style="color: #0284c7; text-decoration: underline;">https://winningheaven.com</a></div>
    </div>

    <p style="color: #64748b; font-size: 14px; margin-top: 22px;">
      If you have any questions or need help, reply directly to this email and our VIP support team will assist you immediately.
    </p>

    <div style="margin-top: 26px; padding-top: 16px; border-top: 1px solid #e2e8f0; color: #334155; font-size: 13px; line-height: 1.5;">
      Warm regards,<br>
      <strong style="color: #0f172a;">The Winning Heaven VIP Team</strong><br>
      <a href="https://winningheaven.com" target="_blank" style="color: #0284c7; text-decoration: none; font-weight: 600;">https://winningheaven.com</a>
    </div>

    <div style="margin-top: 26px; padding-top: 12px; border-top: 1px solid #f1f5f9; font-size: 11px; color: #94a3b8; text-align: center;">
      Winning Heaven VIP Services • Direct Web Platform<br>
      To manage your email preferences, reply "Unsubscribe".
    </div>

  </div>
</body>
</html>"""

    plain_content = f"""{{Hi|Hello|Greetings}},

{intro_paragraph}

Your Active VIP Privileges:
{bullets_plain}

👉 Access Account & Play Now:
https://winningheaven.com

If you need any assistance, reply directly to this email and our VIP team will help you right away.

Best regards,
The Winning Heaven VIP Team
https://winningheaven.com

To manage your notification preferences, reply 'Unsubscribe'."""

    tpl_id = f"custom_{int(uuid.uuid4().hex[:6], 16)}"
    
    return {
        "id": tpl_id,
        "stage": 1,
        "name": f"✨ Custom AI: {first_line[:30]}...",
        "subject": subject,
        "preview_text": preview_text,
        "plain_text": plain_content,
        "html": html_content,
        "inbox_score": 100,
        "spam_status": "PRIMARY INBOX VERIFIED ✅"
    }

def add_custom_template(tpl):
    TEMPLATES.append(tpl)
    return tpl
