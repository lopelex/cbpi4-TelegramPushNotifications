# cbpi-telegram
Telegram Push Notifications for Craftbeerpi

This allows you to send any messages that appear in Craftbeerpi to Telegram.

Setup:

1. Install this plugin from CBPI
2. Install Telegram app from https://telegram.org/
3. Create Telegram Bot and acquire Bot token
    * On Telegram, search `@BotFather`, send him a `/start` message
    * To create a new bot send him `/newbot` message and follow instructions to set up username and name for your new bot
    * BotFather will send you confirmation message with bot token. Save it for later
4. Get Chat ID
    * On Telegram, search your bot (by the username you just created) or by clicking on the link that BotFather gave you inside the bot creation confirmation message, press the “Start” button or send a `/start` message
    * Open a new tab with your browser, enter `https://api.telegram.org/bot<yourtoken>/getUpdates` , replace `<yourtoken>` with your API token, press enter and you should see something like this:
    ```{"ok":true,"result":[{"update_id":77xxxxxxx,"message":{"message_id":333,"from":{"id":34xxxxxxx,"is_bot":false,"first_name":"XXXX","last_name":"XXXX","username":"xxxxxxx","language_code":"en-GB"}```
    * Look for “id”, for instance, 34xxxxxxx above is my chat id. Look for yours and save it for later
    * If you cannot see your chat id, remove your bot from the chat and add it back (to remove click on three dots in the right corner and select delete conversation then add it back by searching for bot username or clicking the link in confirmation message from BotFather again). Open the url described above again and you should find you chat id.
5. Login to your Telegram account (https://my.telegram.org) with the phone number of the developer account to use.
6. Click under API Development tools.
7. A Create new application window will appear. Fill in your application details. There is no need to enter any URL, and only the first two fields (App title and Short name) can currently be changed later.
8. Click on Create application at the end. Remember that your API hash is secret and Telegram won’t let you revoke it. Don’t post it anywhere!
9. Input your Bot token, Chat ID, API ID and API HASH you acquired in previous steps into the Craftbeerpi parameters page (may require a system reboot if parameters not visible).
10. Reboot your system.
11. Everything should now be pushed to your Telegram.