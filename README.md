# Book Car Bot
Bot used to perform bookings to a car (or any other 1-use-at-a-time item).

## Available Commands
The available commands are
- `/book from-to-[certain]` : book etios at [from, to] with given certainty. Eg: `/book today 16:00-18:00`, `/book today 16:00-18:00-F`
- `/getBooked from` : get all bookings from that date. Eg: `/getBooked friday`
- `/getBooked` : get all bookings
- `/unbook from` : Unbook from appointment. Eg: `/unbook friday 16:00`
- `/myBooked` : get my bookings
- `/confirm from` : Confirm uncertain booking. Eg: `/confirm friday 16:00`

## Credentials File
Before deploying the bot, you must complete the values in the `credentials.py` file.
- `bot_token` is a string with the access token obtained from BotFather
- `URL` is a string with the heroku app link created. Eg: `https://appname.herokuapp.com/`
- `allowed_unames` is a list of allowed Telegram usernames. Only these users will be able to run commands

## Steps to Deploy the Bot
Follow these steps to have your bookings bot ready to go.
1. Complete the `allowed_unames` variable from the `credentials.py` file with the Telegram usernames that should be able to use the bot and perform bookings.
2. Send a `/newbot` message to the [BotFather](https://telegram.me/BotFather), which is essentially a bot used to create other bots. Choose a name and a username and you will get a token. 
    - Copy the token to the `bot_token` variable in the `credentials.py` file.
3. Create a new app from the Heroku dashboard or using the Heroku CLI. A free tier works perfectly for this bot.
    - Copy the app's domain to the `URL` variable in the `credentials.py` file.
4. Login to heroku with `heroku login`.
5. If you haven't already, initialize a GIT repository in this directory with `git init`.
6. Add your heroku project as a GIT remote with `heroku git:remote -a {heroku-project-name}`.
7. Deploy the app by adding the files to the repo with `git add .`, creating a commit with `git commit -m "Commit Message"` and push to the heroku remote with `git push heroku master`
    - You can check the status of the deployment by viewing the logs with the command `heroku logs --tail`
8. Go to the app page and check if the webhook is up by accessing `https://appname.herokuapp.com/setwebhook`. If you get a `webhook setup ok` message, the bot should be ready to use.

You can try sending messages to the bot and checking the app's logs to verify that the app is working OK.

## Connect the Bot to your DB
The bot connects to a MongoDB database, where it saves a collection of all bookings made. To connect the bot to your MongoDB database, follow these steps.
1. Set up your Atlas Cluster at [https://cloud.mongodb.com/](https://cloud.mongodb.com/). A free tier works perfectly for this bot. You can find a more detailed explanation of the steps required at [this tutorial](https://www.mongodb.com/developer/how-to/use-atlas-on-heroku/).
2. Create a database user for your cluster with the Password authentication method.
3. Grant network access to your cluster from your app's IP address. If you have a free tier app and no credit card associated to your account, you'll have to allow access from anywhere, as your app's IP address will be dynamic.
    - There are a few Heroku add-ons that allow you to assign a static IP address to your app. Some of them have a free tier that can work perfectly with this bot if your use case does not require plenty of requests. But you need to set up a credit card in your Heroku account to use add-ons (even if you don't have any charges).
4. Set an environment variable named `MONGODB_URI` in Heroku with the URL to connect to your cluster. Copy the connection string obtained from the dashboard (Connect > Connect your application), replace your password and database name and set it with the Heroku CLI. The command will look something like this: `heroku config:set MONGODB_URI="mongodb+srv://yourUsername:yourPassword@yourClusterName.h4nxa.mongodb.net/database?retryWrites=true&w=majority"`.
