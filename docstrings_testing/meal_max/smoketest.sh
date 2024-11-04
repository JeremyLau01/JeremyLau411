#!/bin/bash

# Define the base URL for the Flask API
BASE_URL="http://localhost:9000/api"

# Flag to control whether to echo JSON output
ECHO_JSON=false

# Parse command-line arguments
while [ "$#" -gt 0 ]; do
  case $1 in
    --echo-json) ECHO_JSON=true ;;
    *) echo "Unknown parameter passed: $1"; exit 1 ;;
  esac
  shift
done


###############################################
#
# Health checks
#
###############################################

# Function to check the health of the service
check_health() {
  echo "Checking health status..."
  curl -s -X GET "$BASE_URL/health" | grep -q '"status": "healthy"'
  if [ $? -eq 0 ]; then
    echo "Service is healthy."
  else
    echo "Health check failed."
    exit 1
  fi
}

# Function to check the database connection
check_db() {
  echo "Checking database connection..."
  curl -s -X GET "$BASE_URL/db-check" | grep -q '"database_status": "healthy"'
  if [ $? -eq 0 ]; then
    echo "Database connection is healthy."
  else
    echo "Database check failed."
    exit 1
  fi
}

clear_catalog() {
  echo "Clearing the playlist..."
  curl -s -X DELETE "$BASE_URL/clear-meals" | grep -q '"status": "success"'
}


##########################################################
#
# Meal Management
#
##########################################################


create_meal() {
  meal=$1
  cuisine=$2
  price=$3
  difficulty=$4

  echo "Creating meal: $meal ($cuisine, $price, $difficulty)"
  curl -s -X POST "$BASE_URL/create-meal" -H "Content-Type: application/json" \
    -d "{\"meal\":\"$meal\", \"cuisine\":\"$cuisine\", \"price\":$price, \"difficulty\":\"$difficulty\"}" | grep -q '"status": "combatant added"'

  if [ $? -eq 0 ]; then
    echo "Meal created successfully."
  else
    echo "Failed to create meal."
    exit 1
  fi
}

delete_meal_by_id() {
  meal_id=$1

  echo "Deleting meal by ID ($meal_id)..."
  response=$(curl -s -X DELETE "$BASE_URL/delete-meal/$meal_id")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Meal deleted successfully by ID ($meal_id)."
  else
    echo "Failed to delete meal by ID ($meal_id)."
    exit 1
  fi
}

get_meal_by_id() {
  meal_id=$1

  echo "Retrieving meal by ID ($meal_id)..."
  response=$(curl -s -X GET "$BASE_URL/get-meal-by-id/$meal_id")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Meal retrieved successfully by ID ($meal_id)."
    if [ "$ECHO_JSON" = true ]; then
      echo "Meal JSON (ID $meal_id):"
      echo "$response" | jq .
    fi
  else
    echo "Failed to retrieve meal by ID ($meal_id)."
    exit 1
  fi
}

get_meal_by_name() {
  name_id=$1
  echo "Retrieving meal by name ($name_id)..."
  response=$(curl -s -X GET "$BASE_URL/get-meal-by-name/$name_id")

  if echo "$response" | grep -q '"status": "success"'; then
    echo "Meal retrieved successfully by name ($name_id)."
    if [ "$ECHO_JSON" = true ]; then
      echo "Meal JSON: (ID $name_id)"
      echo "$response" | jq .
    fi
  else
    echo "Failed to retrieve meal by name ($name_id)."
    exit 1
  fi
}

############################################################
#
# Battle Management
#
############################################################
battle() {
  echo "Playing current song..."
  response=$(curl -s -X POST "$BASE_URL/play-current-song")

  if echo "$response" | grep -q '"status": "success"'; then
    echo "Current song is now playing."
  else
    echo "Failed to play current song."
    exit 1
  fi
}


clear_combatants() {
  echo "Clearing combatants..."
  response=$(curl -s -X POST "$BASE_URL/clear-combatants")

  if echo "$response" | grep -q '"status": "combatants cleared"'; then
    echo "Combatants cleared successfully."
  else
    echo "Failed to clear playlist."
    exit 1
  fi
}

get_combatants() {
  echo "Retrieving combatants from battle..."
  response=$(curl -s -X GET "$BASE_URL/get-combatants")

  if echo "$response" | grep -q '"status": "success"'; then
    echo "Combatants retrieved successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Combatant JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to retrieve all songs from playlist."
    exit 1
  fi
}

prep_combatant() {
  meal=$1

  echo "Prepping combatant for battle: $meal"
  response=$(curl -s -X POST "$BASE_URL/prep-combatant" \
    -H "Content-Type: application/json" \
    -d "{\"meal\":\"$meal\"}")

  if echo "$response" | grep -q '"status": "combatant prepared"'; then
    echo "Meal prepped successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Meal JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to add song to playlist."
    exit 1
  fi
}



##########################################################
#
# Leaderboard Management
#
##########################################################

# Function to get the meal leaderboard sorted by play count
get_meal_leaderboard() {
  sort_by=$1

  echo "Retrieving leaderboard sorted by $sort_by..."
  response=$(curl -s -X GET "$BASE_URL/get-leaderboard?sort=$sort_by")

  if echo "$response" | grep -q '"status": "success"'; then
    echo "Leaderboard retrieved successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Leaderboard JSON (sorted by $sort_by):"
      echo "$response" | jq .
    fi
  else
    echo "Failed to retrieve leaderboard."
    exit 1
  fi
}

# Health checks
check_health
check_db
clear_catalog

# Create meals
create_meal "Pizza" "Italian" 20.0 "MED"
create_meal "Sushi" "Japanese" 30.0 "HIGH"
create_meal "Tacos" "Mexican" 10.0 "LOW"

delete_meal_by_id 1
get_meal_by_id 1
get_meal_by_name "Tacos"


get_meal_leaderboard "wins"
get_meal_leaderboard "win_pct"

prep_combatant "Pizza"
get_combatants
prep_combatant "Sushi"
get_combatants
clear_combatants

#get_combatants
#prep_combatant "Queen" "Bohemian Rhapsody" 1975
#prep_combatant "The Beatles" "Let It Be" 1970
#
#get_combatants
#
#battle
#

echo "All tests completed successfully!"
