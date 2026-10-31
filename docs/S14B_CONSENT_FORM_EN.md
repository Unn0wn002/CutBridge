# CutBridge user test: information and consent form (asynchronous)

For: practice runs and general feedback on CutBridge v0.2.5 (development build), English UI
Version: 1 (2026-10-31)

Please read this before you take part, then answer the questions under "7. Your consent" at the end. If anything is unclear, ask nyxelharuka@gmail.com before you decide.

This form is for testers recruited through the English sign-up form. Those sessions are practice runs and general feedback; they are **not** part of the Japanese user study (S14B) and are never counted as its evidence. The Japanese study uses [S14B_CONSENT_FORM_JA.md](S14B_CONSENT_FORM_JA.md).

## 1. About this test

- **Who runs it:** a student, as a personal project. This is not a company or studio study.
- **Purpose:** to find out where CutBridge, a Blender → After Effects handoff tool, is hard to understand or use. We are testing **the tool**, not **you**. Places where you get stuck are the most useful results.
- **Who can take part:** adults aged 18 or over.
- **Payment:** none. This is a student's personal project.
- **Taking part is voluntary.** You can say no, or stop at any time, with no consequences.

## 2. How it works (asynchronous, at your own pace)

There is **no meeting, call or video conference.**

1. After we receive your consent reply, we send you a set of files: the two CutBridge ZIPs, test material, a participant guide and a record sheet.
2. Work through the tasks in the guide on your own computer, whenever suits you. Expect **90–120 minutes**. You can take breaks or split it over several sittings.
3. For each task, write in the record sheet what you did, and what confused you or how it felt.
4. When you're done, send back the record sheet. If you chose to record, send the recording too. You may still decide not to send a recording after choosing one.

Questions are welcome by email (nyxelharuka@gmail.com). We always answer questions about receiving the files or the hash check. Because recording where and why you got stuck is the point of the test, questions about installing or using CutBridge are answered if you're stuck, and are recorded as help. If you can't complete a task, you can also note that and move on.

## 3. Effects on your computer

- **This is an unreleased development build.** It is not a published or supported product.
- You will add one add-on to Blender and four script files to After Effects.
- **Use only the test material.** Don't open your own work files or anything confidential. Backing up important files first is a good idea.
- **CutBridge does not send data automatically.** It contacts the internet only if you press **Check for Updates** in Blender. That fetches a public file from GitHub Pages (github.io), which, like any website, sees your IP address. No test data is sent. You don't need to press it for this test. Blender's CutBridge preferences also show a "Check on Startup" option; in this build it is disabled in code and does nothing.
- **Removing it afterwards:**
  - Blender: open **Edit → Preferences → Add-ons**, find CutBridge, open its menu (▾) and choose **Uninstall**.
  - After Effects: delete the four files (`CutBridge.jsx`, `revision_manager.js`, `qc_plus.js`, `localization.js`) wherever you put them. If you copied them into After Effects' `Scripts/ScriptUI Panels` folder, delete them from there (only these four files, not the folder). CutBridge also leaves one harmless display-language setting in After Effects' preferences.
  - You can also delete the folders you created during the test (packages and the After Effects project).
  - The participant guide repeats these steps.

## 4. What we collect

| Information | Used for | Required? |
| --- | --- | --- |
| Your sign-up form answers (role, experience, software versions, OS, contact, and your other answers on the form) | Choosing testers and contacting you, for example to send the files | Yes |
| Your consent reply (email or message) | A record that you agreed | Yes |
| Your record sheet (result of each task, where you got stuck, comments) | Analysing the results | Yes |
| Screen recording (screen only, or screen and voice) | Seeing steps the record sheet can't show | **Optional**; you choose below |
| Screenshots attached to your record sheet | Seeing the screens where you got stuck | **Optional**; you choose below |

**We don't ask for** your name, age, gender, address, employer or school, or any account ID. Please keep these out of recordings and screenshots too (desktop notifications, email, other windows). If something like that is captured anyway, we will not use that part and will delete it.

## 5. How we handle it

- **Pseudonymous ID.** Records use an ID such as `EN-P01`. Your contact details are kept separately from your results.
- **Storage:** your sign-up answers, consent reply, original record sheet, recording and screenshots are kept in a private place only the student running the test can access. You upload your record sheet and recording to your own private Google Drive folder, which only you and the student can see; as with any Drive upload, your Google account name is shown on the files. **None of these are put anywhere public.**
- **What becomes public:** CutBridge's development records (a public repository) may include, per pseudonymous ID: task results, a summary of problems found, your experience band (beginner, intermediate or advanced), your role category, and the Blender and After Effects versions and OS you used. Nothing that identifies you, such as your name or contact details. Recordings and screenshots are never published.
- **Course report:** the student running the test also uses the results in a report for their course. The report contains only the same per-ID information as the public records above. It never includes your name, contact details, recordings or screenshots.
- **Quotes:** text from your record sheet is quoted in the public records or the course report only if you answer "Yes" to item 4 under "7. Your consent".
- **Deletion (two stages):**
  - Your sign-up answers (including contact details), consent reply, and the link between your contact details and your ID: deleted **by 10 January 2027** (one month after the test period).
  - The original record sheet, recording and screenshots: deleted **by 31 March 2027**. Until then they are kept under your ID only.
- **Third parties:** none. Nothing is shared or sold.

## 6. Withdrawing and deletion requests

- You can stop at any time without giving a reason.
- If you contact nyxelharuka@gmail.com by 10 January 2027, we will delete your record sheet and recording, and remove your ID's results from the current public records.
- Earlier versions in the public repository's history, and copies other people have made, cannot be removed. A course report that has already been submitted may not be changeable either.
- After 10 January 2027 we delete the link between your contact details and your ID, so we can no longer tell which records are yours.

## 7. Your consent

Please answer each item. Replying by email or message with the numbers and your choices is fine. We send the files only after we receive this reply.

1. I am 18 or older. **(Yes / No)**
2. I have read and understood this information, and I agree to take part. **(Yes / No)**
3. Screen recording (choose one):
   - I will record and send my screen and voice (thinking aloud)
   - I will record and send my screen only, no voice
   - No recording (record sheet only)
4. Text from my record sheet may be quoted in the public records and the course report under my pseudonymous ID. **(Yes / No)**
5. I may attach screenshots to my record sheet (they are never published). **(Yes / No)**

Participant ID (filled in by us): `EN-P__`
Date of consent: ________

Thank you for your help.

---

Contact: nyxelharuka@gmail.com
