from app import app, db, User

with app.app_context():
  db.drop_all()
  db.create_all()

  users = [
    ('test'.encode('utf-8'), b'0d6f604f437d39b148ee1ed414c8bd0439033f89f25f4d91c1cf228fc21d8226'),
    ('admin'.encode('utf-8'), b'503aab17c88a38f3c9aa5247a88d1327a36187db0e3c03b58a84ec90dd1cb5cd')
  ]

  for user in users:
    new_user = User(username=user[0], password=user[1])
    db.session.add(new_user)
  db.session.commit()