#!/bin/bash
#
#==============================================================================
#
# TCP Gateway
#
# Build Debian Package
#
#==============================================================================

set -euo pipefail

PACKAGE="tcp-gateway"

CONTROL_FILE="${PACKAGE}/DEBIAN/control"

###############################################################################
# Verify
###############################################################################

if [[ ! -d "${PACKAGE}" ]]; then
    echo "ERROR: ${PACKAGE} directory not found."
    exit 1
fi

if [[ ! -f "${CONTROL_FILE}" ]]; then
    echo "ERROR: ${CONTROL_FILE} not found."
    exit 1
fi

###############################################################################
# Read package information
###############################################################################

VERSION=$(awk '/^Version:/ {print $2}' "${CONTROL_FILE}")
ARCH=$(awk '/^Architecture:/ {print $2}' "${CONTROL_FILE}")

OUTPUT="${PACKAGE}_${VERSION}_${ARCH}.deb"

###############################################################################
# Cleanup
###############################################################################

rm -f "${OUTPUT}"

###############################################################################
# Build
###############################################################################

echo "Building package..."
echo
echo "Package      : ${PACKAGE}"
echo "Version      : ${VERSION}"
echo "Architecture : ${ARCH}"
echo

dpkg-deb --build "${PACKAGE}" "${OUTPUT}"

###############################################################################
# Verify
###############################################################################

echo
echo "Package created successfully."
echo

ls -lh "${OUTPUT}"

echo
echo "Package information:"
echo

dpkg-deb --info "${OUTPUT}"

echo
echo "Contents:"
echo

dpkg-deb --contents "${OUTPUT}"
