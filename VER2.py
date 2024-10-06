class Player:
  def __init__(self, name, position):
      self.name = name
      self.position = position
      self.score = 1

def compare_two_players(player1, player2):
  while True:
      choice = input(f"Which player is better? (1: {player1.name}, 2: {player2.name}): ")
      if choice == '1':
          player1.score += 1
          return player1
      elif choice == '2':
          player2.score += 1
          return player2
      else:
          print("Invalid choice, please enter 1 or 2.")

def rank_players_by_position(players):
  positions = {}
  for player in players:
      if player.position not in positions:
          positions[player.position] = []
      positions[player.position].append(player)

  ranked_players = {}
  for position, position_players in positions.items():
      print(f"\nRanking players for position: {position}")
      for i in range(len(position_players)):
          for j in range(i + 1, len(position_players)):
              compare_two_players(position_players[i], position_players[j])

      ranked_players[position] = sorted(position_players, key=lambda p: p.score, reverse=True)

  return ranked_players

def calculate_position_distribution(ranked_players, total_players_per_team):
  position_distribution = {}
  remaining_slots = total_players_per_team

  for position, players in ranked_players.items():
      ideal_per_team = len(players) // 2
      if ideal_per_team > remaining_slots:
          position_distribution[position] = remaining_slots
          remaining_slots = 0
      else:
          position_distribution[position] = ideal_per_team
          remaining_slots -= ideal_per_team

  if remaining_slots > 0:
      print(f"\nDistributing {remaining_slots} remaining slots:")
      positions_needing_extra = sorted(
          ranked_players.keys(),
          key=lambda p: len(ranked_players[p]) % 2,
          reverse=True
      )

      for position in positions_needing_extra:
          if remaining_slots <= 0:
              break
          extra_players = len(ranked_players[position]) - (position_distribution[position] * 2)
          if extra_players > 0:
              extra_to_add = min(remaining_slots, extra_players)
              position_distribution[position] += extra_to_add
              remaining_slots -= extra_to_add
              print(f"Added {extra_to_add} extra slots to {position}")

  return position_distribution

def display_team_status(team_a, team_b):
  print("\nCurrent Teams Status:")

  for team_name, team in [("A", team_a), ("B", team_b)]:
      print(f"\nTeam {team_name}:")
      positions = {}
      for player in team:
          if player.position not in positions:
              positions[player.position] = []
          positions[player.position].append(f"{player.name} (Score: {player.score})")

      for position, players in positions.items():
          print(f"{position}s ({len(players)}):")
          for player in players:
              print(f"  {player}")

def distribute_players_evenly(ranked_players):
  total_players = sum(len(players) for players in ranked_players.values())
  players_per_team = total_players // 2

  print(f"\nCreating teams with {players_per_team} players each")
  position_distribution = calculate_position_distribution(ranked_players, players_per_team)

  team_a = []
  team_b = []
  team_a_positions = {pos: 0 for pos in ranked_players.keys()}
  team_b_positions = {pos: 0 for pos in ranked_players.keys()}

  for position, target_count in position_distribution.items():
      players = ranked_players[position]
      print(f"\nDistributing {position}s (Target: {target_count} per team)")

      for i, player in enumerate(players):
          if team_a_positions[position] < target_count:
              team_a.append(player)
              team_a_positions[position] += 1
              print(f"Added {player.name} to Team A")
          elif team_b_positions[position] < target_count:
              team_b.append(player)
              team_b_positions[position] += 1
              print(f"Added {player.name} to Team B")
          else:
              display_team_status(team_a, team_b)  # Show teams before asking
              choice = input(f"Extra {position}: {player.name}. Add to which team? (1: Team A, 2: Team B): ")
              if choice == '1':
                  team_a.append(player)
                  team_a_positions[position] += 1
              else:
                  team_b.append(player)
                  team_b_positions[position] += 1

  return team_a, team_b

def fine_tune_teams(team_a, team_b):
  total_a = sum(player.score for player in team_a)
  total_b = sum(player.score for player in team_b)

  if abs(total_a - total_b) <= 1:
      return team_a, team_b

  attempts = 0
  max_attempts = 10

  while abs(total_a - total_b) > 1 and attempts < max_attempts:
      attempts += 1
      if total_a > total_b:
          team_from, team_to = team_a, team_b
      else:
          team_from, team_to = team_b, team_a

      best_diff = abs(total_a - total_b)
      best_swap = None

      for player1 in team_from:
          for player2 in team_to:
              if player1.position == player2.position:
                  new_total_from = total_a - player1.score + player2.score
                  new_total_to = total_b - player2.score + player1.score
                  if abs(new_total_from - new_total_to) < best_diff:
                      best_diff = abs(new_total_from - new_total_to)
                      best_swap = (player1, player2)

      if best_swap:
          player1, player2 = best_swap
          team_from.remove(player1)
          team_to.remove(player2)
          team_from.append(player2)
          team_to.append(player1)
          total_a = sum(player.score for player in team_a)
          total_b = sum(player.score for player in team_b)
          print(f"Swapped {player1.name} with {player2.name} for better balance")
      else:
          break

  return team_a, team_b

def display_teams(team_a, team_b):
  total_a = sum(player.score for player in team_a)
  total_b = sum(player.score for player in team_b)

  for team_name, team in [("A", team_a), ("B", team_b)]:
      print(f"\nTeam {team_name}:")
      positions = {}
      for player in sorted(team, key=lambda x: x.position):
          if player.position not in positions:
              positions[player.position] = []
          positions[player.position].append(f"{player.name} (Score: {player.score})")

      for position, players in positions.items():
          print(f"{position}s ({len(players)}):")
          for player in players:
              print(f"  {player}")

  print(f"\nTeam A Total Score: {total_a}")
  print(f"Team B Total Score: {total_b}")

def main():
  player_data = [
      ("Aadit Menon", "Goalkeeper"),
      ("Aaditey Raj", "Midfielder"),
      ("Adithya Dev", "Defender"),
      ("Affan Waseem Sheikh", "Defender"),
      ("Allen Maadhav", "Striker"),
      ("Arhaan Qureshi", "Striker"),
      ("Azmil Noujoom", "Defender"),
      ("Emaan Chopra", "Midfielder"),
      ("Ethan Benny", "Midfielder"),
      ("Fahad Akhtar", "Midfielder"),
      ("Harold Alex", "Goalkeeper"),
      ("Himanish Ram", "Striker"),
      ("Irshad Khaleejan", "Goalkeeper"),
      ("Jeffin Joseph", "Striker"),
      ("Jivin", "Striker"),
      ("Joshua Rodrigues", "Midfielder"),
      ("Kenneth Joe", "Goalkeeper"),
      ("Krish Kriz", "Striker"),
      ("Kshitij Gupta", "Midfielder"),
      ("Leander", "Defender"),
      ("Maaz Parveen", "Striker"),
      ("Milan Maadhav", "Defender"),
      ("Mujtaba Ali", "Striker"),
      ("Nabeel Ansari", "Striker"),
      ("Ogden Fernandes", "Midfielder"),
      ("Rakshit Jagdeshan", "Goalkeeper"),
      ("Rayan Jasim", "Striker"),
      ("Rayyan Masee", "Defender"),
      ("Rhythm Thakur", "Defender"),
      ("Rithwik Adavi", "Goalkeeper"),
      ("Satvik Kumar", "Striker"),
      ("Suprith SP", "Midfielder"),
      ("Takshil Singh", "Defender"),
      ("Umar Ali Faridi", "Striker"),
  ]

  players = [Player(name, position) for name, position in player_data]

  while True:
      print("\nSelect players by entering their numbers (comma separated):")
      for idx, (name, position) in enumerate(player_data):
          print(f"{idx + 1}. {name} - {position}")

      selected_indices = input("Enter the player numbers you want to include: ").split(',')
      try:
          selected_players = [players[int(idx.strip()) - 1] for idx in selected_indices]
      except (ValueError, IndexError):
          print("Invalid selection, please enter valid player numbers.")
          continue

      ranked_players = rank_players_by_position(selected_players)
      team_a, team_b = distribute_players_evenly(ranked_players)
      team_a, team_b = fine_tune_teams(team_a, team_b)
      display_teams(team_a, team_b)

      another_round = input("\nDo you want to select more players? (y/n): ")
      if another_round.lower() != 'y':
          break

if __name__ == "__main__":
  main()

print("Nabeel is the best player here.")