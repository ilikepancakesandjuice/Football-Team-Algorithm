import subprocess

while True:
  choice = input("Which file do you want to run? (1: ver1.py, 2: ver2.py): ")
  if choice == '1':
    subprocess.run(["python", "ver1.py"])
    break
  elif choice == '2':
    subprocess.run(["python", "ver2.py"])
    break
  else:
    print("Invalid choice, please enter 1 or 2.")