# Database Setup Script

# Copy SQL files to database container
Write-Host "Copying SQL files to container..."
docker compose cp backend/app/database/schema.sql db:/schema.sql
docker compose cp backend/app/database/create_test_dbs.sql db:/create_test_dbs.sql

# Run schema in development database
Write-Host "Setting up development database..."
docker compose exec db psql -U postgres -d TuneQuest2 -f /schema.sql

# Create test databases
Write-Host "Creating test databases..."
docker compose exec db psql -U postgres -f /create_test_dbs.sql

# Run schema in test databases
Write-Host "Setting up test databases..."
docker compose exec db psql -U postgres -d tunequest_test -f /schema.sql
docker compose exec db psql -U postgres -d music_service_test -f /schema.sql

# Clean up copied files
Write-Host "Cleaning up..."
docker compose exec db rm /schema.sql /create_test_dbs.sql

Write-Host "Database setup complete!"
