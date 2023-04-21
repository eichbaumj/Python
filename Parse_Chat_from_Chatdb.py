import xry
import datetime

__contact__ = "%CONTACT%"
__version__ = "1"
__description__ = "Parse chat from chatdb"

class Chat: 
    def __init__(self, message, stamp, direction, name):
        self.message = message
        self.stamp = stamp
        self.direction = direction
        self.name = name
        
def main(image, node):
    entries = []
    buddies = {}
    conn = xry.sqlite.connect(image, r"\private\var\mobile\Applications\com.grindrguy.grindr\Documents\chatdb.sql")
    c = conn.cursor()
    c.execute("select [id], [name] from buddyList")
    for row in c:
        buddies[row[0]] = row[1]
    c.execute("select [msg], [stamp], [from], [buddy] from chat")
    for row in c:
        message = row[0]
        timestamp = datetime.datetime.utcfromtimestamp(float(row[1]))
        direction = row[2]
        name = buddies[row[3]]
        entries.append(Chat(message,timestamp,direction,name))
    #NOW TO ADD THE CHAT MESSAGES (OBJECTS) TO XAMN SPOTLIGHT
    for chat in entries:
        item = image.create_item(xry.nodeids.views.chat_view)
        prop = image.create_property(item, xry.nodeids.views.chat_view.properties.text_body)
        prop.set_value(chat.message)
        prop = image.create_property(item, xry.nodeids.views.chat_view.properties.time)
        prop.set_value(chat.stamp)
        prop = image.create_property(item, xry.nodeids.views.chat_view.properties.direction)
        if chat.direction == 1:
            prop.set_value(xry.xrts.DIRECTION.OUTGOING)
            from_participant = image.create_group(item, xry.xrts.GROUP_TYPE.GROUP_FROM)
            prop = image.create_property(from_participant, xry.proptypes.name)
            prop.set_value("Owner")
            to_participant = image.create_group(item, xry.xrts.GROUP_TYPE.GROUP_TO)
            prop = image.create_property(to_participant, xry.proptypes.name)
            prop.set_value(chat.name)
        else:
            prop.set_value(xry.xrts.DIRECTION.INCOMING)
            from_participant = image.create_group(item, xry.xrts.GROUP_TYPE.GROUP_FROM)
            prop = image.create_property(from_participant, xry.proptypes.name)
            prop.set_value(chat.name)
        prop = image.create_property(item, xry.nodeids.views.chat_view.properties.uid)
        prop.set_value(chat.name)
        prop = image.create_property(item, xry.nodeids.views.chat_view.properties.related_application)
        prop.set_value("Grindr")
        
            
        
        
    
    


