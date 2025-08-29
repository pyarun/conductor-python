#!/bin/bash

# Automated Python Package Release Script
# Usage:
#   ./release.sh [patch|minor|major] [--pre <pre>]
#   ./release.sh <explicit_version>
#
# Examples:
#   ./release.sh patch
#   ./release.sh minor --pre rc1
#   ./release.sh major --pre beta1
#   ./release.sh 1.1.11.rc-1      # will be normalized to 1.1.11rc1 (PEP 440 canonical)
#   ./release.sh 1.1.11rc1        # already canonical
#
# Notes:
# - Pre-release specifiers accepted: a / alpha, b / beta, rc, with optional separators
#   like ".", "-" and will be canonicalized per PEP 440 (e.g., "rc-1", "rc.1" → "rc1",
#   "alpha1" → "a1", "beta2" → "b2").
# - The version written to pyproject.toml and used for the tag is the canonicalized value.

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

usage() {
    cat <<'EOF'
Usage:
  ./release.sh [patch|minor|major] [--pre <pre>]
  ./release.sh <explicit_version>

Examples:
  ./release.sh patch
  ./release.sh minor --pre rc1
  ./release.sh major --pre beta1
  ./release.sh 1.1.11.rc-1      # normalized to 1.1.11rc1
  ./release.sh 1.1.11rc1

Notes:
- Pre-release specifiers accepted: a/alpha, b/beta, rc, with optional separators ".", "-"
  (e.g., "rc-1", "rc.1" both become "rc1"; "alpha1" becomes "a1"; "beta2" becomes "b2").
- The version written to pyproject.toml and used for the git tag is the canonicalized value.
EOF
}

# Normalize a full version string to PEP 440 canonical (best-effort, no Python dependency)
normalize_version() {
    local raw="$1"
    # Lowercase, remove spaces
    local v
    v="$(echo "$raw" | tr '[:upper:]' '[:lower:]' | tr -d ' ')"

    # Normalize long pre-release names
    v="${v//alpha/a}"
    v="${v//beta/b}"

    # Collapse separators between pre tag and number: rc-1 / rc.1 / a-1 / b.1 -> rc1 / a1 / b1
    v="$(echo "$v" | sed -E 's/(a|b|rc)[\.\-]?([0-9]+)/\1\2/g')"

    # Remove dot between release and prerelease: 1.2.3.rc1 -> 1.2.3rc1
    v="$(echo "$v" | sed -E 's/([0-9])\.(a|b|rc)([0-9])/\1\2\3/g')"

    echo "$v"
}

# Normalize just a prerelease token (e.g., "rc-1" -> "rc1")
normalize_prerelease() {
    local raw="$1"
    local p
    p="$(echo "$raw" | tr '[:upper:]' '[:lower:]' | tr -d ' ')"
    p="${p//alpha/a}"
    p="${p//beta/b}"
    p="$(echo "$p" | sed -E 's/^(a|b|rc)[\.\-]?([0-9]+)$/\1\2/')"
    echo "$p"
}

# Validate a canonical version string: X.Y.Z or X.Y.ZrcN / X.Y.ZaN / X.Y.ZbN
is_valid_version() {
    local v="$1"
    if echo "$v" | grep -Eq '^[0-9]+\.[0-9]+\.[0-9]+((a|b|rc)[0-9]+)?$'; then
        return 0
    else
        return 1
    fi
}

# ---- Argument parsing ----
if [ $# -eq 0 ]; then
    print_error "Please specify a bump type (patch|minor|major) or an explicit version"
    usage
    exit 1
fi

BUMP_OR_VERSION="$1"
shift || true

PRE_RAW=""
while [ $# -gt 0 ]; do
    case "$1" in
        --pre)
            if [ $# -lt 2 ]; then
                print_error "--pre requires a value (e.g., rc1, rc-1, alpha1, beta2)"
                exit 1
            fi
            PRE_RAW="$2"
            shift 2
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            print_warning "Unknown argument: $1 (ignored)"
            shift
            ;;
    esac
done

# ---- Preconditions ----
# Check if we're in a git repository
if [ ! -d ".git" ]; then
    print_error "Not in a git repository"
    exit 1
fi

# Check if pyproject.toml exists
if [ ! -f "pyproject.toml" ]; then
    print_error "pyproject.toml not found"
    exit 1
fi

# Check if credentials file exists
if [ ! -f "env/pypi.env" ]; then
    print_error "Credentials file env/pypi.env not found"
    print_warning "Please create env/pypi.env with TWINE_USERNAME and TWINE_PASSWORD"
    exit 1
fi

# Load credentials
# shellcheck disable=SC1091
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

# Get current version from pyproject.toml (first occurrence of version = "x.y.z")
CURRENT_VERSION=$(grep -E '^[[:space:]]*version = "' pyproject.toml | head -n 1 | sed 's/[^"]*"\([^"]*\)".*/\1/')
if [ -z "$CURRENT_VERSION" ]; then
    print_error "Unable to determine current version from pyproject.toml"
    exit 1
fi
print_status "Current version: $CURRENT_VERSION"

# Compute the new version
NEW_VERSION=""
if echo "$BUMP_OR_VERSION" | grep -Eq '^[0-9]'; then
    # Explicit version provided
    RAW_VERSION="$BUMP_OR_VERSION"
    NEW_VERSION="$(normalize_version "$RAW_VERSION")"
    if ! is_valid_version "$NEW_VERSION"; then
        print_error "Explicit version '$RAW_VERSION' normalized to '$NEW_VERSION' is not a valid PEP 440 version (expected X.Y.Z[rcN|aN|bN])"
        exit 1
    fi
    if [ -n "$PRE_RAW" ]; then
        print_warning "Ignoring --pre since explicit version was provided"
    fi
else
    # Bump mode
    case "$BUMP_OR_VERSION" in
        patch|minor|major)
            ;;
        *)
            print_error "Invalid bump type. Use: patch, minor, or major; or provide an explicit version."
            usage
            exit 1
            ;;
    esac

    # Extract numeric base X.Y.Z from CURRENT_VERSION (strip any pre/dev/post)
    BASE_NUM=$(echo "$CURRENT_VERSION" | sed -E 's/^([0-9]+\.[0-9]+\.[0-9]+).*$/\1/')
    IFS='.' read -r MAJOR MINOR PATCH <<< "$BASE_NUM"

    case "$BUMP_OR_VERSION" in
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

    BASE_VERSION="${MAJOR}.${MINOR}.${PATCH}"

    if [ -n "$PRE_RAW" ]; then
        PRE_CANON="$(normalize_prerelease "$PRE_RAW")"
        if ! echo "$PRE_CANON" | grep -Eq '^(a|b|rc)[0-9]+$'; then
            print_error "Invalid pre-release specifier: '$PRE_RAW' (normalized: '$PRE_CANON'). Expected forms like rc1, rc-1, rc.1, alpha1, beta2."
            exit 1
        fi
        NEW_VERSION="${BASE_VERSION}${PRE_CANON}"
    else
        NEW_VERSION="${BASE_VERSION}"
    fi
fi

TAG_NAME="Simplified-${NEW_VERSION}"
print_status "New version: $NEW_VERSION"
print_status "Tag name: $TAG_NAME"

# Update version in pyproject.toml
print_status "Updating version in pyproject.toml..."
# macOS/BSD sed compatibility: create .bak then remove
sed -i.bak -E "s/^([[:space:]]*version = \")([^\"]+)(\")/\1${NEW_VERSION}\3/" pyproject.toml
rm -f pyproject.toml.bak

# Clean previous builds
print_status "Cleaning previous builds..."
rm -rf build/ dist/ *.egg-info/

# Build the package
print_status "Building package..."
python -m pip install --upgrade build twine >/dev/null
python -m build

# Check if build was successful
if [ ! -d "dist" ] || [ -z "$(ls -A dist)" ]; then
    print_error "Build failed - no files in dist directory"
    exit 1
fi

print_status "Build completed successfully"

# Commit version change
print_status "Committing version change..."
git add pyproject.toml
git commit -m "Bump version to ${NEW_VERSION}"

# Create git tag
print_status "Creating git tag ${TAG_NAME}..."
git tag -a "${TAG_NAME}" -m "Simplified Release version ${NEW_VERSION}"

# Upload to PyPI (GitLab Package Registry in this case)
print_status "Uploading to PyPI..."
python -m twine upload \
  --repository-url "https://gitlab.com/api/v4/projects/70495826/packages/pypi" \
  dist/* \
  -u "$TWINE_USERNAME" \
  -p "$TWINE_PASSWORD" --verbose

# Push changes and tags to remote
print_status "Pushing changes to remote repository..."
# git push origin main
git push origin "${TAG_NAME}"

print_status "Release ${NEW_VERSION} completed successfully!"
print_status "Package uploaded to GitLab Package Registry and changes pushed to repository"

# Display summary
echo
echo "=== Release Summary ==="
echo "Version: ${CURRENT_VERSION} → ${NEW_VERSION}"
echo "Git tag: ${TAG_NAME}"
echo "Files uploaded:"
ls -la dist/
echo "======================="
