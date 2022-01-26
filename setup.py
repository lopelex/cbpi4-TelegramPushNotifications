from setuptools import setup

setup(name='TelegramPushNotifications',
      version='0.1',
      description='Plugin to send CraftBeerPi Notifications to a Telegram-Chat',
      author='Pascal Scholz',
      author_email='pascal1404@gmx.de',
      url='',
      include_package_data=True,
      package_data={
        # If any package contains *.txt or *.rst files, include them:
      '': ['*.txt', '*.rst', '*.yaml'],
      'TelegramPushNotifications': ['*','*.txt', '*.rst', '*.yaml']},
      packages=['TelegramPushNotifications'],
      install_requires=[
            'telethon',
      ],
     )