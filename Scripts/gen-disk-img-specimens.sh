#!/bin/bash
#
# Script to generate disk images containing NTFS specimens

EXIT_SUCCESS=0;
EXIT_FAILURE=1;

# Checks the availability of a binary and exits if not available.
#
# Arguments:
#   a string containing the name of the binary
#
assert_availability_binary()
{
	local BINARY=$1;

	which ${BINARY} > /dev/null 2>&1;
	if test $? -ne ${EXIT_SUCCESS};
	then
		echo "Missing binary: ${BINARY}";
		echo "";

		exit ${EXIT_FAILURE};
	fi
}

assert_availability_binary dd;
assert_availability_binary mkntfs;
assert_availability_binary losetup;
assert_availability_binary parted;

# exit immediately with a none zero if a command fails.
set -e;

# cli arguments 
TEST_IMG_NAME=$1 # and location eg: di.raw  
DIR_TO_COPY=$2 # recursively eg: ../Govdocs1/myThread0/

SECTOR_SIZE=512
CLUSTER_SIZE=1024


# Compute the total size of the disk image
TOTAL_IMG_SIZE=0 
for f in $(ls ${DIR_TO_COPY})
do 
    echo "/$f/ ... ";
    for fi in $(ls ${DIR_TO_COPY}/${f})
    do
        echo "/${f}/${fi} <--";
        FILE_SIZE=$(du -b ${DIR_TO_COPY}/${f}/${fi} | awk '{print $1}'); # in bytes
        echo "$FILE_SIZE in bytes";
        TOTAL_IMG_SIZE=$(( $TOTAL_IMG_SIZE+$FILE_SIZE ));
    done;
done;

# add an upper approximate of NTFS SYSTEM files size. 
NTFS_SYS_FILES=$((3*1024*1024))
TOTAL_IMG_SIZE=$(( $TOTAL_IMG_SIZE+$NTFS_SYS_FILES))
echo "TOTAL IMAGE SIZE: $TOTAL_IMG_SIZE in bytes."
echo "TOTAL IMAGE SIZE: $(($TOTAL_IMG_SIZE/$SECTOR_SIZE)) in sectors."
sleep 3

TO_ALIGN_PARTITIONS=2048 # in sectors
TOTAL_IMG_SIZE=$(( $TOTAL_IMG_SIZE + $TO_ALIGN_PARTITIONS * $SECTOR_SIZE ))

# define the mount point
MOUNT_POINT="/mnt/${TEST_IMG_NAME}";
mkdir -p $MOUNT_POINT

# the looping device that will be used 
FREE_DEV=$(losetup --find | awk -F "/" '{print $3}') 
echo "The free device is ${FREE_DEV}."

# create the TEST_IMG file and make it NTFS formatted
dd if=/dev/zero of=${TEST_IMG_NAME} bs=${SECTOR_SIZE} count=$(( ${TOTAL_IMG_SIZE}/${SECTOR_SIZE} )) status=progress 2> /dev/null;
mkntfs -F -q -L "label_${TEST_IMG_NAME}" -s ${SECTOR_SIZE} ${TEST_IMG_NAME};
sleep 5

# mount in the free looping device 
losetup -f ${TEST_IMG_NAME}

# print the devices and mounted dirs
losetup -a

# partition

startp1="${TO_ALIGN_PARTITIONS}s"
endp1="$(( $TOTAL_IMG_SIZE / $SECTOR_SIZE -1))s"
parted -s /dev/"${FREE_DEV}" mklabel msdos mkpart primary NTFS $startp1 $endp1;
parted -s /dev/"${FREE_DEV}" print;
sleep 3

# Copying ....
for f in $(ls ${DIR_TO_COPY})
do 
    echo "/${f}/ ... ";
    for fi in $(ls ${DIR_TO_COPY}/${f})
    do
        echo "/${f}/${fi} <--"
        cp ${DIR_TO_COPY}/${f}/${fi} ${MOUNT_POINT}/${fi}
    done;
done;

# unmount and delete the looping device 
losetup -d /dev/${FREE_DEV}

# Copy and then Remove the working image file.
cp ${TEST_IMG_NAME} ../test_data/${TEST_IMG_NAME}
rm -f ${TEST_IMG_NAME};

exit ${EXIT_SUCCESS};
