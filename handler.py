import config
import re
from random import choice
import sys
import subprocess
import json
import handler


def isadmin(nick):
    admins = json.loads(open("admins").read())
    if nick in admins:
        return True
    return False


def getwtf(wtf):
    answer = subprocess.check_output(["wtf", wtf])
    return answer


def geteix(eix):
    answer = subprocess.check_output(["eix", "-c", eix])
    answer = str(answer, "ascii").split("\n")[0]
    return answer


class MyHandler():
    def __init__(self):
        self.ignored = []

    def ignore(self, nick):
        self.ignored.append(nick)

    def pubmsg(self, c, e):
        nick = e.source.nick
        msg = ''.join(e.arguments)
        if not isadmin(nick):
            for i in self.ignored:
                if i in str(nick):
                    print("Ignoring!")
                    return
        # !ignore
        match = re.match('\!ignore (.*)', msg)
        if match:
            if not isadmin(nick):
                return
            self.ignore(match.group(1))
            c.privmsg(config.CHANNEL,
                      "Now igoring %s." % match.group(1))
        match = re.match('\!admin reload', msg)
        if match:
            if not isadmin(nick):
                return
            reload(handler)
            c.privmsg(config.CHANNEL, str(handler))
            return
        # !cignore
        match = re.match("\!cignore", msg)
        if match:
            if not isadmin(nick):
                return
            self.ignored = []
            c.privmsg(config.CHANNEL, "Ignore list cleared.")
            print(self.ignored)
            return
        # !quit
        match = re.match('\!quit', msg)
        if match:
            if isadmin(nick):
                sys.exit(0)
            else:
                c.privmsg(config.CHANNEL,
                          "No.")
            return
        # !wtf
        match = re.match('\!wtf ([A-Za-z0-9]+)', msg)
        if match:
            wtf = match.group(1)
            c.privmsg(config.CHANNEL,
                      "%s" % (getwtf(wtf).decode().strip("\n")
                      .replace("\n", ", ")))
            return
        # !eix
        match = re.match('\!eix ([A-Za-z0-9][A-Za-z0-9\\-_/]*)', msg)
        if match:
            wtf = match.group(1)
            c.privmsg(config.CHANNEL,
                      "%s" % (geteix(wtf)))
            return

        # !throw
        match = re.match('\!throw (.*) at (.*)', msg)
        if match:
            c.privmsg(config.CHANNEL, "%s has been\
 thrown at %s!" % (match.group(1), match.group(2)))
            return
        # !kill
        match = re.match('\!kill (.*)', msg)
        if match:
            user = match.group(1)
            if user.lower() == "tjhsstbot":
                c.privmsg(config.CHANNEL,
                          "I'm not that stupid!")
                return
            c.privmsg(config.CHANNEL, "Die, %s!" % user)
        # !say
        match = re.match('\!say (.*)', msg)
        if match:
            to_say = match.group(1).strip()
            print('Saying, "%s"' % to_say)
            c.privmsg(config.CHANNEL, to_say)
            return
        # !bike
        bicycle1 = " _f_,_"
        bicycle2 = "(_)`(_)"
        match = re.match("\!bike", msg)
        if match:
            c.privmsg(config.CHANNEL, bicycle1)
            c.privmsg(config.CHANNEL, bicycle2)
            return
        # !pester
        match = re.match("\!pester ([a-zA-Z0-9]+) (.*)", msg)
        if match:
            s = match.group(2)
            c.privmsg(config.CHANNEL,
                      "%s: %s %s %s" % (match.group(1), s, s, s))
            return
        # !slogan
        match = re.match("\!slogan (.*)", msg)
        if match:
            thing = match.group(1).strip()
            choices = [
                "%s -- awesome.",
                "%s -- the future.",
                "The sight of %s.",
                "The wonder of %s!",
                "Amazing %s.",
                "%s is the best!",
                "%s: bug-free!"
            ]
            c.privmsg(config.CHANNEL,
                      choice(choices) % thing)
            return
        # !excuse
        match = re.match("\!excuse", msg)
        if match:
            x = choice(open("excuses", "r").readlines())
            c.privmsg(config.CHANNEL, x.rstrip())
            return
        # ++ and --
        match = re.match(r"([a-zA-Z0-9]+)(\+\+|--)", msg)
        if match:
            uname = match.group(1)
            score = 1 if "+" in match.group(2) else -1
            scores = json.loads(open("score").read())
            if uname in scores:
                scores[uname] += score
            else:
                scores[uname] = score
            f = open("score", "w")
            f.write(json.dumps(scores))
            f.close()
            return
        # !score
        match = re.match("\!score ([a-zA-Z0-9]+)", msg)
        if match:
            uname = match.group(1)
            try:
                score = json.loads(open("score").read())[uname]
            except:
                score = 0
            finally:
                c.privmsg(config.CHANNEL,
                          "%s has %i points!" % (uname, score))
            return
        match = re.match(r".*((?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))).*", msg)
        if match:
            print(match.group(1))
            import lxml.html
            t = lxml.html.parse(match.group(1))
            c.privmsg(config.CHANNEL, t.find(".//title").text)
            return
        # !award
        match = re.match("\!award (.*)", msg)
        if match:
            uname = match.group(1)
            c.privmsg(config.CHANNEL,
                      "%s: I hereby award you this gold medal." % uname)
            return

        # !dialup
        match = re.match("\!dialup", msg)
        if match:
            c.privmsg(config.CHANNEL,
                      "creffett: %s" % ("get dialup " * 15))
