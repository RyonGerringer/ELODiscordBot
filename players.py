from replit import db




# adds new player to database
def add_player(user, tag):
    print(user, tag)
    
    db[user] = [tag, 1500]
    print("Successfully Added",user, tag)
    return (f"**{user}**\nYou start with **{get_elo(user)}** ELO Points.\nActivisionID: {tag}")

# delete a user
def del_player(user):
  try:
    del db[user]
    return f"Successfully deleted {user}"
  except:
    return f"Could not delete {user}"

def is_user(user):
    print("IS-USER?",user)
    if user in db.keys():
        print("True")
        return True
    else:
        print("false")
        return False
    
    


def get_stats(user):
  print("Getting stats for", user)
  values = db[user]
  out = f"__**{user}'s Stats**__\n\n**ActivisionID:** {values[0]}\n**ELO**: {values[1]}"
  return out
def get_elo(user):
  values = db[user]
  return values[1]
def get_gamertag(user):
  values = db[user]
  return values[0]


def show_player(user):
    out = f"-{get_elo(user)}- {get_gamertag(user)}"
    return out


  
def list_users():
  if len(db.keys()) == 0:
    return "List is empty"
  else:
    return db.keys()

def clear():
  for i in db.keys():
    del db[i]
  return("Successfully Cleared List of Users")



