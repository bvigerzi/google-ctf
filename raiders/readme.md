# RAIDERS OF CORRUPTION

```bash
~ file disk10.img
disk10.img: Linux Software RAID version 1.2 (1) UUID=ad89154a:f0c39ce3:99c46240:21b5e681 name=0 level=5 disks=10
```

mounted: (RAID 5)
            |
disk01, disk02, disk03 ... disk10

## Binwalk of disk01.img

- Interesting info from the binwalk
- Most other files are JPEG or TIFF images

```
1832088       0x1BF498        JPEG image data, JFIF standard 1.01
2093469       0x1FF19D        TROC filesystem, 542332236 file entries
2095067       0x1FF7DB        TROC filesystem, 777213260 file entries
2213162       0x21C52A        Copyright string: "copyright implications you should read!*"
2215866       0x21CFBA        Copyright string: "copyright"
2215903       0x21CFDF        Copyright string: "copyright letters written, etc.  that I am not thought"
2284375       0x22DB57        eCos RTOS string reference: "ecost the sum is due,"
2696192       0x292400        JPEG image data, JFIF standard 1.01
```

## Questions To Be Addressed

### Process of how RAID 5 constructs and map disks

- TODO

### What different mechanisms are used to construct a disk

- TODO

### How were the disk images dumped/created?

- TODO

### How disks can be grouped together?

- TODO

### DISKS 10,9,4,3,1

- GCTF2021 (Google CTF 2021)
