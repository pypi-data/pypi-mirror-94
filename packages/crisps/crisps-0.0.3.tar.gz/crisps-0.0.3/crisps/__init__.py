class new():
  def __init__(self, name, kilogram, height):
    self.name = name
    self.kilogram = kilogram
    self.height = height
    int(height)
    int(kilogram)
  
  def eat(self, kgram):
    self.kgram = kgram
    app.kilogram+= int(kgram)
  
  def doctor(c):
      app.height -= 100
      if (app.kilogram > app.height):
        print("You are fat!")
      else:
        print("You are normal")


