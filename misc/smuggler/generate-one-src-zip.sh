#! /bin/bash

# run this to generate a zip file that should be downloadable from the challenge page

# parameter validation
[ -z $1 ] && echo "usage $0 <dir> [<dir2>]" && exit
[ ! -d $1 ] && echo "no such directory: $1" &&  exit

CHAL_NAME=$1
SOURCE_DIR_NAME=${CHAL_NAME}-source

ZIP_DIR=${TMPDIR}${SOURCE_DIR_NAME}
rm -rf $ZIP_DIR
mkdir $ZIP_DIR

mkdir $ZIP_DIR/$CHAL_NAME
rm -rf $CHAL_NAME/node_modules
cp -r $CHAL_NAME/* $ZIP_DIR/$CHAL_NAME

EXTRA_DIR=$2
if [ "$EXTRA_DIR" ]; then
  [ ! -d $EXTRA_DIR ] && echo "no such directory: $EXTRA_DIR" &&  exit
  mkdir $ZIP_DIR/$EXTRA_DIR
  rm -rf $EXTRA_DIR/node_modules
  cp -r $EXTRA_DIR/* $ZIP_DIR/$EXTRA_DIR
fi

# redact the flag from any copied source
# -i '' means replace inline with no backup file created
sed -i '' 's/wctf{[^}]*}/wctf{redacted}/' $ZIP_DIR/**/*

rm -f $ZIP_DIR/../$SOURCE_DIR_NAME.zip
cd $ZIP_DIR/..
zip -r $SOURCE_DIR_NAME.zip $SOURCE_DIR_NAME
cd -

# .gitignore will prevent target/* from being committed 
mkdir -p target
rm -f target/${SOURCE_DIR_NAME}.zip
mv $ZIP_DIR/../$SOURCE_DIR_NAME.zip target/${SOURCE_DIR_NAME}.zip
rm -rf $ZIP_DIR
