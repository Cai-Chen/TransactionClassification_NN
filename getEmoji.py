import json

def getEmoji(category, title = None):
    # Use the keywords to find emoji
    if title is not None:
        words = title.split(' ')
        with open('./emoji.json', 'r', encoding='utf-8') as load_f:
            load_json = json.load(load_f)
            for card in load_json:
                tags = card['tags']
                # If the title has word in this tags
                if len(set([x.upper() for x in words]).intersection([x.upper() for x in tags])) > 0:
                    return card['emoji']
    # Use the category to find emoji
    with open('./category.json', 'r', encoding='utf-8') as load_f:
        load_json = json.load(load_f)
        for card in load_json:
            if category == card['category']:
                return card['emoji']
    # Return GENERAL
    return "🎈"
