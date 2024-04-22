FILE=$1

if [[ $FILE != "portinari2photo" && $FILE != "portinari2photo_aug" ]]; then
    echo "Available datasets from Google Drive are: portinari2photo, portinari2photo_aug"
    exit 1
fi

if [[ $FILE == "portinari2photo" ]]; then
    GD_ID=1yYYYB35RbPEACMfPc9qUFnKEuXTaSEf4
elif [[ $FILE == "portinari2photo_aug" ]]; then
    GD_ID=1cngNH5QwCXIhJ79WiVMozZCOOs2AM5dg
fi

echo "Specified [$FILE]"
URL=https://docs.google.com/uc?export=download&id=$GD_ID
ZIP_FILE=./datasets/$FILE.zip
TARGET_DIR=./datasets/$FILE/
wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate $URL -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=${GD_ID}" -O $ZIP_FILE && rm -rf /tmp/cookies.txt
mkdir $TARGET_DIR
unzip $ZIP_FILE -d ./datasets/
rm $ZIP_FILE