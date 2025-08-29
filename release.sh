#!/bin/bash

# Automated Python Package Release Script
# Usage: ./release.sh [patch|minor|major]

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if version bump type is provided
if [ $# -eq 0 ]; then
    print_error "Please specify version bump type: patch, minor, or major"
    echo "Usage: $0 [patch|minor|major]"
    exit 1
fi

BUMP_TYPE=$1

# Validate bump type
if [[ ! "$BUMP_TYPE" =~ ^(patch|minor|major)$ ]]; then
    print_error "Invalid bump type. Use: patch, minor, or major"
    exit 1
fi

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    print_error "Not in a git repository"
    exit 1
fi

# Check if setup.py exists
if [ ! -f "setup.py" ]; then
    print_error "setup.py not found"
    exit 1
fi

# Check if credentials file exists
if [ ! -f "env/pypi.env" ]; then
    print_error "Credentials file env/pypi.env not found"
    print_warning "Please create env/pypi.env with TWINE_USERNAME and TWINE_PASSWORD"
    exit 1
fi

# Load credentials
source env/pypi.env

if [ -z "$TWINE_USERNAME" ] || [ -z "$TWINE_PASSWORD" ]; then
    print_error "TWINE_USERNAME or TWINE_PASSWORD not set in env/pypi.env"
    exit 1
fi

print_status "Starting automated release process..."

# Check for uncommitted changes
if [ -n "$(git status --porcelain)" ]; then
    print_error "There are uncommitted changes. Please commit or stash them first."
    git status --short
    exit 1
fi

# Get current version from setup.py
CURRENT_VERSION=$(grep -E "^\s*version\s*=" setup.py | head -1 | sed -E "s/^[^0-9]*([0-9]+\.[0-9]+\.[0-9]+).*/\1/")
if [ -z "$CURRENT_VERSION" ]; then
    print_error "Could not determine current version from setup.py"
    exit 1
fi
print_status "Current version: $CURRENT_VERSION"

# Calculate new version
IFS='.' read -ra VERSION_PARTS <<< "$CURRENT_VERSION"
MAJOR=${VERSION_PARTS[0]}
MINOR=${VERSION_PARTS[1]}
PATCH=${VERSION_PARTS[2]}

case $BUMP_TYPE in
    "major")
        MAJOR=$((MAJOR + 1))
        MINOR=0
        PATCH=0
        ;;
    "minor")
        MINOR=$((MINOR + 1))
        PATCH=0
        ;;
    "patch")
        PATCH=$((PATCH + 1))
        ;;
esac

NEW_VERSION="${MAJOR}.${MINOR}.${PATCH}"
TAG_NAME="Simplified-${NEW_VERSION}"

print_status "New version: $NEW_VERSION"
print_status "Tag name: $TAG_NAME"

# Update version in setup.py
print_status "Updating version in setup.py..."
sed -i.bak "s/version = \"$CURRENT_VERSION\"/version = \"$NEW_VERSION\"/" setup.py
rm -f setup.py.bak

# Clean previous builds
print_status "Cleaning previous builds..."
rm -rf build/ dist/ *.egg-info/

# Build the package
print_status "Building package..."
python -m pip install --upgrade build twine
python -m build

# Check if build was successful
if [ ! -d "dist" ] || [ -z "$(ls -A dist)" ]; then
    print_error "Build failed - no files in dist directory"
    exit 1
fi

print_status "Build completed successfully"

# Commit version change
print_status "Committing version change..."
git add setup.py
git commit -m "Bump version to $NEW_VERSION"

# Create git tag with the new format
print_status "Creating git tag $TAG_NAME..."
git tag -a "$TAG_NAME" -m "Release version $NEW_VERSION"

# Upload to GitLab Package Registry
print_status "Uploading to GitLab Package Registry..."
python -m twine upload \
  --repository-url "https://gitlab.com/api/v4/projects/70495826/packages/pypi" \
  dist/* \
  -u "$TWINE_USERNAME" \
  -p "$TWINE_PASSWORD" --verbose

# Push changes and tags to remote
print_status "Pushing changes to remote repository..."
git push origin main
git push origin "$TAG_NAME"

print_status "Release $NEW_VERSION completed successfully!"
print_status "Package uploaded to GitLab Package Registry and changes pushed to repository"

# Display summary
echo
echo "=== Release Summary ==="
echo "Version: $CURRENT_VERSION → $NEW_VERSION"
echo "Bump type: $BUMP_TYPE"
echo "Git tag: $TAG_NAME"
echo "Files uploaded:"
ls -la dist/
echo "======================="