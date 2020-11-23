#!/bin/bash
#
# Script to generate disk images containing NTFS specimens
#
# USAGE: sudo bash gen-disk-img-specimens.sh di1.raw ../Govdocs1/myThread0

EXIT_SUCCESS=0
EXIT_FAILURE=1

# Checks the availability of a binary and exits if not available.
#
# Arguments:
#   a string containing the name of the binary
#
assert_availability_binary() {
    local BINARY=$1

    which "${BINARY}" >/dev/null 2>&1
    if test $? -ne ${EXIT_SUCCESS}; then
        echo "Missing binary: ${BINARY}"
        echo ""

        exit ${EXIT_FAILURE}
    fi
}

assert_availability_binary dd
assert_availability_binary mkntfs
assert_availability_binary losetup
assert_availability_binary parted

# exit immediately with a none zero value if a command fails.
set -e

# cli arguments
TEST_IMG_NAME=$1 # eg: di.raw
IMG_WITHOUT_EXT=$(echo "${TEST_IMG_NAME}" |awk -F'.' '{print $1}')
DIR_TO_COPY=$2   # eg: ../Govdocs1/myThread0

SECTOR_SIZE=512

# Compute the total size of the disk image
compute_total_needed_size() {

    #local FILE_SIZE, NTFS_SYS_FILES, TO_ALIGN_PARTITIONS
    TOTAL_IMG_SIZE=0
    for f in $(ls ${DIR_TO_COPY}); do
        echo "/$f/ ... "
        for fi in $(ls ${DIR_TO_COPY}/${f}); do
            #echo "/${f}/${fi} <--"
            FILE_SIZE=$(du -b ${DIR_TO_COPY}/${f}/${fi} | awk '{print $1}') # in bytes
            #echo "$FILE_SIZE in bytes"
            TOTAL_IMG_SIZE=$((TOTAL_IMG_SIZE +FILE_SIZE))
        done
    done

    # add an upper approximate of NTFS SYSTEM files size.
    NTFS_SYS_FILES=$((3 * 1024 * 1024))
    TOTAL_IMG_SIZE=$((TOTAL_IMG_SIZE + NTFS_SYS_FILES))
    sleep 3

    TO_ALIGN_PARTITIONS=2048 # in sectors
    TOTAL_IMG_SIZE=$((TOTAL_IMG_SIZE + TO_ALIGN_PARTITIONS * SECTOR_SIZE))
}

compute_total_needed_size
echo "Disk img size is computed:"
echo " - TOTAL IMAGE SIZE: ${TOTAL_IMG_SIZE} in bytes."
echo " - TOTAL IMAGE SIZE: $((TOTAL_IMG_SIZE / SECTOR_SIZE )) in sectors."
sleep 5

# define the mount point
MOUNT_POINT="/mnt/${IMG_WITHOUT_EXT}"
mkdir -p "${MOUNT_POINT}"

# create the TEST_IMG file and make it NTFS formatted
dd if=/dev/zero of="${TEST_IMG_NAME}" bs="${SECTOR_SIZE}" count=$((TOTAL_IMG_SIZE / SECTOR_SIZE)) status=progress 2>/dev/null

# the looping device that will be used
FREE_DEV=$(losetup --find)
echo "The free device is: s"

# set up and control the free looping device
losetup --show "${FREE_DEV}" "${TEST_IMG_NAME}"
sleep 3

# partition
startp1="${TO_ALIGN_PARTITIONS}s"
parted -s "${FREE_DEV}" -- mklabel msdos mkpart primary NTFS $startp1 -1s
parted -s "${FREE_DEV}" print
sleep 3

mkntfs -F -q -L "label_${IMG_WITHOUT_EXT}" -s ${SECTOR_SIZE} "${FREE_DEV}p1"

sleep 3
mount "${FREE_DEV}p1" "${MOUNT_POINT}"

# print everything
lsblk -o NAME,FSTYPE,LABEL,UUID,MOUNTPOINT

sleep 3
# Copying ....
copy_dir_content() {

    for f in $(ls ${DIR_TO_COPY}); 
    do
        for fi in $(ls ${DIR_TO_COPY}/${f}); do
            cp "${DIR_TO_COPY}/${f}/${fi}" "${MOUNT_POINT}/${fi}"
        done
    done

}

copy_dir_content;

# unmount and delete the looping device
umount "${MOUNT_POINT}"
losetup --detach "${FREE_DEV}"

# Copy and then Remove the working image file.
cp "${TEST_IMG_NAME}" "../test_data/${TEST_IMG_NAME}"
rm -f "${TEST_IMG_NAME}"

exit ${EXIT_SUCCESS}
