#!/bin/bash
set -euo pipefail
# -e: exit on error
# -u: treat unset variables as error
# -o pipefail: pipeline fails if any command fails

# Color codes for better output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored messages
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Function to display help
show_help() {
    cat << EOF
Usage: $0 <command> [arguments]

Commands:
  makemigrations <message>    Create new migration with given message
  migrate [revision]          Apply migrations (default: head)
  downgrade [revision]        Downgrade migrations (default: -1)
  status                      Show current migration status
  history                     Show migration history
  init                        Initialize alembic in project
  help                        Show this help message

Examples:
  $0 makemigrations "Add users table"
  $0 migrate
  $0 downgrade -1
  $0 status
EOF
}

# Check if alembic is installed
check_alembic() {
    if ! command -v alembic &> /dev/null; then
        print_error "Alembic is not installed. Please install with: pip install alembic"
        exit 1
    fi
}

# Check if alembic.ini exists
check_alembic_config() {
    if [[ ! -f "alembic.ini" ]]; then
        print_error "alembic.ini not found. Run '$0 init' first or navigate to project root."
        exit 1
    fi
}

# Initialize alembic in project
init_alembic() {
    if [[ -f "alembic.ini" ]]; then
        print_warning "Alembic already initialized in this directory."
        read -p "Do you want to reinitialize? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_info "Aborted."
            exit 0
        fi
    fi

    print_info "Initializing Alembic..."
    alembic init alembic

    # Check if initialization was successful
    if [[ $? -eq 0 ]] && [[ -f "alembic.ini" ]]; then
        print_info "Alembic initialized successfully!"
        print_info "Remember to configure alembic.ini with your database URL."
    else
        print_error "Failed to initialize Alembic."
        exit 1
    fi
}

# Create migration
makemigrations() {
    local message="$1"
    if [[ -z "$message" ]]; then
        print_error "Migration message is required."
        echo "Usage: $0 makemigrations \"Your migration message\""
        exit 1
    fi

    print_info "Creating migration: $message"
    alembic revision --autogenerate -m "$message"

    if [[ $? -eq 0 ]]; then
        print_info "Migration created successfully."
        print_info "Review the migration file before applying."
    fi
}

# Apply migrations
migrate() {
    local target="${1:-head}"

    print_info "Applying migrations up to: $target"
    alembic upgrade "$target"

    if [[ $? -eq 0 ]]; then
        print_info "Migrations applied successfully."
    fi
}

# Downgrade migrations
downgrade() {
    local target="${1:--1}"

    print_info "Downgrading to: $target"

    # Safety check for production
    if [[ -z "${ALEMBIC_PRODUCTION:-}" ]]; then
        alembic downgrade "$target"
    else
        print_warning "Running in production mode. Are you sure? (y/N): "
        read -p "" -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            alembic downgrade "$target"
        else
            print_info "Downgrade aborted."
        fi
    fi
}

# Show migration status
show_status() {
    print_info "Current migration status:"
    alembic current
}

# Show migration history
show_history() {
    print_info "Migration history:"
    alembic history --verbose
}

# Main script logic
main() {
    # Check for alembic installation
    check_alembic

    command="${1:-help}"

    case $command in
        "init")
            init_alembic
            ;;
        "makemigrations"|"mm")
            check_alembic_config
            if [[ -z "${2:-}" ]]; then
                print_error "Migration message is required."
                show_help
                exit 1
            fi
            makemigrations "$2"
            ;;
        "migrate"|"m")
            check_alembic_config
            migrate "${2:-head}"
            ;;
        "downgrade"|"d")
            check_alembic_config
            downgrade "${2:--1}"
            ;;
        "status"|"s")
            check_alembic_config
            show_status
            ;;
        "history"|"h")
            check_alembic_config
            show_history
            ;;
        "help"|"--help"|"-h")
            show_help
            ;;
        *)
            print_error "Unknown command: $command"
            show_help
            exit 1
            ;;
    esac
}

# Handle script interruption
trap 'print_error "Script interrupted by user"; exit 1' INT TERM

# Run main function with all arguments
main "$@"
