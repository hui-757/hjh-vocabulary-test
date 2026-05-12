huajianghui@huajianghui:~/work6$ make -f Makefile1
gcc -g -c -o main1.o main1.c
as -g -o myAdd.o myAdd.s
gcc -g -o main1 main1.o myAdd.o
huajianghui@huajianghui:~/work6$ ./main1
a + b = 579
huajianghui@huajianghui:~/work6$ 

// int mySub(int a, int b);
int mySub(int a, int b) {
    return a - b;
}



huajianghui@huajianghui:~/work6$ make -f Makefile2
as -g -o main2.o main2.s
gcc -g -c -o mySub.o mySub.c
gcc -g -o main2 main2.o mySub.o
huajianghui@huajianghui:~/work6$ ./main2
huajianghui@huajianghui:~/work6$ gdb ./main2
GNU gdb (Ubuntu 15.1-1ubuntu1~24.04.1) 15.1


huajianghui@huajianghui:~/work6$ gcc inline.c -o inline
huajianghui@huajianghui:~/work6$ ./inline
a + b = 300
huajianghui@huajianghui:~/work6$ 


huajianghui@huajianghui:~/work6$ gcc -g main4.c Len.s -o main4
Len.s: Assembler messages:
Len.s: Warning: end of file not at end of a line; newline inserted
huajianghui@huajianghui:~/work6$ ./main4
字符串: "GNU ARM Assembly Experiment"
长度: 27
huajianghui@huajianghui:~/work6$



huajianghui@huajianghui:~/ex7$ mount | grep /
sysfs on /sys type sysfs (rw,nosuid,nodev,noexec,relatime)
proc on /proc type proc (rw,nosuid,nodev,noexec,relatime)
udev on /dev type devtmpfs (rw,nosuid,relatime,size=1938268k,nr_inodes=484567,mode=755,inode64)
devpts on /dev/pts type devpts (rw,nosuid,noexec,relatime,gid=5,mode=620,ptmxmode=000)
tmpfs on /run type tmpfs (rw,nosuid,nodev,noexec,relatime,size=399360k,mode=755,inode64)
efivarfs on /sys/firmware/efi/efivars type efivarfs (rw,nosuid,nodev,noexec,relatime)
/dev/vda2 on / type ext4 (rw,relatime)
securityfs on /sys/kernel/security type securityfs (rw,nosuid,nodev,noexec,relatime)
tmpfs on /dev/shm type tmpfs (rw,nosuid,nodev,inode64)
tmpfs on /run/lock type tmpfs (rw,nosuid,nodev,noexec,relatime,size=5120k,inode64)
cgroup2 on /sys/fs/cgroup type cgroup2 (rw,nosuid,nodev,noexec,relatime,nsdelegate,memory_recursiveprot)
pstore on /sys/fs/pstore type pstore (rw,nosuid,nodev,noexec,relatime)
bpf on /sys/fs/bpf type bpf (rw,nosuid,nodev,noexec,relatime,mode=700)
systemd-1 on /proc/sys/fs/binfmt_misc type autofs (rw,relatime,fd=32,pgrp=1,timeout=0,minproto=5,maxproto=5,direct,pipe_ino=7422)
hugetlbfs on /dev/hugepages type hugetlbfs (rw,nosuid,nodev,relatime,pagesize=2M)
mqueue on /dev/mqueue type mqueue (rw,nosuid,nodev,noexec,relatime)
debugfs on /sys/kernel/debug type debugfs (rw,nosuid,nodev,noexec,relatime)
tracefs on /sys/kernel/tracing type tracefs (rw,nosuid,nodev,noexec,relatime)
fusectl on /sys/fs/fuse/connections type fusectl (rw,nosuid,nodev,noexec,relatime)
configfs on /sys/kernel/config type configfs (rw,nosuid,nodev,noexec,relatime)
/dev/vda1 on /boot/efi type vfat (rw,relatime,fmask=0022,dmask=0022,codepage=437,iocharset=iso8859-1,shortname=mixed,errors=remount-ro)
binfmt_misc on /proc/sys/fs/binfmt_misc type binfmt_misc (rw,nosuid,nodev,noexec,relatime)
tmpfs on /run/user/1000 type tmpfs (rw,nosuid,nodev,relatime,size=399356k,nr_inodes=99839,mode=700,uid=1000,gid=1000,inode64)
huajianghui@huajianghui:~/ex7$ 


huajianghui@huajianghui:~/ex7$ touch testfile.txt
huajianghui@huajianghui:~/ex7$ ln -s testfile.txt soft_link.txt
huajianghui@huajianghui:~/ex7$ ls -l
total 8
-rw-rw-r-- 1 huajianghui huajianghui 2748 May  5 07:30 ex07.c
-rw-rw-r-- 1 huajianghui huajianghui  331 May  5 07:19 makefile
lrwxrwxrwx 1 huajianghui huajianghui   12 May  5 09:55 soft_link.txt -> testfile.txt
-rw-rw-r-- 1 huajianghui huajianghui    0 May  5 09:55 testfile.txt
huajianghui@huajianghui:~/ex7$ 


huajianghui@huajianghui:~/ex7$ ln testfile.txt hard_link.txt
huajianghui@huajianghui:~/ex7$ ls -li
total 8
392775 -rw-rw-r-- 1 huajianghui huajianghui 2748 May  5 07:30 ex07.c
392792 -rw-rw-r-- 2 huajianghui huajianghui    0 May  5 09:55 hard_link.txt
392776 -rw-rw-r-- 1 huajianghui huajianghui  331 May  5 07:19 makefile
392794 lrwxrwxrwx 1 huajianghui huajianghui   12 May  5 09:55 soft_link.txt -> testfile.txt
392792 -rw-rw-r-- 2 huajianghui huajianghui    0 May  5 09:55 testfile.txt
huajianghui@huajianghui:~/ex7$ 


huajianghui@huajianghui:~/ex7$ ls -l
total 8
-rw-rw-r-- 1 huajianghui huajianghui 2748 May  5 07:30 ex07.c
-rw-rw-r-- 2 huajianghui huajianghui    0 May  5 09:55 hard_link.txt
-rw-rw-r-- 1 huajianghui huajianghui  331 May  5 07:19 makefile
lrwxrwxrwx 1 huajianghui huajianghui   12 May  5 09:55 soft_link.txt -> testfile.txt
-rw-rw-r-- 2 huajianghui huajianghui    0 May  5 09:55 testfile.txt
huajianghui@huajianghui:~/ex7$ chmod 755 testfile.txt
huajianghui@huajianghui:~/ex7$ ls -l testfile.txt
-rwxr-xr-x 2 huajianghui huajianghui 0 May  5 09:55 testfile.txt



huajianghui@huajianghui:~/ex7$ ls -l testfile.txt
-rwxr-xr-x 2 huajianghui huajianghui 0 May  5 09:55 testfile.txt
huajianghui@huajianghui:~/ex7$ sudo chown root:root testfile.txt
huajianghui@huajianghui:~/ex7$ ls -l testfile.txt
-rwxr-xr-x 2 root root 0 May  5 09:55 testfile.txt
huajianghui@huajianghui:~/ex7$ 



huajianghui@huajianghui:~$ make
gcc -Wall -g -DENABLE_LOG=1 -o ex07 ex07.c
huajianghui@huajianghui:~$ ./ex07
=== Original random data ===
251 304 782 485 410 525 748 448 359 918
874 703  67 537 360  46 269 520 762 935
261 797 441 806 200 472 557 273 475 990
312 726 295  94 211 705 620 311 154 331
230 380  35 649 917 395 695 187 916 457
474 529 606 267 336 158 739 893 432 566
883 744 644 530 839 207 588 811 519 742
142 101 474 177 102 743 925 150 282 193
959 756 722 566  23 410  76 114 303 508
680 539 253 324  69 444 884 657 255 403

=== Data read from random.dat ===
251 304 782 485 410 525 748 448 359 918
874 703  67 537 360  46 269 520 762 935
261 797 441 806 200 472 557 273 475 990
312 726 295  94 211 705 620 311 154 331
230 380  35 649 917 395 695 187 916 457
474 529 606 267 336 158 739 893 432 566
883 744 644 530 839 207 588 811 519 742
142 101 474 177 102 743 925 150 282 193
959 756 722 566  23 410  76 114 303 508
680 539 253 324  69 444 884 657 255 403

=== Sorted data ===
23  35  46  67  69  76  94 101 102 114
142 150 154 158 177 187 193 200 207 211
230 251 253 255 261 267 269 273 282 295
303 304 311 312 324 331 336 359 360 380
395 403 410 410 432 441 444 448 457 472
474 474 475 485 508 519 520 525 529 530
537 539 557 566 566 588 606 620 644 649
657 680 695 703 705 722 726 739 742 743
744 748 756 762 782 797 806 811 839 874
883 884 893 916 917 918 925 935 959 990
huajianghui@huajianghui:~$ 