from errbot import BotPlugin, botcmd, arg_botcmd, webhook
import requests
import pandas as pd
import json


class Itdog(BotPlugin):
    """
    itdog
    """

    def activate(self):
        """
        Triggers on plugin activation

        You should delete it if you're not using it to override any default behaviour
        """
        super(Itdog, self).activate()

    def deactivate(self):
        """
        Triggers on plugin deactivation

        You should delete it if you're not using it to override any default behaviour
        """
        super(Itdog, self).deactivate()

    def get_configuration_template(self):
        """
        Defines the configuration structure this plugin supports

        You should delete it if your plugin doesn't use any configuration like this
        """
        return {'itdog_api': "http://itdog.chatops.xxxxxxx.cn-shanghai.fc.devsapp.net"
               }

    def check_configuration(self, configuration):
        """
        Triggers when the configuration is checked, shortly before activation

        Raise a errbot.ValidationException in case of an error

        You should delete it if you're not using it to override any default behaviour
        """
        super(Itdog, self).check_configuration(configuration)

    def callback_connect(self):
        """
        Triggers when bot is connected

        You should delete it if you're not using it to override any default behaviour
        """
        return('itdog is here')

    def callback_message(self, message):
        """
        Triggered for every received message that isn't coming from the bot itself

        You should delete it if you're not using it to override any default behaviour
        """
        pass

    def callback_botmessage(self, message):
        """
        Triggered for every message that comes from the bot itself

        You should delete it if you're not using it to override any default behaviour
        """
        pass

    @webhook
    def example_webhook(self, incoming_request):
        """A webhook which simply returns 'Example'"""
        return "Example"

    # Passing split_args_with=None will cause arguments to be split on any kind
    # of whitespace, just like Python's split() does
    
    #@botcmd(split_args_with=None)
    #def itdog(self, message, args):
     #   """A command which simply returns itdog test result'"""
      #  return "example usage: !itdog https://www.elsevier.com to get itdog test result"

    @arg_botcmd('url', type=str)
    @arg_botcmd('--favorite-number', type=int, unpack_args=False)
    def itdog(self, message, args):
        """
        A command which returns itdog test result.

        If you include --favorite-number, it will also tell you their
        favorite number.
        """
        if args.favorite_number is None:
            api = 'http://itdog.chatops.1671409927271754.cn-shanghai.fc.devsapp.net/itdog?url='
            url = api+args.url
            r = requests.get(url)
            r = json.loads(r.text)
            result = list()
            for each in r:
                each = json.loads(each)
                result.append(each)
            for each in result:
                for key in each.keys():
                  tmp = list()
                  tmp.append(each[key])
                  each[key] = tmp
            df = pd.DataFrame(result)
            http_status = df.http_code.value_counts()
            http_status = http_status.div(http_status.sum())
            http_status = http_status.apply(lambda x: format(x, '.2%')) 
            http_status = http_status.to_markdown()
            ip = df.ip.value_counts()
            ip = ip.to_markdown()
            markdown = http_status + ip
            return markdown
        else:
            return f'Hello {args.url}, I hear your favorite number is {args.favorite_number}.'
