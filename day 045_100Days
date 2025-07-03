import os, time

org = []

print("Welcome to life organizer.")

def add():
  time.sleep(1)
  os.system('clear')
  name = input("Name : ").capitalize()
  date = input("Date : ")
  priority = input("Priority : ").capitalize()
  row = [name, date, priority]
  org.append(row)
  print("Added to list")

def view():
  time.sleep(1)
  os.system('clear')
  option = input("Please select an option : \n1. View all \n2. View by priority \n3. View by date \n")
  if option == "1":
    for row in org:
      for item in row:
        print(item, end=" | ")
        print()
  elif option == "2":
    priority = input("What priority : ").capitalize()
    for row in org:
      if priority in row:
        for item in row:
          print(item, end=" | ")
        print()
  elif option == "3":
    date = input("What date : ")
    for row in org:
      if date in row:
        for item in row:
          print(item, end=" | ")
        print()

def edit():
  time.sleep(1)
  os.system("clear")
  find = input("Name of organization to edit: ")
  found = False
  for row in org:
    if find in row:
      found = True
  if not found:
    print("Couldnt find that organization")
    return
  for row in org:
    if find in row:
      org.remove(row)
  name = input("Name : ").capitalize()
  date = input("Date : ")
  priority = input("Priority : ").capitalize()
  row = [name, date, priority]
  org.append(row)
  print("Edited")

def remove():
  time.sleep(1)
  os.system("clear")
  find = input("Name of organization to remove: ")
  for row in org:
    if find in row:
      org.remove(row)

while True:
  menu = input("1: Add \n2: View \n3: Edit \n4: Remove \n5: Exit \n")
  if menu == "1":
    add()
  elif menu == "2":
    view()
  elif menu == "3":
    edit()
  elif menu == "4":
    remove()
  elif menu == "5":
    break

  time.sleep(1)
  os.system('clear')
