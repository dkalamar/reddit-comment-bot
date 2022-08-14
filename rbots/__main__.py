import argparse
import logging
import os
import random
import praw

from rbots.charbot import CharBot, CharBotConfig


def parse_args():
    parser = argparse.ArgumentParser(description="Run bot")
    parser.add_argument("-t", "--type", default="char")
    parser.add_argument("-f", "--config-path", required=True,default=os.environ.get('CONFIG_PATH'))
    parser.add_argument("-s", "--subreddit", required=True, default=os.environ.get('SUBREDDIT'))
    parser.add_argument("-u", "--reddit-username",
                        default=os.environ.get('REDDIT_USERNAME'))
    parser.add_argument("-p", "--reddit-password",
                        default=os.environ.get('REDDIT_PASSWORD'))

    parser.add_argument("--client-id", default=os.environ.get('CLIENT_ID'))
    parser.add_argument("--client-secret",
                        default=os.environ.get('CLIENT_SECRET'))
    parser.add_argument("--user-agent", default=os.environ.get("USER",f"rcomment-{random.randint(0,10000)}"))
    parser.add_argument("--skip-existing", default=True,
                        action="store_true")
    parser.add_argument("--no-skip-existing",
                        dest="skip-existing", action="store_false")
    parser.add_argument("--dryrun", default=False, action="store_true")
    parser.add_argument("--log-level",default=os.environ.get("LOG_LEVEL","WARNING"))

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    logging.root.setLevel(args.log_level)
    reddit = praw.Reddit(
        username=args.reddit_username,
        password=args.reddit_password,
        client_id=args.client_id,
        client_secret=args.client_secret,
        user_agent=args.user_agent)
    cf = CharBotConfig.from_path(args.config_path)
    cb = CharBot(reddit, cf)
    while True:
        try:
            cb.scroll(args.subreddit, dry_run=args.dryrun,
                      skip_existing=args.skip_existing)
        except Exception as e:
            logging.error(e)