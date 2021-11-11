from replit import db




# adds new player to database
def add_player(user, tag):
  print(user, tag)
  if user in db.keys():
    print("Name Exists")
    return ("You already have an account registered!")
  else:
    db[user] = [tag, 1500]
    print("Successfully Added",user, tag)
    return (f"Successfully Added. \n{user} you start with 1500 ELO Points.\nActivisionID: {tag}")

# delete a user
def del_player(user):
  try:
    del db[user]
    return f"Successfully deleted {user}"
  except:
    return f"Could not delete {user}"

def get_stats(user):
  print(user)
  values = db[user]
  out = f"__**{user}'s Stats**__\n\n**ActivisionID:** {values[0]}\n**ELO**: {values[1]}"
  return out
def get_elo(user):
  values = db[user]
  return values[1]
def get_gamertag(user):
  values = db[user]
  return values[0]


  
def list_users():
  if len(db.keys()) == 0:
    return "List is empty"
  else:
    return db.keys()

def clear():
  for i in db.keys():
    del db[i]
  return("Successfully Cleared List of Users")



