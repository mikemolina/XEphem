#! /bin/sh
#
# xephem-get-orig-source.sh - Script para generar tarball fuente de xephem desde el upstream

XEPHEM_GIT_URL="https://github.com/XEphem/XEphem.git"
XEPHEM_GIT_COMMIT="0a1b50503bdf202fb6fa7ca62124b0242a004e69"
COMMIT_SHORT_FORM="$(echo $XEPHEM_GIT_COMMIT | sed -e 's/^\([[:xdigit:]]\{,7\}\).*/\1/')"
date=`date '+%Y%m%d'`

# Clonar repositorio
if ! [ -d "xephem" ]
then
    git clone "$XEPHEM_GIT_URL" "xephem-git${COMMIT_SHORT_FORM}"
fi
cp -R "xephem" "xephem-git${COMMIT_SHORT_FORM}"
cd "xephem-git${COMMIT_SHORT_FORM}"
git checkout "$XEPHEM_GIT_COMMIT"

# Version upstream
POINTVER=$(../version.sh)
XEPHEM_VERSION="${POINTVER}+git${COMMIT_SHORT_FORM}"
cd ..

# Renombrar upstream
mv "xephem-git${COMMIT_SHORT_FORM}" "xephem-${XEPHEM_VERSION}"

# Remover directorios vacios
echo "Removiendo directorios vacios..."
find xephem-${XEPHEM_VERSION} -type d -empty -delete

# Empacar paquete
rm -fR xephem-${XEPHEM_VERSION}/.github
rm -fR xephem-${XEPHEM_VERSION}/.tito
rm -fR xephem-${XEPHEM_VERSION}/.nojekyll
tar --exclude-vcs -cJf "xephem-${XEPHEM_VERSION}.tar.xz" "xephem-${XEPHEM_VERSION}/"
rm -fR xephem-${XEPHEM_VERSION}
