import requests
import json
import config

def retrieve_messages(channel_id, to_fetch=-1):
    headers = {
        'authorization': config.auth
    }

    fetched = 0
    tag = 0
    last_message_id = None

    while True:
        query_params = f'limit={50}'
        if last_message_id is not None:
            query_params += f'&before={last_message_id}'

        r = requests.get(f'https://discord.com//api/v9/channels/{channel_id}/messages?{query_params}', headers=headers)
        messages = json.loads(r.text)

        # end if there are no more messages to fetch
        if len(messages) == 0:
             break
        
        # end if we have fetched enough messages
        fetched += len(messages)
        if to_fetch != -1 and fetched >= to_fetch:
            break

        last_message_id = messages[-1]['id']

        with open(f"messages/messages{tag}.json", "w") as outfile:
            json.dump(messages, outfile)
        tag += 1

        if to_fetch != -1: 
            print(f'Messages left to fetch: {to_fetch - fetched}')
        else:
            print(f'Messages fetched: {fetched}')

    print(f'Done fetching {fetched} messages into files 0 through {tag}!')

retrieve_messages(config.general_channel_id)
